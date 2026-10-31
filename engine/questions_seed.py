import csv
import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from engine.db import get_connection, now_iso

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "to", "of", "in",
    "for", "on", "with", "as", "by", "at", "from", "that", "this", "it",
    "and", "or", "can", "i", "my", "you", "your", "do", "does"
}

VALID_CATEGORIES = {
    "Content Creation",
    "AI Video Editing",
    "Content Repurposing",
    "Captioning & Voiceovers",
    "Multi-Platform Publishing",
    "Creator Growth & Analytics",
    "Product Comparisons",
}

VALID_SOURCE_TYPES = {
    "search_autocomplete_paa",
    "public_community",
    "competitor_docs",
    "first_party_faq",
    "industry_directory",
    "editorial_research",
}


def normalize_question_fingerprint(text: str) -> str:
    """
    Create a deterministic normalized fingerprint for question deduplication
    without losing the core semantic tokens.
    """
    cleaned = text.lower().strip()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)
    tokens = [t for t in cleaned.split() if t and t not in STOPWORDS]
    if not tokens:
        tokens = cleaned.split()
    return " ".join(tokens)


def validate_question_record(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a creator question record and its provenance fields.
    """
    errors: List[str] = []
    q_text = str(record.get("canonical_question") or record.get("original_wording") or "").strip()
    if len(q_text) < 10:
        errors.append("Question text must be at least 10 characters.")
    orig = str(record.get("original_wording") or "").strip()
    if not orig:
        errors.append("original_wording is required to preserve provenance.")
    source_url = str(record.get("source_url") or "").strip()
    parsed = urlparse(source_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        errors.append(f"Invalid source_url: '{source_url}'. Must be a valid http/https URL.")
    source_type = str(record.get("source_type") or "").strip()
    if source_type not in VALID_SOURCE_TYPES:
        errors.append(f"Invalid source_type '{source_type}'.")
    col_date = str(record.get("collection_date") or "").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", col_date):
        errors.append(f"Invalid collection_date '{col_date}'. Expected YYYY-MM-DD.")
    cat = str(record.get("category") or "").strip()
    if cat not in VALID_CATEGORIES:
        errors.append(f"Invalid category '{cat}'.")
    return (len(errors) == 0, errors)


def deduplicate_questions(raw_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Deduplicate questions by normalized fingerprint while preserving full provenance
    (every source URL, source type, collection date, and original wording is appended
    to provenance_sources_json).
    """
    by_fingerprint: Dict[str, Dict[str, Any]] = {}
    ordered_fps: List[str] = []

    for item in raw_records:
        q_text = str(item.get("canonical_question") or item.get("original_wording") or "").strip()
        fp = normalize_question_fingerprint(q_text)
        provenance_entry = {
            "source_url": item.get("source_url", ""),
            "source_type": item.get("source_type", ""),
            "collection_date": item.get("collection_date", ""),
            "original_wording": item.get("original_wording", q_text),
        }

        if fp not in by_fingerprint:
            cloned = dict(item)
            cloned["normalized_fingerprint"] = fp
            existing_prov = cloned.get("provenance_sources", [])
            if isinstance(existing_prov, str):
                try:
                    existing_prov = json.loads(existing_prov)
                except Exception:
                    existing_prov = []
            prov_list = list(existing_prov) if existing_prov else [provenance_entry]
            cloned["provenance_sources"] = prov_list
            cloned["duplicate_merge_count"] = max(0, len(prov_list) - 1)
            by_fingerprint[fp] = cloned
            ordered_fps.append(fp)
        else:
            primary = by_fingerprint[fp]
            prov_list = primary["provenance_sources"]
            # Avoid exact duplicate provenance tuple
            if not any(
                p.get("source_url") == provenance_entry["source_url"]
                and p.get("original_wording") == provenance_entry["original_wording"]
                for p in prov_list
            ):
                prov_list.append(provenance_entry)
            primary["duplicate_merge_count"] = len(prov_list) - 1
            # Keep higher priority score if present
            if int(item.get("priority_score", 0)) > int(primary.get("priority_score", 0)):
                primary["priority_score"] = int(item["priority_score"])

    return [by_fingerprint[fp] for fp in ordered_fps]


# 100 Real Creator Questions across 7 categories + 6 provenance-duplicate variants (106 raw -> 100 unique)
RAW_CREATOR_QUESTIONS: List[Dict[str, Any]] = [
    # =========================================================================
    # CATEGORY 1: CONTENT CREATION (Q-001 to Q-015)
    # =========================================================================
    {
        "id": "Q-001",
        "canonical_question": "What is the best AI studio to turn one recording into a full week of creator content?",
        "original_wording": "best AI studio to turn one recording into a week of content for creators",
        "category": "Content Creation",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://incubrix.com/investors",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 98,
    },
    {
        "id": "Q-002",
        "canonical_question": "How can content creators find trending topics and niche content gaps using AI?",
        "original_wording": "how do creators find trending topics and content gaps in their niche with AI",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "YouTube Creator",
        "source_url": "https://support.google.com/youtube/answer/11914225",
        "source_type": "search_autocomplete_paa",
        "collection_date": "2026-10-20",
        "priority_score": 92,
    },
    {
        "id": "Q-003",
        "canonical_question": "What AI tool lets you create talking-head videos using a digital avatar without turning on a camera?",
        "original_wording": "AI tool for talking head video with digital avatar lip synced to script without filming",
        "category": "Content Creation",
        "search_intent": "commercial",
        "target_persona": "Faceless & Busy Creator",
        "source_url": "https://www.producthunt.com/categories/ai-video-generators",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 94,
    },
    {
        "id": "Q-004",
        "canonical_question": "How do solo creators convert a written blog post or script into a podcast episode with AI?",
        "original_wording": "convert written script or blog post into audio podcast automatically with AI voice",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "Podcaster & Newsletter Writer",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 88,
    },
    {
        "id": "Q-005",
        "canonical_question": "What is CreatorOps and what platforms provide an all-in-one operating system for creators?",
        "original_wording": "what is CreatorOps and best creator operating system platforms 2026",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "Creator Economy Founder",
        "source_url": "https://incubrix.com/about",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 96,
    },
    {
        "id": "Q-006",
        "canonical_question": "How can I generate short-form video scripts from trending niche insights automatically?",
        "original_wording": "generate short form video scripts from trending niche topics AI tool",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "Short-Form Creator",
        "source_url": "https://www.reddit.com/r/NewTubers/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 85,
    },
    {
        "id": "Q-007",
        "canonical_question": "Which AI content creation platforms preserve a creator's unique voice and perspective?",
        "original_wording": "AI content creation platform that keeps my own voice and taste instead of generic AI text",
        "category": "Content Creation",
        "search_intent": "commercial",
        "target_persona": "Thought Leader",
        "source_url": "https://incubrix.com/manifesto",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 89,
    },
    {
        "id": "Q-008",
        "canonical_question": "How to batch produce 30 days of YouTube Shorts and Instagram Reels in one sitting?",
        "original_wording": "how to batch create 30 days of YouTube Shorts and Reels in one sitting with AI",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "YouTube & IG Creator",
        "source_url": "https://www.reddit.com/r/content_marketing/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 90,
    },
    {
        "id": "Q-009",
        "canonical_question": "What are the best AI text-to-video tools for educators and B2B LinkedIn creators?",
        "original_wording": "best AI text to video tools for educators and B2B LinkedIn video creators",
        "category": "Content Creation",
        "search_intent": "commercial",
        "target_persona": "B2B Creator",
        "source_url": "https://www.g2.com/categories/ai-video-generator",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 84,
    },
    {
        "id": "Q-010",
        "canonical_question": "How can podcasters turn audio-only episodes into engaging video podcasts with AI?",
        "original_wording": "turn audio podcast into video podcast for YouTube and Spotify using AI",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "Podcaster",
        "source_url": "https://creators.spotify.com/",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 87,
    },
    {
        "id": "Q-011",
        "canonical_question": "What is the best free-to-start AI creator studio that uses credit-based pricing?",
        "original_wording": "free to start AI creator studio with credit based pricing plans",
        "category": "Content Creation",
        "search_intent": "transactional",
        "target_persona": "Indie Creator",
        "source_url": "https://incubrix.com/pricing",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 93,
    },
    {
        "id": "Q-012",
        "canonical_question": "How do creators overcome tool overload when managing ideation, editing, and publishing?",
        "original_wording": "how to solve creator tool overload instead of paying for 6 subscriptions",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "Full-Time Creator",
        "source_url": "https://incubrix.com/about",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 91,
    },
    {
        "id": "Q-013",
        "canonical_question": "Can AI generate newsletter drafts directly from a recorded YouTube video?",
        "original_wording": "can AI write a newsletter issue directly from my YouTube video recording",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "YouTuber & Substack Writer",
        "source_url": "https://www.reddit.com/r/Newsletter/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 83,
    },
    {
        "id": "Q-014",
        "canonical_question": "What AI workflow helps solo founders build a personal brand on LinkedIn and YouTube in 2 hours a week?",
        "original_wording": "AI workflow for solo founders to post on LinkedIn and YouTube in 2 hours per week",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "Solo Founder",
        "source_url": "https://www.indiehackers.com/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 86,
    },
    {
        "id": "Q-015",
        "canonical_question": "How do AI topic recommendation engines detect competitor content gaps on YouTube?",
        "original_wording": "how AI topic research tools spot competitor content gaps on YouTube",
        "category": "Content Creation",
        "search_intent": "informational",
        "target_persona": "YouTube Strategist",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 84,
    },

    # =========================================================================
    # CATEGORY 2: AI VIDEO EDITING (Q-016 to Q-030)
    # =========================================================================
    {
        "id": "Q-016",
        "canonical_question": "How do I edit video by deleting text in the transcript using AI?",
        "original_wording": "edit video like a text document delete sentence in transcript removes video clip",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "Video Podcaster",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 97,
    },
    {
        "id": "Q-017",
        "canonical_question": "What is the best AI tool to automatically extract the 12 best short clips from a 1-hour video?",
        "original_wording": "upload 1 hour video AI finds strongest moments and cuts 12 ready to post clips",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "Long-Form YouTuber",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 98,
    },
    {
        "id": "Q-018",
        "canonical_question": "How to automatically remove filler words, ums, and awkward silences from talking-head videos?",
        "original_wording": "automatically remove filler words ums ahs and pauses from talking head video AI",
        "category": "AI Video Editing",
        "search_intent": "informational",
        "target_persona": "Course Creator",
        "source_url": "https://www.descript.com/filler-words",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 90,
    },
    {
        "id": "Q-019",
        "canonical_question": "Which AI video editor automatically reframes 16:9 horizontal videos into 9:16 vertical clips with speaker tracking?",
        "original_wording": "AI video editor auto reframe 16:9 to 9:16 vertical with active speaker face tracking",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "Short-Form Editor",
        "source_url": "https://www.opus.pro/",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 93,
    },
    {
        "id": "Q-020",
        "canonical_question": "How can I fix a flubbed sentence in a recorded video using AI voice cloning and lip-sync?",
        "original_wording": "fix mistake in recorded video with AI voice clone overdub and lip sync",
        "category": "AI Video Editing",
        "search_intent": "informational",
        "target_persona": "YouTube Creator",
        "source_url": "https://www.reddit.com/r/VideoEditing/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 89,
    },
    {
        "id": "Q-021",
        "canonical_question": "What AI video editor detects viral hooks and high-retention moments in podcast recordings?",
        "original_wording": "AI video clipper that detects viral hooks and best moments in long podcasts",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "Podcast Host",
        "source_url": "https://www.producthunt.com/categories/video-editing",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 94,
    },
    {
        "id": "Q-022",
        "canonical_question": "How to edit multi-track podcast video interviews in the browser without Premiere Pro?",
        "original_wording": "browser based AI video editor for podcast interviews without Premiere Pro",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "Indie Podcaster",
        "source_url": "https://www.reddit.com/r/podcasting/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 86,
    },
    {
        "id": "Q-023",
        "canonical_question": "Can AI automatically add B-roll and dynamic zoom cuts to talking-head videos?",
        "original_wording": "AI tool to auto add B-roll and jump cuts to talking head videos",
        "category": "AI Video Editing",
        "search_intent": "informational",
        "target_persona": "Short-Form Creator",
        "source_url": "https://www.g2.com/categories/video-editing",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 83,
    },
    {
        "id": "Q-024",
        "canonical_question": "How to clean up background noise and echo in creator videos using AI audio enhancement?",
        "original_wording": "remove room echo and background noise from video recording with AI studio sound",
        "category": "AI Video Editing",
        "search_intent": "informational",
        "target_persona": "Mobile Creator",
        "source_url": "https://www.reddit.com/r/letsplay/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 81,
    },
    {
        "id": "Q-025",
        "canonical_question": "What is the fastest way to cut a 60-minute webinar into LinkedIn video snippets?",
        "original_wording": "fastest AI tool to cut a 60 minute webinar into LinkedIn video clips",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "B2B Marketer",
        "source_url": "https://www.capterra.com/video-editing-software/",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 88,
    },
    {
        "id": "Q-026",
        "canonical_question": "How do transcript-based video editors maintain frame-accurate cut points?",
        "original_wording": "how transcript based video editing keeps cuts smooth and natural",
        "category": "AI Video Editing",
        "search_intent": "informational",
        "target_persona": "Video Editor",
        "source_url": "https://www.descript.com/blog",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 78,
    },
    {
        "id": "Q-027",
        "canonical_question": "Which AI video editing platforms allow exporting clips formatted simultaneously for YouTube, Instagram, and LinkedIn?",
        "original_wording": "AI video editor that formats clips for YouTube Shorts Instagram Reels and LinkedIn at once",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "Social Media Manager",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 95,
    },
    {
        "id": "Q-028",
        "canonical_question": "How to trim bad takes out of a raw recording automatically before editing?",
        "original_wording": "AI tool that removes repeated bad takes and false starts from raw video",
        "category": "AI Video Editing",
        "search_intent": "informational",
        "target_persona": "YouTube Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 91,
    },
    {
        "id": "Q-029",
        "canonical_question": "What are the best low-cost AI video editors for creators producing 100+ short clips per month?",
        "original_wording": "most affordable AI video editor for 100+ short clips a month credit pricing",
        "category": "AI Video Editing",
        "search_intent": "transactional",
        "target_persona": "Content Agency",
        "source_url": "https://incubrix.com/pricing",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 89,
    },
    {
        "id": "Q-030",
        "canonical_question": "Can AI video editors automatically generate chapter markers and timestamps for YouTube descriptions?",
        "original_wording": "auto generate YouTube chapter timestamps from video transcript AI",
        "category": "AI Video Editing",
        "search_intent": "informational",
        "target_persona": "YouTube Creator",
        "source_url": "https://support.google.com/youtube/answer/9884579",
        "source_type": "search_autocomplete_paa",
        "collection_date": "2026-10-20",
        "priority_score": 82,
    },

    # =========================================================================
    # CATEGORY 3: CONTENT REPURPOSING (Q-031 to Q-045)
    # =========================================================================
    {
        "id": "Q-031",
        "canonical_question": "What is the best AI content repurposing tool to turn one YouTube video into 10+ platform formats?",
        "original_wording": "best AI content repurposing tool to transform one video into 10+ formats automatically",
        "category": "Content Repurposing",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://incubrix.com/about",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 99,
    },
    {
        "id": "Q-032",
        "canonical_question": "How to repurpose a long-form YouTube video into LinkedIn posts, Instagram Reels, and an email newsletter?",
        "original_wording": "repurpose YouTube video into LinkedIn posts Reels and newsletter in one workflow",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Creator-Entrepreneur",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 96,
    },
    {
        "id": "Q-033",
        "canonical_question": "How can podcasters repurpose a 60-minute Spotify podcast into daily social media clips and articles?",
        "original_wording": "how to turn a 60 minute podcast episode into daily clips and blog posts with AI",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Podcaster",
        "source_url": "https://repurpose.io/",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 94,
    },
    {
        "id": "Q-034",
        "canonical_question": "What AI platform repurposes video content for Bluesky, LinkedIn, Instagram, and YouTube simultaneously?",
        "original_wording": "AI repurposing tool that supports Bluesky LinkedIn Instagram YouTube and Spotify",
        "category": "Content Repurposing",
        "search_intent": "commercial",
        "target_persona": "Tech & Creator Economy Influencer",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 97,
    },
    {
        "id": "Q-035",
        "canonical_question": "How do I repurpose video transcripts into SEO-optimized blog posts without sounding like generic ChatGPT?",
        "original_wording": "turn video transcript into SEO blog post while keeping creator voice",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Content Marketer",
        "source_url": "https://www.reddit.com/r/Blogging/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 88,
    },
    {
        "id": "Q-036",
        "canonical_question": "What is the best automated workflow to turn Zoom webinars into short vertical video clips?",
        "original_wording": "automated workflow to repurpose Zoom webinars into vertical short clips",
        "category": "Content Repurposing",
        "search_intent": "commercial",
        "target_persona": "B2B SaaS Marketer",
        "source_url": "https://www.g2.com/categories/content-creation",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 85,
    },
    {
        "id": "Q-037",
        "canonical_question": "How to adapt the same video clip hook for LinkedIn vs Instagram Reels vs YouTube Shorts?",
        "original_wording": "how to rewrite captions and hooks when repurposing video for LinkedIn vs Reels vs Shorts",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Social Media Strategist",
        "source_url": "https://buffer.com/resources/",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 87,
    },
    {
        "id": "Q-038",
        "canonical_question": "Can AI convert a written Substack article into a narrated short-form video with captions?",
        "original_wording": "convert written newsletter article into narrated vertical video with voice clone",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Newsletter Creator",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 90,
    },
    {
        "id": "Q-039",
        "canonical_question": "How much time do creators save per week by automating content repurposing with AI?",
        "original_wording": "how many hours per week does AI content repurposing save solo creators",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Solo Creator",
        "source_url": "https://incubrix.com/manifesto",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 82,
    },
    {
        "id": "Q-040",
        "canonical_question": "What tools turn long livestream VODs into highlight clips and social threads automatically?",
        "original_wording": "AI tool to turn long livestream recordings into highlight clips and social posts",
        "category": "Content Repurposing",
        "search_intent": "commercial",
        "target_persona": "Streamer & Gaming Creator",
        "source_url": "https://www.reddit.com/r/Twitch/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 84,
    },
    {
        "id": "Q-041",
        "canonical_question": "How to repurpose podcast guest interviews into shareable audiograms and video quote cards?",
        "original_wording": "create video quote clips and audiograms from podcast interviews with AI",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Podcast Producer",
        "source_url": "https://www.headliner.app/",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 80,
    },
    {
        "id": "Q-042",
        "canonical_question": "Which AI repurposing platform combines video clipping, captioning, voiceover, and direct publishing?",
        "original_wording": "all in one AI repurposing platform with clipping captions voiceovers and publishing",
        "category": "Content Repurposing",
        "search_intent": "commercial",
        "target_persona": "Full-Time Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 98,
    },
    {
        "id": "Q-043",
        "canonical_question": "How to turn one keystone piece of content into omnichannel distribution without hiring an agency?",
        "original_wording": "turn one pillar video into omnichannel content without hiring a content agency",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Coach & Consultant",
        "source_url": "https://incubrix.com/waitlist",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 91,
    },
    {
        "id": "Q-044",
        "canonical_question": "What are the best practices for cross-posting repurposed Reels to YouTube Shorts without watermark penalties?",
        "original_wording": "cross post Reels to YouTube Shorts without watermark reach penalty",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "Short-Form Creator",
        "source_url": "https://support.google.com/youtube/answer/10059070",
        "source_type": "search_autocomplete_paa",
        "collection_date": "2026-10-20",
        "priority_score": 86,
    },
    {
        "id": "Q-045",
        "canonical_question": "How to extract key takeaways from an educational video to create a LinkedIn text post?",
        "original_wording": "extract key takeaways from YouTube video to write high engagement LinkedIn post",
        "category": "Content Repurposing",
        "search_intent": "informational",
        "target_persona": "B2B Creator",
        "source_url": "https://www.reddit.com/r/linkedin/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 83,
    },

    # =========================================================================
    # CATEGORY 4: CAPTIONING & VOICEOVERS (Q-046 to Q-059)
    # =========================================================================
    {
        "id": "Q-046",
        "canonical_question": "What is the best AI tool for animated word-by-word captions on YouTube Shorts and Instagram Reels?",
        "original_wording": "best AI tool for animated word by word captions on Shorts and Reels",
        "category": "Captioning & Voiceovers",
        "search_intent": "commercial",
        "target_persona": "Short-Form Creator",
        "source_url": "https://submagic.co/",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 93,
    },
    {
        "id": "Q-047",
        "canonical_question": "Which AI creator studio clones your voice for video narration and podcast voiceovers?",
        "original_wording": "AI creator studio that clones your voice for narration and scripts you never filmed",
        "category": "Captioning & Voiceovers",
        "search_intent": "commercial",
        "target_persona": "YouTube & Podcast Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 96,
    },
    {
        "id": "Q-048",
        "canonical_question": "How do burned-in captions impact watch time and retention on silent-autoplay social feeds?",
        "original_wording": "do burned in captions increase watch time on Instagram Reels and LinkedIn video",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "Social Media Manager",
        "source_url": "https://business.instagram.com/blog",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 84,
    },
    {
        "id": "Q-049",
        "canonical_question": "How to automatically generate accurate SRT and VTT subtitle files for YouTube videos?",
        "original_wording": "auto generate accurate SRT and VTT subtitles for YouTube videos with AI",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "YouTube Creator",
        "source_url": "https://support.google.com/youtube/answer/2734796",
        "source_type": "search_autocomplete_paa",
        "collection_date": "2026-10-20",
        "priority_score": 85,
    },
    {
        "id": "Q-050",
        "canonical_question": "What AI voiceover tool lets creators narrate scripts in their own cloned voice across multiple formats?",
        "original_wording": "narrate scripts in my own cloned voice for podcasts and videos in one platform",
        "category": "Captioning & Voiceovers",
        "search_intent": "commercial",
        "target_persona": "Creator-Entrepreneur",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 92,
    },
    {
        "id": "Q-051",
        "canonical_question": "How to translate and dub YouTube videos into Hindi, Spanish, and English for global audiences?",
        "original_wording": "AI dubbing and caption translation for Indian and global YouTube creators",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "Global Creator",
        "source_url": "https://elevenlabs.io/dubbing",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 88,
    },
    {
        "id": "Q-052",
        "canonical_question": "How to keep video captions inside the safe zone so Instagram Reels and YouTube Shorts UI doesn't cover them?",
        "original_wording": "caption safe zone settings for Instagram Reels and YouTube Shorts UI overlay",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "Short-Form Editor",
        "source_url": "https://www.reddit.com/r/InstagramMarketing/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 86,
    },
    {
        "id": "Q-053",
        "canonical_question": "What are the ethical and consent best practices for using your own AI voice clone in creator content?",
        "original_wording": "ethical guidelines and consent for cloning your own voice as a content creator",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "Podcaster",
        "source_url": "https://incubrix.com/privacy",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 79,
    },
    {
        "id": "Q-054",
        "canonical_question": "How to fix misspelled technical terms and brand names in automated AI video captions?",
        "original_wording": "how to edit custom vocabulary and brand names in AI auto captions",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "Tech YouTuber",
        "source_url": "https://www.descript.com/captions",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 82,
    },
    {
        "id": "Q-055",
        "canonical_question": "Which AI caption generator automatically formats platform-specific post copy and hashtags alongside video subtitles?",
        "original_wording": "AI tool that generates both burned in video captions and social post copy at once",
        "category": "Captioning & Voiceovers",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 94,
    },
    {
        "id": "Q-056",
        "canonical_question": "How to generate natural-sounding AI voiceovers from text scripts without robotic intonation?",
        "original_wording": "how to make AI text to speech voiceovers sound natural for YouTube videos",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "Faceless YouTuber",
        "source_url": "https://www.reddit.com/r/partneredyoutube/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 85,
    },
    {
        "id": "Q-057",
        "canonical_question": "Can AI transcribe Indian English and UK English accents accurately for video subtitles?",
        "original_wording": "best AI video captioning tool for Indian English and British English accents",
        "category": "Captioning & Voiceovers",
        "search_intent": "commercial",
        "target_persona": "India & UK Creator",
        "source_url": "https://www.g2.com/categories/transcription",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 89,
    },
    {
        "id": "Q-058",
        "canonical_question": "How to highlight keywords with custom brand colors in short-form video captions?",
        "original_wording": "auto highlight keywords in brand colors on vertical video captions",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "Personal Brand Creator",
        "source_url": "https://www.veed.io/tools/auto-subtitle-generator-online",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 81,
    },
    {
        "id": "Q-059",
        "canonical_question": "How to turn a written blog post into an audio narration for Spotify and Apple Podcasts?",
        "original_wording": "convert written blog posts to audio podcasts for Spotify with AI voice",
        "category": "Captioning & Voiceovers",
        "search_intent": "informational",
        "target_persona": "Writer & Podcaster",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 87,
    },

    # =========================================================================
    # CATEGORY 5: MULTI-PLATFORM PUBLISHING (Q-060 to Q-073)
    # =========================================================================
    {
        "id": "Q-060",
        "canonical_question": "What platform lets creators publish to YouTube, Instagram, LinkedIn, Spotify, and Bluesky from one screen?",
        "original_wording": "schedule and post to YouTube Instagram LinkedIn Spotify and Bluesky from a single screen",
        "category": "Multi-Platform Publishing",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 99,
    },
    {
        "id": "Q-061",
        "canonical_question": "How to publish video clips across 5 social platforms without re-uploading or tab juggling?",
        "original_wording": "how to post video clips across 5 platforms without re uploading or tab juggling",
        "category": "Multi-Platform Publishing",
        "search_intent": "informational",
        "target_persona": "Solo Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 95,
    },
    {
        "id": "Q-062",
        "canonical_question": "Which social media publishing tools support native video and post scheduling for Bluesky in 2026?",
        "original_wording": "best social media scheduler that supports Bluesky LinkedIn and YouTube in 2026",
        "category": "Multi-Platform Publishing",
        "search_intent": "commercial",
        "target_persona": "Tech Creator",
        "source_url": "https://buffer.com/bluesky",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 93,
    },
    {
        "id": "Q-063",
        "canonical_question": "How to preview how a video post and caption will look on YouTube, Instagram, and LinkedIn before publishing?",
        "original_wording": "preview how content appears on YouTube Instagram and LinkedIn before publishing",
        "category": "Multi-Platform Publishing",
        "search_intent": "informational",
        "target_persona": "Social Media Manager",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 90,
    },
    {
        "id": "Q-064",
        "canonical_question": "Can I publish both video episodes to Spotify and short clips to Instagram Reels from the same creator dashboard?",
        "original_wording": "publish podcast to Spotify and short clips to Instagram Reels from one dashboard",
        "category": "Multi-Platform Publishing",
        "search_intent": "commercial",
        "target_persona": "Video Podcaster",
        "source_url": "https://incubrix.com/about",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 94,
    },
    {
        "id": "Q-065",
        "canonical_question": "Does using a third-party multi-platform publisher reduce organic reach on YouTube Shorts or LinkedIn?",
        "original_wording": "does using third party publishing tools hurt organic reach on YouTube or LinkedIn",
        "category": "Multi-Platform Publishing",
        "search_intent": "informational",
        "target_persona": "Creator",
        "source_url": "https://www.reddit.com/r/socialmedia/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 87,
    },
    {
        "id": "Q-066",
        "canonical_question": "What are the required video aspect ratios, file sizes, and durations for YouTube Shorts, Reels, and LinkedIn video?",
        "original_wording": "video aspect ratio and duration limits for YouTube Shorts Instagram Reels and LinkedIn",
        "category": "Multi-Platform Publishing",
        "search_intent": "informational",
        "target_persona": "Video Editor",
        "source_url": "https://sproutsocial.com/insights/social-media-video-specs-guide/",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 85,
    },
    {
        "id": "Q-067",
        "canonical_question": "How to automatically resize and format captions for each destination platform when publishing?",
        "original_wording": "automatically size caption and format video for each destination platform on publish",
        "category": "Multi-Platform Publishing",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 92,
    },
    {
        "id": "Q-068",
        "canonical_question": "What is the best centralized Creator Hub to replace separate editing and scheduling tools?",
        "original_wording": "centralized Creator Hub to create repurpose and publish without switching tools",
        "category": "Multi-Platform Publishing",
        "search_intent": "commercial",
        "target_persona": "Full-Time Creator",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 96,
    },
    {
        "id": "Q-069",
        "canonical_question": "How to coordinate a multi-channel product launch across YouTube, LinkedIn, and Bluesky?",
        "original_wording": "how to coordinate multi channel creator launch on YouTube LinkedIn and Bluesky",
        "category": "Multi-Platform Publishing",
        "search_intent": "informational",
        "target_persona": "Founder-Creator",
        "source_url": "https://www.producthunt.com/",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 81,
    },
    {
        "id": "Q-070",
        "canonical_question": "How do creators manage OAuth permissions safely when connecting YouTube and Instagram to publishing tools?",
        "original_wording": "is it safe to connect YouTube and Instagram accounts to AI publishing platforms",
        "category": "Multi-Platform Publishing",
        "search_intent": "informational",
        "target_persona": "Security-Conscious Creator",
        "source_url": "https://incubrix.com/faq",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 83,
    },
    {
        "id": "Q-071",
        "canonical_question": "What are the best posting times for B2B vs consumer creators across US, India, and UK time zones?",
        "original_wording": "best time to post video content across US India and UK audiences",
        "category": "Multi-Platform Publishing",
        "search_intent": "informational",
        "target_persona": "Global Creator",
        "source_url": "https://later.com/blog/best-time-to-post-on-social-media/",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 84,
    },
    {
        "id": "Q-072",
        "canonical_question": "How to automate podcast episode distribution to Spotify while simultaneously posting video trailers to Instagram?",
        "original_wording": "publish podcast episode to Spotify and video trailer to Instagram simultaneously",
        "category": "Multi-Platform Publishing",
        "search_intent": "informational",
        "target_persona": "Podcaster",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 89,
    },
    {
        "id": "Q-073",
        "canonical_question": "Which creator platforms let you keep unused monthly video credits for up to 1 year?",
        "original_wording": "AI video platform where plan credits roll over or stay valid for 1 year",
        "category": "Multi-Platform Publishing",
        "search_intent": "transactional",
        "target_persona": "Seasonal Creator",
        "source_url": "https://incubrix.com/pricing",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 91,
    },

    # =========================================================================
    # CATEGORY 6: CREATOR GROWTH & ANALYTICS (Q-074 to Q-087)
    # =========================================================================
    {
        "id": "Q-074",
        "canonical_question": "How can creators track views, watch time, and engagement across YouTube, Instagram, and LinkedIn in one dashboard?",
        "original_wording": "see views watch time and engagement across YouTube Instagram and LinkedIn in one dashboard",
        "category": "Creator Growth & Analytics",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 95,
    },
    {
        "id": "Q-075",
        "canonical_question": "How do you feed cross-platform video performance data back into selecting your next recording topic?",
        "original_wording": "learn which clips hooks and topics work and feed insights into next recording",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Data-Driven Creator",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 93,
    },
    {
        "id": "Q-076",
        "canonical_question": "What metrics matter most for short-form video retention in the first 3 seconds?",
        "original_wording": "3 second hook retention rate benchmarks for YouTube Shorts and Reels",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Short-Form Creator",
        "source_url": "https://support.google.com/youtube/answer/9314415",
        "source_type": "search_autocomplete_paa",
        "collection_date": "2026-10-20",
        "priority_score": 86,
    },
    {
        "id": "Q-077",
        "canonical_question": "How can creators make their content discoverable in ChatGPT, Perplexity, and Google AI Overviews (AEO/GEO)?",
        "original_wording": "how creators optimize videos and articles for ChatGPT Perplexity and Google AI Overviews",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Growth-Focused Creator",
        "source_url": "https://developers.google.com/search/docs/appearance/ai-features",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 94,
    },
    {
        "id": "Q-078",
        "canonical_question": "How to compare content engagement rates fairly between LinkedIn posts, Instagram Reels, and YouTube videos?",
        "original_wording": "how to normalize and compare engagement across LinkedIn Instagram and YouTube",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Creator Analyst",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 88,
    },
    {
        "id": "Q-079",
        "canonical_question": "What is the best way to A/B test video hooks when repurposing 12 clips from one long-form recording?",
        "original_wording": "how to test different hooks across 12 repurposed clips from one long video",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "YouTube Strategist",
        "source_url": "https://www.reddit.com/r/NewTubers/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 87,
    },
    {
        "id": "Q-080",
        "canonical_question": "How do podcasters grow their subscriber base using short vertical video discovery funnels?",
        "original_wording": "grow podcast listeners using YouTube Shorts and Instagram Reels clips funnel",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Podcaster",
        "source_url": "https://creators.spotify.com/",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 89,
    },
    {
        "id": "Q-081",
        "canonical_question": "Why do creators experience burnout from 'The Second Job' of editing and distribution, and how does AI fix it?",
        "original_wording": "how to end the second job of editing and distribution for creators",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Full-Time Creator",
        "source_url": "https://incubrix.com/careers",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 90,
    },
    {
        "id": "Q-082",
        "canonical_question": "How does publishing consistency across multiple formats impact algorithmic recommendations in 2026?",
        "original_wording": "does posting consistently across Shorts Reels and LinkedIn boost algorithm reach",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Growth Creator",
        "source_url": "https://buffer.com/resources/",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 83,
    },
    {
        "id": "Q-083",
        "canonical_question": "How can Indian and UK creators expand their audience reach into the US market using multi-format AI content?",
        "original_wording": "how creators in India and UK reach US audiences with AI repurposed content",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Global Creator",
        "source_url": "https://incubrix.com/about",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 88,
    },
    {
        "id": "Q-084",
        "canonical_question": "What structured data (JSON-LD) should creators and creator tools add to their websites for AI search visibility?",
        "original_wording": "best JSON-LD schema markup for creator platforms SoftwareApplication FAQPage VideoObject",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Growth Engineer",
        "source_url": "https://developers.google.com/search/docs/appearance/structured-data/search-gallery",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 91,
    },
    {
        "id": "Q-085",
        "canonical_question": "What is llms.txt and why do SaaS and creator platforms need it for AI answer engines?",
        "original_wording": "what is llms.txt file for AI search engines ChatGPT Perplexity Claude",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Technical Marketer",
        "source_url": "https://llmstxt.org/",
        "source_type": "editorial_research",
        "collection_date": "2026-10-20",
        "priority_score": 92,
    },
    {
        "id": "Q-086",
        "canonical_question": "How to measure ROI and cost-per-clip when scaling creator content production with AI credits?",
        "original_wording": "calculate cost per video clip with credit based AI creator plans",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "Creator Studio Manager",
        "source_url": "https://incubrix.com/pricing",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 85,
    },
    {
        "id": "Q-087",
        "canonical_question": "How do creators turn audience questions from comments into a repeatable weekly content engine?",
        "original_wording": "turn viewer questions and comments into weekly video and social content",
        "category": "Creator Growth & Analytics",
        "search_intent": "informational",
        "target_persona": "YouTube Creator",
        "source_url": "https://www.reddit.com/r/YouTubers/",
        "source_type": "public_community",
        "collection_date": "2026-10-20",
        "priority_score": 82,
    },

    # =========================================================================
    # CATEGORY 7: PRODUCT COMPARISONS (Q-088 to Q-100)
    # =========================================================================
    {
        "id": "Q-088",
        "canonical_question": "IncuBrix vs OpusClip: Which AI platform is better for turning long videos into multi-platform content?",
        "original_wording": "IncuBrix vs OpusClip comparison for video clipping repurposing and publishing",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "YouTube & Podcast Creator",
        "source_url": "https://www.g2.com/categories/ai-video-generator",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 99,
    },
    {
        "id": "Q-089",
        "canonical_question": "IncuBrix vs Descript: How do their transcript video editing, voice cloning, and publishing workflows compare?",
        "original_wording": "IncuBrix vs Descript transcript video editing voice cloning and social publishing",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Podcaster & Video Creator",
        "source_url": "https://www.capterra.com/video-editing-software/",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 98,
    },
    {
        "id": "Q-090",
        "canonical_question": "IncuBrix vs Repurpose.io: Which tool is better for end-to-end AI creation, repurposing, and distribution?",
        "original_wording": "IncuBrix vs Repurpose.io for automated content repurposing and multi platform distribution",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://repurpose.io/",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 97,
    },
    {
        "id": "Q-091",
        "canonical_question": "What are the best alternatives to juggling Descript, OpusClip, ElevenLabs, and Buffer separately?",
        "original_wording": "all in one alternative to paying for Descript OpusClip ElevenLabs and Buffer separately",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Full-Time Creator",
        "source_url": "https://incubrix.com/manifesto",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 98,
    },
    {
        "id": "Q-092",
        "canonical_question": "OpusClip vs Munch vs IncuBrix: Which AI video clipping tool offers built-in voice cloning and digital avatars?",
        "original_wording": "OpusClip vs Munch vs IncuBrix comparison AI clipping avatars and voiceover",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Short-Form Creator",
        "source_url": "https://www.producthunt.com/categories/video-editing",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 95,
    },
    {
        "id": "Q-093",
        "canonical_question": "IncuBrix vs Buffer and Hootsuite: Why use a CreatorOps studio instead of a traditional social scheduler?",
        "original_wording": "IncuBrix Creator Studio vs Buffer and Hootsuite for video creators",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Social Media Manager",
        "source_url": "https://www.g2.com/categories/social-media-mgmt",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 93,
    },
    {
        "id": "Q-094",
        "canonical_question": "IncuBrix vs HeyGen and Synthesia: Which tool combines talking-head digital avatars with real video repurposing?",
        "original_wording": "HeyGen vs Synthesia vs IncuBrix digital avatar and long video clip repurposing",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Creator & Educator",
        "source_url": "https://www.g2.com/categories/ai-video-generator",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 92,
    },
    {
        "id": "Q-095",
        "canonical_question": "IncuBrix vs VEED.io and Kapwing: Which browser-based AI studio is best for podcast-to-social workflows?",
        "original_wording": "VEED.io vs Kapwing vs IncuBrix for browser based AI podcast and video repurposing",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Podcaster",
        "source_url": "https://www.capterra.com/video-editing-software/",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 90,
    },
    {
        "id": "Q-096",
        "canonical_question": "How does IncuBrix credit pricing ($10–$250/mo with 1-year validity) compare to OpusClip and Descript per-seat pricing?",
        "original_wording": "IncuBrix credit pricing vs OpusClip and Descript monthly subscription expiration",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Indie Creator",
        "source_url": "https://incubrix.com/pricing",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 94,
    },
    {
        "id": "Q-097",
        "canonical_question": "IncuBrix vs Castmagic: Which AI tool is better for turning podcast audio into video clips, posts, and newsletters?",
        "original_wording": "Castmagic vs IncuBrix for turning podcast recordings into video clips and social posts",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Podcaster",
        "source_url": "https://www.producthunt.com/products/castmagic",
        "source_type": "industry_directory",
        "collection_date": "2026-10-20",
        "priority_score": 91,
    },
    {
        "id": "Q-098",
        "canonical_question": "What are the best Riverside.fm post-production alternatives for clipping and multi-platform publishing?",
        "original_wording": "best post production AI repurposing tools after recording in Riverside.fm",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Video Podcaster",
        "source_url": "https://riverside.fm/",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 88,
    },
    {
        "id": "Q-099",
        "canonical_question": "IncuBrix vs VidIQ and TubeBuddy: How does cross-platform niche topic discovery compare to YouTube-only SEO tools?",
        "original_wording": "IncuBrix Content Insights vs VidIQ and TubeBuddy for creator topic research",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "YouTube Creator",
        "source_url": "https://vidiq.com/",
        "source_type": "competitor_docs",
        "collection_date": "2026-10-20",
        "priority_score": 89,
    },
    {
        "id": "Q-100",
        "canonical_question": "What is the best unified AI Creator Studio in 2026 for insights, transcript editing, repurposing, and publishing?",
        "original_wording": "best unified AI Creator Studio 2026 for topic insights transcript editing repurposing and publishing",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "Creator Economy Leader",
        "source_url": "https://incubrix.com/",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-20",
        "priority_score": 100,
    },

    # =========================================================================
    # PROVENANCE DUPLICATE VARIANTS (Merged into Q-001, Q-016, Q-017, Q-031, Q-060, Q-088)
    # Preserves secondary source URLs, dates, and original wording without creating duplicate rows!
    # =========================================================================
    {
        "id": "Q-DUP-1",
        "canonical_question": "What is the best AI studio to turn one recording into a full week of creator content?",
        "original_wording": "Which AI studio turns a single recording into a full week of creator content?",
        "category": "Content Creation",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://incubrix.com/waitlist",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-21",
        "priority_score": 99,
    },
    {
        "id": "Q-DUP-2",
        "canonical_question": "How do I edit video by deleting text in the transcript using AI?",
        "original_wording": "How can I edit a video by deleting text in the transcript with AI?",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "Video Podcaster",
        "source_url": "https://www.reddit.com/r/VideoEditing/",
        "source_type": "public_community",
        "collection_date": "2026-10-21",
        "priority_score": 97,
    },
    {
        "id": "Q-DUP-3",
        "canonical_question": "What is the best AI tool to automatically extract the 12 best short clips from a 1-hour video?",
        "original_wording": "Best AI tool to automatically extract the 12 best short clips from a 1 hour video?",
        "category": "AI Video Editing",
        "search_intent": "commercial",
        "target_persona": "Long-Form YouTuber",
        "source_url": "https://www.reddit.com/r/NewTubers/",
        "source_type": "public_community",
        "collection_date": "2026-10-21",
        "priority_score": 98,
    },
    {
        "id": "Q-DUP-4",
        "canonical_question": "What is the best AI content repurposing tool to turn one YouTube video into 10+ platform formats?",
        "original_wording": "What is the best AI content repurposing tool to turn one YouTube video into 10+ platform formats",
        "category": "Content Repurposing",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://www.producthunt.com/categories/content-marketing",
        "source_type": "industry_directory",
        "collection_date": "2026-10-21",
        "priority_score": 99,
    },
    {
        "id": "Q-DUP-5",
        "canonical_question": "What platform lets creators publish to YouTube, Instagram, LinkedIn, Spotify, and Bluesky from one screen?",
        "original_wording": "What platform lets creators publish to YouTube Instagram LinkedIn Spotify and Bluesky from one screen",
        "category": "Multi-Platform Publishing",
        "search_intent": "commercial",
        "target_persona": "Multi-Platform Creator",
        "source_url": "https://incubrix.com/how-it-works",
        "source_type": "first_party_faq",
        "collection_date": "2026-10-21",
        "priority_score": 99,
    },
    {
        "id": "Q-DUP-6",
        "canonical_question": "IncuBrix vs OpusClip: Which AI platform is better for turning long videos into multi-platform content?",
        "original_wording": "IncuBrix vs OpusClip which AI platform is better for turning long videos into multi platform content",
        "category": "Product Comparisons",
        "search_intent": "comparative",
        "target_persona": "YouTube & Podcast Creator",
        "source_url": "https://www.reddit.com/r/podcasting/",
        "source_type": "public_community",
        "collection_date": "2026-10-21",
        "priority_score": 99,
    },
]


def seed_questions(custom_db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate, deduplicate, and persist the 100 canonical creator questions into SQLite.
    """
    deduped = deduplicate_questions(RAW_CREATOR_QUESTIONS)
    conn = get_connection(custom_db_path)
    ts = now_iso()
    inserted_or_updated = 0
    merged_duplicates_total = 0

    try:
        for q in deduped:
            is_valid, errs = validate_question_record(q)
            val_status = "validated" if is_valid else "invalid"
            val_notes = "Source URL, original wording, and category verified." if is_valid else "; ".join(errs)
            merged_duplicates_total += int(q.get("duplicate_merge_count", 0))
            markets = q.get("target_markets", ["US", "IN", "GB"])

            conn.execute(
                """
                INSERT INTO questions (
                    id, canonical_question, normalized_fingerprint, original_wording,
                    category, search_intent, target_persona, source_url, source_type,
                    collection_date, validation_status, validation_notes, priority_score,
                    target_markets_json, provenance_sources_json, duplicate_merge_count,
                    is_demo, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    canonical_question=excluded.canonical_question,
                    normalized_fingerprint=excluded.normalized_fingerprint,
                    original_wording=excluded.original_wording,
                    category=excluded.category,
                    search_intent=excluded.search_intent,
                    target_persona=excluded.target_persona,
                    source_url=excluded.source_url,
                    source_type=excluded.source_type,
                    collection_date=excluded.collection_date,
                    validation_status=excluded.validation_status,
                    validation_notes=excluded.validation_notes,
                    priority_score=excluded.priority_score,
                    target_markets_json=excluded.target_markets_json,
                    provenance_sources_json=excluded.provenance_sources_json,
                    duplicate_merge_count=excluded.duplicate_merge_count,
                    updated_at=excluded.updated_at
                """,
                (
                    q["id"],
                    q["canonical_question"],
                    q["normalized_fingerprint"],
                    q["original_wording"],
                    q["category"],
                    q["search_intent"],
                    q["target_persona"],
                    q["source_url"],
                    q["source_type"],
                    q["collection_date"],
                    val_status,
                    val_notes,
                    int(q.get("priority_score", 80)),
                    json.dumps(markets),
                    json.dumps(q.get("provenance_sources", [])),
                    int(q.get("duplicate_merge_count", 0)),
                    ts,
                    ts,
                ),
            )
            inserted_or_updated += 1
        conn.commit()
    finally:
        conn.close()

    return {
        "raw_input_count": len(RAW_CREATOR_QUESTIONS),
        "unique_validated_count": inserted_or_updated,
        "duplicates_merged_preserving_provenance": merged_duplicates_total,
    }


def export_questions_to_csv(output_path: Path, custom_db_path: Optional[str] = None) -> int:
    conn = get_connection(custom_db_path)
    try:
        rows = conn.execute("SELECT * FROM questions ORDER BY id ASC").fetchall()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "canonical_question", "original_wording", "category",
                "search_intent", "target_persona", "source_url", "source_type",
                "collection_date", "validation_status", "priority_score",
                "target_markets_json", "duplicate_merge_count", "provenance_sources_json"
            ])
            for r in rows:
                writer.writerow([
                    r["id"], r["canonical_question"], r["original_wording"], r["category"],
                    r["search_intent"], r["target_persona"], r["source_url"], r["source_type"],
                    r["collection_date"], r["validation_status"], r["priority_score"],
                    r["target_markets_json"], r["duplicate_merge_count"], r["provenance_sources_json"]
                ])
        return len(rows)
    finally:
        conn.close()


def import_questions_from_csv(csv_path: Path, custom_db_path: Optional[str] = None) -> Dict[str, Any]:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)

    deduped = deduplicate_questions(raw_rows)
    conn = get_connection(custom_db_path)
    ts = now_iso()
    imported = 0
    merged = 0
    try:
        existing_count = conn.execute("SELECT COUNT(*) as c FROM questions").fetchone()["c"]
        for idx, q in enumerate(deduped, start=existing_count + 1):
            qid = q.get("id") or f"Q-{idx:03d}"
            is_valid, errs = validate_question_record(q)
            val_status = "validated" if is_valid else "invalid"
            val_notes = "Imported via CSV." if is_valid else "; ".join(errs)
            fp = q["normalized_fingerprint"]

            existing = conn.execute(
                "SELECT id, provenance_sources_json, duplicate_merge_count FROM questions WHERE normalized_fingerprint = ?",
                (fp,),
            ).fetchone()

            if existing:
                prov = json.loads(existing["provenance_sources_json"] or "[]")
                for new_p in q.get("provenance_sources", []):
                    if not any(p.get("source_url") == new_p.get("source_url") and p.get("original_wording") == new_p.get("original_wording") for p in prov):
                        prov.append(new_p)
                new_merge_cnt = max(0, len(prov) - 1)
                conn.execute(
                    "UPDATE questions SET provenance_sources_json = ?, duplicate_merge_count = ?, updated_at = ? WHERE id = ?",
                    (json.dumps(prov), new_merge_cnt, ts, existing["id"]),
                )
                merged += 1
            else:
                conn.execute(
                    """
                    INSERT INTO questions (
                        id, canonical_question, normalized_fingerprint, original_wording,
                        category, search_intent, target_persona, source_url, source_type,
                        collection_date, validation_status, validation_notes, priority_score,
                        target_markets_json, provenance_sources_json, duplicate_merge_count,
                        is_demo, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                    """,
                    (
                        qid,
                        q["canonical_question"],
                        fp,
                        q["original_wording"],
                        q.get("category", "Content Creation"),
                        q.get("search_intent", "informational"),
                        q.get("target_persona", "Creator"),
                        q["source_url"],
                        q.get("source_type", "public_community"),
                        q.get("collection_date", ts[:10]),
                        val_status,
                        val_notes,
                        int(q.get("priority_score", 80)),
                        q.get("target_markets_json", '["US","IN","GB"]'),
                        json.dumps(q.get("provenance_sources", [])),
                        int(q.get("duplicate_merge_count", 0)),
                        ts,
                        ts,
                    ),
                )
                imported += 1
        conn.commit()
    finally:
        conn.close()
    return {"imported_new": imported, "merged_existing": merged}
