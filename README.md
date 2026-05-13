# CyberNova Analytics Dashboard

Live web analytics and business intelligence dashboard — built for CET333 Product Development, University of Sunderland.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)
![Deployed on Streamlit](https://img.shields.io/badge/Deployed%20on-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

&nbsp;

## What is this?

CyberNova Analytics Dashboard is a real-time web intelligence platform that transforms raw web server log data into business insights. It was built for CyberNova Analytics Ltd, a fictional technology company, and demonstrates how data engineering, visualisation, and product thinking come together in a deployable application.

The dashboard answers questions like:

- Which services are customers actually requesting?
- Which countries are driving the most traffic?
- Which marketing channels are converting, and which are wasting budget?
- Is web activity growing or declining over the month?

Everything updates in real time. Every chart, every KPI, every insight card responds to whatever month and filters you have selected.

&nbsp;

## Live Demo

Deployed on Streamlit Community Cloud — no installation needed to view it.

```
https://cybernova-analytics-dashboard.streamlit.app
```

&nbsp;

## Features

**Real-time simulation**
Data loads incrementally every 10 seconds, replicating the feel of live web traffic arriving. Once the end of the dataset is reached the simulation loops, so the dashboard stays active through an entire presentation without freezing.

**Month-by-month navigation**
The full dataset spans January to December 2026 across 285,000+ rows. Instead of loading everything at once, each month lives in its own published Google Sheets tab and is fetched on demand. Switching months is fast.

**Filters that actually work**
Country, service category, and campaign source filters apply simultaneously across every KPI and chart on the page. Nothing is static.

**Business insights in plain English**
Below the charts, the dashboard generates a written summary of what the data is actually saying — top service, top region, best-converting channel, demo request volume — all derived live from the filtered data.

**Dark mode and light mode**
Full theme support. Every chart, card, sidebar, and dropdown switches cleanly between both.

&nbsp;

## Dashboard Sections

| Section | Description |
| --- | --- |
| KPI Cards | Total visits, unique visitors, conversion rate, demo requests, AI advisory requests |
| Service Demand | Horizontal bar chart ranking services by request volume |
| Website Activity Over Time | Daily event count trend across the selected month |
| Regional Demand | Visits broken down by country |
| Marketing Channel Effectiveness | Total visits vs conversions per campaign source, overlaid |
| Interaction Mix | What users are actually doing on the site |
| Device Breakdown | Desktop, Mobile, and Tablet split as a donut chart |
| Business Insights | Auto-generated plain-English summary of the current filtered view |
| Recent Activity | Live table of the 25 most recent interactions |

&nbsp;

## Data

The dataset simulates IIS-format web server logs. Each row is one web interaction.

| Column | Description |
| --- | --- |
| `date` | Request date in dd/mm/yyyy format |
| `time` | Request time |
| `ip_address` | Client IP, used to count unique visitors |
| `method` | HTTP method, GET or POST |
| `resource` | Page or endpoint accessed |
| `status_code` | HTTP response code |
| `country` | Country of origin |
| `service_category` | Which CyberNova service the interaction relates to |
| `interaction_type` | Nature of the interaction, Demo Request, Page Visit, etc. |
| `is_conversion` | Whether the visit converted, Yes or No |
| `campaign_source` | Marketing channel that drove the visit |
| `device_type` | Desktop, Mobile, or Tablet |
| `response_group` | Grouped outcome, Successful, Client Error, etc. |

Total dataset: approximately **285,000 rows** across 12 months, partitioned into one Google Sheets tab per month.

&nbsp;

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) Python 3 |
| Framework | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) Streamlit |
| Data processing | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) Pandas |
| Visualisation | ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white) Plotly |
| Data storage | ![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=flat-square&logo=google-sheets&logoColor=white) Google Sheets CSV API |

&nbsp;

## Getting Started

**Clone the repo**

```bash
git clone https://github.com/ofilemfetane10/cybernova-analytics-dashboard.git
cd cybernova-analytics-dashboard
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Run locally**

```bash
python -m streamlit run app.py
```

Opens at `http://localhost:8501`.

&nbsp;

## Project Structure

```
cybernova-analytics-dashboard/
│
├── app.py               Main dashboard, all logic and UI
├── requirements.txt     Python dependencies
└── README.md            You are here
```

&nbsp;

## Design Decisions

**Monthly partitioning over a single dataset**
Loading 285,000 rows in one request is slow and unnecessary when the user only ever looks at one month at a time. Splitting into twelve tabs and fetching on demand keeps each load to 18,000 to 28,000 rows, which is fast enough to feel instant.

**Looping simulation instead of a static snapshot**
Revealing data in batches simulates what a real analytics system looks like when events arrive continuously. The loop means the dashboard never freezes mid-presentation, which matters when you are demoing live.

**Google Sheets as the data layer**
No database to set up, no server to maintain. Publishing each tab as a CSV means the app fetches data with a single HTTP call, and Streamlit's caching means re-visiting the same month costs nothing after the first load.

&nbsp;

## Academic Context

```
Module       CET333 Product Development
Institution  University of Sunderland
```

This project demonstrates requirements analysis and solution design, scalable data architecture for large datasets, interactive visualisation for business decision-making, and end-to-end deployment of a data product.

*CyberNova Analytics Dashboard — CET333 Product Development*
