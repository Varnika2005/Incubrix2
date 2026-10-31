import { z } from 'zod';

export const VALID_CATEGORIES = [
  'Content Creation',
  'AI Video Editing',
  'Content Repurposing',
  'Captioning & Voiceovers',
  'Multi-Platform Publishing',
  'Creator Growth & Analytics',
  'Product Comparisons',
] as const;

export const VALID_SOURCE_TYPES = [
  'search_autocomplete_paa',
  'public_community',
  'competitor_docs',
  'first_party_faq',
  'industry_directory',
  'editorial_research',
] as const;

export const VALID_PROVIDERS = [
  'google_search',
  'chatgpt',
  'gemini',
  'perplexity',
  'claude',
] as const;

export const VALID_MARKETS = ['US', 'IN', 'GB'] as const;

export const CreateQuestionSchema = z.object({
  canonical_question: z.string().min(10, 'Question must be at least 10 characters'),
  original_wording: z.string().min(5, 'Original wording is required to preserve provenance'),
  category: z.enum(VALID_CATEGORIES),
  search_intent: z.enum(['informational', 'commercial', 'transactional', 'comparative']).default('informational'),
  target_persona: z.string().min(2).default('Creator'),
  source_url: z.string().url('Must be a valid http/https source URL'),
  source_type: z.enum(VALID_SOURCE_TYPES),
  collection_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Must be YYYY-MM-DD'),
  priority_score: z.number().int().min(1).max(100).default(85),
  target_markets: z.array(z.enum(VALID_MARKETS)).min(1).default(['US', 'IN', 'GB']),
});

export const ManualObservationSchema = z.object({
  question_id: z.string().min(3),
  provider: z.enum(VALID_PROVIDERS),
  market: z.enum(VALID_MARKETS).default('US'),
  observation_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  pass_number: z.number().int().min(1).max(5).default(1),
  collection_method: z.string().optional().default('manual_research'),
  evidence_reference: z.string().optional(),
  raw_response_text: z.string().min(10, 'Raw response evidence text must be at least 10 characters'),
  citation_urls: z.array(z.string().url()).optional().default([]),
  google_organic_rank: z.number().int().min(1).max(100).nullable().optional(),
  answer_box_present: z.boolean().optional().default(false),
  answer_box_owner: z.string().nullable().optional(),
  ai_overview_present: z.boolean().optional().default(false),
  ai_overview_cites_incubrix: z.boolean().optional().default(false),
});

export const TriggerVisibilityRunSchema = z.object({
  mode: z.enum(['test', 'live']).default('test'),
  markets: z.array(z.enum(VALID_MARKETS)).min(1).default(['US', 'IN', 'GB']),
  providers: z.array(z.enum(VALID_PROVIDERS)).min(1).default(['google_search', 'chatgpt', 'gemini', 'perplexity', 'claude']),
  limit: z.number().int().min(1).max(100).default(10),
  pass_number: z.number().int().min(1).max(5).default(1),
});

export const UpdateContentPageSchema = z.object({
  title: z.string().min(20),
  meta_description: z.string().min(80).max(170),
  direct_answer_summary: z.string().min(50),
  body_markdown: z.string().min(100),
  json_ld_schema: z.string().min(20),
  status: z.enum(['draft', 'reviewed', 'ready_to_publish']),
});

export const GenerateBriefSchema = z.object({
  question_id: z.string().min(3),
  content_type: z.enum(['how_to_guide', 'product_comparison', 'faq_page', 'glossary_entry', 'problem_solving_guide']).default('how_to_guide'),
});

export const UpdateCitationSchema = z.object({
  verification_status: z.enum(['verified_live', 'verified_indexed', 'pending_check', 'unreachable']),
  priority_tier: z.enum(['Tier 1', 'Tier 2', 'Tier 3']).optional(),
  notes: z.string().optional(),
});

export const UpdateLaunchTaskSchema = z.object({
  status: z.enum(['completed', 'in_progress', 'planned']),
  measured_metric: z.string().min(3).optional(),
});
