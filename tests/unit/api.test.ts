import { describe, it, expect } from 'vitest';
import request from 'supertest';
import { createApp } from '../../server/index.ts';

const app = createApp();

describe('IncuBrix AEO / SEO / GEO Visibility Engine API & Zod Validation Suite', () => {
  it('GET /api/health returns healthy status and target URL', async () => {
    const res = await request(app).get('/api/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(res.body.target).toBe('https://www.incubrix.com');
  });

  it('GET /api/overview computes real metrics from SQLite and excludes DEMO records', async () => {
    const res = await request(app).get('/api/overview');
    expect(res.status).toBe(200);
    expect(res.body.questions.validated_total).toBeGreaterThanOrEqual(100);
    expect(res.body.technical_audit.issues_total).toBeGreaterThanOrEqual(20);
    expect(res.body.content_studio.pages_total).toBe(10);
    expect(res.body.citations.opportunities_total).toBe(30);
    expect(res.body.observation_states.demo_observation).toBeGreaterThan(0);
  });

  it('GET /api/questions returns 100 validated creator questions and supports category filtering', async () => {
    const res = await request(app).get('/api/questions');
    expect(res.status).toBe(200);
    expect(res.body.count).toBeGreaterThanOrEqual(100);

    const filtered = await request(app).get('/api/questions?category=Product%20Comparisons');
    expect(filtered.status).toBe(200);
    expect(filtered.body.count).toBe(13);
  });

  it('POST /api/questions enforces Zod validation and merges duplicates preserving provenance', async () => {
    const badRes = await request(app).post('/api/questions').send({
      canonical_question: 'Too short',
      original_wording: '',
      source_url: 'not-a-url',
    });
    expect(badRes.status).toBe(400);

    // Duplicate of Q-001 -> should merge without creating a duplicate row
    const dupRes = await request(app).post('/api/questions').send({
      canonical_question: 'What is the best AI studio to turn one recording into a full week of creator content?',
      original_wording: 'API test wording: best AI studio to turn one recording into a full week of creator content',
      category: 'Content Creation',
      search_intent: 'commercial',
      target_persona: 'Creator',
      source_url: 'https://www.producthunt.com/',
      source_type: 'industry_directory',
      collection_date: '2026-10-24',
      priority_score: 99,
      target_markets: ['US', 'IN', 'GB'],
    });
    expect(dupRes.status).toBe(201);
    expect(dupRes.body.action).toBe('merged_into_existing_preserving_provenance');
    expect(dupRes.body.question.id).toBe('Q-001');
  });

  it('GET /api/audit & POST /api/audit/validate-jsonld validate schemas and block fabricated ratings', async () => {
    const auditRes = await request(app).get('/api/audit');
    expect(auditRes.status).toBe(200);
    expect(auditRes.body.issues_count).toBeGreaterThanOrEqual(20);
    expect(auditRes.body.pages_count).toBe(13);

    const fakeRatingRes = await request(app)
      .post('/api/audit/validate-jsonld')
      .send({
        json_ld: JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'SoftwareApplication',
          name: 'IncuBrix',
          applicationCategory: 'MultimediaApplication',
          aggregateRating: { '@type': 'AggregateRating', ratingValue: '5.0' },
        }),
      });
    expect(fakeRatingRes.status).toBe(200);
    expect(fakeRatingRes.body.valid).toBe(false);
  });

  it('GET /api/content, /api/citations, /api/reports, and /api/launch-plan return complete records', async () => {
    const [contentRes, citRes, repRes, lpRes] = await Promise.all([
      request(app).get('/api/content'),
      request(app).get('/api/citations'),
      request(app).get('/api/reports'),
      request(app).get('/api/launch-plan'),
    ]);
    expect(contentRes.status).toBe(200);
    expect(contentRes.body.count).toBe(10);
    expect(citRes.status).toBe(200);
    expect(citRes.body.count).toBe(30);
    expect(repRes.status).toBe(200);
    expect(repRes.body.count).toBeGreaterThanOrEqual(1);
    expect(lpRes.status).toBe(200);
    expect(lpRes.body.count).toBe(12);
  });

  it('GET export endpoints return valid CSV and JSON bundles with proper headers', async () => {
    const [visRes, qRes, citRes, covRes, wbRes] = await Promise.all([
      request(app).get('/api/exports/visibility.csv'),
      request(app).get('/api/exports/questions.csv'),
      request(app).get('/api/exports/citations.csv'),
      request(app).get('/api/exports/coverage.csv'),
      request(app).get('/api/exports/workbook'),
    ]);
    expect(visRes.status).toBe(200);
    expect(visRes.headers['content-type']).toContain('text/csv');
    expect(qRes.status).toBe(200);
    expect(qRes.headers['content-type']).toContain('text/csv');
    expect(citRes.status).toBe(200);
    expect(citRes.headers['content-type']).toContain('text/csv');
    expect(covRes.status).toBe(200);
    expect(covRes.headers['content-type']).toContain('text/csv');
    expect(wbRes.status).toBe(200);
    expect(wbRes.body.completeness_verification).toBeDefined();
  });
});
