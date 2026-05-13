# CyberNova Analytics API
# This Flask API acts as the data access layer for the Streamlit dashboard.
# It reads monthly Google Sheets CSV partitions and exposes them as JSON endpoints.
# The dashboard can then consume this API instead of reading Google Sheets directly.

from flask import Flask, jsonify
import pandas as pd


# Create the Flask application.
app = Flask(__name__)


# Published Google Sheets CSV base URL.
# The gid value is replaced depending on the selected monthly partition.
BASE_MONTH_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRck5N3u4GpJFRIFRekZ-slAcRe68Fyz1Zmxgj3gMbvkMBb0HBUQ1DmGh12MvU3QWEAlxZ1_wFEzz1K"
    "/pub?gid={gid}&single=true&output=csv"
)


# Each month has its own Google Sheets tab.
# This matches the same monthly partition structure used by the dashboard.
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


# API home route.
# This confirms that the API is running and shows example endpoints.
@app.route("/")
def home():
    return jsonify({
        "message": "CyberNova API is running",
        "description": "This API provides monthly web log data for the CyberNova Streamlit dashboard.",
        "available_endpoints": [
            "/api/logs/2026-01",
            "/api/logs/2026-02",
            "/api/logs/2026-03",
            "/api/logs/2026-04",
            "/api/logs/2026-05",
            "/api/logs/2026-06",
            "/api/logs/2026-07",
            "/api/logs/2026-08",
            "/api/logs/2026-09",
            "/api/logs/2026-10",
            "/api/logs/2026-11",
            "/api/logs/2026-12",
            "/api/latest/2026-05"
        ]
    })


# Helper function to load a selected month from Google Sheets.
# Keeping this separate avoids repeating the same read_csv logic in every endpoint.
def load_month_dataframe(month: str) -> pd.DataFrame:
    if month not in MONTH_GIDS:
        return pd.DataFrame()

    url = BASE_MONTH_URL.format(gid=MONTH_GIDS[month])
    df = pd.read_csv(url, low_memory=False)

    return df


# Full monthly logs endpoint.
# Example: http://127.0.0.1:5000/api/logs/2026-05
@app.route("/api/logs/<month>")
def get_logs(month):
    if month not in MONTH_GIDS:
        return jsonify({
            "error": "Invalid month",
            "valid_months": list(MONTH_GIDS.keys())
        }), 400

    df = load_month_dataframe(month)

    return jsonify({
        "month": month,
        "record_count": len(df),
        "records": df.to_dict(orient="records")
    })


# Latest records endpoint.
# This is useful for a real-time-style dashboard view because it exposes only recent activity.
# Example: http://127.0.0.1:5000/api/latest/2026-05
@app.route("/api/latest/<month>")
def get_latest_logs(month):
    if month not in MONTH_GIDS:
        return jsonify({
            "error": "Invalid month",
            "valid_months": list(MONTH_GIDS.keys())
        }), 400

    df = load_month_dataframe(month)
    latest_df = df.tail(500)

    return jsonify({
        "month": month,
        "record_count": len(latest_df),
        "latest_records": latest_df.to_dict(orient="records")
    })


# Run the Flask API locally on port 5000.
# Keep this terminal open while the Streamlit dashboard is running.
if __name__ == "__main__":
    app.run(debug=True, port=5000)