# CyberNova Analytics Dashboard
# Business Intelligence and Data Analytics Project
# This Streamlit application analyses simulated IIS web server logs and presents
# stakeholder-specific business intelligence views for CyberNova Analytics.

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    page_title="CyberNova Analytics",
    layout="wide",
    page_icon="CN"
)


refresh_count = st_autorefresh(interval=10_000, key="refresh")


BASE_MONTH_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRck5N3u4GpJFRIFRekZ-slAcRe68Fyz1Zmxgj3gMbvkMBb0HBUQ1DmGh12MvU3QWEAlxZ1_wFEzz1K"
    "/pub?gid={gid}&single=true&output=csv"
)


MONTH_GIDS = {
    "2026-01": "190784173",
    "2026-02": "892438961",
    "2026-03": "2066746225",
    "2026-04": "483259368",
    "2026-05": "2138791989",
    "2026-06": "1975543257",
    "2026-07": "1347959723",
    "2026-08": "1186832265",
    "2026-09": "2088800065",
    "2026-10": "383944149",
    "2026-11": "1382952024",
    "2026-12": "616073200",
}


st.sidebar.markdown("### Display")
light_mode = st.sidebar.toggle("Light mode", value=False)
st.sidebar.markdown("---")


if light_mode:
    APP_BG = "#f3f7fb"
    SIDEBAR_BG = "#ffffff"
    TEXT_MAIN = "#0f172a"
    TEXT_MUTED = "#475569"
    CARD_BG = "#ffffff"
    CARD_BORDER = "#d8e2ef"
    KPI_BG = "#ffffff"
    ACCENT = "#2563eb"
    ACCENT_2 = "#0f766e"
    ACCENT_SOFT = "rgba(37,99,235,0.12)"
    GRID = "rgba(15,23,42,0.10)"
    SHADOW = "0 8px 24px rgba(15,23,42,0.08)"
    MOVING_AVG = "#d97706"
else:
    APP_BG = "linear-gradient(160deg, #060d1a 0%, #0b1527 100%)"
    SIDEBAR_BG = "#080f1e"
    TEXT_MAIN = "#e8f0fe"
    TEXT_MUTED = "#9fb4d0"
    CARD_BG = "rgba(14,22,42,0.97)"
    CARD_BORDER = "rgba(255,255,255,0.08)"
    KPI_BG = "rgba(14,22,42,0.97)"
    ACCENT = "#60a5fa"
    ACCENT_2 = "#22c55e"
    ACCENT_SOFT = "rgba(96,165,250,0.14)"
    GRID = "rgba(255,255,255,0.06)"
    SHADOW = "0 8px 28px rgba(0,0,0,0.28)"
    MOVING_AVG = "#facc15"


st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, .stApp {{
    background: {APP_BG} !important;
    font-family: 'DM Sans', sans-serif !important;
    color: {TEXT_MAIN} !important;
}}

.block-container {{
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
}}

section[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {CARD_BORDER};
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT_MAIN} !important;
}}

div[data-baseweb="select"] > div {{
    background-color: {CARD_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
    color: {TEXT_MAIN} !important;
}}

div[data-baseweb="select"] * {{
    color: {TEXT_MAIN} !important;
}}

div[data-baseweb="popover"], div[data-baseweb="popover"] * {{
    background-color: {CARD_BG} !important;
    color: {TEXT_MAIN} !important;
}}

ul[role="listbox"], li[role="option"] {{
    background-color: {CARD_BG} !important;
    color: {TEXT_MAIN} !important;
}}

li[role="option"]:hover {{
    background-color: {ACCENT_SOFT} !important;
}}

h1 {{
    font-size: 2.35rem !important;
    font-weight: 800 !important;
    color: {TEXT_MAIN} !important;
    letter-spacing: -0.04em !important;
    margin-bottom: 0.1rem !important;
}}

h2, h3 {{
    color: {TEXT_MAIN} !important;
    font-weight: 800 !important;
}}

.page-subtitle {{
    color: {TEXT_MUTED};
    font-size: 1rem;
    margin-bottom: 1.1rem;
}}

.story-banner {{
    background: linear-gradient(135deg, {ACCENT_SOFT}, rgba(34,197,94,0.08));
    border: 1px solid {CARD_BORDER};
    border-radius: 18px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: {SHADOW};
}}

.story-banner strong {{
    color: {TEXT_MAIN};
}}

.story-banner p {{
    color: {TEXT_MUTED};
    margin: 0.25rem 0 0 0;
    line-height: 1.55;
}}

.kpi {{
    background: {KPI_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 18px;
    padding: 1rem 1.1rem;
    box-shadow: {SHADOW};
    min-height: 120px;
}}

.kpi-label {{
    font-size: 0.74rem;
    font-weight: 700;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.45rem;
}}

.kpi-value {{
    font-size: 1.85rem;
    font-weight: 800;
    color: {TEXT_MAIN};
    line-height: 1.1;
    font-family: 'DM Mono', monospace;
}}

.kpi-accent .kpi-value {{
    color: {ACCENT};
}}

.kpi-sub {{
    font-size: 0.78rem;
    color: {TEXT_MUTED};
    margin-top: 0.5rem;
}}

.insight {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 3px solid {ACCENT};
    border-radius: 12px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.65rem;
}}

.insight p {{
    color: {TEXT_MAIN};
    margin: 0;
    line-height: 1.6;
    font-size: 0.9rem;
}}

.section-caption {{
    color: {TEXT_MUTED};
    font-size: 0.86rem;
    margin-top: -0.25rem;
    margin-bottom: 0.7rem;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 18px;
    padding: 1rem;
    box-shadow: {SHADOW};
}}

[data-testid="stMetricValue"] {{
    color: {TEXT_MAIN} !important;
}}

[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED} !important;
}}

/* Keep radio button labels readable in both dark mode and light mode. */
div[role="radiogroup"] label,
div[role="radiogroup"] label span,
div[role="radiogroup"] p {{
    color: {TEXT_MAIN} !important;
    opacity: 1 !important;
}}
</style>
""", unsafe_allow_html=True)


# Clean the loaded web log dataset.
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip() for c in df.columns]

    text_cols = [
        "country", "service_category", "interaction_type",
        "is_conversion", "campaign_source", "device_type",
        "resource", "method", "response_group"
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["datetime"] = pd.to_datetime(
        df["date"].astype(str).str.strip() + " " + df["time"].astype(str).str.strip(),
        dayfirst=True,
        errors="coerce"
    )

    df = df.dropna(subset=["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)
    return df


# Load only the selected monthly partition through the Flask API.
# The API acts as a separate data access layer between Streamlit and Google Sheets.
# This makes the dashboard API-driven while keeping the rest of the dashboard logic unchanged.
@st.cache_data(ttl=60, show_spinner=False)
def load_month_data(month_key: str) -> pd.DataFrame:
    GID_MAP = {
        "2026-01": "YOUR_GID_1",
        "2026-02": "YOUR_GID_2",
        "2026-03": "YOUR_GID_3",
        "2026-04": "YOUR_GID_4",
        "2026-05": "YOUR_GID_5",
        "2026-06": "YOUR_GID_6",
        "2026-07": "YOUR_GID_7",
        "2026-08": "YOUR_GID_8",
        "2026-09": "YOUR_GID_9",
        "2026-10": "YOUR_GID_10",
        "2026-11": "YOUR_GID_11",
        "2026-12": "YOUR_GID_12"
    }

    BASE_SHEETS_URL = (
        "https://docs.google.com/spreadsheets/d/e/"
        "YOUR_SHEET_ID/pub"
    )

    @st.cache_data(ttl=300)
    def load_data(month_key):
        gid = GID_MAP.get(month_key)

        if gid is None:
            st.error(f"No GID configured for {month_key}")
            return pd.DataFrame()

        csv_url = f"{BASE_SHEETS_URL}?gid={gid}&single=true&output=csv"

        try:
            df = pd.read_csv(csv_url)
            return df

        except Exception as e:
            st.error(f"Failed to load data: {e}")
            return pd.DataFrame()
        
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data["records"])

        return clean_dataframe(df)

    except Exception as e:
        st.error(f"Data Pipeline Offline: {e}")
        return pd.DataFrame()


# Shared Plotly layout for consistent chart styling.
def make_base_layout():
    return dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=TEXT_MAIN, size=12),
        margin=dict(l=8, r=8, t=20, b=8),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=TEXT_MAIN)),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=TEXT_MAIN)),
    )


BASE = make_base_layout()


# Reusable KPI card component.
def kpi_card(column, label, value, sub="", accent=False):
    cls = "kpi kpi-accent" if accent else "kpi"
    column.markdown(
        f"""
        <div class="{cls}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Reusable insight card component.
def insight(text):
    st.markdown(f'<div class="insight"><p>{text}</p></div>', unsafe_allow_html=True)


# Reusable page introduction component.
def page_intro(title, subtitle, strategic_title, strategic_text):
    st.title(title)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="story-banner">
            <strong>{strategic_title}</strong>
            <p>{strategic_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# Horizontal bar chart for ranked categories.
def horizontal_bar(df, x_col, y_col, x_title, height=330):
    fig = go.Figure(go.Bar(
        x=df[x_col],
        y=df[y_col],
        orientation="h",
        marker=dict(
            color=df[x_col],
            colorscale=[[0, ACCENT_SOFT], [1, ACCENT]],
            showscale=False
        ),
        marker_line_width=0,
        hovertemplate="%{y}: %{x:,}<extra></extra>"
    ))
    fig.update_layout(**BASE, xaxis_title=x_title, height=height)
    return fig


# Vertical bar chart for categorical comparisons.
def vertical_bar(df, x_col, y_col, x_title, y_title, height=330):
    fig = go.Figure(go.Bar(
        x=df[x_col],
        y=df[y_col],
        marker=dict(
            color=df[y_col],
            colorscale=[[0, ACCENT_SOFT], [1, ACCENT]],
            showscale=False
        ),
        marker_line_width=0,
        hovertemplate="%{x}: %{y:,}<extra></extra>"
    ))
    fig.update_layout(**BASE, xaxis_title=x_title, yaxis_title=y_title, height=height)
    return fig


# Line chart for trend analysis.
# A 3-day moving average is added to support basic predictive trend interpretation.
def line_chart(df, x_col, y_col, x_title, y_title, height=330):
    chart_df = df.copy()

    fig = go.Figure(go.Scatter(
        x=chart_df[x_col],
        y=chart_df[y_col],
        mode="lines+markers",
        name="Daily Volume",
        line=dict(color=ACCENT, width=2.5),
        marker=dict(size=4, color=ACCENT),
        fill="tozeroy",
        fillcolor=ACCENT_SOFT,
        hovertemplate="%{x}: %{y:,}<extra></extra>"
    ))

    if len(chart_df) >= 3:
        chart_df["moving_avg"] = chart_df[y_col].rolling(window=3).mean()

        fig.add_trace(go.Scatter(
            x=chart_df[x_col],
            y=chart_df["moving_avg"],
            mode="lines",
            name="3-Day Moving Average",
            line=dict(color=MOVING_AVG, width=2.2, dash="dash"),
            hovertemplate="%{x}: %{y:,.0f}<extra></extra>"
        ))

    fig.update_layout(
        **BASE,
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,
        legend=dict(
            orientation="h",
            y=1.08,
            x=0,
            font=dict(color=TEXT_MAIN)
        )
    )
    return fig


# Geographic demand map.
# Regional mode focuses on Africa, International mode displays the world map,
# and a selected single country zooms directly to that country.
def country_demand_map(country_counts, map_scope="Regional", selected_country="All countries", height=360):

    country_iso = {
        "Botswana": "BWA",
        "South Africa": "ZAF",
        "Zimbabwe": "ZWE",
        "Zambia": "ZMB",
        "Namibia": "NAM",
        "Mozambique": "MOZ",
        "Lesotho": "LSO",
        "Eswatini": "SWZ",
        "Swaziland": "SWZ",
        "Angola": "AGO",
        "Malawi": "MWI",
        "Kenya": "KEN",
        "Nigeria": "NGA",
        "United Kingdom": "GBR",
        "UK": "GBR",
        "United States": "USA",
        "USA": "USA",
        "India": "IND"
    }

    map_df = country_counts.copy()
    map_df["iso_alpha"] = map_df["country"].map(country_iso)
    map_df = map_df.dropna(subset=["iso_alpha"])

    fig = go.Figure(
        go.Choropleth(
            locations=map_df["iso_alpha"],
            z=map_df["count"],
            text=map_df["country"],
            locationmode="ISO-3",
            colorscale=[
                [0, "rgba(96,165,250,0.18)"],
                [0.45, "#2563eb"],
                [1, "#60a5fa"]
            ],
            marker_line_color="rgba(255,255,255,0.18)",
            marker_line_width=0.7,
            colorbar=dict(
                title="Demand",
                thickness=12,
                len=0.72,
                tickfont=dict(color=TEXT_MAIN)
            ),
            hovertemplate="<b>%{text}</b><br>Demand: %{z:,}<extra></extra>"
        )
    )

    geo_settings = dict(
        projection_type="natural earth",
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(255,255,255,0.16)",
        showcountries=True,
        countrycolor="rgba(255,255,255,0.12)",
        showland=True,
        landcolor="rgba(15,23,42,0.45)",
        showocean=True,
        oceancolor="rgba(6,13,26,0.8)",
        bgcolor="rgba(0,0,0,0)"
    )

    # When one country is selected in the sidebar, zoom directly to that country.
    if selected_country != "All countries":
        geo_settings["fitbounds"] = "locations"
        geo_settings["visible"] = True

    # Otherwise, Regional stays Africa and International stays world.
    elif map_scope == "Regional":
        geo_settings["scope"] = "africa"

    fig.update_geos(**geo_settings)
    fig.update_layout(**BASE, height=height)

    return fig


# Sidebar navigation for stakeholder-specific views.
st.sidebar.markdown("### Navigation")
selected_view = st.sidebar.radio(
    "Stakeholder view",
    [
        "Executive Overview",
        "Sales Intelligence",
        "Marketing Analytics",
        "Operations Intelligence"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")


# Month selector for monthly partition loading.
selected_month = st.sidebar.selectbox(
    "Month",
    list(MONTH_GIDS.keys()),
    index=4
)


# Load selected month.
with st.spinner(f"Loading {selected_month} data..."):
    df_source = load_month_data(selected_month)


# Live simulation settings.
MAX_ROWS = len(df_source)
START_ROWS = min(15_000, MAX_ROWS)
ROWS_PER_BATCH = 250


# Session state stores the active month and number of visible rows.
if "loaded_month" not in st.session_state:
    st.session_state.loaded_month = selected_month

if "live_row_count" not in st.session_state:
    st.session_state.live_row_count = START_ROWS

if "last_refresh_count" not in st.session_state:
    st.session_state.last_refresh_count = refresh_count


# Reset row counter when the selected month changes.
if st.session_state.loaded_month != selected_month:
    st.session_state.loaded_month = selected_month
    st.session_state.live_row_count = START_ROWS
    st.session_state.last_refresh_count = refresh_count


# May 2026 is treated as the live month.
# Other months show the full static historical partition.
if selected_month == "2026-05":
    if refresh_count != st.session_state.last_refresh_count:
        st.session_state.last_refresh_count = refresh_count
        next_count = st.session_state.live_row_count + ROWS_PER_BATCH

        if next_count >= MAX_ROWS:
            st.session_state.live_row_count = START_ROWS
        else:
            st.session_state.live_row_count = next_count
else:
    st.session_state.live_row_count = MAX_ROWS


# Use only the currently visible portion of the month.
df = df_source.head(st.session_state.live_row_count).copy()


# Stop execution if the selected data does not load.
if df.empty:
    st.error("No data loaded. Check your published Google Sheet month tabs or Flask API.")
    st.stop()


# Show data loading status in the sidebar.
st.sidebar.caption(
    f"Fast API month-tab loading<br>"
    f"Live: **{st.session_state.live_row_count:,}** of **{MAX_ROWS:,}** records loaded",
    unsafe_allow_html=True
)


# Build filter options dynamically from the loaded dataset.
countries_list = (
    ["All countries"] + sorted(df["country"].dropna().unique().tolist())
    if "country" in df.columns else ["All countries"]
)

services_list = (
    ["All categories"] + sorted(df["service_category"].dropna().unique().tolist())
    if "service_category" in df.columns else ["All categories"]
)

campaign_list = (
    ["All sources"] + sorted(df["campaign_source"].dropna().unique().tolist())
    if "campaign_source" in df.columns else ["All sources"]
)


# Apply sidebar filters.
selected_country = st.sidebar.selectbox("Country", countries_list)
selected_service = st.sidebar.selectbox("Service category", services_list)
selected_campaign = st.sidebar.selectbox("Campaign source", campaign_list)

filtered_df = df.copy()

if selected_country != "All countries":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_service != "All categories":
    filtered_df = filtered_df[filtered_df["service_category"] == selected_service]

if selected_campaign != "All sources":
    filtered_df = filtered_df[filtered_df["campaign_source"] == selected_campaign]

if filtered_df.empty:
    st.warning("No data matches the selected filters. Try adjusting the filters.")
    st.stop()


# Core KPI calculations.
total_visits = len(filtered_df)

unique_visitors = (
    filtered_df["ip_address"].nunique()
    if "ip_address" in filtered_df.columns else 0
)

conversions = (
    filtered_df["is_conversion"].astype(str).str.lower().eq("yes").sum()
    if "is_conversion" in filtered_df.columns else 0
)

conversion_rate = (conversions / total_visits * 100) if total_visits > 0 else 0


# Convert interaction types to lowercase once for consistent keyword matching.
interaction_series = (
    filtered_df["interaction_type"].astype(str).str.lower()
    if "interaction_type" in filtered_df.columns
    else pd.Series([], dtype="object")
)


# Stakeholder-specific business indicators.
demo_requests = interaction_series.str.contains("demo", na=False).sum()
ai_requests = interaction_series.str.contains("ai advisory|advisory", na=False).sum()
event_interest = interaction_series.str.contains("event|webinar", na=False).sum()
consultation_requests = interaction_series.str.contains("consultation", na=False).sum()
risk_requests = interaction_series.str.contains("risk", na=False).sum()
prototype_enquiries = interaction_series.str.contains("prototype", na=False).sum()

service_requests = interaction_series.str.contains(
    "request|enquiry|interest|consultation|demo|advisory|risk|prototype|event|webinar",
    na=False
).sum()

high_intent_leads = (
    demo_requests +
    consultation_requests +
    ai_requests +
    risk_requests +
    prototype_enquiries
)


# Estimated pipeline value.
# These values are simple assumptions used to translate engagement into business potential.
estimated_revenue = (
    (demo_requests * 850) +
    (consultation_requests * 700) +
    (ai_requests * 450) +
    (risk_requests * 650) +
    (prototype_enquiries * 900)
)


# Advanced business health measures.
# These derived measures move the dashboard beyond simple counts and support
# higher-level business decision-making.
lead_weights = {
    "demo": 10,
    "consultation": 8,
    "advisory": 7,
    "risk": 6,
    "prototype": 6,
    "webinar": 3,
    "event": 3
}


def calculate_lead_quality_score(text):
    text = str(text).lower()
    score = 0

    for keyword, weight in lead_weights.items():
        if keyword in text:
            score += weight

    return score


if "interaction_type" in filtered_df.columns:
    filtered_df["lead_quality_score"] = filtered_df["interaction_type"].apply(calculate_lead_quality_score)
    total_lead_quality_score = int(filtered_df["lead_quality_score"].sum())
else:
    total_lead_quality_score = 0


# Server Reliability Index.
# This measures the share of requests that did not result in 4xx or 5xx server/client errors.
if "status_code" in filtered_df.columns:
    status_as_text = filtered_df["status_code"].astype(str)
    error_count = int(status_as_text.str.startswith(("4", "5")).sum())
    error_rate = (error_count / total_visits * 100) if total_visits > 0 else 0
    server_reliability = 100 - error_rate
else:
    error_count = 0
    error_rate = 0
    server_reliability = 100


# Aggregations used for charts.
service_counts = (
    filtered_df["service_category"].value_counts().reset_index()
    if "service_category" in filtered_df.columns
    else pd.DataFrame(columns=["service_category", "count"])
)
service_counts.columns = ["service_category", "count"]

country_counts = (
    filtered_df["country"].value_counts().reset_index()
    if "country" in filtered_df.columns
    else pd.DataFrame(columns=["country", "count"])
)
country_counts.columns = ["country", "count"]


# Campaign performance table.
campaign_conv = pd.DataFrame()

if "campaign_source" in filtered_df.columns and "is_conversion" in filtered_df.columns:
    campaign_conv = (
        filtered_df
        .groupby("campaign_source", dropna=False)
        .agg(
            total=("campaign_source", "size"),
            conversions=("is_conversion", lambda x: x.astype(str).str.lower().eq("yes").sum())
        )
        .reset_index()
    )

    campaign_conv["conv_rate"] = (
        campaign_conv["conversions"] / campaign_conv["total"] * 100
    ).round(1)


# Daily trend data.
trend_df = pd.DataFrame(columns=["date", "count"])

if "datetime" in filtered_df.columns and filtered_df["datetime"].notna().any():
    trend_df = (
        filtered_df
        .groupby(filtered_df["datetime"].dt.date)
        .size()
        .reset_index(name="count")
    )
    trend_df.columns = ["date", "count"]


# Peak Demand Hour.
# This identifies the busiest hour of activity in the selected dataset.
if "datetime" in filtered_df.columns and filtered_df["datetime"].notna().any():
    hourly_counts = (
        filtered_df
        .assign(hour=filtered_df["datetime"].dt.hour)
        .groupby("hour")
        .size()
        .reset_index(name="visits")
    )

    if not hourly_counts.empty:
        peak_hour = int(hourly_counts.loc[hourly_counts["visits"].idxmax(), "hour"])
        peak_hour_visits = int(hourly_counts["visits"].max())
    else:
        peak_hour = 0
        peak_hour_visits = 0
else:
    hourly_counts = pd.DataFrame(columns=["hour", "visits"])
    peak_hour = 0
    peak_hour_visits = 0


# Interaction type distribution.
interaction_mix = pd.DataFrame(columns=["interaction_type", "count"])

if "interaction_type" in filtered_df.columns:
    interaction_mix = (
        filtered_df["interaction_type"]
        .value_counts()
        .head(8)
        .reset_index()
    )
    interaction_mix.columns = ["interaction_type", "count"]


# Device distribution.
device_counts = pd.DataFrame(columns=["device_type", "count"])

if "device_type" in filtered_df.columns:
    device_counts = filtered_df["device_type"].value_counts().reset_index()
    device_counts.columns = ["device_type", "count"]


# Status code distribution.
status_counts = pd.DataFrame(columns=["status_code", "count"])

if "status_code" in filtered_df.columns:
    status_counts = filtered_df["status_code"].value_counts().reset_index()
    status_counts.columns = ["status_code", "count"]


# Extract top values for insight cards.
top_service = service_counts.iloc[0]["service_category"] if not service_counts.empty else "N/A"
top_service_count = int(service_counts.iloc[0]["count"]) if not service_counts.empty else 0

top_country = country_counts.iloc[0]["country"] if not country_counts.empty else "N/A"
top_country_count = int(country_counts.iloc[0]["count"]) if not country_counts.empty else 0

best_channel = "N/A"
best_channel_rate = 0

if not campaign_conv.empty:
    best_row = campaign_conv.loc[campaign_conv["conv_rate"].idxmax()]
    best_channel = best_row["campaign_source"]
    best_channel_rate = best_row["conv_rate"]


# Market Concentration Ratio.
# This shows how dependent CyberNova is on its highest-demand country.
market_concentration = (
    (top_country_count / total_visits) * 100
    if total_visits > 0 else 0
)


# Show whether the selected month is live or historical.
if selected_month == "2026-05":
    st.success("API-driven live dashboard active")
else:
    st.info("Static historical API data view")


# Executive Overview.
if selected_view == "Executive Overview":
    page_intro(
        "Executive Overview",
        f"Strategic performance view for CyberNova Analytics — {selected_month}",
        "Strategic performance intelligence",
        "This view consolidates revenue potential, conversion strength, regional demand, service performance, and business health into a concise executive decision layer."
    )

    st.subheader("Business Health Metrics")
    st.markdown(
        '<div class="section-caption">Derived business measures that support sales prioritisation, reliability monitoring, regional expansion, and operational planning.</div>',
        unsafe_allow_html=True
    )

    bh1, bh2, bh3, bh4 = st.columns(4)

    kpi_card(
        bh1,
        "Lead Quality Score",
        f"{total_lead_quality_score:,}",
        "Weighted sales opportunity score",
        True
    )

    kpi_card(
        bh2,
        "Server Reliability",
        f"{server_reliability:.1f}%",
        f"{error_rate:.1f}% error rate"
    )

    kpi_card(
        bh3,
        "Market Concentration",
        f"{market_concentration:.1f}%",
        f"Top market: {top_country}"
    )

    kpi_card(
        bh4,
        "Peak Demand Hour",
        f"{peak_hour}:00",
        f"{peak_hour_visits:,} visits recorded"
    )

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Pipeline Revenue", f"BWP {estimated_revenue:,.0f}", "Estimated commercial value", True)
    kpi_card(c2, "Conversion Rate", f"{conversion_rate:.1f}%", f"{conversions:,} conversions", True)
    kpi_card(c3, "Total Requests", f"{service_requests:,}", "Service-related demand")
    kpi_card(c4, "Top Region", f"{top_country}", f"{top_country_count:,} visits")
    kpi_card(c5, "Top Service", f"{top_service}", f"{top_service_count:,} engagements")

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 0.85])

    with left.container(border=True):
        st.subheader("Growth and Demand Trend")
        st.markdown(
            '<div class="section-caption">Daily traffic pattern with a 3-day moving average for basic trend interpretation.</div>',
            unsafe_allow_html=True
        )
        if not trend_df.empty:
            st.plotly_chart(line_chart(trend_df, "date", "count", "Date", "Events", 360), use_container_width=True)

    with right.container(border=True):
        st.subheader("Conversion Funnel")
        st.markdown(
            '<div class="section-caption">Progression from website activity to high-value business outcomes.</div>',
            unsafe_allow_html=True
        )

        funnel_values = [total_visits, service_requests, high_intent_leads, conversions]
        funnel_labels = ["Visits", "Service Requests", "High-Intent Leads", "Conversions"]

        fig = go.Figure(go.Funnel(
            y=funnel_labels,
            x=funnel_values,
            marker=dict(color=[ACCENT_SOFT, ACCENT_SOFT, ACCENT, ACCENT_2]),
            textinfo="value+percent initial"
        ))
        fig.update_layout(**BASE, height=360)
        st.plotly_chart(fig, use_container_width=True)

    left2, right2 = st.columns(2)

    with left2.container(border=True):
        st.subheader("Regional Demand Map")
        st.markdown(
            '<div class="section-caption">Geographic distribution of CyberNova demand by country.</div>',
            unsafe_allow_html=True
        )

        executive_map_scope = st.radio(
            "Map view",
            ["Regional", "International"],
            horizontal=True,
            label_visibility="collapsed",
            key="executive_map_scope"
        )

        if not country_counts.empty:
            st.plotly_chart(
                country_demand_map(
                    country_counts,
                    map_scope=executive_map_scope,
                    selected_country=selected_country,
                    height=420
                ),
                use_container_width=True
            )

    with right2.container(border=True):
        st.subheader("Top Services")
        st.markdown(
            '<div class="section-caption">Services attracting the strongest market interest.</div>',
            unsafe_allow_html=True
        )
        if not service_counts.empty:
            s = service_counts.sort_values("count")
            st.plotly_chart(horizontal_bar(s, "count", "service_category", "Requests", 360), use_container_width=True)

    with st.container(border=True):
        st.subheader("Executive Insights")
        insight(f"<strong>{top_country}</strong> is the strongest current market with <strong>{top_country_count:,}</strong> visits, indicating a priority region for continued commercial attention.")
        insight(f"<strong>{top_service}</strong> leads service demand with <strong>{top_service_count:,}</strong> engagements, showing the strongest area of customer interest.")
        insight(f"The dashboard estimates <strong>BWP {estimated_revenue:,.0f}</strong> in pipeline value from high-intent activity, giving management a practical commercial performance indicator.")
        insight(f"The conversion rate is <strong>{conversion_rate:.1f}%</strong>, while the weighted lead quality score is <strong>{total_lead_quality_score:,}</strong>, helping executives compare volume against lead value.")
        insight(f"Server reliability is <strong>{server_reliability:.1f}%</strong>, with peak demand occurring around <strong>{peak_hour}:00</strong>, supporting operational planning and capacity decisions.")


# Sales Intelligence.
elif selected_view == "Sales Intelligence":
    page_intro(
        "Sales Intelligence",
        f"Lead prioritisation and conversion opportunity view — {selected_month}",
        "Commercial opportunity intelligence",
        "This view identifies high-intent customer actions and highlights where the sales team should focus follow-up to improve conversion outcomes."
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Lead Quality Score", f"{total_lead_quality_score:,}", "Weighted lead value", True)
    kpi_card(c2, "Demo Requests", f"{demo_requests:,}", "Immediate follow-up leads", True)
    kpi_card(c3, "Consultations", f"{consultation_requests:,}", "Advisory sales interest")
    kpi_card(c4, "Conversions", f"{conversions:,}", "Confirmed high-value actions")
    kpi_card(c5, "Sales Conversion", f"{conversion_rate:.1f}%", "Filtered conversion rate")

    left, right = st.columns(2)

    with left.container(border=True):
        st.subheader("Sales Lead Funnel")
        st.markdown(
            '<div class="section-caption">Progression from visitor traffic to sales-ready opportunities.</div>',
            unsafe_allow_html=True
        )

        funnel_values = [total_visits, service_requests, high_intent_leads, demo_requests + consultation_requests, conversions]
        funnel_labels = ["Visits", "Service Requests", "High-Intent Leads", "Demo + Consultation", "Conversions"]

        fig = go.Figure(go.Funnel(
            y=funnel_labels,
            x=funnel_values,
            marker=dict(color=[ACCENT_SOFT, ACCENT_SOFT, ACCENT, ACCENT, ACCENT_2]),
            textinfo="value+percent initial"
        ))
        fig.update_layout(**BASE, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with right.container(border=True):
        st.subheader("Sales Opportunity Map")
        st.markdown(
            '<div class="section-caption">Country-level view of high-intent sales opportunities.</div>',
            unsafe_allow_html=True
        )

        sales_df = filtered_df[
            interaction_series.str.contains("demo|consultation|advisory|risk|prototype", na=False)
        ].copy()

        if not sales_df.empty and "country" in sales_df.columns:
            sales_country = sales_df["country"].value_counts().reset_index()
            sales_country.columns = ["country", "count"]

            sales_map_scope = st.radio(
                "Map view",
                ["Regional", "International"],
                horizontal=True,
                label_visibility="collapsed",
                key="sales_map_scope"
            )

            st.plotly_chart(
                country_demand_map(
                    sales_country,
                    map_scope=sales_map_scope,
                    selected_country=selected_country,
                    height=420
                ),
                use_container_width=True
            )
        else:
            st.info("No sales opportunity data available for this filter.")

    left2, right2 = st.columns(2)

    with left2.container(border=True):
        st.subheader("High-Intent Interaction Mix")
        st.markdown(
            '<div class="section-caption">Sales-relevant actions customers are taking.</div>',
            unsafe_allow_html=True
        )

        if "interaction_type" in filtered_df.columns:
            sales_mix = filtered_df[
                interaction_series.str.contains("demo|consultation|advisory|risk|prototype", na=False)
            ]["interaction_type"].value_counts().reset_index()
            sales_mix.columns = ["interaction_type", "count"]

            if not sales_mix.empty:
                st.plotly_chart(horizontal_bar(sales_mix.sort_values("count"), "count", "interaction_type", "Lead Count", 340), use_container_width=True)

    with right2.container(border=True):
        st.subheader("Sales Channel Efficiency")
        st.markdown(
            '<div class="section-caption">Campaign sources ranked by conversion efficiency.</div>',
            unsafe_allow_html=True
        )

        if not campaign_conv.empty:
            c = campaign_conv.sort_values("conv_rate")
            fig = go.Figure(go.Bar(
                x=c["conv_rate"],
                y=c["campaign_source"],
                orientation="h",
                marker_color=ACCENT,
                hovertemplate="%{y}: %{x:.1f}% conversion rate<extra></extra>"
            ))
            fig.update_layout(**BASE, xaxis_title="Conversion Rate (%)", height=340)
            st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Sales Priorities")
        insight(f"The weighted lead quality score is <strong>{total_lead_quality_score:,}</strong>, helping the sales team prioritise high-value actions rather than treating all clicks equally.")
        insight(f"Prioritise the <strong>{demo_requests:,}</strong> demo requests because these users have already shown direct product interest.")
        insight(f"<strong>{top_country}</strong> should be treated as the strongest sales territory in the current view.")
        insight(f"Leads from <strong>{best_channel}</strong> should receive focused attention because this source currently has the highest conversion efficiency at <strong>{best_channel_rate:.1f}%</strong>.")
        insight("Demo, consultation, advisory and risk assessment interactions should be treated as qualified lead indicators rather than ordinary traffic.")


# Marketing Analytics.
elif selected_view == "Marketing Analytics":
    page_intro(
        "Marketing Analytics",
        f"Campaign performance and audience engagement view — {selected_month}",
        "Market engagement intelligence",
        "This view evaluates how acquisition channels, digital campaigns, events, and audience behaviour contribute to measurable engagement and conversion performance."
    )

    engagement_rate = (service_requests / total_visits * 100) if total_visits > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Website Traffic", f"{total_visits:,}", "Filtered visits", True)
    kpi_card(c2, "Engagement Rate", f"{engagement_rate:.1f}%", "Service-related actions", True)
    kpi_card(c3, "Event Interest", f"{event_interest:,}", "Webinar and event demand")
    kpi_card(c4, "Campaign Conversions", f"{conversions:,}", "Converted interactions")
    kpi_card(c5, "Best Channel", f"{best_channel}", f"{best_channel_rate:.1f}% conversion")

    left, right = st.columns(2)

    with left.container(border=True):
        st.subheader("Campaign Performance")
        st.markdown(
            '<div class="section-caption">Total visits compared with conversions by acquisition source.</div>',
            unsafe_allow_html=True
        )

        if not campaign_conv.empty:
            c = campaign_conv.sort_values("total", ascending=True)

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=c["total"],
                y=c["campaign_source"],
                orientation="h",
                name="Total Visits",
                marker_color=ACCENT_SOFT,
                hovertemplate="%{y}: %{x:,} visits<extra></extra>"
            ))
            fig.add_trace(go.Bar(
                x=c["conversions"],
                y=c["campaign_source"],
                orientation="h",
                name="Conversions",
                marker_color=ACCENT,
                hovertemplate="%{y}: %{x:,} conversions<extra></extra>"
            ))
            fig.update_layout(
                **BASE,
                barmode="overlay",
                xaxis_title="Count",
                height=360,
                legend=dict(orientation="h", y=1.08, x=0, font=dict(color=TEXT_MAIN))
            )
            st.plotly_chart(fig, use_container_width=True)

    with right.container(border=True):
        st.subheader("Engagement Trend")
        st.markdown(
            '<div class="section-caption">Daily engagement pattern with a 3-day moving average for campaign monitoring.</div>',
            unsafe_allow_html=True
        )
        if not trend_df.empty:
            st.plotly_chart(line_chart(trend_df, "date", "count", "Date", "Events", 360), use_container_width=True)

    left2, right2 = st.columns(2)

    with left2.container(border=True):
        st.subheader("Device Behaviour")
        st.markdown(
            '<div class="section-caption">How visitors access CyberNova digital content.</div>',
            unsafe_allow_html=True
        )

        if not device_counts.empty:
            fig = go.Figure(go.Pie(
                labels=device_counts["device_type"],
                values=device_counts["count"],
                hole=0.55,
                marker=dict(colors=[ACCENT, ACCENT_SOFT, TEXT_MUTED]),
                hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>"
            ))
            fig.update_layout(
                **BASE,
                height=340,
                legend=dict(
                    orientation="h",
                    y=-0.1,
                    x=0.5,
                    xanchor="center",
                    font=dict(color=TEXT_MAIN)
                )
            )
            st.plotly_chart(fig, use_container_width=True)

    with right2.container(border=True):
        st.subheader("Event and Webinar Engagement")
        st.markdown(
            '<div class="section-caption">Marketing demand linked to promotional events and awareness activities.</div>',
            unsafe_allow_html=True
        )

        event_df = filtered_df[
            interaction_series.str.contains("event|webinar", na=False)
        ].copy()

        if not event_df.empty and "campaign_source" in event_df.columns:
            event_campaign = event_df["campaign_source"].value_counts().reset_index()
            event_campaign.columns = ["campaign_source", "count"]
            st.plotly_chart(horizontal_bar(event_campaign.sort_values("count"), "count", "campaign_source", "Event Interest", 340), use_container_width=True)
        else:
            st.info("No event or webinar engagement data available for this filter.")

    with st.container(border=True):
        st.subheader("Marketing Insights")
        insight(f"<strong>{best_channel}</strong> is currently the most efficient acquisition source with a <strong>{best_channel_rate:.1f}%</strong> conversion rate.")
        insight(f"The engagement rate is <strong>{engagement_rate:.1f}%</strong>, showing how many visitors moved beyond basic browsing into service-related actions.")
        insight(f"<strong>{event_interest:,}</strong> event-related interactions indicate the level of market response to awareness and webinar activity.")
        insight(f"Market concentration is <strong>{market_concentration:.1f}%</strong>, showing how much current demand depends on the leading country.")
        insight("Marketing decisions should compare high-traffic sources against high-conversion sources before reallocating campaign effort.")


# Operations Intelligence.
else:
    page_intro(
        "Operations Intelligence",
        f"Service monitoring and operational behaviour view — {selected_month}",
        "Operational performance intelligence",
        "This view monitors service demand, AI assistant usage, request behaviour, server reliability, and traffic timing patterns to support operational planning."
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "AI Requests", f"{ai_requests:,}", "Cyber assistant usage", True)
    kpi_card(c2, "Service Demand", f"{service_requests:,}", "Operational workload", True)
    kpi_card(c3, "Reliability", f"{server_reliability:.1f}%", f"{error_count:,} error responses")
    kpi_card(c4, "Peak Hour", f"{peak_hour}:00", f"{peak_hour_visits:,} visits")
    kpi_card(c5, "Status Types", f"{status_counts['status_code'].nunique() if not status_counts.empty else 0}", "Response groups")

    left, right = st.columns(2)

    with left.container(border=True):
        st.subheader("Service Demand Distribution")
        st.markdown(
            '<div class="section-caption">Operational view of the most requested CyberNova services.</div>',
            unsafe_allow_html=True
        )
        if not service_counts.empty:
            st.plotly_chart(horizontal_bar(service_counts.sort_values("count"), "count", "service_category", "Requests", 360), use_container_width=True)

    with right.container(border=True):
        st.subheader("Interaction Mix")
        st.markdown(
            '<div class="section-caption">User activity patterns across the digital platform.</div>',
            unsafe_allow_html=True
        )
        if not interaction_mix.empty:
            st.plotly_chart(horizontal_bar(interaction_mix.sort_values("count"), "count", "interaction_type", "Count", 360), use_container_width=True)

    left2, right2 = st.columns(2)

    with left2.container(border=True):
        st.subheader("Operational Traffic Trend")
        st.markdown(
            '<div class="section-caption">Daily volume pattern with a 3-day moving average for monitoring load and demand.</div>',
            unsafe_allow_html=True
        )
        if not trend_df.empty:
            st.plotly_chart(line_chart(trend_df, "date", "count", "Date", "Events", 340), use_container_width=True)

    with right2.container(border=True):
        st.subheader("Status Code Monitoring")
        st.markdown(
            '<div class="section-caption">Operational response monitoring from server logs, used to support the reliability index.</div>',
            unsafe_allow_html=True
        )

        if not status_counts.empty:
            status_counts["status_code"] = status_counts["status_code"].astype(str)
            status_counts = status_counts.sort_values("count", ascending=True)

            fig = go.Figure(go.Bar(
                x=status_counts["count"],
                y=status_counts["status_code"],
                orientation="h",
                marker=dict(
                    color=status_counts["count"],
                    colorscale=[[0, ACCENT_SOFT], [1, ACCENT]],
                    showscale=False
                ),
                text=status_counts["count"],
                texttemplate="%{text:,}",
                textposition="auto",
                hovertemplate="Status %{y}<br>Count: %{x:,}<extra></extra>"
            ))

            status_layout = BASE.copy()
            status_layout["margin"] = dict(l=70, r=35, t=20, b=45)

            fig.update_layout(
                **status_layout,
                height=340,
                xaxis_title="Count",
                yaxis_title="Status Code"
            )

            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(type="category")

            st.plotly_chart(fig, use_container_width=True)

    if not hourly_counts.empty:
        with st.container(border=True):
            st.subheader("Peak Demand Analysis")
            st.markdown(
                '<div class="section-caption">Hourly traffic distribution showing the strongest demand period for operational capacity planning.</div>',
                unsafe_allow_html=True
            )

            fig = go.Figure(go.Bar(
                x=hourly_counts["hour"],
                y=hourly_counts["visits"],
                marker=dict(
                    color=hourly_counts["visits"],
                    colorscale=[[0, ACCENT_SOFT], [1, ACCENT]],
                    showscale=False
                ),
                hovertemplate="Hour %{x}:00<br>Visits: %{y:,}<extra></extra>"
            ))

            fig.update_layout(
                **BASE,
                height=330,
                xaxis_title="Hour of Day",
                yaxis_title="Visits"
            )

            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Operational Insights")
        insight(f"AI advisory requests reached <strong>{ai_requests:,}</strong>, showing direct usage of CyberNova's AI-powered support capability.")
        insight(f"<strong>{top_service}</strong> creates the largest service workload with <strong>{top_service_count:,}</strong> interactions.")
        insight(f"Server reliability is <strong>{server_reliability:.1f}%</strong>, based on an error rate of <strong>{error_rate:.1f}%</strong> from 4xx and 5xx responses.")
        insight(f"Peak demand occurs around <strong>{peak_hour}:00</strong>, when <strong>{peak_hour_visits:,}</strong> visits were recorded.")
        insight("The service demand, interaction mix, status code and hourly demand charts help operations understand where support capacity is most needed.")

    display_cols = [
        c for c in [
            "datetime", "country", "resource", "service_category",
            "interaction_type", "lead_quality_score", "is_conversion",
            "status_code", "campaign_source", "device_type"
        ]
        if c in filtered_df.columns
    ]

    with st.container(border=True):
        st.subheader("Recent Website Activity")
        st.markdown(
            '<div class="section-caption">Latest interactions in the filtered operational view.</div>',
            unsafe_allow_html=True
        )
        st.dataframe(
            filtered_df.sort_values("datetime", ascending=False)[display_cols].head(25),
            use_container_width=True,
            height=330,
            hide_index=True
        )