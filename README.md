# Netflix Data Analysis

A reproducible exploratory data analysis (EDA) project that examines Netflix movies and TV shows using **Python, Pandas, NumPy, Matplotlib, Seaborn, and Jupyter Notebook**. The analysis focuses on catalog composition, release trends, genre popularity, ratings, movie duration, and country-wise distribution.

## Project outcomes

The pipeline downloads a real public Netflix titles dataset, cleans semi-structured fields, generates six publication-ready charts, and writes summary tables for downstream reporting. The project is organized so that the analysis can be rerun after replacing the source CSV with a newer snapshot.

## Quick start

```bash
cd netflix-data-analysis
bash fetch_dataset.sh
python3 src/analyze_netflix.py
```

Generated artifacts are saved in `outputs/`, including:

| Artifact | Purpose |
|---|---|
| `outputs/figures/` | Six PNG visualizations for the report or portfolio |
| `outputs/summary_metrics.csv` | Core catalog metrics |
| `outputs/top_genres.csv` | Genre frequency table |
| `outputs/top_countries.csv` | Country frequency table |
| `outputs/rating_counts.csv` | Rating frequency table |
| `notebooks/netflix_analysis.ipynb` | Step-by-step notebook version |
| `REPORT.md` | Written findings and methodology |

## Dataset

The project uses the public `netflix_titles.csv` dataset, commonly distributed through the Kaggle **Netflix Movies and TV Shows** dataset. The CSV includes title identifiers, format, title, director, cast, country, date added, release year, rating, duration, and genre tags. Because the catalog snapshot is historical and the country and genre columns are multi-valued, findings should be interpreted as snapshot-level descriptive insights rather than current Netflix availability or causal claims.

## Portfolio summary

> **Netflix Data Analysis —** Analyzed a Netflix titles dataset with Python, Pandas, NumPy, Matplotlib, and Seaborn to identify content trends, genre popularity, ratings distribution, movie-length patterns, and country-wise insights. Built a reproducible EDA workflow and six visualizations to communicate findings clearly.

## Repository structure

```text
├── data/                       # downloaded source data
├── notebooks/                  # executable notebook
├── outputs/figures/            # generated charts
├── src/analyze_netflix.py      # reusable analysis pipeline
├── REPORT.md                   # written findings
├── requirements.txt
└── fetch_dataset.sh
```
