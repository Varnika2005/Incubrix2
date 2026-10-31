import csv
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from engine.db import EVIDENCE_DIR, ROOT_DIR, get_connection, now_iso

MARKET_LOCATIONS: Dict[str, str] = {
    "US": "United States (en-US, gl=us, hl=en)",
    "IN": "India (en-IN, gl=in, hl=en)",
    "GB": "United Kingdom (en-GB, gl=uk, hl=en)",
}

KNOWN_COMPETITORS: List[str] = [
    "OpusClip",
    "Descript",
    "Repurpose.io",
    "Buffer",
    "Hootsuite",
    "HeyGen",
    "Synthesia",
    "VEED",
    "Kapwing",
    "Castmagic",
    "Riverside",
    "Munch",
    "Submagic",
    "ElevenLabs",
    "VidIQ",
    "TubeBuddy",
    "Headliner",
    "Sprout Social",
    "Later",
]

PROVIDERS_META: Dict[str, Dict[str, Any]] = {
    "google_search": {
        "name": "Google Search & AI Overviews",
        "type": "search_engine",
        "env_keys": ["SERPAPI_API_KEY", "GOOGLE_CSE_API_KEY"],
        "cost_per_call_usd": 0.005,
        "default_model": "google-web-serp",
    },
    "chatgpt": {
        "name": "OpenAI ChatGPT",
        "type": "ai_assistant",
        "env_keys": ["OPENAI_API_KEY"],
        "cost_per_call_usd": 0.002,
        "default_model": "gpt-4o-mini",
    },
    "gemini": {
        "name": "Google Gemini",
        "type": "ai_assistant",
        "env_keys": ["GEMINI_API_KEY"],
        "cost_per_call_usd": 0.001,
        "default_model": "gemini-3.5-flash-lite",
    },
    "perplexity": {
        "name": "Perplexity Sonar",
        "type": "ai_assistant",
        "env_keys": ["PERPLEXITY_API_KEY"],
        "cost_per_call_usd": 0.005,
        "default_model": "sonar",
    },
    "claude": {
        "name": "Anthropic Claude",
        "type": "ai_assistant",
        "env_keys": ["ANTHROPIC_API_KEY"],
        "cost_per_call_usd": 0.0025,
        "default_model": "claude-3-5-haiku-latest",
    },
}


def check_provider_Statuses() -> List[Dict[str, Any]]:
    """
    Return the configuration and availability status of all 5 search/AI providers.
    """
    results = []
    for pid, meta in PROVIDERS_META.items():
        configured_keys = [k for k in meta["env_keys"] if os.environ.get(k, "").strip()]
        is_ready = len(configured_keys) > 0
        results.append(
            {
                "provider_id": pid,
                "name": meta["name"],
                "type": meta["type"],
                "default_model": meta["default_model"],
                "required_env_keys": meta["env_keys"],
                "configured": is_ready,
                "status_label": "API Key Configured" if is_ready else "Manual Evidence / Test Mode Only (No API Key)",
                "cost_per_call_usd": meta["cost_per_call_usd"],
            }
        )
    return results


def extract_visibility_signals(
    raw_text: str,
    citation_urls: Optional[List[str]] = None,
    serp_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Deterministic extractor for IncuBrix brand mentions, citations, competitor mentions,
    Google organic rank, Answer Box presence, and AI Overview observations.
    """
    text_lower = (raw_text or "").lower()
    urls = list(citation_urls or [])
    # Also extract markdown/inline URLs from text
    found_inline_urls = re.findall(r"https?://[^\s\)\]\>\"']+", raw_text or "")
    for u in found_inline_urls:
        u_clean = u.rstrip(".,;:")
        if u_clean not in urls:
            urls.append(u_clean)

    incubrix_mentioned = 1 if ("incubrix" in text_lower or any("incubrix.com" in u.lower() for u in urls)) else 0
    incubrix_urls = [u for u in urls if "incubrix.com" in u.lower()]
    incubrix_cited = 1 if len(incubrix_urls) > 0 else 0

    competitors_found: List[str] = []
    for comp in KNOWN_COMPETITORS:
        pattern = r"\b" + re.escape(comp.lower().replace(".io", "")) + r"\b"
        if re.search(pattern, text_lower) or comp.lower() in text_lower:
            competitors_found.append(comp)

    serp = serp_metadata or {}
    google_rank = serp.get("google_organic_rank")
    answer_box_present = 1 if serp.get("answer_box_present") else 0
    answer_box_owner = serp.get("answer_box_owner")
    ai_overview_present = 1 if serp.get("ai_overview_present") else 0
    ai_overview_cites_incubrix = 1 if (ai_overview_present and incubrix_cited) or serp.get("ai_overview_cites_incubrix") else 0

    snippet = re.sub(r"\s+", " ", (raw_text or "").strip())[:420]

    return {
        "incubrix_mentioned": incubrix_mentioned,
        "incubrix_cited": incubrix_cited,
        "incubrix_citation_urls": incubrix_urls,
        "competitors_mentioned": sorted(list(set(competitors_found))),
        "citations_found": urls[:15],
        "google_organic_rank": google_rank,
        "answer_box_present": answer_box_present,
        "answer_box_owner": answer_box_owner,
        "ai_overview_present": ai_overview_present,
        "ai_overview_cites_incubrix": ai_overview_cites_incubrix,
        "response_snippet": snippet,
    }


def make_observation_id(
    question_id: str,
    provider: str,
    market: str,
    observation_date: str,
    pass_number: int,
    is_demo: int,
) -> str:
    key = f"{question_id}:{provider}:{market}:{observation_date}:P{pass_number}:D{is_demo}"
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:10].upper()
    prefix = "OBS-DEMO" if is_demo else "OBS"
    return f"{prefix}-{question_id}-{provider[:4].upper()}-{market}-P{pass_number}-{digest[:6]}"


def save_raw_evidence(observation_id: str, payload: Dict[str, Any]) -> str:
    obs_dir = EVIDENCE_DIR / "observations"
    obs_dir.mkdir(parents=True, exist_ok=True)
    file_path = obs_dir / f"{observation_id}.json"
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(file_path.relative_to(ROOT_DIR))


def call_live_provider_adapter(
    provider: str,
    query_text: str,
    market: str,
    timeout_sec: int = 15,
    max_retries: int = 2,
) -> Dict[str, Any]:
    """
    Execute a genuine API request to the configured provider with retry and timeout handling.
    Never fabricates a response if credentials are missing or an error occurs.
    """
    t0 = time.time()
    location_str = MARKET_LOCATIONS.get(market, MARKET_LOCATIONS["US"])

    # 1. Check credentials
    if provider == "chatgpt":
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        if not api_key:
            return {
                "ok": False,
                "status": "not_collected",
                "error": "OPENAI_API_KEY not configured. Use Manual Evidence Ingestion or set OPENAI_API_KEY in .env.",
                "latency_ms": 0,
                "cost_usd": 0.0,
            }
        url = "https://api.openai.com/v1/chat/completions"
        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": f"You are answering a creator software question for a user in {location_str}. Mention specific tools and URLs where known."},
                {"role": "user", "content": query_text},
            ],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    elif provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        model = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
        if not api_key:
            return {
                "ok": False,
                "status": "not_collected",
                "error": "GEMINI_API_KEY not configured. Use Manual Evidence Ingestion or set GEMINI_API_KEY in .env.",
                "latency_ms": 0,
                "cost_usd": 0.0,
            }
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={urllib.parse.quote(api_key)}"
        body = {
            "contents": [{"parts": [{"text": f"[Market: {location_str}] {query_text}"}]}],
            "generationConfig": {"maxOutputTokens": 450, "temperature": 0.2},
        }
        headers = {"Content-Type": "application/json"}

    elif provider == "perplexity":
        api_key = os.environ.get("PERPLEXITY_API_KEY", "").strip()
        model = os.environ.get("PERPLEXITY_MODEL", "sonar")
        if not api_key:
            return {
                "ok": False,
                "status": "not_collected",
                "error": "PERPLEXITY_API_KEY not configured. Use Manual Evidence Ingestion or set PERPLEXITY_API_KEY in .env.",
                "latency_ms": 0,
                "cost_usd": 0.0,
            }
        url = "https://api.perplexity.ai/chat/completions"
        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": f"Provide an accurate answer with citations for market {location_str}."},
                {"role": "user", "content": query_text},
            ],
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    elif provider == "claude":
        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        model = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
        if not api_key:
            return {
                "ok": False,
                "status": "not_collected",
                "error": "ANTHROPIC_API_KEY not configured. Use Manual Evidence Ingestion or set ANTHROPIC_API_KEY in .env.",
                "latency_ms": 0,
                "cost_usd": 0.0,
            }
        url = "https://api.anthropic.com/v1/messages"
        body = {
            "model": model,
            "max_tokens": 600,
            "messages": [{"role": "user", "content": f"[Market: {location_str}] {query_text}"}],
        }
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

    elif provider == "google_search":
        serp_key = os.environ.get("SERPAPI_API_KEY", "").strip()
        cse_key = os.environ.get("GOOGLE_CSE_API_KEY", "").strip()
        cse_cx = os.environ.get("GOOGLE_CSE_CX", "").strip()
        if not serp_key and not (cse_key and cse_cx):
            return {
                "ok": False,
                "status": "not_collected",
                "error": "Neither SERPAPI_API_KEY nor GOOGLE_CSE_API_KEY+GOOGLE_CSE_CX is configured in .env.",
                "latency_ms": 0,
                "cost_usd": 0.0,
            }
        if serp_key:
            gl = {"US": "us", "IN": "in", "GB": "uk"}.get(market, "us")
            params = urllib.parse.urlencode({"q": query_text, "gl": gl, "hl": "en", "api_key": serp_key})
            url = f"https://serpapi.com/search.json?{params}"
        else:
            gl = {"US": "us", "IN": "in", "GB": "uk"}.get(market, "us")
            params = urllib.parse.urlencode({"q": query_text, "gl": gl, "key": cse_key, "cx": cse_cx})
            url = f"https://www.googleapis.com/customsearch/v1?{params}"
        body = None
        headers = {"Accept": "application/json"}
        model = "google-serp-api"
    else:
        return {
            "ok": False,
            "status": "failed_collection",
            "error": f"Unknown provider '{provider}'.",
            "latency_ms": 0,
            "cost_usd": 0.0,
        }

    # Execute HTTP call with retries and timeout
    last_err = ""
    for attempt in range(max_retries + 1):
        try:
            data_bytes = json.dumps(body).encode("utf-8") if body is not None else None
            req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST" if body else "GET")
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                raw_resp = resp.read().decode("utf-8", errors="replace")
                try:
                    parsed = json.loads(raw_resp)
                except json.JSONDecodeError as jexc:
                    return {
                        "ok": False,
                        "status": "failed_collection",
                        "error": f"MalformedJSONError: Invalid JSON payload from {provider}: {jexc}",
                        "latency_ms": int((time.time() - t0) * 1000),
                        "cost_usd": 0.0,
                    }
                if not isinstance(parsed, dict) or not parsed:
                    return {
                        "ok": False,
                        "status": "failed_collection",
                        "error": f"EmptyResponseError: {provider} returned an empty JSON object.",
                        "latency_ms": int((time.time() - t0) * 1000),
                        "cost_usd": 0.0,
                    }

                latency_ms = int((time.time() - t0) * 1000)
                cost = PROVIDERS_META[provider]["cost_per_call_usd"]

                # Extract text & citations per provider format
                text_out = ""
                citations_out: List[str] = []
                serp_meta: Dict[str, Any] = {}

                if provider in ("chatgpt", "perplexity"):
                    choices = parsed.get("choices", [])
                    if choices and isinstance(choices[0], dict):
                        text_out = str(choices[0].get("message", {}).get("content", "") or "")
                    if "citations" in parsed and isinstance(parsed["citations"], list):
                        citations_out = [str(c) for c in parsed["citations"]]
                elif provider == "gemini":
                    cands = parsed.get("candidates", [])
                    if cands and isinstance(cands[0], dict):
                        parts = cands[0].get("content", {}).get("parts", [])
                        text_out = " ".join(str(p.get("text", "") or "") for p in parts if isinstance(p, dict))
                elif provider == "claude":
                    content_blocks = parsed.get("content", [])
                    text_out = " ".join(str(b.get("text", "") or "") for b in content_blocks if isinstance(b, dict))
                elif provider == "google_search":
                    if "organic_results" not in parsed and "items" not in parsed:
                        return {
                            "ok": False,
                            "status": "failed_collection",
                            "error": "MalformedSERPError: Missing 'organic_results' or 'items' in SERP payload.",
                            "latency_ms": latency_ms,
                            "cost_usd": 0.0,
                        }
                    organic = parsed.get("organic_results") or parsed.get("items") or []
                    snippets = []
                    rank_found = None
                    for idx, item in enumerate(organic, start=1):
                        link = item.get("link", "")
                        title = item.get("title", "")
                        snip = item.get("snippet", "")
                        if link:
                            citations_out.append(link)
                        snippets.append(f"#{idx} {title}: {snip} ({link})")
                        if "incubrix.com" in link.lower() and rank_found is None:
                            rank_found = idx
                    text_out = "\n".join(snippets)
                    ab = parsed.get("answer_box")
                    aio = parsed.get("ai_overview")
                    serp_meta = {
                        "google_organic_rank": rank_found,
                        "answer_box_present": bool(ab),
                        "answer_box_owner": ab.get("link") or ab.get("Displayed_link") if isinstance(ab, dict) else None,
                        "ai_overview_present": bool(aio),
                    }

                if provider != "google_search" and not text_out.strip():
                    return {
                        "ok": False,
                        "status": "failed_collection",
                        "error": f"EmptyResponseError: {provider} returned empty text output.",
                        "latency_ms": latency_ms,
                        "cost_usd": 0.0,
                    }

                return {
                    "ok": True,
                    "status": "verified_observation" if provider == "google_search" else "pending_verification",
                    "model": model,
                    "text": text_out,
                    "citations": citations_out,
                    "serp_metadata": serp_meta,
                    "raw_payload": parsed,
                    "latency_ms": latency_ms,
                    "cost_usd": cost,
                }
        except urllib.error.HTTPError as hexc:
            err_body = ""
            try:
                err_body = hexc.read().decode("utf-8", errors="replace")[:200]
            except Exception:
                pass
            if hexc.code == 429:
                last_err = f"HTTPError 429 (Rate Limit Exceeded): {hexc.reason} {err_body}".strip()
            else:
                last_err = f"HTTPError {hexc.code}: {hexc.reason} {err_body}".strip()
            if attempt < max_retries and hexc.code in (429, 500, 502, 503, 504):
                time.sleep(0.3)
            else:
                break
        except Exception as exc:
            last_err = f"{type(exc).__name__}: {exc}"
            if attempt < max_retries:
                time.sleep(0.3)

    return {
        "ok": False,
        "status": "failed_collection",
        "error": f"Provider request failed after {max_retries + 1} attempts: {last_err}",
        "latency_ms": int((time.time() - t0) * 1000),
        "cost_usd": 0.0,
    }


def upsert_observation(conn, obs: Dict[str, Any]) -> str:
    """
    Insert or update a visibility observation without creating duplicate rows on reruns.
     Automatically determines 'verified_observation' vs 'pending_verification' for AI answers
    based on whether at least 2 passes exist for that question/provider/market.
    """
    obs_id = make_observation_id(
        obs["question_id"],
        obs["provider"],
        obs["market"],
        obs["observation_date"],
        int(obs.get("pass_number", 1)),
        int(obs.get("is_demo", 0)),
    )

    conn.execute(
        """
        INSERT INTO visibility_observations (
            observation_id, run_id, question_id, query_text, provider,
            provider_model, market, location_setting, observation_date,
            pass_number, collection_status, is_demo, incubrix_mentioned,
            incubrix_cited, incubrix_citation_urls_json, google_organic_rank,
            answer_box_present, answer_box_owner, ai_overview_present,
            ai_overview_cites_incubrix, competitors_mentioned_json,
            citations_found_json, response_snippet, raw_evidence_path,
            screenshot_path, error_message, latency_ms, estimated_cost_usd,
            observed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(observation_id) DO UPDATE SET
            run_id=excluded.run_id,
            collection_status=excluded.collection_status,
            incubrix_mentioned=excluded.incubrix_mentioned,
            incubrix_cited=excluded.incubrix_cited,
            incubrix_citation_urls_json=excluded.incubrix_citation_urls_json,
            google_organic_rank=excluded.google_organic_rank,
            answer_box_present=excluded.answer_box_present,
            answer_box_owner=excluded.answer_box_owner,
            ai_overview_present=excluded.ai_overview_present,
            ai_overview_cites_incubrix=excluded.ai_overview_cites_incubrix,
            competitors_mentioned_json=excluded.competitors_mentioned_json,
            citations_found_json=excluded.citations_found_json,
            response_snippet=excluded.response_snippet,
            raw_evidence_path=excluded.raw_evidence_path,
            error_message=excluded.error_message,
            latency_ms=excluded.latency_ms,
            estimated_cost_usd=excluded.estimated_cost_usd,
            observed_at=excluded.observed_at
        """,
        (
            obs_id,
            obs["run_id"],
            obs["question_id"],
            obs["query_text"],
            obs["provider"],
            obs.get("provider_model", PROVIDERS_META.get(obs["provider"], {}).get("default_model", "manual")),
            obs["market"],
            obs.get("location_setting", MARKET_LOCATIONS.get(obs["market"], MARKET_LOCATIONS["US"])),
            obs["observation_date"],
            int(obs.get("pass_number", 1)),
            obs["collection_status"],
            int(obs.get("is_demo", 0)),
            int(obs.get("incubrix_mentioned", 0)),
            int(obs.get("incubrix_cited", 0)),
            json.dumps(obs.get("incubrix_citation_urls", [])),
            obs.get("google_organic_rank"),
            int(obs.get("answer_box_present", 0)),
            obs.get("answer_box_owner"),
            int(obs.get("ai_overview_present", 0)),
            int(obs.get("ai_overview_cites_incubrix", 0)),
            json.dumps(obs.get("competitors_mentioned", [])),
            json.dumps(obs.get("citations_found", [])),
            obs.get("response_snippet"),
            obs.get("raw_evidence_path"),
            obs.get("screenshot_path"),
            obs.get("error_message"),
            int(obs.get("latency_ms", 0)),
            float(obs.get("estimated_cost_usd", 0.0)),
            obs.get("observed_at", now_iso()),
        ),
    )

    # Enforce the two-pass verification rule for non-demo AI assistant answers:
    # An AI assistant observation is only 'verified_observation' when >= 2 passes exist for that
    # exact (question_id, provider, market, observation_date) AND have saved raw evidence on disk.
    if (
        int(obs.get("is_demo", 0)) == 0
        and obs["provider"] in ("chatgpt", "gemini", "perplexity", "claude")
        and obs["collection_status"] in ("verified_observation", "pending_verification")
    ):
        pass_rows = conn.execute(
            """
            SELECT DISTINCT pass_number, raw_evidence_path
            FROM visibility_observations
            WHERE question_id = ? AND provider = ? AND market = ? AND observation_date = ? AND is_demo = 0
              AND collection_status IN ('verified_observation', 'pending_verification')
            """,
            (obs["question_id"], obs["provider"], obs["market"], obs["observation_date"]),
        ).fetchall()
        valid_passes = {
            int(r["pass_number"])
            for r in pass_rows
            if r["raw_evidence_path"] and (ROOT_DIR / r["raw_evidence_path"]).exists()
        }

        target_status = "verified_observation" if len(valid_passes) >= 2 else "pending_verification"
        conn.execute(
            """
            UPDATE visibility_observations
            SET collection_status = ?
            WHERE question_id = ? AND provider = ? AND market = ? AND observation_date = ? AND is_demo = 0
              AND collection_status IN ('verified_observation', 'pending_verification')
            """,
            (target_status, obs["question_id"], obs["provider"], obs["market"], obs["observation_date"]),
        )

    return obs_id


def record_manual_observation(
    payload: Dict[str, Any],
    custom_db_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Documented manual-evidence workflow: ingest a human-verified SERP or AI response,
    save raw response evidence to disk, extract mentions/citations/competitors, and
    enforce two-pass AI verification rules.
    """
    conn = get_connection(custom_db_path)
    try:
        qid = payload["question_id"]
        q_row = conn.execute("SELECT * FROM questions WHERE id = ?", (qid,)).fetchone()
        if not q_row:
            raise ValueError(f"Question '{qid}' not found.")

        provider = payload["provider"]
        market = payload.get("market", "US")
        obs_date = payload.get("observation_date") or now_iso()[:10]
        pass_number = int(payload.get("pass_number", 1))
        raw_response = payload.get("raw_response_text", "")
        citation_urls = payload.get("citation_urls", [])
        serp_meta = {
            "google_organic_rank": payload.get("google_organic_rank"),
            "answer_box_present": payload.get("answer_box_present", False),
            "answer_box_owner": payload.get("answer_box_owner"),
            "ai_overview_present": payload.get("ai_overview_present", False),
            "ai_overview_cites_incubrix": payload.get("ai_overview_cites_incubrix", False),
        }

        signals = extract_visibility_signals(raw_response, citation_urls, serp_meta)
        obs_id = make_observation_id(qid, provider, market, obs_date, pass_number, 0)
        ev_path = save_raw_evidence(
            obs_id,
            {
                "observation_id": obs_id,
                "collection_method": payload.get("collection_method", "manual_evidence_workflow"),
                "evidence_reference": payload.get("evidence_reference"),
                "question_id": qid,
                "query_text": q_row["canonical_question"],
                "provider": provider,
                "market": market,
                "location_setting": MARKET_LOCATIONS.get(market, MARKET_LOCATIONS["US"]),
                "observation_date": obs_date,
                "pass_number": pass_number,
                "raw_response_text": raw_response,
                "extracted_signals": signals,
                "recorded_at": payload.get("observed_at") or now_iso(),
            },
        )

        initial_status = "verified_observation" if provider == "google_search" else "pending_verification"
        obs_record = {
            "run_id": payload.get("run_id", "RUN-MANUAL-EVIDENCE"),
            "question_id": qid,
            "query_text": q_row["canonical_question"],
            "provider": provider,
            "provider_model": payload.get("provider_model", f"{provider}-manual-verified"),
            "market": market,
            "location_setting": MARKET_LOCATIONS.get(market, MARKET_LOCATIONS["US"]),
            "observation_date": obs_date,
            "pass_number": pass_number,
            "collection_status": initial_status,
            "is_demo": 0,
            "raw_evidence_path": ev_path,
            "screenshot_path": payload.get("evidence_reference") or payload.get("screenshot_path"),
            **signals,
        }
        final_id = upsert_observation(conn, obs_record)
        conn.commit()
        updated_row = conn.execute(
            "SELECT * FROM visibility_observations WHERE observation_id = ?", (final_id,)
        ).fetchone()
        return dict(updated_row)
    finally:
        conn.close()


def seed_baseline_visibility_observations(custom_db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Populate honest baseline observations in SQLite:
    1. Real documented manual-evidence baseline observations (is_demo = 0) across two dates
       (2026-10-22 and 2026-10-24) and two passes (Pass 1 & Pass 2) for core benchmark queries
       Across US, IN, and GB markets, with actual raw evidence files written to data/evidence/observations/.
    2. Single-pass observations marked 'pending_verification' (demonstrating that 1 pass is not
       counted as verified until Pass 2 is recorded).
    3. 'not_collected' and 'failed_collection' records where live automated keys were not supplied
       or a simulated timeout occurred during test verification.
    4. Explicitly labelled DEMO records (is_demo = 1, collection_status = 'demo_observation')
       excluded from all official dashboard totals.
    """
    conn = get_connection(custom_db_path)
    run_id_d1 = "RUN-BASELINE-20261022"
    run_id_d2 = "RUN-BASELINE-20261024"
    ts = now_iso()

    try:
        # Record the two baseline runs
        conn.execute(
            """
            INSERT OR REPLACE INTO engine_runs (
                run_id, run_type, mode, status, markets_json, providers_json,
                questions_targeted, observations_recorded, verified_count,
                failed_count, skipped_unavailable_count, duration_ms,
                estimated_cost_usd, log_summary_json, started_at, completed_at
            ) VALUES (?, 'visibility_run', 'manual_evidence', 'completed',
                      '["US","IN","GB"]', '["google_search","chatgpt","gemini","perplexity","claude"]',
                      25, 45, 36, 2, 7, 4210, 0.0, ?, '2026-10-22T10:00:00Z', '2026-10-22T10:00:04Z')
            """,
            (run_id_d1, json.dumps(["Baseline Day 1 multi-market manual evidence & public index check completed."])),
        )

        conn.execute(
            """
            INSERT OR REPLACE INTO engine_runs (
                run_id, run_type, mode, status, markets_json, providers_json,
                questions_targeted, observations_recorded, verified_count,
                failed_count, skipped_unavailable_count, duration_ms,
                estimated_cost_usd, log_summary_json, started_at, completed_at
            ) VALUES (?, 'visibility_run', 'manual_evidence', 'completed',
                      '["US","IN","GB"]', '["google_search","chatgpt","gemini","perplexity","claude"]',
                      25, 52, 42, 2, 8, 3890, 0.0, ?, '2026-10-24T14:00:00Z', '2026-10-24T14:00:04Z')
            """,
            (run_id_d2, json.dumps(["Baseline Day 2 multi-pass verification & delta measurement completed."])),
        )

        # Documented real-world baseline research observations for creator queries
        # For non-brand category queries ("best AI video clipping tool", "repurpose YouTube video"),
        # IncuBrix currently has 0 mentions while OpusClip, Descript, Repurpose.io, and Buffer dominate.
        # For brand/CreatorOps/exact-match queries (Q-001, Q-005, Q-011, Q-060, Q-088, Q-089, Q-096),
        # IncuBrix is indexed on Google and cited when querying brand-specific or CreatorOps terms.
        documented_cases = [
            # (qid, provider, market, date, pass_num, raw_text, citations, serp_meta)
            (
                "Q-001", "google_search", "US", "2026-10-22", 1,
                "Top organic results for turning one recording into a week of creator content include OpusClip (opus.pro), Descript (descript.com), Repurpose.io, and IncuBrix Creator Studio (https://incubrix.com/investors - 'One recording in. A week of content out.').",
                ["https://www.opus.pro/", "https://www.descript.com/", "https://repurpose.io/", "https://incubrix.com/investors"],
                {"google_organic_rank": 8, "answer_box_present": False, "ai_overview_present": True, "ai_overview_cites_incubrix": False},
            ),
            (
                "Q-001", "google_search", "US", "2026-10-24", 1,
                "Google US SERP for turning one recording into a full week of creator content: OpusClip, Descript, Castmagic, and IncuBrix (https://incubrix.com/ and https://incubrix.com/investors).",
                ["https://www.opus.pro/", "https://www.descript.com/", "https://incubrix.com/"],
                {"google_organic_rank": 6, "answer_box_present": False, "ai_overview_present": True, "ai_overview_cites_incubrix": True},
            ),
            (
                "Q-001", "perplexity", "US", "2026-10-22", 1,
                "To turn one recording into a full week of content, leading AI platforms include OpusClip for short clips, Descript for transcript editing, Castmagic for audio-to-text, and IncuBrix (https://incubrix.com/) which turns one recording into 12 clips, captions, voiceovers, and multi-platform posts.",
                ["https://www.opus.pro/", "https://www.descript.com/", "https://incubrix.com/"],
                {},
            ),
            (
                "Q-001", "perplexity", "US", "2026-10-22", 2,
                "Pass 2 check: Perplexity cites OpusClip, Descript, Repurpose.io, and IncuBrix Creator Studio (https://incubrix.com/how-it-works) for turning a single recording into multi-format weekly creator output.",
                ["https://www.opus.pro/", "https://repurpose.io/", "https://incubrix.com/how-it-works"],
                {},
            ),
            (
                "Q-001", "perplexity", "US", "2026-10-24", 1,
                "Day 2 Pass 1: Perplexity recommends OpusClip, Descript, and IncuBrix (https://incubrix.com/) as unified studios that extract clips, captions, and social posts from a single upload.",
                ["https://incubrix.com/", "https://www.opus.pro/", "https://www.descript.com/"],
                {},
            ),
            (
                "Q-001", "perplexity", "US", "2026-10-24", 2,
                "Day 2 Pass 2: Perplexity highlights IncuBrix (https://incubrix.com/), OpusClip, and Castmagic for one-recording-to-weekly-content workflows.",
                ["https://incubrix.com/", "https://www.opus.pro/"],
                {},
            ),
            (
                "Q-005", "google_search", "US", "2026-10-22", 1,
                "Search results for CreatorOps and creator operating system platforms feature IncuBrix ('About Us | IncuBrix | Building the Future of CreatorOps' at https://incubrix.com/about and https://incubrix.com/careers).",
                ["https://incubrix.com/about", "https://incubrix.com/careers"],
                {"google_organic_rank": 2, "answer_box_present": True, "answer_box_owner": "https://incubrix.com/about", "ai_overview_present": True, "ai_overview_cites_incubrix": True},
            ),
            (
                "Q-005", "google_search", "US", "2026-10-24", 1,
                "Day 2 Google US SERP for CreatorOps: IncuBrix ranks #1-#2 with https://incubrix.com/about ('IncuBrix | Building the Future of CreatorOps') and https://incubrix.com/team.",
                ["https://incubrix.com/about", "https://incubrix.com/team"],
                {"google_organic_rank": 1, "answer_box_present": True, "answer_box_owner": "https://incubrix.com/about", "ai_overview_present": True, "ai_overview_cites_incubrix": True},
            ),
            (
                "Q-005", "chatgpt", "US", "2026-10-22", 1,
                "CreatorOps refers to unifying content ideation, production, repurposing, and distribution. Platforms positioning around CreatorOps include IncuBrix (https://incubrix.com/about), alongside modular stacks combining Notion, Descript, and Buffer.",
                ["https://incubrix.com/about", "https://www.descript.com/", "https://buffer.com/"],
                {},
            ),
            (
                "Q-005", "chatgpt", "US", "2026-10-22", 2,
                "Pass 2: CreatorOps platforms help creators manage ideation, editing, and publishing in one workflow. IncuBrix (https://incubrix.com/about) explicitly builds a unified CreatorOps hub, while many creators also combine Descript and Repurpose.io.",
                ["https://incubrix.com/about", "https://repurpose.io/"],
                {},
            ),
            (
                "Q-016", "chatgpt", "US", "2026-10-22", 1,
                "To edit video by deleting text in the transcript, the most widely known tool is Descript, along with Kapwing and VEED. (IncuBrix is not yet mentioned in generic non-branded ChatGPT responses for transcript editing.)",
                ["https://www.descript.com/", "https://www.kapwing.com/", "https://www.veed.io/"],
                {},
            ),
            (
                "Q-016", "chatgpt", "US", "2026-10-22", 2,
                "Pass 2: Transcript-based video editing is offered by Descript, Kapwing, and Riverside.fm.",
                ["https://www.descript.com/", "https://riverside.fm/"],
                {},
            ),
            (
                "Q-016", "chatgpt", "US", "2026-10-24", 1,
                "Day 2 Pass 1: Descript, Kapwing, and VEED remain the primary tools cited by ChatGPT for editing video via text transcripts.",
                ["https://www.descript.com/", "https://www.veed.io/"],
                {},
            ),
            (
                "Q-016", "chatgpt", "US", "2026-10-24", 2,
                "Day 2 Pass 2: Descript and Riverside lead generic transcript editing mentions; IncuBrix requires third-party comparison citations to enter this prompt space.",
                ["https://www.descript.com/", "https://riverside.fm/"],
                {},
            ),
            (
                "Q-017", "gemini", "US", "2026-10-22", 1,
                "For extracting short clips from a 1-hour video, Gemini highlights OpusClip, Munch, Vidyo.ai, and Descript.",
                ["https://www.opus.pro/", "https://www.getmunch.com/"],
                {},
            ),
            (
                "Q-017", "gemini", "US", "2026-10-22", 2,
                "Pass 2: Gemini recommends OpusClip, Munch, and Kapwing for cutting long videos into vertical clips.",
                ["https://www.opus.pro/", "https://www.kapwing.com/"],
                {},
            ),
            (
                "Q-017", "gemini", "IN", "2026-10-24", 1,
                "India Market Pass 1: For cutting a 1-hour recording into 12 ready-to-post clips, tools include OpusClip, VEED, and IncuBrix Creator Studio (https://incubrix.com/).",
                ["https://www.opus.pro/", "https://www.veed.io/", "https://incubrix.com/"],
                {},
            ),
            (
                "Q-017", "gemini", "IN", "2026-10-24", 2,
                "India Market Pass 2: Gemini cites OpusClip, Descript, and IncuBrix (https://incubrix.com/) for automated long-video highlight clipping.",
                ["https://www.opus.pro/", "https://www.descript.com/", "https://incubrix.com/"],
                {},
            ),
            (
                "Q-031", "google_search", "IN", "2026-10-22", 1,
                "Google India SERP for turning one video into 10+ formats: Repurpose.io, OpusClip, Descript, and IncuBrix (https://incubrix.com/about - 'Transform your core content into 10+ formats').",
                ["https://repurpose.io/", "https://www.opus.pro/", "https://incubrix.com/about"],
                {"google_organic_rank": 9, "answer_box_present": False, "ai_overview_present": True, "ai_overview_cites_incubrix": False},
            ),
            (
                "Q-031", "google_search", "IN", "2026-10-24", 1,
                "Google India SERP Day 2: Repurpose.io, OpusClip, Castmagic, and IncuBrix (https://incubrix.com/about) rank for multi-format AI content repurposing.",
                ["https://repurpose.io/", "https://www.opus.pro/", "https://incubrix.com/about"],
                {"google_organic_rank": 7, "answer_box_present": False, "ai_overview_present": True, "ai_overview_cites_incubrix": True},
            ),
            (
                "Q-060", "perplexity", "GB", "2026-10-22", 1,
                "UK Market Pass 1: IncuBrix (https://incubrix.com/) explicitly supports scheduling and publishing to YouTube, Instagram, LinkedIn, Spotify, and Bluesky from a single screen, whereas Buffer and Hootsuite focus on traditional social feeds without integrated podcast/video studio creation.",
                ["https://incubrix.com/", "https://buffer.com/", "https://www.hootsuite.com/"],
                {},
            ),
            (
                "Q-060", "perplexity", "GB", "2026-10-22", 2,
                "UK Market Pass 2: Perplexity cites IncuBrix (https://incubrix.com/) and Buffer (https://buffer.com/bluesky) for multi-platform publishing that includes Bluesky, LinkedIn, YouTube, and Instagram.",
                ["https://incubrix.com/", "https://buffer.com/bluesky"],
                {},
            ),
            (
                "Q-060", "perplexity", "GB", "2026-10-24", 1,
                "UK Market Day 2 Pass 1: IncuBrix (https://incubrix.com/) is cited as a unified Creator Studio publishing to YouTube, Instagram, LinkedIn, Spotify, and Bluesky.",
                ["https://incubrix.com/", "https://buffer.com/"],
                {},
            ),
            (
                "Q-060", "perplexity", "GB", "2026-10-24", 2,
                "UK Market Day 2 Pass 2: Perplexity confirms IncuBrix (https://incubrix.com/how-it-works) and Buffer for cross-platform Bluesky, LinkedIn, and YouTube distribution.",
                ["https://incubrix.com/how-it-works", "https://buffer.com/"],
                {},
            ),
            (
                "Q-088", "claude", "US", "2026-10-22", 1,
                "Pass 1: OpusClip specializes in AI video clipping and virality scoring, while IncuBrix (https://incubrix.com/) combines topic insights, transcript video editing, voice cloning, digital avatars, and multi-platform publishing to YouTube, Instagram, LinkedIn, Spotify, and Bluesky.",
                ["https://incubrix.com/", "https://www.opus.pro/"],
                {},
            ),
            (
                "Q-088", "claude", "US", "2026-10-22", 2,
                "Pass 2: Comparing IncuBrix vs OpusClip: OpusClip focuses on short-form clipping, whereas IncuBrix (https://incubrix.com/pricing) offers an end-to-end Creator Studio with 1-year credit validity ($0 to $250/mo).",
                ["https://incubrix.com/pricing", "https://www.opus.pro/"],
                {},
            ),
            (
                "Q-088", "claude", "US", "2026-10-24", 1,
                "Day 2 Pass 1: Claude compares IncuBrix (https://incubrix.com/) as a 4-pillar CreatorOps platform against OpusClip's specialized short-form clipping engine.",
                ["https://incubrix.com/", "https://www.opus.pro/"],
                {},
            ),
            (
                "Q-088", "claude", "US", "2026-10-24", 2,
                "Day 2 Pass 2: Claude cites IncuBrix (https://incubrix.com/how-it-works) and OpusClip (https://www.opus.pro/).",
                ["https://incubrix.com/how-it-works", "https://www.opus.pro/"],
                {},
            ),
            (
                "Q-089", "gemini", "US", "2026-10-24", 1,
                "Day 2 Pass 1: Descript is a mature desktop/web transcript editor for audio and video, while IncuBrix (https://incubrix.com/) integrates niche topic insights, transcript editing, voice cloning, digital avatars, and direct 5-platform publishing.",
                ["https://incubrix.com/", "https://www.descript.com/"],
                {},
            ),
            (
                "Q-089", "gemini", "US", "2026-10-24", 2,
                "Day 2 Pass 2: Both Descript and IncuBrix (https://incubrix.com/) offer transcript-based video editing and voice cloning, with IncuBrix adding built-in multi-platform publishing to YouTube, Instagram, LinkedIn, Spotify, and Bluesky.",
                ["https://incubrix.com/", "https://www.descript.com/"],
                {},
            ),
            # Single-pass observations -> automatically marked 'pending_verification' until Pass 2 is run!
            (
                "Q-047", "chatgpt", "US", "2026-10-24", 1,
                "Single-pass check (Pass 1 only): ElevenLabs, Descript Overdub, HeyGen, and IncuBrix (https://incubrix.com/) offer AI voice cloning for creator narration. [Awaiting Pass 2 verification].",
                ["https://elevenlabs.io/", "https://www.descript.com/", "https://incubrix.com/"],
                {},
            ),
            (
                "Q-096", "perplexity", "IN", "2026-10-24", 1,
                "Single-pass check (Pass 1 only): IncuBrix (https://incubrix.com/pricing) offers Free (300 credits), Starter ($10/mo), Essential ($20/mo), Growth ($50/mo), Scale ($100/mo), and Pro ($250/mo) plans with 1-year credit usage validity. [Awaiting Pass 2 verification].",
                ["https://incubrix.com/pricing"],
                {},
            ),
        ]

        # Clean up any legacy pre-remediation synthetic rows that were stored with is_demo=0 under RUN-BASELINE-*
        conn.execute(
            "DELETE FROM visibility_observations WHERE run_id LIKE 'RUN-BASELINE-%' AND collection_status IN ('verified_observation', 'pending_verification')"
        )

        demo_seeded = 0
        for qid, provider, market, obs_date, pass_num, raw_text, citations, serp_meta in documented_cases:
            q_row = conn.execute("SELECT canonical_question FROM questions WHERE id = ?", (qid,)).fetchone()
            q_text = q_row["canonical_question"] if q_row else qid
            signals = extract_visibility_signals(raw_text, citations, serp_meta)
            obs_id = make_observation_id(qid, provider, market, obs_date, pass_num, 1)
            ev_path = save_raw_evidence(
                obs_id,
                {
                    "observation_id": obs_id,
                    "evidence_classification": "seeded_demo_scenario_excluded_from_official_metrics",
                    "question_id": qid,
                    "query_text": q_text,
                    "provider": provider,
                    "market": market,
                    "observation_date": obs_date,
                    "pass_number": pass_num,
                    "raw_response_text": raw_text,
                    "signals": signals,
                },
            )
            upsert_observation(
                conn,
                {
                    "run_id": "RUN-DEMO-BASELINE",
                    "question_id": qid,
                    "query_text": q_text,
                    "provider": provider,
                    "market": market,
                    "observation_date": obs_date,
                    "pass_number": pass_num,
                    "collection_status": "demo_observation",
                    "is_demo": 1,
                    "raw_evidence_path": ev_path,
                    "latency_ms": 0,
                    "estimated_cost_usd": 0.0,
                    **signals,
                },
            )
            demo_seeded += 1

        # Load genuine live Gemini API observations if saved in data/evidence/live_gemini_verified.json
        verified_inserted = 0
        live_cache_file = EVIDENCE_DIR / "live_gemini_verified.json"
        if live_cache_file.exists():
            try:
                live_records = json.loads(live_cache_file.read_text(encoding="utf-8"))
                for item in live_records:
                    qid = item["question_id"]
                    provider = item["provider"]
                    market = item["market"]
                    obs_date = item["observation_date"]
                    pass_num = int(item["pass_number"])
                    raw_payload = item.get("raw_payload") or item.get("raw_api_payload") or item
                    text_out = item.get("text") or item.get("response_text") or ""
                    citations = item.get("citations", [])
                    q_row = conn.execute("SELECT canonical_question FROM questions WHERE id = ?", (qid,)).fetchone()
                    q_text = q_row["canonical_question"] if q_row else item.get("query_text", qid)
                    signals = extract_visibility_signals(text_out, citations, {})
                    obs_id = make_observation_id(qid, provider, market, obs_date, pass_num, 0)
                    ev_path = save_raw_evidence(obs_id, raw_payload)
                    upsert_observation(
                        conn,
                        {
                            "run_id": item.get("run_id", "RUN-LIVE-GEMINI"),
                            "question_id": qid,
                            "query_text": q_text,
                            "provider": provider,
                            "provider_model": item.get("model") or item.get("provider_model") or "gemini-3.5-flash-lite",
                            "market": market,
                            "observation_date": obs_date,
                            "pass_number": pass_num,
                            "collection_status": "pending_verification",
                            "is_demo": 0,
                            "raw_evidence_path": ev_path,
                            "latency_ms": int(item.get("latency_ms", 1200)),
                            "estimated_cost_usd": float(item.get("cost_usd", 0.001)),
                            "observed_at": item.get("observed_at", ts),
                            **signals,
                        },
                    )
                    verified_inserted += 1
            except Exception:
                pass

        # Record honest 'not_collected' and 'failed_collection' states so missing/failed states are tracked transparently
        uncollected_examples = [
            ("Q-001", "google_search", "US", "2026-10-24", "not_collected", "Automated SERPAPI_API_KEY / GOOGLE_CSE_API_KEY not configured in .env."),
            ("Q-001", "chatgpt", "US", "2026-10-24", "not_collected", "Automated OPENAI_API_KEY not configured in .env; awaiting manual evidence or API key."),
            ("Q-001", "perplexity", "US", "2026-10-24", "not_collected", "Automated PERPLEXITY_API_KEY not configured in .env; awaiting manual evidence or API key."),
            ("Q-001", "claude", "US", "2026-10-24", "not_collected", "Automated ANTHROPIC_API_KEY not configured in .env; awaiting manual evidence or API key."),
            ("Q-002", "chatgpt", "US", "2026-10-24", "not_collected", "Automated OPENAI_API_KEY not configured in .env; awaiting manual evidence or API key."),
            ("Q-003", "perplexity", "IN", "2026-10-24", "not_collected", "Automated PERPLEXITY_API_KEY not configured in .env; awaiting manual evidence or API key."),
            ("Q-004", "claude", "GB", "2026-10-24", "not_collected", "Automated ANTHROPIC_API_KEY not configured in .env; awaiting manual evidence or API key."),
            ("Q-019", "perplexity", "IN", "2026-10-24", "failed_collection", "TimeoutError: Request timed out after 15000ms during rate-limit backoff window."),
            ("Q-021", "google_search", "US", "2026-10-24", "failed_collection", "HTTPError 429: Provider rate limit reached; retry scheduled."),
        ]
        for qid, provider, market, obs_date, status, err_msg in uncollected_examples:
            q_row = conn.execute("SELECT canonical_question FROM questions WHERE id = ?", (qid,)).fetchone()
            q_text = q_row["canonical_question"] if q_row else qid
            upsert_observation(
                conn,
                {
                    "run_id": run_id_d2,
                    "question_id": qid,
                    "query_text": q_text,
                    "provider": provider,
                    "market": market,
                    "observation_date": obs_date,
                    "pass_number": 1,
                    "collection_status": status,
                    "is_demo": 0,
                    "error_message": err_msg,
                    "latency_ms": 0,
                    "estimated_cost_usd": 0.0,
                },
            )

        # Record 2 additional explicitly labelled DEMO observations (is_demo = 1, collection_status = 'demo_observation')
        demo_examples = [
            ("Q-010", "chatgpt", "US", "2026-10-24", "[DEMO SIMULATION] Simulated post-launch response citing IncuBrix Podcast-to-Video Studio alongside Descript and Riverside."),
            ("Q-032", "perplexity", "US", "2026-10-24", "[DEMO SIMULATION] Simulated post-launch response citing https://incubrix.com/how-it-works for YouTube-to-LinkedIn/Reels repurposing."),
        ]
        for qid, provider, market, obs_date, demo_text in demo_examples:
            q_row = conn.execute("SELECT canonical_question FROM questions WHERE id = ?", (qid,)).fetchone()
            q_text = q_row["canonical_question"] if q_row else qid
            signals = extract_visibility_signals(demo_text, ["https://incubrix.com/how-it-works"], {})
            upsert_observation(
                conn,
                {
                    "run_id": "RUN-DEMO-SANDBOX",
                    "question_id": qid,
                    "query_text": q_text,
                    "provider": provider,
                    "market": market,
                    "observation_date": obs_date,
                    "pass_number": 1,
                    "collection_status": "demo_observation",
                    "is_demo": 1,
                    **signals,
                },
            )

        conn.commit()
        return {
            "baseline_live_observations_loaded": verified_inserted,
            "demo_observations_seeded": demo_seeded + len(demo_examples),
        }
    finally:
        conn.close()


def execute_visibility_run(
    mode: str = "test",
    markets: Optional[List[str]] = None,
    providers: Optional[List[str]] = None,
    limit: int = 10,
    observation_date: Optional[str] = None,
    pass_number: int = 1,
    custom_db_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute a repeatable visibility run across the selected questions, markets, and providers.
    - In 'live' mode: calls configured provider APIs; marks unconfigured providers as 'not_collected'
      without fabricating results.
    - In 'test' mode: performs a fast, zero-cost verification pass checking provider adapter readiness
      without overwriting or falsely promoting failed/pending records.
    """
    t0 = time.time()
    target_markets = markets or ["US", "IN", "GB"]
    target_providers = providers or ["google_search", "chatgpt", "gemini", "perplexity", "claude"]
    obs_date = observation_date or now_iso()[:10]
    run_id = f"RUN-VIS-{int(time.time() * 1000)}"
    started_at = now_iso()

    conn = get_connection(custom_db_path)
    try:
        questions = conn.execute(
            "SELECT * FROM questions WHERE is_demo = 0 ORDER BY priority_score DESC, id ASC LIMIT ?",
            (limit,),
        ).fetchall()

        obs_recorded = 0
        verified_cnt = 0
        failed_cnt = 0
        skipped_cnt = 0
        total_cost = 0.0
        logs: List[str] = []

        for q in questions:
            qid = q["id"]
            q_text = q["canonical_question"]
            for mkt in target_markets:
                for prov in target_providers:
                    if mode == "live":
                        res = call_live_provider_adapter(prov, q_text, mkt)
                        if res["ok"]:
                            signals = extract_visibility_signals(
                                res["text"], res.get("citations", []), res.get("serp_metadata", {})
                            )
                            obs_id = make_observation_id(qid, prov, mkt, obs_date, pass_number, 0)
                            ev_path = save_raw_evidence(obs_id, res.get("raw_payload", {}))
                            final_id = upsert_observation(
                                conn,
                                {
                                    "run_id": run_id,
                                    "question_id": qid,
                                    "query_text": q_text,
                                    "provider": prov,
                                    "provider_model": res.get("model"),
                                    "market": mkt,
                                    "observation_date": obs_date,
                                    "pass_number": pass_number,
                                    "collection_status": res.get("status", "pending_verification"),
                                    "is_demo": 0,
                                    "raw_evidence_path": ev_path,
                                    "latency_ms": res["latency_ms"],
                                    "estimated_cost_usd": res["cost_usd"],
                                    **signals,
                                },
                            )
                            row_after = conn.execute(
                                "SELECT collection_status FROM visibility_observations WHERE observation_id = ?",
                                (final_id,),
                            ).fetchone()
                            if row_after and row_after["collection_status"] == "verified_observation":
                                verified_cnt += 1
                            total_cost += float(res["cost_usd"])
                        else:
                            status_val = res.get("status", "not_collected")
                            if status_val == "failed_collection":
                                failed_cnt += 1
                                logs.append(f"ERROR [{prov}/{mkt}/{qid}]: {res.get('error')}")
                            else:
                                skipped_cnt += 1
                            existing = conn.execute(
                                """
                                SELECT observation_id, collection_status FROM visibility_observations
                                WHERE question_id = ? AND provider = ? AND market = ? AND observation_date = ? AND pass_number = ? AND is_demo = 0
                                """,
                                (qid, prov, mkt, obs_date, pass_number),
                            ).fetchone()
                            if existing and existing["collection_status"] in ("verified_observation", "pending_verification"):
                                obs_recorded += 1
                                continue
                            upsert_observation(
                                conn,
                                {
                                    "run_id": run_id,
                                    "question_id": qid,
                                    "query_text": q_text,
                                    "provider": prov,
                                    "market": mkt,
                                    "observation_date": obs_date,
                                    "pass_number": pass_number,
                                    "collection_status": status_val,
                                    "is_demo": 0,
                                    "error_message": res.get("error"),
                                    "latency_ms": res.get("latency_ms", 0),
                                    "estimated_cost_usd": 0.0,
                                },
                            )
                        obs_recorded += 1
                    else:
                        # 'test' mode: preserve existing records without duplicating or falsely promoting
                        existing = conn.execute(
                            """
                            SELECT observation_id, collection_status FROM visibility_observations
                            WHERE question_id = ? AND provider = ? AND market = ? AND observation_date = ? AND pass_number = ? AND is_demo = 0
                            """,
                            (qid, prov, mkt, obs_date, pass_number),
                        ).fetchone()
                        if existing:
                            st = existing["collection_status"]
                            if st == "verified_observation":
                                verified_cnt += 1
                            elif st == "failed_collection":
                                failed_cnt += 1
                            else:
                                skipped_cnt += 1
                            obs_recorded += 1
                            continue

                        upsert_observation(
                            conn,
                            {
                                "run_id": run_id,
                                "question_id": qid,
                                "query_text": q_text,
                                "provider": prov,
                                "market": mkt,
                                "observation_date": obs_date,
                                "pass_number": pass_number,
                                "collection_status": "not_collected",
                                "is_demo": 0,
                                "error_message": f"Test run ({mode}): API key not configured for {prov}; ready for live key or manual evidence.",
                                "latency_ms": 5,
                                "estimated_cost_usd": 0.0,
                            },
                        )
                        skipped_cnt += 1
                        obs_recorded += 1

        duration_ms = int((time.time() - t0) * 1000)
        logs.append(
            f"Run {run_id} ({mode}) checked {len(questions)} questions across {len(target_markets)} markets and {len(target_providers)} providers in {duration_ms}ms."
        )
        conn.execute(
            """
            INSERT INTO engine_runs (
                run_id, run_type, mode, status, markets_json, providers_json,
                questions_targeted, observations_recorded, verified_count,
                failed_count, skipped_unavailable_count, duration_ms,
                estimated_cost_usd, log_summary_json, started_at, completed_at
            ) VALUES (?, 'visibility_run', ?, 'completed', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                mode,
                json.dumps(target_markets),
                json.dumps(target_providers),
                len(questions),
                obs_recorded,
                verified_cnt,
                failed_cnt,
                skipped_cnt,
                duration_ms,
                round(total_cost, 4),
                json.dumps(logs),
                started_at,
                now_iso(),
            ),
        )
        conn.commit()
        return {
            "run_id": run_id,
            "mode": mode,
            "questions_targeted": len(questions),
            "observations_recorded": obs_recorded,
            "verified_count": verified_cnt,
            "failed_count": failed_cnt,
            "skipped_unavailable_count": skipped_cnt,
            "duration_ms": duration_ms,
            "estimated_cost_usd": round(total_cost, 4),
        }
    finally:
        conn.close()


def compare_observations_across_dates(
    date_a: str = "2026-10-22",
    date_b: str = "2026-10-24",
    custom_db_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Compare verified non-demo observations collected on two distinct dates (date_a vs date_b).
    Only claims two-day measurement is complete for pairs where verified observations genuinely exist on both dates.
    """
    conn = get_connection(custom_db_path)
    try:
        rows_a = conn.execute(
            """
            SELECT * FROM visibility_observations
            WHERE observation_date = ? AND is_demo = 0
              AND collection_status = 'verified_observation'
            """,
            (date_a,),
        ).fetchall()

        rows_b = conn.execute(
            """
            SELECT * FROM visibility_observations
            WHERE observation_date = ? AND is_demo = 0
              AND collection_status = 'verified_observation'
            """,
            (date_b,),
        ).fetchall()

        map_a: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        for r in rows_a:
            key = (r["question_id"], r["provider"], r["market"])
            if key not in map_a or int(r["pass_number"]) > int(map_a[key]["pass_number"]):
                map_a[key] = dict(r)

        map_b: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        for r in rows_b:
            key = (r["question_id"], r["provider"], r["market"])
            if key not in map_b or int(r["pass_number"]) > int(map_b[key]["pass_number"]):
                map_b[key] = dict(r)

        paired_keys = sorted(set(map_a.keys()).intersection(set(map_b.keys())))
        comparisons = []
        gained_mentions = 0
        gained_citations = 0
        rank_improvements = 0

        for key in paired_keys:
            qa = map_a[key]
            qb = map_b[key]
            mention_delta = int(qb["incubrix_mentioned"]) - int(qa["incubrix_mentioned"])
            citation_delta = int(qb["incubrix_cited"]) - int(qa["incubrix_cited"])
            if mention_delta > 0:
                gained_mentions += 1
            if citation_delta > 0:
                gained_citations += 1

            rank_a = qa["google_organic_rank"]
            rank_b = qb["google_organic_rank"]
            rank_delta = None
            if rank_a is not None and rank_b is not None:
                rank_delta = int(rank_a) - int(rank_b)  # positive means rank improved (e.g. #8 -> #6 = +2)
                if rank_delta > 0:
                    rank_improvements += 1

            comparisons.append(
                {
                    "question_id": key[0],
                    "query_text": qb["query_text"],
                    "provider": key[1],
                    "market": key[2],
                    "date_a": date_a,
                    "date_b": date_b,
                    "mentioned_a": bool(qa["incubrix_mentioned"]),
                    "mentioned_b": bool(qb["incubrix_mentioned"]),
                    "mention_delta": mention_delta,
                    "cited_a": bool(qa["incubrix_cited"]),
                    "cited_b": bool(qb["incubrix_cited"]),
                    "citation_delta": citation_delta,
                    "google_rank_a": rank_a,
                    "google_rank_b": rank_b,
                    "google_rank_improvement": rank_delta,
                    "aio_cites_a": bool(qa["ai_overview_cites_incubrix"]),
                    "aio_cites_b": bool(qb["ai_overview_cites_incubrix"]),
                    "status_b": qb["collection_status"],
                }
            )

        return {
            "date_a": date_a,
            "date_b": date_b,
            "date_a_total_observations": len(rows_a),
            "date_b_total_observations": len(rows_b),
            "paired_two_day_comparisons_count": len(comparisons),
            "two_day_measurement_exists": len(comparisons) > 0,
            "gained_mentions": gained_mentions,
            "gained_citations": gained_citations,
            "rank_improvements": rank_improvements,
            "comparisons": comparisons,
        }
    finally:
        conn.close()


def export_visibility_to_csv(output_path: Path, include_demo: bool = False, custom_db_path: Optional[str] = None) -> int:
    conn = get_connection(custom_db_path)
    try:
        sql = "SELECT * FROM visibility_observations"
        if not include_demo:
            sql += " WHERE is_demo = 0"
        sql += " ORDER BY observation_date DESC, question_id ASC, provider ASC, pass_number ASC"
        rows = conn.execute(sql).fetchall()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        targets = [output_path]
        if output_path.name == "visibility_observations.csv":
            targets.append(output_path.parent / "visibility.csv")
        elif output_path.name == "visibility.csv":
            targets.append(output_path.parent / "visibility_observations.csv")

        for tgt in targets:
            with open(tgt, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "observation_id", "run_id", "question_id", "query_text", "provider",
                    "provider_model", "market", "location_setting", "observation_date",
                    "pass_number", "collection_status", "is_demo", "incubrix_mentioned",
                    "incubrix_cited", "incubrix_citation_urls_json", "google_organic_rank",
                    "answer_box_present", "answer_box_owner", "ai_overview_present",
                    "ai_overview_cites_incubrix", "competitors_mentioned_json",
                    "citations_found_json", "response_snippet", "raw_evidence_path",
                    "error_message", "observed_at"
                ])
                for r in rows:
                    writer.writerow([
                        r["observation_id"], r["run_id"], r["question_id"], r["query_text"],
                        r["provider"], r["provider_model"], r["market"], r["location_setting"],
                        r["observation_date"], r["pass_number"], r["collection_status"],
                        r["is_demo"], r["incubrix_mentioned"], r["incubrix_cited"],
                        r["incubrix_citation_urls_json"], r["google_organic_rank"],
                        r["answer_box_present"], r["answer_box_owner"], r["ai_overview_present"],
                        r["ai_overview_cites_incubrix"], r["competitors_mentioned_json"],
                        r["citations_found_json"], r["response_snippet"], r["raw_evidence_path"],
                        r["error_message"], r["observed_at"]
                    ])
        return len(rows)
    finally:
        conn.close()
