# Performance Campaign Control
### Google Ads Campaign Operations Dashboard

An internal campaign operations system for Google Search and Display Ads — enabling bulk campaign creation, keyword and audience management, placement exclusions, bid strategy updates, and automated performance-based pausing via the Google Ads API.

Built by **Srikanth Reddy** · Performance Marketing & Automation Lead

---

## Overview

This tool replaces manual Google Ads UI operations and disconnected scripts with a single internal dashboard. It is operated exclusively on advertising accounts managed under the organisation's MCC — not offered to third-party clients.

**Current status:** UI shell complete · Mock mode · Awaiting Google Ads API developer token approval

---

## Modules

| Module | Category | Input | Action |
|--------|----------|-------|--------|
| `create_search_campaigns_bulk` | Campaigns | campaigns.csv | Create Search campaigns with keywords + RSA ad copy |
| `create_display_campaigns_bulk` | Campaigns | display_campaigns.csv | Create Display campaigns with audiences + assets |
| `enable_campaigns_by_name` | Enable/Pause | campaign_names.csv | Enable paused campaigns by name |
| `pause_campaigns_by_name` | Enable/Pause | campaign_names.csv | Pause active campaigns by name |
| `pause_adgroups_by_campaign` | Enable/Pause | campaign_ids.csv | Pause all ad groups within specified campaigns |
| `update_daily_budget_bulk` | Budget | update_budget.csv | Update daily budget by campaign name |
| `update_bid_strategy_bulk` | Bidding | bid_strategy.csv | Switch bid strategy (tCPA / tROAS / MaxConv) |
| `update_target_cpa_bulk` | Bidding | target_cpa.csv | Update Target CPA values across campaigns |
| `update_target_roas_bulk` | Bidding | target_roas.csv | Update Target ROAS values across campaigns |
| `add_keywords_bulk` | Keywords | keywords.csv | Add keywords with match type to ad groups |
| `add_negative_keywords_bulk` | Keywords | negative_keywords.csv | Add negatives at campaign or ad group level |
| `harvest_search_terms` | Keywords | campaign_ids + date range | Pull search terms report, flag converters |
| `promote_search_terms` | Keywords | search_terms_to_add.csv | Promote search terms to exact / phrase match |
| `change_keyword_match_types` | Keywords | match_type_changes.csv | Bulk change keyword match types via API |
| `add_placements_bulk` | Display | managed_placements.csv | Add managed placements to Display ad groups |
| `exclude_placements_bulk` | Display | placement_exclusions.csv | Bulk exclude placements from Display campaigns |
| `assign_audiences_bulk` | Display | audiences.csv | Assign in-market / affinity / remarketing lists |
| `exclude_audiences_bulk` | Display | audience_exclusions.csv | Exclude audience segments from ad groups |
| `update_rsa_assets_bulk` | Ad Copy | rsa_assets.csv | Update RSA headlines and descriptions in bulk |
| `update_display_ad_assets` | Ad Copy | display_assets.csv | Swap responsive display ad headlines / images |
| `update_final_urls_bulk` | Ad Copy | url_updates.csv | Update final URLs across ads via bulk input |
| `auto_pause_low_roas` | Auto Pause | campaign performance report | Pause campaigns below ROAS threshold |
| `auto_pause_high_cpa` | Auto Pause | campaign performance report | Pause campaigns exceeding CPA target |
| `auto_pause_low_cvr` | Auto Pause | campaign performance report | Pause campaigns below conversion rate floor |
| `auto_pause_impression_share` | Auto Pause | campaign performance report | Flag campaigns losing 30%+ IS to budget |
| `fetch_campaign_performance` | Reports | campaign_ids + date range | Campaign stats: impressions, clicks, conv, cost |
| `fetch_keyword_performance` | Reports | campaign_ids + date range | Keyword ROAS, CPA, CVR, search IS via GAQL |
| `fetch_placement_performance` | Reports | campaign_ids + date range | Placement performance for Display campaigns |
| `fetch_search_terms_report` | Reports | campaign_ids + date range | Full search terms report with match breakdown |
| `sync_stats_to_gsheet` | Automation | Google Sheets (Sheet1+2) | Sync campaign stats to internal tracker sheet |

---

## Campaign Scoring Framework

Each campaign is scored daily on a **1–10 composite scale** derived from four performance signals pulled via GAQL.

| Metric | Weight | Low signal (1–3) | High signal (7–10) |
|--------|--------|-----------------|-------------------|
| ROAS | 35% | Below target ROAS floor | Exceeds target ROAS consistently |
| CPA | 30% | CPA above target ceiling with conversions | CPA at or below target |
| CVR | 20% | CVR below floor with 50+ clicks | CVR above benchmark |
| Impression Share | 15% | IS Lost (Budget) > 30% | IS Lost (Budget) < 10% |

**Score-to-action mapping:**

| Score 1–3 | Score 4–6 | Score 7–10 |
|-----------|-----------|------------|
| PAUSE | HOLD at min budget | SCALE |

---

## Tech Stack

| Component | Detail |
|-----------|--------|
| Language | Python 3.10+ |
| Framework | Streamlit |
| Google Ads API | `google-ads` 21.x Python client library |
| Auth | OAuth 2.0 · `google-ads.yaml` · MCC `login_customer_id` |
| Query language | GAQL via `GoogleAdsService.search()` |
| Data I/O | CSV input files parsed via `pandas` |
| Audit store | Google Sheets API (service account) · Sheet3 |
| Deployment | Streamlit Cloud |

---

## API Architecture

```
Auth Layer      →  OAuth 2.0 (google-ads.yaml) · developer token · MCC login_customer_id
Service Layer   →  CampaignService · AdGroupService · KeywordPlanAdGroupKeywordService
                   CampaignCriterionService · AdGroupCriterionService · CampaignBudgetService
                   GoogleAdsService (GAQL reporting)
Operation Layer →  Mutate operations via service.mutate() · batched · partial failure enabled
Reporting Layer →  GoogleAdsService.search() · GAQL · streamed to Sheets or CSV
Audit Layer     →  Every write logged to Google Sheets Sheet3 (resource, op type, ID, timestamp)
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/srikanthreddy979797-sys/performance-campaign-control.git
cd performance-campaign-control
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API credentials

Create `google-ads.yaml` in the project root (never commit this file):

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
login_customer_id: YOUR_MCC_ID
use_proto_plus: True
```

### 4. Run locally

```bash
streamlit run app.py
```

### 5. Deploy to Streamlit Cloud

- Push to GitHub (credentials stay local, never committed)
- Connect repo at [share.streamlit.io](https://share.streamlit.io)
- Set `app.py` as the main file
- Add credentials via Streamlit Cloud **Secrets** (not environment variables)

---

## Security

- `google-ads.yaml` is in `.gitignore` and never committed
- All API operations are scoped to the organisation's MCC only
- No third-party advertiser account access
- OAuth credentials restricted to authorised team members
- Audit log records every write operation with timestamp and metric snapshot

---

## Account Scope

All Google Ads API operations are performed exclusively on advertising accounts managed under the organisation's MCC. This tool is not a software product offered to external clients. It is an internal operations system built to improve campaign management efficiency across the organisation's own advertising portfolio.

---

## Roadmap

- [ ] Connect live `google-ads` Python client (pending API developer token approval)
- [ ] Scheduled auto-pause via Streamlit background jobs or Cloud Scheduler
- [ ] Google Sheets audit sync (Sheet3) via service account
- [ ] CSV template downloads for all 25+ modules
- [ ] FastAPI backend migration for concurrent API calls at scale

---

*Google Ads Campaign Control Dashboard · v1.0 · Internal use only*
