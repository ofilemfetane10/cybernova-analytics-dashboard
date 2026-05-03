import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Set the browser tab title, page layout, and icon
st.set_page_config(
    page_title="CyberNova Analytics",
    layout="wide",
    page_icon="CN"
)

# Auto-refresh the page every 10 seconds to simulate live incoming data
refresh_count = st_autorefresh(interval=10_000, key="refresh")

# Base URL template for loading each month tab from the published Google Sheet.
# The {gid} placeholder gets replaced with the specific tab ID for each month.
BASE_MONTH_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRck5N3u4GpJFRIFRekZ-slAcRe68Fyz1Zmxgj3gMbvkMBb0HBUQ1DmGh12MvU3QWEAlxZ1_wFEzz1K"
    "/pub?gid={gid}&single=true&output=csv"
)

# Each month has its own published tab in Google Sheets.
# The gid is the unique identifier for that tab and is found in the published CSV link.
# Only the selected month is fetched, which keeps loading fast.
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

# Sidebar toggle so users can switch between dark and light display modes
st.sidebar.markdown("### Display")
light_mode = st.sidebar.toggle("Light mode", value=False)
st.sidebar.markdown("---")

# Two complete sets of colour variables, one for light mode and one for dark mode.
# Every colour used in the dashboard references these variables so switching themes
# changes the entire look in one go.
if light_mode:
    APP_BG = "#f0f4f9"
    SIDEBAR_BG = "#ffffff"
    TEXT_MAIN = "#0f172a"
    TEXT_MUTED = "#475569"
    CARD_BG = "#ffffff"
    CARD_BORDER = "#dbe3ef"
    KPI_BG = "#ffffff"
    ACCENT = "#2563eb"
    ACCENT_SOFT = "rgba(37,99,235,0.12)"
    GRID = "rgba(15,23,42,0.10)"
    SHADOW = "0 4px 18px rgba(15,23,42,0.08)"
else:
    APP_BG = "linear-gradient(160deg, #060d1a 0%, #0b1527 100%)"
    SIDEBAR_BG = "#080f1e"
    TEXT_MAIN = "#e8f0fe"
    TEXT_MUTED = "#9fb4d0"
    CARD_BG = "rgba(14,22,42,0.97)"
    CARD_BORDER = "rgba(255,255,255,0.08)"
    KPI_BG = "rgba(14,22,42,0.97)"
    ACCENT = "#60a5fa"
    ACCENT_SOFT = "rgba(96,165,250,0.14)"
    GRID = "rgba(255,255,255,0.06)"
    SHADOW = "0 8px 28px rgba(0,0,0,0.28)"

# Custom CSS injected into the app to control fonts, backgrounds, card styles,
# and KPI card appearance. The f-string means theme colour variables are applied
# at the moment the page renders.
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, .stApp {{
    background: {APP_BG} !important;
    font-family: 'DM Sans', sans-serif !important;
    color: {TEXT_MAIN} !important;
}}

.block-container {{
    max-width: 1400px;
    padding-top: 1.4rem;
    padding-bottom: 2.5rem;
}}

section[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {CARD_BORDER};
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT_MAIN} !important;
}}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {{
    color: {TEXT_MAIN} !important;
}}

[data-baseweb="select"] * {{
    color: {TEXT_MAIN} !important;
}}

[data-baseweb="select"] > div {{
    background-color: {CARD_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
}}

[data-baseweb="popover"] * {{
    color: {TEXT_MAIN} !important;
}}

h1 {{
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    color: {TEXT_MAIN} !important;
    letter-spacing: -0.04em !important;
    margin-bottom: 0.1rem !important;
}}

h2, h3 {{
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: {TEXT_MAIN} !important;
    margin-bottom: 0.1rem !important;
}}

.kpi {{
    background: {KPI_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 16px;
    padding: 1rem 1.1rem 0.9rem;
    box-shadow: {SHADOW};
}}

.kpi-label {{
    font-size: 0.78rem;
    font-weight: 600;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.4rem;
}}

.kpi-value {{
    font-size: 2rem;
    font-weight: 800;
    color: {TEXT_MAIN};
    line-height: 1;
    font-family: 'DM Mono', monospace;
}}

.kpi-accent .kpi-value {{
    color: {ACCENT};
}}

.kpi-sub {{
    font-size: 0.76rem;
    color: {ACCENT};
    margin-top: 0.35rem;
}}

.insight {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 3px solid {ACCENT};
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
}}

.insight p {{
    font-size: 0.88rem;
    color: {TEXT_MAIN};
    margin: 0;
    line-height: 1.65;
}}

.section-caption {{
    color: {TEXT_MUTED};
    font-size: 0.85rem;
    margin-top: -0.1rem;
    margin-bottom: 0.6rem;
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
</style>
""", unsafe_allow_html=True)


# This function cleans up a raw dataframe after it is loaded from Google Sheets.
# It strips whitespace from column names and text values, then combines the
# separate date and time columns into one proper datetime column for filtering
# and charting. Rows where the datetime could not be parsed are dropped.
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

    # dayfirst=True tells pandas the dates are in dd/mm/yyyy format
    df["datetime"] = pd.to_datetime(
        df["date"].astype(str).str.strip() + " " + df["time"].astype(str).str.strip(),
        dayfirst=True,
        errors="coerce"
    )

    df = df.dropna(subset=["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)

    return df


# This function fetches one month of data from the published Google Sheet CSV.
# Results are cached for 30 minutes so switching between months does not
# trigger a fresh network request every time.
@st.cache_data(ttl=1800, show_spinner=False)
def load_month_data(month_key: str) -> pd.DataFrame:
    gid = MONTH_GIDS[month_key]
    url = BASE_MONTH_URL.format(gid=gid)
    df = pd.read_csv(url, low_memory=False)
    return clean_dataframe(df)


st.sidebar.markdown("### Filters")

# Month selector — changing this triggers a fresh data load for that month only
selected_month = st.sidebar.selectbox(
    "Month",
    list(MONTH_GIDS.keys()),
    index=3
)

# Load only the selected month's data and show a spinner while it fetches
with st.spinner(f"Loading {selected_month} data..."):
    df_source = load_month_data(selected_month)

MAX_ROWS = len(df_source)
START_ROWS = min(15_000, MAX_ROWS)
ROWS_PER_BATCH = 2_500

# Session state keeps track of how many rows have been revealed so far
# and which month is currently active so we can detect when the user switches
if "loaded_month" not in st.session_state:
    st.session_state.loaded_month = selected_month

if "live_row_count" not in st.session_state:
    st.session_state.live_row_count = START_ROWS

if "last_refresh_count" not in st.session_state:
    st.session_state.last_refresh_count = refresh_count

# When the user picks a different month, reset the row counter back to the start
if st.session_state.loaded_month != selected_month:
    st.session_state.loaded_month = selected_month
    st.session_state.live_row_count = START_ROWS
    st.session_state.last_refresh_count = refresh_count

# Each time the 10-second autorefresh fires, reveal the next batch of rows
if refresh_count != st.session_state.last_refresh_count:
    st.session_state.last_refresh_count = refresh_count
    st.session_state.live_row_count = min(
        st.session_state.live_row_count + ROWS_PER_BATCH,
        MAX_ROWS
    )

# Slice the full month dataframe down to however many rows are currently live
df = df_source.head(st.session_state.live_row_count).copy()

st.sidebar.caption(
    f"Fast month-tab loading<br>"
    f"Live: **{st.session_state.live_row_count:,}** of **{MAX_ROWS:,}** records loaded",
    unsafe_allow_html=True
)

if df.empty:
    st.error("No data loaded. Check your published Google Sheet month tabs.")
    st.stop()

# Build the dropdown options from whatever values exist in the live data slice
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

selected_country = st.sidebar.selectbox("Country", countries_list)
selected_service = st.sidebar.selectbox("Service category", services_list)
selected_campaign = st.sidebar.selectbox("Campaign source", campaign_list)

# Apply each active filter in turn to produce the final subset used by all charts
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

# KPI calculations — each metric is derived from the filtered dataframe
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

# Lowercase the interaction type column once so all keyword searches are consistent
interaction_series = (
    filtered_df["interaction_type"].astype(str).str.lower()
    if "interaction_type" in filtered_df.columns
    else pd.Series([], dtype="object")
)

demo_requests = interaction_series.str.contains("demo", na=False).sum()
ai_requests = interaction_series.str.contains("ai advisory|advisory", na=False).sum()
event_interest = interaction_series.str.contains("event", na=False).sum()

service_requests = interaction_series.str.contains(
    "request|enquiry|interest|consultation", na=False
).sum()

# Aggregations that power the charts below
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

# Campaign conversion table: total visits and total conversions grouped by source
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

# Daily event counts used by the activity trend line chart
trend_df = pd.DataFrame(columns=["date", "count"])

if "datetime" in filtered_df.columns and filtered_df["datetime"].notna().any():
    trend_df = (
        filtered_df
        .groupby(filtered_df["datetime"].dt.date)
        .size()
        .reset_index(name="count")
    )
    trend_df.columns = ["date", "count"]

interaction_mix = pd.DataFrame(columns=["interaction_type", "count"])

if "interaction_type" in filtered_df.columns:
    interaction_mix = (
        filtered_df["interaction_type"]
        .value_counts()
        .head(7)
        .reset_index()
    )
    interaction_mix.columns = ["interaction_type", "count"]

device_counts = pd.DataFrame(columns=["device_type", "count"])

if "device_type" in filtered_df.columns:
    device_counts = filtered_df["device_type"].value_counts().reset_index()
    device_counts.columns = ["device_type", "count"]

# Shared Plotly layout dictionary applied to every chart so they all look consistent
BASE = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color=TEXT_MAIN, size=12),
    margin=dict(l=8, r=8, t=20, b=8),
    xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=TEXT_MAIN)),
    yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=TEXT_MAIN)),
)

# Page header and subtitle showing which month is currently selected
st.title("CyberNova Analytics")

st.markdown(
    f'<div style="font-size:1rem;color:{TEXT_MUTED};margin-bottom:0.5rem;">'
    f'Live Web Activity and Customer Demand Intelligence — {selected_month}</div>',
    unsafe_allow_html=True
)

# Five KPI cards across the top of the page.
# The conversion rate card uses the accent colour to draw attention to it.
c1, c2, c3, c4, c5 = st.columns(5)

kpi_items = [
    (c1, "Total Visits", f"{total_visits:,}", "Live web activity", False),
    (c2, "Unique Visitors", f"{unique_visitors:,}", "Distinct IPs", False),
    (c3, "Conversion Rate", f"{conversion_rate:.1f}%", f"{conversions:,} conversions", True),
    (c4, "Demo Requests", f"{demo_requests:,}", "High-intent signals", False),
    (c5, "AI Advisory Requests", f"{ai_requests:,}", "Advisory engagement", False),
]

for col, label, value, sub, accent in kpi_items:
    cls = "kpi kpi-accent" if accent else "kpi"
    col.markdown(
        f'<div class="{cls}"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True
    )

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# Secondary row of supporting metrics below the main KPI cards
s1, s2, s3, s4 = st.columns(4)

s1.metric("Event Interest", f"{event_interest:,}")
s2.metric("Total Service Reqs", f"{service_requests:,}")
s3.metric("Conversions", f"{conversions:,}")
s4.metric("Device Types", f"{device_counts['device_type'].nunique() if not device_counts.empty else 0}")

st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

# Row 1: horizontal bar chart showing which services get the most requests (left)
# and a line chart showing how many events happened each day of the month (right)
left, right = st.columns(2)

with left.container(border=True):
    st.subheader("Service Demand")
    st.markdown(
        '<div class="section-caption">Most requested services in the selected month.</div>',
        unsafe_allow_html=True
    )

    if not service_counts.empty:
        s = service_counts.sort_values("count")

        fig = go.Figure(go.Bar(
            x=s["count"],
            y=s["service_category"],
            orientation="h",
            marker=dict(
                color=s["count"],
                colorscale=[[0, ACCENT_SOFT], [1, ACCENT]],
                showscale=False
            ),
            marker_line_width=0,
            hovertemplate="%{y}: %{x:,}<extra></extra>"
        ))

        fig.update_layout(**BASE, xaxis_title="Requests", height=340)
        st.plotly_chart(fig, use_container_width=True)

with right.container(border=True):
    st.subheader("Website Activity Over Time")
    st.markdown(
        '<div class="section-caption">Daily event volume for the selected month.</div>',
        unsafe_allow_html=True
    )

    if not trend_df.empty:
        fig = go.Figure(go.Scatter(
            x=trend_df["date"],
            y=trend_df["count"],
            mode="lines+markers",
            line=dict(color=ACCENT, width=2.5),
            marker=dict(size=4, color=ACCENT),
            fill="tozeroy",
            fillcolor=ACCENT_SOFT,
            hovertemplate="%{x|%d %b}: %{y:,} events<extra></extra>"
        ))

        fig.update_layout(**BASE, xaxis_title="Date", yaxis_title="Events", height=340)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

# Row 2: bar chart of traffic by country (left) and an overlaid bar chart
# comparing total visits against conversions for each marketing channel (right)
left2, right2 = st.columns(2)

with left2.container(border=True):
    st.subheader("Regional Demand")
    st.markdown(
        '<div class="section-caption">Traffic by country in the selected month.</div>',
        unsafe_allow_html=True
    )

    if not country_counts.empty:
        fig = go.Figure(go.Bar(
            x=country_counts["country"],
            y=country_counts["count"],
            marker=dict(
                color=country_counts["count"],
                colorscale=[[0, ACCENT_SOFT], [1, ACCENT]],
                showscale=False
            ),
            marker_line_width=0,
            hovertemplate="%{x}: %{y:,}<extra></extra>"
        ))

        fig.update_layout(**BASE, xaxis_title="Country", yaxis_title="Visits", height=340)
        st.plotly_chart(fig, use_container_width=True)

with right2.container(border=True):
    st.subheader("Marketing Channel Effectiveness")
    st.markdown(
        '<div class="section-caption">Total visits vs conversions per campaign source.</div>',
        unsafe_allow_html=True
    )

    if not campaign_conv.empty:
        c = campaign_conv.sort_values("conv_rate", ascending=True)

        fig = go.Figure()

        # The faded background bars represent total visit volume per channel
        fig.add_trace(go.Bar(
            x=c["total"],
            y=c["campaign_source"],
            orientation="h",
            name="Total Visits",
            marker_color=ACCENT_SOFT,
            marker_line_width=0,
            hovertemplate="%{y} visits: %{x:,}<extra></extra>"
        ))

        # The solid foreground bars show how many of those visits converted
        fig.add_trace(go.Bar(
            x=c["conversions"],
            y=c["campaign_source"],
            orientation="h",
            name="Conversions",
            marker_color=ACCENT,
            marker_line_width=0,
            hovertemplate="%{y} conversions: %{x:,}<extra></extra>"
        ))

        fig.update_layout(
            **BASE,
            barmode="overlay",
            xaxis_title="Count",
            height=340,
            legend=dict(orientation="h", y=1.08, x=0, font=dict(color=TEXT_MAIN))
        )

        st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

# Row 3: horizontal bar chart of what users are doing on the site (left)
# and a donut chart showing the Desktop / Mobile / Tablet split (right)
left3, right3 = st.columns(2)

with left3.container(border=True):
    st.subheader("Interaction Mix")
    st.markdown(
        '<div class="section-caption">What users are doing on the site.</div>',
        unsafe_allow_html=True
    )

    if not interaction_mix.empty:
        m = interaction_mix.sort_values("count")

        fig = go.Figure(go.Bar(
            x=m["count"],
            y=m["interaction_type"],
            orientation="h",
            marker=dict(color=ACCENT, line_width=0),
            hovertemplate="%{y}: %{x:,}<extra></extra>"
        ))

        fig.update_layout(**BASE, xaxis_title="Count", height=300)
        st.plotly_chart(fig, use_container_width=True)

with right3.container(border=True):
    st.subheader("Device Breakdown")
    st.markdown(
        '<div class="section-caption">How visitors are accessing the site.</div>',
        unsafe_allow_html=True
    )

    if not device_counts.empty:
        # Three colours cover the three device categories
        colors = [ACCENT, ACCENT_SOFT, TEXT_MUTED]

        fig = go.Figure(go.Pie(
            labels=device_counts["device_type"],
            values=device_counts["count"],
            marker=dict(
                colors=colors[:len(device_counts)],
                line=dict(color="rgba(0,0,0,0)", width=0)
            ),
            hole=0.52,
            hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>",
            textfont=dict(color=TEXT_MAIN)
        ))

        fig.update_layout(
            **BASE,
            height=300,
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.1,
                x=0.5,
                xanchor="center",
                font=dict(color=TEXT_MAIN)
            )
        )

        st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

# Pull the top values from each aggregation to use in the insight text below
top_service = service_counts.iloc[0]["service_category"] if not service_counts.empty else "N/A"
top_service_count = int(service_counts.iloc[0]["count"]) if not service_counts.empty else 0

top_country = country_counts.iloc[0]["country"] if not country_counts.empty else "N/A"
top_country_count = int(country_counts.iloc[0]["count"]) if not country_counts.empty else 0

# Find which marketing channel has the highest conversion rate
best_channel = ""

if not campaign_conv.empty:
    best_row = campaign_conv.loc[campaign_conv["conv_rate"].idxmax()]
    best_channel = (
        f"<strong>{best_row['campaign_source']}</strong> leads with a "
        f"<strong>{best_row['conv_rate']:.1f}%</strong> conversion rate "
        f"({int(best_row['conversions'])} conversions from {int(best_row['total'])} visits)"
    )

# Business insights section — plain English summary of what the data is showing.
# Each insight card is generated dynamically from the filtered data so it always
# reflects the current month and filter selection.
with st.container(border=True):
    st.subheader("Business Insights")
    st.markdown(
        f'<div class="section-caption">Interpretation of the current filtered view for {selected_month}.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="insight"><p><strong>{top_service}</strong> generated the highest customer '
        f'activity with <strong>{top_service_count:,}</strong> interactions. '
        f'It is currently the strongest entry point into the service funnel.</p></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="insight"><p><strong>{top_country}</strong> is the top traffic source with '
        f'<strong>{top_country_count:,}</strong> visits, making it the most immediate market '
        f'opportunity in this period.</p></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="insight"><p>The conversion rate is <strong>{conversion_rate:.1f}%</strong>. '
        f'<strong>{conversions:,}</strong> of {total_visits:,} interactions resulted in a '
        f'commercially relevant action such as a demo request or advisory engagement.</p></div>',
        unsafe_allow_html=True
    )

    if best_channel:
        st.markdown(
            f'<div class="insight"><p>Among marketing channels, {best_channel}. '
            f'This channel should be prioritised in budget allocation.</p></div>',
            unsafe_allow_html=True
        )

    if demo_requests > 0:
        st.markdown(
            f'<div class="insight"><p><strong>{demo_requests:,}</strong> demo requests were recorded '
            f'in this period. These are high-intent leads and should be followed up by the sales '
            f'team promptly.</p></div>',
            unsafe_allow_html=True
        )

# Table showing the 25 most recent interactions from the filtered data
display_cols = [
    c for c in [
        "datetime", "country", "resource", "service_category",
        "interaction_type", "is_conversion", "status_code",
        "campaign_source", "device_type"
    ]
    if c in filtered_df.columns
]

with st.container(border=True):
    st.subheader("Recent Website Activity")
    st.markdown(
        '<div class="section-caption">Last 25 interactions in the filtered view.</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        filtered_df.sort_values("datetime", ascending=False)[display_cols].head(25),
        use_container_width=True,
        height=340,
        hide_index=True
    )