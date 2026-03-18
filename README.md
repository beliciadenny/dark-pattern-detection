# 🕵️ Dark Pattern Detection

Detects manipulative UI patterns across e-commerce websites using machine learning and NLP, maps findings to EU DSA & FTC regulations, and visualises results in Power BI.

## What it does
- Scrapes UI text from 15 Indian & global e-commerce sites using Playwright
- Classifies 6 dark pattern types using XGBoost + TF-IDF features
- Maps each finding to EU DSA / FTC regulation clauses
- Generates before/after remediation suggestions
- Exports findings to a 3-page Power BI dashboard

## Tech Stack
Python · Playwright · XGBoost · SHAP · TF-IDF · Pandas · Matplotlib · Power BI

## Results
- 1,077 UI texts scraped across 15 sites
- 50 dark pattern instances detected
- 6 pattern types classified
- Macro F1 score: 0.87

## Run it
```bash
pip install -r requirements.txt
playwright install chromium
jupyter notebook notebook/dark_pattern_detection_v3.ipynb
```

## Dashboard
See `dashboard/dark_pattern_dashboard.pdf` for the full Power BI report.
