# Nassau Candy Distributor — Profitability Analysis

## Project Overview
A comprehensive data analytics project analyzing profitability across 10,194 order records for Nassau Candy Distributor.

## Live Dashboard
[Click here to view the live Streamlit dashboard](https://nassau-candy-profitability.streamlit.app)

## What this project covers
- Product-level profitability analysis across 13 products
- Division performance comparison (Chocolate, Sugar, Other)
- Regional sales analysis (Pacific, Atlantic, Interior, Gulf)
- Pareto 80/20 revenue concentration analysis
- Cost diagnostics and margin risk flagging
- Interactive executive summary for stakeholders

## Key Findings
1. Chocolate division generates 92.9% of total revenue — concentration risk
2. Sugar division has 66.6% margin but only 0.3% revenue — hidden opportunity
3. Other division margin of 44.8% is 23 points below Chocolate
4. Just 5 products generate 88% of all company revenue

## Tools Used
- WPS Spreadsheets — data cleaning and KPI calculation
- SQL — data querying and aggregation
- Power BI — interactive dashboard (4 pages)
- Python / Streamlit — web application deployment
- Plotly — interactive charts

## Files in this repository
- `app.py` — Streamlit web application
- `requirements.txt` — Python dependencies
- `Nassau_Candy_Distributor.csv` — dataset (upload this too)
- `Nassau_Candy_Research_Paper.pdf` — full research paper
- `Nassau_Candy_Executive_Summary.pdf` — executive summary
- `Nassau_Candy_Dashboard.pdf` — Power BI dashboard export

## How to run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Prepared by
Khushi | Data Analytics Project | May 2026
