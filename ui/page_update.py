"""
ui/page_update.py — Data Management page for Football AI Nexus Engine
Redesigned with full Nexus Engine v9.0 dark navy UI.
"""
import os
import glob
from pathlib import Path
import streamlit as st
import pandas as pd

from src.config import DATA_DIR, MODEL_PATH
from src.predict import update_season_csv_from_api
from utils import silent

STABILIZE_REPORT_PATH = Path(DATA_DIR).parent / "artifacts" / "reports" / "stabilize_backtest_report.json"

# ═══════════════════════════════════════════════════════════════
# GOOGLE FONTS
# ═══════════════════════════════════════════════════════════════
_GF = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Syne:wght@700;800&"
    "family=DM+Sans:wght@400;500;600;700&"
    "family=JetBrains+Mono:wght@600;700&display=swap');"
)

# ═══════════════════════════════════════════════════════════════
# PAGE CSS
# ═══════════════════════════════════════════════════════════════
_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@600;700&display=swap');

.main .block-container { padding-top:1.5rem; max-width:1100px; }

/* Header */
.pg-eyebrow {
    font-family:'DM Sans',sans-serif; font-size:.8rem; font-weight:700;
    letter-spacing:5px; text-transform:uppercase; color:#38BDF8; margin-bottom:10px;
}
.pg-title {
    font-family:'Syne',sans-serif; font-size:3.2rem; font-weight:800;
    color:#F0F6FF; letter-spacing:-.5px; line-height:1.05; margin-bottom:6px;
}
.pg-title em { font-style:normal; color:#38BDF8; }
.pg-sub {
    font-family:'DM Sans',sans-serif; font-size:1.05rem;
    color:rgba(148,187,233,.44); line-height:1.6;
}

/* Section divider */
.div-wrap { display:flex; align-items:center; gap:16px; margin:36px 0 24px; }
.div-line  { flex:1; height:1px; background:rgba(255,255,255,.06); }
.div-label {
    font-family:'DM Sans',sans-serif; font-size:.72rem; font-weight:700;
    letter-spacing:3px; text-transform:uppercase;
    color:rgba(148,187,233,.28); white-space:nowrap;
}

/* Cards */
.nx-card {
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.13);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.nx-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.nx-card.accent-blue::before  { background: linear-gradient(90deg, #38BDF8, transparent); }
.nx-card.accent-purple::before { background: linear-gradient(90deg, #C084FC, transparent); }
.nx-card.accent-green::before  { background: linear-gradient(90deg, #34D399, transparent); }
.nx-card.accent-amber::before  { background: linear-gradient(90deg, #F59E0B, transparent); }

.nx-card-title {
    font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:800;
    color:#F0F6FF; margin-bottom:6px; display:flex; align-items:center; gap:10px;
}
.nx-card-sub {
    font-family:'DM Sans',sans-serif; font-size:.85rem;
    color:rgba(148,187,233,.5); margin-bottom:20px;
    font-family:'JetBrains Mono',monospace; font-size:.75rem;
    word-break: break-all;
}

/* Buttons */
[data-testid="stButton"] > button {
    font-family:'DM Sans',sans-serif !important;
    font-weight:700 !important;
    letter-spacing:1px !important;
    border-radius:10px !important;
    padding:10px 24px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0EA5E9, #38BDF8) !important;
    border: none !important;
    color: #0B1628 !important;
    font-weight:800 !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #38BDF8, #7DD3FC) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(56,189,248,.35) !important;
}
[data-testid="stButton"] > button[kind="secondary"] {
    background: rgba(192,132,252,.1) !important;
    border: 1px solid rgba(192,132,252,.3) !important;
    color: #C084FC !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: rgba(192,132,252,.18) !important;
    border-color: rgba(192,132,252,.5) !important;
    transform: translateY(-1px) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,.07) !important;
    border: 1px solid rgba(255,255,255,.15) !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
}
[data-testid="stMetricLabel"] {
    font-family:'DM Sans',sans-serif !important;
    font-size:.7rem !important;
    letter-spacing:2.5px !important;
    text-transform:uppercase !important;
    color:rgba(148,187,233,.5) !important;
}
[data-testid="stMetricValue"] {
    font-family:'Syne',sans-serif !important;
    font-size:1.5rem !important;
    color:#F0F6FF !important;
}

/* Status badges */
.badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-family:'DM Sans',sans-serif; font-size:.72rem; font-weight:700;
    letter-spacing:1.5px; text-transform:uppercase;
    padding: 4px 12px; border-radius: 99px; border: 1px solid;
}
.badge-green  { color:#34D399; background:rgba(52,211,153,.1); border-color:rgba(52,211,153,.3); }
.badge-amber  { color:#F59E0B; background:rgba(245,158,11,.1); border-color:rgba(245,158,11,.3); }
.badge-blue   { color:#38BDF8; background:rgba(56,189,248,.1); border-color:rgba(56,189,248,.3); }
.badge::before {
    content:''; width:5px; height:5px; border-radius:50%;
    background:currentColor;
}

/* Path badge */
.path-badge {
    display: inline-flex; align-items: center; gap: 8px;
    font-family:'JetBrains Mono',monospace; font-size:.72rem;
    color:rgba(148,187,233,.5);
    background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.08);
    border-radius:8px; padding:6px 14px;
    margin-top:8px; word-break:break-all;
}

/* File table */
.file-row {
    display: flex; align-items: center; gap:16px;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,.05);
    transition: background 0.15s ease;
    border-radius: 8px;
}
.file-row:hover {
    background: rgba(255,255,255,.04);
}
.file-name {
    font-family:'DM Sans',sans-serif; font-weight:700;
    color:#F0F6FF; font-size:.9rem; flex:1;
}
.file-rows {
    font-family:'JetBrains Mono',monospace; font-size:.8rem;
    color:#38BDF8; background:rgba(56,189,248,.08);
    border:1px solid rgba(56,189,248,.2);
    border-radius:6px; padding:2px 10px;
}
.file-err {
    font-family:'DM Sans',sans-serif; font-size:.82rem;
    color:rgba(248,113,113,.7);
}

/* Dataframe override */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-width: 1px !important;
}

/* Spinner */
.stSpinner > div { border-top-color:#38BDF8 !important; }
</style>"""


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════
def _divider(label: str):
    st.markdown(
        f'<div class="div-wrap"><span class="div-line"></span>'
        f'<span class="div-label">{label}</span>'
        f'<span class="div-line"></span></div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════
def page_update(ctx):
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Page Header ──────────────────────────────────────────────
    st.markdown("""
        <div style="margin-bottom:32px;">
            <div class="pg-eyebrow">⚡ Nexus Engine · Operations</div>
            <div class="pg-title">Data <em>Management</em></div>
            <div class="pg-sub">Sync live data · Run backtests · Inspect local datasets</div>
        </div>
    """, unsafe_allow_html=True)

    # ── Path Info ────────────────────────────────────────────────
    st.markdown(
        f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:28px;">'
        f'<span class="path-badge">📁 DATA: {DATA_DIR}</span>'
        f'<span class="path-badge">🤖 MODEL: {MODEL_PATH}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ════════════════════════════════════════════════════════════
    # SECTION 1 — System Update
    # ════════════════════════════════════════════════════════════
    _divider("System Update")

    st.markdown("""
        <div class="nx-card accent-blue">
            <div class="nx-card-title">☁️ Live Season Sync</div>
            <div style="font-family:'DM Sans',sans-serif;font-size:.9rem;
                color:rgba(148,187,233,.65);line-height:1.7;margin-bottom:20px;">
                Fetch the latest Premier League 2025 results from <b style="color:#38BDF8;">football-data.org API</b>
                and update local CSV. New matches will be appended automatically.
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("☁️ Sync Season 2025 via API", type="primary"):
        with st.spinner("Connecting to API..."):
            df_new = silent(update_season_csv_from_api)
        if df_new is not None:
            st.success(f"✅ Update successful — **{len(df_new):,}** matches indexed.")
            st.dataframe(df_new.head(10), use_container_width=True)
        else:
            st.error("❌ Failed to fetch update. Check API key and network.")

    # ════════════════════════════════════════════════════════════
    # SECTION 2 — STABILIZE Backtest
    # ════════════════════════════════════════════════════════════
    _divider("STABILIZE Backtest")

    stabilize_on = ctx.get('stabilize_connected', False)
    badge_html = (
        '<span class="badge badge-green">Linked</span>'
        if stabilize_on else
        '<span class="badge badge-amber">Not Linked</span>'
    )

    st.markdown(
        f'<div class="nx-card accent-purple">'
        f'<div class="nx-card-title">🧠 Neural Network Backtest &nbsp;{badge_html}</div>'
        f'<div style="font-family:\'DM Sans\',sans-serif;font-size:.9rem;'
        f'color:rgba(148,187,233,.65);line-height:1.7;margin-bottom:16px;">'
        f'Rolling-origin walk-forward backtest (2020–2025). '
        f'Results are loaded into ctx for monitoring — <b style="color:#C084FC;">not</b> overriding live inference.'
        f'</div>'
        f'<span class="path-badge">📄 {STABILIZE_REPORT_PATH}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if stabilize_on:
        sm = ctx.get('stabilize_summary', {})
        if sm:
            c1, c2, c3 = st.columns(3, gap="medium")
            c1.metric("Val Accuracy",     f"{sm.get('avg_val_accuracy_after', 0):.3f}")
            c2.metric("Holdout Accuracy", f"{sm.get('final_holdout_accuracy_after', 0):.3f}")
            c3.metric("Holdout Macro-F1", f"{sm.get('final_holdout_macro_f1_after', 0):.3f}")
            st.write("")
    else:
        st.info("STABILIZE report not linked yet. Run backtest below to generate it.")

    if st.button("▶ Run STABILIZE Backtest (2020–2025)", type="secondary"):
        with st.spinner("Running rolling-origin backtest..."):
            from pipelines.train_pipeline import main as run_stabilize_backtest
            silent(run_stabilize_backtest)
        st.success("✅ STABILIZE backtest complete. Reloading UI context...")
        st.cache_resource.clear()
        st.rerun()

    # ════════════════════════════════════════════════════════════
    # SECTION 3 — Local Datasets
    # ════════════════════════════════════════════════════════════
    _divider("Local Datasets")

    files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))

    st.markdown(
        f'<div class="nx-card accent-amber">'
        f'<div class="nx-card-title">📂 CSV Files in /data</div>'
        f'<div style="font-family:\'DM Sans\',sans-serif;font-size:.85rem;'
        f'color:rgba(148,187,233,.5);margin-bottom:16px;">',
        unsafe_allow_html=True,
    )

    if files:
        rows_html = ""
        for f in files:
            try:
                df_tmp = pd.read_csv(f)
                rows_html += (
                    f'<div class="file-row">'
                    f'<span style="font-size:1rem;">📄</span>'
                    f'<span class="file-name">{os.path.basename(f)}</span>'
                    f'<span class="file-rows">{len(df_tmp):,} rows</span>'
                    f'</div>'
                )
            except Exception:
                rows_html += (
                    f'<div class="file-row">'
                    f'<span style="font-size:1rem;">⚠️</span>'
                    f'<span class="file-name" style="color:rgba(248,113,113,.8);">'
                    f'{os.path.basename(f)}</span>'
                    f'<span class="file-err">Unable to read</span>'
                    f'</div>'
                )

        total = len(files)
        st.markdown(
            f'<div class="nx-card accent-amber">'
            f'<div class="nx-card-title">📂 CSV Files &nbsp;'
            f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:.85rem;'
            f'color:#F59E0B;background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.25);'
            f'border-radius:6px;padding:2px 10px;font-weight:700;">{total} files</span>'
            f'</div>'
            f'<div style="margin-top:4px;">{rows_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="nx-card accent-amber">'
            '<div class="nx-card-title">📂 CSV Files</div>'
            '<div style="font-family:\'DM Sans\',sans-serif;font-size:.9rem;'
            'color:rgba(148,187,233,.4);padding:24px 0;text-align:center;">'
            '🗂 No CSV files found in data directory.</div>'
            '</div>',
            unsafe_allow_html=True,
        )