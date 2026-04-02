import streamlit as st
import pandas as pd
import json
from datetime import datetime, date, timedelta
import time
import random

st.set_page_config(
    page_title="Google Ads Campaign Control",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: #0a0a0f;
    border-right: 1px solid #1e1e2e;
}

[data-testid="stSidebar"] * {
    color: #c8c8d8 !important;
}

[data-testid="stSidebar"] .stRadio label {
    color: #c8c8d8 !important;
}

.sidebar-logo {
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 1rem;
}

.sidebar-logo h2 {
    color: #ffffff !important;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0;
}

.sidebar-logo p {
    color: #5a5a7a !important;
    font-size: 11px;
    margin: 4px 0 0;
    font-family: 'DM Mono', monospace;
}

.metric-card {
    background: #f8f8fc;
    border: 1px solid #e8e8f0;
    border-radius: 8px;
    padding: 1rem 1.2rem;
}

.metric-card .label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #888899;
    margin-bottom: 4px;
}

.metric-card .value {
    font-size: 26px;
    font-weight: 600;
    color: #0a0a1a;
    font-family: 'DM Mono', monospace;
}

.metric-card .delta {
    font-size: 12px;
    margin-top: 2px;
    font-family: 'DM Mono', monospace;
}

.metric-card .delta.up { color: #1a9e5f; }
.metric-card .delta.down { color: #c93b3b; }

.section-header {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #444466;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e8e8f0;
    margin-bottom: 1.2rem;
}

.module-card {
    background: #ffffff;
    border: 1px solid #e8e8f0;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.15s;
}

.module-card:hover {
    border-color: #aaaacc;
}

.module-tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
}

.tag-search { background: #e6f1fb; color: #185fa5; }
.tag-display { background: #e1f5ee; color: #0f6e56; }
.tag-auto { background: #faeeda; color: #854f0b; }
.tag-report { background: #eeedfe; color: #534ab7; }
.tag-budget { background: #faece7; color: #993c1d; }

.score-bar-wrap {
    background: #f0f0f8;
    border-radius: 4px;
    height: 6px;
    width: 100%;
}

.score-bar {
    height: 6px;
    border-radius: 4px;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
}

.badge-active { background: #eaf3de; color: #3b6d11; }
.badge-paused { background: #faeeda; color: #854f0b; }
.badge-removed { background: #fcebeb; color: #a32d2d; }

.run-log {
    background: #0a0a0f;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #8888aa;
    max-height: 220px;
    overflow-y: auto;
}

.run-log .log-line { margin: 2px 0; }
.run-log .log-ok { color: #5fcf9a; }
.run-log .log-warn { color: #f5c842; }
.run-log .log-err { color: #f07070; }
.run-log .log-info { color: #7090e8; }

.stButton > button {
    background: #0a0a1a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 0.45rem 1.1rem !important;
}

.stButton > button:hover {
    background: #1e1e3a !important;
}

div[data-testid="column"] .stButton > button {
    width: 100%;
}

.stDownloadButton > button {
    background: #f0f0f8 !important;
    color: #333355 !important;
    border: 1px solid #ccccdd !important;
    border-radius: 6px !important;
    font-size: 12px !important;
}

.stTabs [data-baseweb="tab"] {
    font-size: 13px;
    font-weight: 500;
}

.api-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-family: 'DM Mono', monospace;
}

.api-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}

.api-dot.connected { background: #1a9e5f; }
.api-dot.mock { background: #f5c842; }
</style>
""", unsafe_allow_html=True)

if "run_logs" not in st.session_state:
    st.session_state.run_logs = []
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []
if "campaigns" not in st.session_state:
    st.session_state.campaigns = [
        {"id": "C-001", "name": "Brand | Search | IN", "type": "Search", "status": "ACTIVE", "budget": 2500, "bid_strategy": "Target ROAS", "roas": 4.2, "cpa": 180, "cvr": 3.8, "is_lost": 8, "spend": 1840, "revenue": 7728, "score": 8},
        {"id": "C-002", "name": "NonBrand | Search | IN", "type": "Search", "status": "ACTIVE", "budget": 5000, "bid_strategy": "Target CPA", "roas": 2.1, "cpa": 320, "cvr": 1.9, "is_lost": 22, "spend": 3200, "revenue": 6720, "score": 5},
        {"id": "C-003", "name": "Competitor | Search | IN", "type": "Search", "status": "PAUSED", "budget": 1500, "bid_strategy": "Max Conversions", "roas": 0.8, "cpa": 680, "cvr": 0.7, "is_lost": 45, "spend": 890, "revenue": 712, "score": 2},
        {"id": "C-004", "name": "Retargeting | Display | IN", "type": "Display", "status": "ACTIVE", "budget": 3000, "bid_strategy": "Target CPM", "roas": 3.5, "cpa": 210, "cvr": 2.9, "is_lost": 5, "spend": 1200, "revenue": 4200, "score": 7},
        {"id": "C-005", "name": "Prospecting | Display | IN", "type": "Display", "status": "ACTIVE", "budget": 4000, "bid_strategy": "Max Clicks", "roas": 1.4, "cpa": 420, "cvr": 1.1, "is_lost": 31, "spend": 2800, "revenue": 3920, "score": 4},
    ]

def add_log(msg, level="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.run_logs.insert(0, {"ts": ts, "msg": msg, "level": level})
    if len(st.session_state.run_logs) > 50:
        st.session_state.run_logs = st.session_state.run_logs[:50]

def add_audit(op_type, resource, change, status="SUCCESS"):
    st.session_state.audit_log.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation": op_type,
        "resource": resource,
        "change": change,
        "status": status
    })

def render_logs():
    if not st.session_state.run_logs:
        st.markdown('<div class="run-log"><span style="color:#555577">— no operations run yet —</span></div>', unsafe_allow_html=True)
        return
    lines = ""
    for entry in st.session_state.run_logs[:20]:
        cls = {"ok": "log-ok", "warn": "log-warn", "err": "log-err", "info": "log-info"}.get(entry["level"], "log-info")
        prefix = {"ok": "✓", "warn": "!", "err": "✗", "info": "→"}.get(entry["level"], "→")
        lines += f'<div class="log-line {cls}">[{entry["ts"]}] {prefix} {entry["msg"]}</div>'
    st.markdown(f'<div class="run-log">{lines}</div>', unsafe_allow_html=True)

def score_color(score):
    if score >= 7: return "#1a9e5f"
    if score >= 4: return "#d4920a"
    return "#c93b3b"

def score_action(score):
    if score >= 7: return "SCALE"
    if score >= 4: return "HOLD"
    return "PAUSE"

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>Campaign Control</h2>
        <p>Google Ads API · v1.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="api-status"><span class="api-dot mock"></span><span style="color:#aaaacc;font-size:11px;font-family:DM Mono,monospace">MOCK MODE — no live API</span></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    nav = st.radio("", [
        "Overview",
        "Campaigns",
        "Keywords",
        "Display & Audiences",
        "Bids & Budget",
        "Ad Copy & Assets",
        "Auto-Pause Engine",
        "GAQL Reports",
        "Audit Log",
        "API Config"
    ], label_visibility="collapsed")

# ── MAIN CONTENT ─────────────────────────────────────────────────────────────

if nav == "Overview":
    st.markdown("## Dashboard Overview")
    st.caption(f"Last refresh: {datetime.now().strftime('%d %b %Y, %H:%M')} · Mock data · MCC not connected")

    total_spend = sum(c["spend"] for c in st.session_state.campaigns)
    total_rev = sum(c["revenue"] for c in st.session_state.campaigns)
    blended_roas = total_rev / total_spend if total_spend else 0
    active = sum(1 for c in st.session_state.campaigns if c["status"] == "ACTIVE")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="label">Total Spend</div><div class="value">₹{total_spend:,.0f}</div><div class="delta up">↑ 12% vs last week</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="label">Total Revenue</div><div class="value">₹{total_rev:,.0f}</div><div class="delta up">↑ 8% vs last week</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="label">Blended ROAS</div><div class="value">{blended_roas:.2f}x</div><div class="delta down">↓ 0.3x vs target</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="label">Active Campaigns</div><div class="value">{active}/{len(st.session_state.campaigns)}</div><div class="delta">1 paused · auto-pause</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Campaign Scoring — Today</div>', unsafe_allow_html=True)

    for c in st.session_state.campaigns:
        col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1, 1, 1, 1.5, 1])
        with col1:
            badge = f'<span class="status-badge badge-{"active" if c["status"]=="ACTIVE" else "paused"}">{c["status"]}</span>'
            st.markdown(f'**{c["name"]}** {badge}', unsafe_allow_html=True)
            st.caption(f'{c["type"]} · {c["bid_strategy"]}')
        with col2:
            st.metric("ROAS", f'{c["roas"]}x')
        with col3:
            st.metric("CPA", f'₹{c["cpa"]}')
        with col4:
            st.metric("CVR", f'{c["cvr"]}%')
        with col5:
            clr = score_color(c["score"])
            action = score_action(c["score"])
            st.markdown(f'''
            <div style="padding:4px 0">
              <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                <span style="font-family:DM Mono,monospace;font-weight:500;color:{clr}">Score: {c["score"]}/10</span>
                <span style="font-size:10px;font-weight:600;color:{clr}">{action}</span>
              </div>
              <div class="score-bar-wrap"><div class="score-bar" style="width:{c["score"]*10}%;background:{clr}"></div></div>
            </div>''', unsafe_allow_html=True)
        with col6:
            st.markdown(f'<div style="font-size:12px;color:#888899;margin-top:4px;font-family:DM Mono,monospace">IS Lost: {c["is_lost"]}%</div>', unsafe_allow_html=True)
        st.divider()

    st.markdown('<div class="section-header">Operation Log</div>', unsafe_allow_html=True)
    render_logs()

elif nav == "Campaigns":
    st.markdown("## Campaign Management")
    tab1, tab2, tab3 = st.tabs(["Create Campaigns", "Enable / Pause", "Manage Existing"])

    with tab1:
        network = st.radio("Network", ["Search", "Display"], horizontal=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if network == "Search":
            st.markdown('<div class="section-header">Bulk Search Campaign Creation</div>', unsafe_allow_html=True)
            st.info("Upload a structured CSV to create Search campaigns with keywords, RSA ad copy, bid strategy, and geo targeting pre-configured.", icon="ℹ️")

            with st.expander("CSV Format — campaigns.csv"):
                sample = pd.DataFrame({
                    "campaign_name": ["Brand|Search|IN", "NonBrand|Search|IN"],
                    "daily_budget": [2500, 5000],
                    "bid_strategy": ["TARGET_ROAS", "TARGET_CPA"],
                    "target_roas": [4.0, ""],
                    "target_cpa": ["", 300],
                    "geo": ["IN", "IN"],
                    "language": ["en", "en"],
                    "ad_schedule": ["Mon-Sun 6-23", "Mon-Sun 6-23"],
                    "network": ["SEARCH", "SEARCH"]
                })
                st.dataframe(sample, use_container_width=True)
                st.download_button("Download template", sample.to_csv(index=False), "campaigns_template.csv", "text/csv")

            uploaded = st.file_uploader("Upload campaigns.csv", type=["csv"], key="camp_upload")
            col1, col2 = st.columns(2)
            with col1:
                account_id = st.text_input("Customer Account ID", placeholder="123-456-7890")
            with col2:
                dry_run = st.checkbox("Dry run (validate only, no API writes)", value=True)

            if st.button("Create Search Campaigns"):
                if not account_id:
                    st.error("Enter a Customer Account ID.")
                else:
                    with st.spinner("Processing..."):
                        time.sleep(1.2)
                    add_log(f"[MOCK] create_search_campaigns_bulk → account {account_id}", "info")
                    add_log("Parsed campaigns.csv — 2 rows validated", "ok")
                    add_log("DRY RUN: no API writes executed", "warn")
                    add_audit("CREATE", "Search Campaigns", f"2 campaigns · account {account_id} · dry_run={dry_run}")
                    st.success("Dry run complete — 2 campaigns validated. Connect API credentials to execute.")
                    st.rerun()

        else:
            st.markdown('<div class="section-header">Bulk Display Campaign Creation</div>', unsafe_allow_html=True)
            st.info("Upload CSV with audience segments, placement lists, responsive display ad assets, and exclusion lists.", icon="ℹ️")
            with st.expander("CSV Format — display_campaigns.csv"):
                sample = pd.DataFrame({
                    "campaign_name": ["Retargeting|Display|IN"],
                    "daily_budget": [3000],
                    "bid_strategy": ["TARGET_CPM"],
                    "target_cpm": [80],
                    "audience_type": ["REMARKETING"],
                    "audience_list_id": ["RL-00123"],
                    "placement_exclusion_list": ["adult,gaming"],
                    "frequency_cap": ["5/day"],
                    "geo": ["IN"]
                })
                st.dataframe(sample, use_container_width=True)
                st.download_button("Download template", sample.to_csv(index=False), "display_campaigns_template.csv", "text/csv")

            uploaded = st.file_uploader("Upload display_campaigns.csv", type=["csv"], key="disp_upload")
            if st.button("Create Display Campaigns"):
                with st.spinner("Processing..."):
                    time.sleep(1.0)
                add_log("[MOCK] create_display_campaigns_bulk → 1 campaign validated", "ok")
                add_log("DRY RUN: audience segments, placement lists staged — no write", "warn")
                st.success("Validated. Connect API credentials to execute.")
                st.rerun()

    with tab2:
        st.markdown('<div class="section-header">Enable / Pause Campaigns</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            pause_names = st.text_area("Campaign names to PAUSE (one per line)", height=120, placeholder="Brand|Search|IN\nNonBrand|Search|IN")
            if st.button("Pause Campaigns", key="pause_btn"):
                names = [n.strip() for n in pause_names.split("\n") if n.strip()]
                if names:
                    with st.spinner("Executing..."):
                        time.sleep(0.8)
                    for n in names:
                        add_log(f"[MOCK] pause_campaigns_by_name → '{n}'", "ok")
                        add_audit("UPDATE", n, "Status → PAUSED")
                    st.success(f"{len(names)} campaign(s) paused (mock).")
                    st.rerun()
        with cols[1]:
            enable_names = st.text_area("Campaign names to ENABLE (one per line)", height=120, placeholder="Competitor|Search|IN")
            if st.button("Enable Campaigns", key="enable_btn"):
                names = [n.strip() for n in enable_names.split("\n") if n.strip()]
                if names:
                    with st.spinner("Executing..."):
                        time.sleep(0.8)
                    for n in names:
                        add_log(f"[MOCK] enable_campaigns_by_name → '{n}'", "ok")
                        add_audit("UPDATE", n, "Status → ENABLED")
                    st.success(f"{len(names)} campaign(s) enabled (mock).")
                    st.rerun()

    with tab3:
        st.markdown('<div class="section-header">Campaign Inventory</div>', unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.campaigns)[["id", "name", "type", "status", "budget", "bid_strategy", "roas", "cpa", "spend"]]
        df.columns = ["ID", "Name", "Type", "Status", "Budget (₹)", "Bid Strategy", "ROAS", "CPA (₹)", "Spend (₹)"]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Export CSV", df.to_csv(index=False), "campaigns_export.csv", "text/csv")

elif nav == "Keywords":
    st.markdown("## Keyword Management")
    tab1, tab2, tab3, tab4 = st.tabs(["Add Keywords", "Negatives", "Search Term Harvest", "Match Type Changes"])

    with tab1:
        st.markdown('<div class="section-header">Bulk Keyword Addition</div>', unsafe_allow_html=True)
        with st.expander("CSV Format — keywords.csv"):
            sample = pd.DataFrame({
                "campaign_name": ["Brand|Search|IN", "Brand|Search|IN"],
                "ad_group_name": ["Brand Core", "Brand Core"],
                "keyword": ["acme software", "acme platform"],
                "match_type": ["EXACT", "PHRASE"],
                "cpc_bid": [15.0, 12.0],
                "status": ["ENABLED", "ENABLED"]
            })
            st.dataframe(sample, use_container_width=True)
            st.download_button("Download template", sample.to_csv(index=False), "keywords_template.csv", "text/csv")
        uploaded = st.file_uploader("Upload keywords.csv", type=["csv"])
        if st.button("Add Keywords"):
            with st.spinner("Processing..."):
                time.sleep(0.8)
            add_log("[MOCK] add_keywords_bulk → 2 keywords staged", "ok")
            add_audit("CREATE", "Keywords", "2 keywords · Brand|Search|IN · EXACT+PHRASE")
            st.success("Keywords staged (mock). Connect API to execute.")
            st.rerun()

    with tab2:
        st.markdown('<div class="section-header">Negative Keyword Lists</div>', unsafe_allow_html=True)
        neg_level = st.radio("Apply at", ["Campaign level", "Ad group level", "Shared list"], horizontal=True)
        neg_terms = st.text_area("Negative keywords (one per line)", height=140, placeholder="free\ncheap\njobs")
        campaign_target = st.text_input("Target campaign name (or shared list name)")
        if st.button("Add Negatives"):
            terms = [t.strip() for t in neg_terms.split("\n") if t.strip()]
            if terms and campaign_target:
                with st.spinner("Processing..."):
                    time.sleep(0.6)
                add_log(f"[MOCK] add_negative_keywords_bulk → {len(terms)} terms → {campaign_target}", "ok")
                add_audit("CREATE", "Negative Keywords", f"{len(terms)} negatives → {campaign_target} ({neg_level})")
                st.success(f"{len(terms)} negative keywords added (mock).")
                st.rerun()

    with tab3:
        st.markdown('<div class="section-header">Search Term Harvest</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            campaign_ids = st.text_area("Campaign IDs (one per line)", height=100, placeholder="C-001\nC-002")
        with col2:
            date_from = st.date_input("From", value=date.today() - timedelta(days=30))
            date_to = st.date_input("To", value=date.today())
        conv_threshold = st.slider("Min conversions to flag as converter", 0, 10, 1)
        if st.button("Pull Search Terms Report"):
            with st.spinner("Running GAQL query..."):
                time.sleep(1.5)
            mock_terms = pd.DataFrame({
                "Search Term": ["buy acme software", "acme pricing", "acme vs competitor", "acme free trial", "acme demo"],
                "Match Type": ["BROAD", "BROAD", "BROAD", "BROAD", "PHRASE"],
                "Clicks": [145, 89, 67, 230, 55],
                "Conversions": [8, 4, 2, 0, 3],
                "Cost (₹)": [1820, 980, 760, 1240, 430],
                "Action": ["PROMOTE", "PROMOTE", "PROMOTE", "NEGATIVE", "PROMOTE"]
            })
            st.dataframe(mock_terms, use_container_width=True, hide_index=True)
            add_log("[MOCK] harvest_search_terms → 5 terms returned · 4 converters flagged", "ok")
            st.download_button("Export search terms", mock_terms.to_csv(index=False), "search_terms.csv", "text/csv")

    with tab4:
        st.markdown('<div class="section-header">Match Type Changes</div>', unsafe_allow_html=True)
        st.info("Upload CSV to bulk-change keyword match types across campaigns.", icon="ℹ️")
        with st.expander("CSV Format — match_type_changes.csv"):
            sample = pd.DataFrame({
                "campaign_name": ["NonBrand|Search|IN"],
                "ad_group_name": ["Generic"],
                "keyword": ["software solution"],
                "current_match_type": ["BROAD"],
                "new_match_type": ["PHRASE"]
            })
            st.dataframe(sample, use_container_width=True)
            st.download_button("Download template", sample.to_csv(index=False), "match_type_template.csv", "text/csv")
        uploaded = st.file_uploader("Upload match_type_changes.csv", type=["csv"], key="mt_upload")
        if st.button("Apply Match Type Changes"):
            with st.spinner("Processing..."):
                time.sleep(0.8)
            add_log("[MOCK] change_keyword_match_types → validated, no write", "warn")
            st.success("Changes staged (mock). Connect API to execute.")
            st.rerun()

elif nav == "Display & Audiences":
    st.markdown("## Display & Audience Management")
    tab1, tab2, tab3, tab4 = st.tabs(["Placements", "Audiences", "Exclusions", "Site Categories"])

    with tab1:
        st.markdown('<div class="section-header">Placement Operations</div>', unsafe_allow_html=True)
        op = st.radio("Operation", ["Add managed placements", "Exclude placements"], horizontal=True)
        with st.expander("CSV Format"):
            sample = pd.DataFrame({
                "campaign_name": ["Prospecting|Display|IN"],
                "ad_group_name": ["Tech Audiences"],
                "placement_url": ["techcrunch.com"],
                "placement_type": ["WEBSITE"]
            })
            st.dataframe(sample, use_container_width=True)
            st.download_button("Download template", sample.to_csv(index=False), "placements_template.csv", "text/csv")
        uploaded = st.file_uploader("Upload placements CSV", type=["csv"], key="pl_upload")
        if st.button("Execute Placement Operation"):
            with st.spinner("Processing..."):
                time.sleep(0.8)
            fn = "add_placements_bulk" if "Add" in op else "exclude_placements_bulk"
            add_log(f"[MOCK] {fn} → staged, no write", "warn")
            add_audit("CREATE" if "Add" in op else "REMOVE", "Placements", f"{op} · mock")
            st.success(f"{op} staged (mock).")
            st.rerun()

    with tab2:
        st.markdown('<div class="section-header">Audience Assignment</div>', unsafe_allow_html=True)
        aud_type = st.selectbox("Audience type", ["In-market", "Affinity", "Remarketing list", "Similar audiences"])
        campaign = st.text_input("Target campaign name", placeholder="Prospecting|Display|IN")
        ad_group = st.text_input("Target ad group name", placeholder="Broad Audiences")
        audience_id = st.text_input("Audience list ID", placeholder="RL-00123 or IM-5678")
        bid_adj = st.slider("Bid adjustment (%)", -90, 300, 0)
        if st.button("Assign Audience"):
            if campaign and audience_id:
                with st.spinner("Processing..."):
                    time.sleep(0.8)
                add_log(f"[MOCK] assign_audiences_bulk → {aud_type} {audience_id} → {campaign}", "ok")
                add_audit("CREATE", "Audience", f"{aud_type} {audience_id} → {campaign} · bid adj {bid_adj}%")
                st.success("Audience assignment staged (mock).")
                st.rerun()

    with tab3:
        st.markdown('<div class="section-header">Audience Exclusions</div>', unsafe_allow_html=True)
        ex_campaign = st.text_input("Campaign to exclude from", placeholder="Prospecting|Display|IN")
        ex_audience = st.text_input("Audience list ID to exclude", placeholder="RL-99999")
        if st.button("Exclude Audience"):
            if ex_campaign and ex_audience:
                with st.spinner("Processing..."):
                    time.sleep(0.6)
                add_log(f"[MOCK] exclude_audiences_bulk → {ex_audience} excluded from {ex_campaign}", "ok")
                add_audit("REMOVE", "Audience Exclusion", f"{ex_audience} excluded from {ex_campaign}")
                st.success("Exclusion staged (mock).")
                st.rerun()

    with tab4:
        st.markdown('<div class="section-header">Site Category & Content Exclusions</div>', unsafe_allow_html=True)
        st.multiselect("Exclude site categories", [
            "Adult", "Gambling", "Tragedy & Conflict", "Sensitive Social Issues",
            "Parked Domains", "Error Pages", "Juvenile/Children's Content", "Politics"
        ], default=["Adult", "Gambling"])
        st.multiselect("Exclude content labels", ["DL-MA", "DL-T", "DL-PG", "DL-G"], default=["DL-MA"])
        if st.button("Apply Exclusions"):
            with st.spinner("Processing..."):
                time.sleep(0.8)
            add_log("[MOCK] site category exclusions staged", "warn")
            st.success("Category exclusions staged (mock).")
            st.rerun()

elif nav == "Bids & Budget":
    st.markdown("## Bids & Budget Management")
    tab1, tab2, tab3 = st.tabs(["Daily Budgets", "Bid Strategy", "Target CPA / ROAS"])

    with tab1:
        st.markdown('<div class="section-header">Bulk Budget Updates</div>', unsafe_allow_html=True)
        with st.expander("CSV Format — update_budget.csv"):
            sample = pd.DataFrame({
                "campaign_name": ["Brand|Search|IN", "NonBrand|Search|IN"],
                "new_daily_budget": [3000, 6000]
            })
            st.dataframe(sample, use_container_width=True)
            st.download_button("Download template", sample.to_csv(index=False), "budget_template.csv", "text/csv")
        uploaded = st.file_uploader("Upload update_budget.csv", type=["csv"], key="bud_upload")
        if st.button("Update Budgets"):
            with st.spinner("Processing..."):
                time.sleep(0.8)
            add_log("[MOCK] update_daily_budget_bulk → 2 budgets staged", "warn")
            add_audit("UPDATE", "Campaign Budget", "2 campaigns · mock")
            st.success("Budget updates staged (mock).")
            st.rerun()

    with tab2:
        st.markdown('<div class="section-header">Bid Strategy Switch</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            camp_name = st.text_input("Campaign name", placeholder="NonBrand|Search|IN")
            current_strat = st.selectbox("Current strategy", ["TARGET_CPA", "TARGET_ROAS", "MAXIMIZE_CONVERSIONS", "MAXIMIZE_CLICKS", "ENHANCED_CPC", "TARGET_CPM"])
        with col2:
            new_strat = st.selectbox("New strategy", ["TARGET_ROAS", "TARGET_CPA", "MAXIMIZE_CONVERSIONS", "MAXIMIZE_CLICKS", "ENHANCED_CPC", "TARGET_CPM"])
            transition_note = st.text_input("Note / reason", placeholder="ROAS stable, scaling bid strategy")
        if st.button("Switch Bid Strategy"):
            if camp_name:
                with st.spinner("Processing..."):
                    time.sleep(0.8)
                add_log(f"[MOCK] update_bid_strategy_bulk → {camp_name} · {current_strat} → {new_strat}", "ok")
                add_audit("UPDATE", camp_name, f"Bid strategy: {current_strat} → {new_strat}")
                st.success(f"Strategy switch staged (mock): {current_strat} → {new_strat}")
                st.rerun()

    with tab3:
        st.markdown('<div class="section-header">Target CPA / ROAS Updates</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Target CPA**")
            with st.expander("CSV Format — target_cpa.csv"):
                sample = pd.DataFrame({"campaign_name": ["Brand|Search|IN"], "target_cpa": [150]})
                st.dataframe(sample, use_container_width=True)
                st.download_button("Download template", sample.to_csv(index=False), "target_cpa_template.csv", "text/csv")
            uploaded_cpa = st.file_uploader("Upload target_cpa.csv", type=["csv"], key="cpa_up")
            if st.button("Update Target CPA"):
                with st.spinner("Processing..."):
                    time.sleep(0.8)
                add_log("[MOCK] update_target_cpa_bulk → staged", "warn")
                st.success("CPA updates staged (mock).")
                st.rerun()
        with col2:
            st.markdown("**Target ROAS**")
            with st.expander("CSV Format — target_roas.csv"):
                sample = pd.DataFrame({"campaign_name": ["Brand|Search|IN"], "target_roas": [4.5]})
                st.dataframe(sample, use_container_width=True)
                st.download_button("Download template", sample.to_csv(index=False), "target_roas_template.csv", "text/csv")
            uploaded_roas = st.file_uploader("Upload target_roas.csv", type=["csv"], key="roas_up")
            if st.button("Update Target ROAS"):
                with st.spinner("Processing..."):
                    time.sleep(0.8)
                add_log("[MOCK] update_target_roas_bulk → staged", "warn")
                st.success("ROAS updates staged (mock).")
                st.rerun()

elif nav == "Ad Copy & Assets":
    st.markdown("## Ad Copy & Asset Management")
    tab1, tab2, tab3 = st.tabs(["RSA Assets", "Display Ad Assets", "Final URLs"])

    with tab1:
        st.markdown('<div class="section-header">RSA Headline & Description Updates</div>', unsafe_allow_html=True)
        with st.expander("CSV Format — rsa_assets.csv"):
            sample = pd.DataFrame({
                "campaign_name": ["Brand|Search|IN"],
                "ad_group_name": ["Brand Core"],
                "ad_id": ["AD-00123"],
                "asset_type": ["HEADLINE"],
                "asset_position": [1],
                "new_text": ["Award-Winning Software Platform"],
                "pin_to_position": ["PINNED_TO_POSITION_1"]
            })
            st.dataframe(sample, use_container_width=True)
            st.download_button("Download template", sample.to_csv(index=False), "rsa_assets_template.csv", "text/csv")
        uploaded = st.file_uploader("Upload rsa_assets.csv", type=["csv"], key="rsa_up")
        if st.button("Update RSA Assets"):
            with st.spinner("Processing..."):
                time.sleep(1.0)
            add_log("[MOCK] update_rsa_assets_bulk → staged · no write", "warn")
            add_audit("UPDATE", "RSA Assets", "Headlines/descriptions staged · mock")
            st.success("RSA asset updates staged (mock).")
            st.rerun()

    with tab2:
        st.markdown('<div class="section-header">Responsive Display Ad Assets</div>', unsafe_allow_html=True)
        with st.expander("CSV Format — display_assets.csv"):
            sample = pd.DataFrame({
                "campaign_name": ["Prospecting|Display|IN"],
                "ad_id": ["AD-00456"],
                "asset_type": ["MARKETING_IMAGE"],
                "new_asset_url": ["https://cdn.example.com/banner_v2.jpg"],
                "action": ["REPLACE"]
            })
            st.dataframe(sample, use_container_width=True)
            st.download_button("Download template", sample.to_csv(index=False), "display_assets_template.csv", "text/csv")
        uploaded = st.file_uploader("Upload display_assets.csv", type=["csv"], key="da_up")
        if st.button("Update Display Assets"):
            with st.spinner("Processing..."):
                time.sleep(0.8)
            add_log("[MOCK] update_display_ad_assets → staged", "warn")
            st.success("Display asset updates staged (mock).")
            st.rerun()

    with tab3:
        st.markdown('<div class="section-header">Final URL Bulk Updates</div>', unsafe_allow_html=True)
        with st.expander("CSV Format — url_updates.csv"):
            sample = pd.DataFrame({
                "campaign_name": ["Brand|Search|IN"],
                "ad_group_name": ["Brand Core"],
                "ad_id": ["AD-00123"],
                "new_final_url": ["https://acme.com/lp-v3"],
                "new_tracking_template": ["{lpurl}?utm_source=google&utm_medium=cpc"]
            })
            st.dataframe(sample, use_container_width=True)
            st.download_button("Download template", sample.to_csv(index=False), "url_updates_template.csv", "text/csv")
        uploaded = st.file_uploader("Upload url_updates.csv", type=["csv"], key="url_up")
        if st.button("Update Final URLs"):
            with st.spinner("Processing..."):
                time.sleep(0.8)
            add_log("[MOCK] update_final_urls_bulk → staged", "warn")
            add_audit("UPDATE", "Final URLs", "Bulk URL update staged · mock")
            st.success("URL updates staged (mock).")
            st.rerun()

elif nav == "Auto-Pause Engine":
    st.markdown("## Auto-Pause Engine")
    st.info("Four daily rule scripts enforce performance thresholds automatically. All actions logged to the audit sheet.", icon="⚡")

    st.markdown('<div class="section-header">Scoring Weights</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: roas_w = st.slider("ROAS weight", 0.0, 1.0, 0.35, 0.05)
    with col2: cpa_w = st.slider("CPA weight", 0.0, 1.0, 0.30, 0.05)
    with col3: cvr_w = st.slider("CVR weight", 0.0, 1.0, 0.20, 0.05)
    with col4: is_w = st.slider("IS weight", 0.0, 1.0, 0.15, 0.05)

    total_w = roas_w + cpa_w + cvr_w + is_w
    if abs(total_w - 1.0) > 0.01:
        st.warning(f"Weights sum to {total_w:.2f} — should equal 1.0. Adjust sliders.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Rule Thresholds</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Auto-pause: Low ROAS**")
        roas_floor = st.number_input("ROAS floor (pause if below)", value=1.5, step=0.1, format="%.1f")
        roas_min_spend = st.number_input("Min spend to evaluate (₹)", value=500, step=100)

        st.markdown("**Auto-pause: High CPA**")
        cpa_ceil = st.number_input("CPA ceiling (₹, pause if above)", value=500, step=50)
        cpa_min_conv = st.number_input("Min conversions to evaluate", value=1, step=1)

    with col2:
        st.markdown("**Auto-pause: Low CVR**")
        cvr_floor = st.number_input("CVR floor % (pause if below)", value=0.5, step=0.1, format="%.1f")
        cvr_min_clicks = st.number_input("Min clicks to evaluate", value=50, step=10)

        st.markdown("**Auto-pause: Impression Share**")
        is_lost_ceil = st.number_input("IS Lost Budget % ceiling (flag if above)", value=30, step=5)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Run Auto-Pause Scripts</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Run: Low ROAS"):
            with st.spinner("Evaluating..."):
                time.sleep(1.2)
            paused = [c for c in st.session_state.campaigns if c["roas"] < roas_floor and c["spend"] >= roas_min_spend and c["status"] == "ACTIVE"]
            for c in paused:
                c["status"] = "PAUSED"
                add_log(f"[AUTO-PAUSE] ROAS rule: '{c['name']}' paused (ROAS {c['roas']}x < floor {roas_floor}x)", "warn")
                add_audit("AUTO-PAUSE", c["name"], f"ROAS {c['roas']}x below floor {roas_floor}x")
            if not paused:
                add_log("[AUTO-PAUSE] ROAS rule: no campaigns below threshold", "ok")
            st.rerun()
    with col2:
        if st.button("Run: High CPA"):
            with st.spinner("Evaluating..."):
                time.sleep(1.0)
            paused = [c for c in st.session_state.campaigns if c["cpa"] > cpa_ceil and c["status"] == "ACTIVE"]
            for c in paused:
                c["status"] = "PAUSED"
                add_log(f"[AUTO-PAUSE] CPA rule: '{c['name']}' paused (CPA ₹{c['cpa']} > ceiling ₹{cpa_ceil})", "warn")
                add_audit("AUTO-PAUSE", c["name"], f"CPA ₹{c['cpa']} above ceiling ₹{cpa_ceil}")
            if not paused:
                add_log("[AUTO-PAUSE] CPA rule: no campaigns above threshold", "ok")
            st.rerun()
    with col3:
        if st.button("Run: Low CVR"):
            with st.spinner("Evaluating..."):
                time.sleep(1.0)
            paused = [c for c in st.session_state.campaigns if c["cvr"] < cvr_floor and c["status"] == "ACTIVE"]
            for c in paused:
                c["status"] = "PAUSED"
                add_log(f"[AUTO-PAUSE] CVR rule: '{c['name']}' paused (CVR {c['cvr']}% < floor {cvr_floor}%)", "warn")
                add_audit("AUTO-PAUSE", c["name"], f"CVR {c['cvr']}% below floor {cvr_floor}%")
            if not paused:
                add_log("[AUTO-PAUSE] CVR rule: no campaigns below threshold", "ok")
            st.rerun()
    with col4:
        if st.button("Run: IS Flag"):
            with st.spinner("Evaluating..."):
                time.sleep(0.8)
            flagged = [c for c in st.session_state.campaigns if c["is_lost"] > is_lost_ceil]
            for c in flagged:
                add_log(f"[IS-FLAG] '{c['name']}' IS Lost Budget {c['is_lost']}% > {is_lost_ceil}% — budget constrained", "warn")
                add_audit("FLAG", c["name"], f"IS Lost {c['is_lost']}% above {is_lost_ceil}% — review budget")
            if not flagged:
                add_log("[IS-FLAG] All campaigns within IS threshold", "ok")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Current Scores vs Thresholds</div>', unsafe_allow_html=True)
    for c in st.session_state.campaigns:
        col1, col2, col3, col4, col5 = st.columns([2.5, 1, 1, 1, 1])
        with col1:
            badge_cls = "badge-active" if c["status"] == "ACTIVE" else "badge-paused"
            st.markdown(f'**{c["name"]}** <span class="status-badge {badge_cls}">{c["status"]}</span>', unsafe_allow_html=True)
        with col2:
            color = "#c93b3b" if c["roas"] < roas_floor else "#1a9e5f"
            st.markdown(f'<span style="color:{color};font-family:DM Mono,monospace;font-size:13px">ROAS {c["roas"]}x</span>', unsafe_allow_html=True)
        with col3:
            color = "#c93b3b" if c["cpa"] > cpa_ceil else "#1a9e5f"
            st.markdown(f'<span style="color:{color};font-family:DM Mono,monospace;font-size:13px">CPA ₹{c["cpa"]}</span>', unsafe_allow_html=True)
        with col4:
            color = "#c93b3b" if c["cvr"] < cvr_floor else "#1a9e5f"
            st.markdown(f'<span style="color:{color};font-family:DM Mono,monospace;font-size:13px">CVR {c["cvr"]}%</span>', unsafe_allow_html=True)
        with col5:
            color = "#d4920a" if c["is_lost"] > is_lost_ceil else "#1a9e5f"
            st.markdown(f'<span style="color:{color};font-family:DM Mono,monospace;font-size:13px">IS Lost {c["is_lost"]}%</span>', unsafe_allow_html=True)
        st.divider()

    st.markdown('<div class="section-header">Operation Log</div>', unsafe_allow_html=True)
    render_logs()

elif nav == "GAQL Reports":
    st.markdown("## GAQL Performance Reports")
    st.caption("All reports use GoogleAdsService.search() with GAQL queries. Connect API credentials to pull live data.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Campaigns", "Keywords", "Placements", "Search Terms", "Audiences"])

    report_meta = {
        "Campaigns": ("fetch_campaign_performance", "impressions, clicks, conversions, cost, roas"),
        "Keywords": ("fetch_keyword_performance", "keyword, match_type, impressions, clicks, conv, cost, search_is"),
        "Placements": ("fetch_placement_performance", "placement_url, impressions, clicks, conv, cost"),
        "Search Terms": ("fetch_search_terms_report", "search_term, match_type, clicks, conv, cost"),
        "Audiences": ("fetch_audience_performance", "audience_name, segment_type, impressions, clicks, conv"),
    }

    for tab_name, tab_obj in zip(["Campaigns", "Keywords", "Placements", "Search Terms", "Audiences"],
                                  [tab1, tab2, tab3, tab4, tab5]):
        with tab_obj:
            fn_name, fields = report_meta[tab_name]
            st.markdown(f'<div class="section-header">{tab_name} Report</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1: d_from = st.date_input("From", value=date.today() - timedelta(days=30), key=f"df_{tab_name}")
            with col2: d_to = st.date_input("To", value=date.today(), key=f"dt_{tab_name}")
            with col3:
                camp_filter = st.text_input("Campaign name filter (optional)", key=f"cf_{tab_name}", placeholder="Brand|Search|IN")

            with st.expander("GAQL Query"):
                resource = tab_name.lower().replace(" ", "_")
                gaql = f"""SELECT
  campaign.name,
  campaign.id,
  {chr(10).join('  ' + f + ',' for f in fields.split(', '))}
  segments.date
FROM {resource if resource != "search_terms" else "search_term_view"}
WHERE segments.date BETWEEN '{d_from}' AND '{d_to}'
{"  AND campaign.name = '" + camp_filter + "'" if camp_filter else ""}
ORDER BY metrics.cost_micros DESC
LIMIT 1000"""
                st.code(gaql, language="sql")

            if st.button(f"Pull {tab_name} Report", key=f"pull_{tab_name}"):
                with st.spinner(f"Running GAQL · {fn_name}..."):
                    time.sleep(1.5)
                rows = []
                for c in st.session_state.campaigns:
                    rows.append({
                        "Campaign": c["name"], "Impressions": random.randint(5000, 50000),
                        "Clicks": random.randint(100, 2000), "Conversions": random.randint(2, 80),
                        "Cost (₹)": c["spend"], "Revenue (₹)": c["revenue"],
                        "ROAS": c["roas"], "CPA (₹)": c["cpa"]
                    })
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
                add_log(f"[MOCK] {fn_name} → {len(df)} rows returned (mock)", "ok")
                st.download_button(f"Export {tab_name} CSV", df.to_csv(index=False), f"{resource}_report.csv", "text/csv")

elif nav == "Audit Log":
    st.markdown("## Audit Log")
    st.caption("Every API write operation is logged here. In production, this syncs to Google Sheets (Sheet3).")

    if st.session_state.audit_log:
        df = pd.DataFrame(st.session_state.audit_log)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Export audit log", df.to_csv(index=False), "audit_log.csv", "text/csv")
        if st.button("Clear log"):
            st.session_state.audit_log = []
            st.rerun()
    else:
        st.info("No operations logged yet. Run operations from any module to generate audit entries.", icon="📋")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Google Sheets Sync</div>', unsafe_allow_html=True)
    sheet_id = st.text_input("Google Sheet ID", placeholder="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms")
    if st.button("Sync to Google Sheets"):
        if sheet_id and st.session_state.audit_log:
            with st.spinner("Syncing..."):
                time.sleep(1.0)
            add_log(f"[MOCK] sync_stats_to_gsheet → Sheet3 · {len(st.session_state.audit_log)} rows staged", "warn")
            st.success("Sync staged (mock). Connect service account credentials to execute.")
            st.rerun()
        else:
            st.error("Enter a Sheet ID and run some operations first.")

elif nav == "API Config":
    st.markdown("## API Configuration")
    st.warning("This section configures live Google Ads API credentials. All operations currently run in mock mode.", icon="⚠️")

    st.markdown('<div class="section-header">OAuth 2.0 Credentials</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        client_id = st.text_input("Client ID", type="password", placeholder="••••••••.apps.googleusercontent.com")
        client_secret = st.text_input("Client Secret", type="password")
        refresh_token = st.text_input("Refresh Token", type="password")
    with col2:
        dev_token = st.text_input("Developer Token", type="password")
        mcc_id = st.text_input("MCC Login Customer ID", placeholder="123-456-7890")
        env = st.selectbox("Environment", ["Sandbox", "Production"])

    st.markdown('<div class="section-header">google-ads.yaml Preview</div>', unsafe_allow_html=True)
    yaml_preview = f"""developer_token: {'[SET]' if dev_token else '[NOT SET]'}
client_id: {'[SET]' if client_id else '[NOT SET]'}
client_secret: {'[SET]' if client_secret else '[NOT SET]'}
refresh_token: {'[SET]' if refresh_token else '[NOT SET]'}
login_customer_id: {mcc_id if mcc_id else '[NOT SET]'}
use_proto_plus: True"""
    st.code(yaml_preview, language="yaml")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Test Connection"):
            if all([client_id, client_secret, refresh_token, dev_token, mcc_id]):
                with st.spinner("Testing connection..."):
                    time.sleep(1.5)
                add_log("[MOCK] API connection test → credentials validated (mock)", "ok")
                st.success("Connection test passed (mock). Real validation requires live credentials.")
                st.rerun()
            else:
                st.error("Fill all credential fields before testing.")
    with col2:
        if st.button("Save Configuration"):
            st.info("In production: credentials saved to google-ads.yaml (never committed to version control).")

    st.markdown('<div class="section-header">API Rate Limits</div>', unsafe_allow_html=True)
    st.markdown("""
    | Operation | Daily Limit | Rate |
    |-----------|------------|------|
    | Mutate operations | 15,000 / customer / day | Batched per request |
    | GAQL queries | Unlimited | 1,000 rows/page |
    | Bulk uploads | 5MB / request | — |
    """)

