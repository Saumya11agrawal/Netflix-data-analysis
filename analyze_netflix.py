from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'netflix_titles.csv'
OUT = ROOT / 'outputs'
FIG = OUT / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

sns.set_theme(style='whitegrid', context='notebook')
PALETTE = {'Movie':'#e50914', 'TV Show':'#221f1f'}


def load_and_clean(path=DATA):
    df = pd.read_csv(path)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month_name()
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    df['duration_num'] = pd.to_numeric(df['duration'].str.extract(r'(\d+)')[0], errors='coerce')
    df['primary_country'] = df['country'].fillna('Unknown').str.split(',').str[0].str.strip()
    df['genre'] = df['listed_in'].fillna('Unknown').str.split(',').str[0].str.strip()
    df['rating'] = df['rating'].fillna('Unknown')
    return df


def save_bar(series, title, xlabel, filename, color='#e50914', horizontal=False):
    fig, ax = plt.subplots(figsize=(10, 6))
    if horizontal:
        series.sort_values().plot.barh(ax=ax, color=color)
    else:
        series.plot.bar(ax=ax, color=color)
        ax.tick_params(axis='x', rotation=35)
    ax.set_title(title, fontsize=16, weight='bold', pad=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('')
    fig.tight_layout()
    fig.savefig(FIG / filename, dpi=180, bbox_inches='tight')
    plt.close(fig)


def run(df):
    # 1. Format mix
    type_counts = df['type'].value_counts()
    save_bar(type_counts, 'Netflix catalog mix by format', 'Number of titles', '01_format_mix.png', horizontal=True)

    # 2. Release-year trend
    yearly = df.groupby(['release_year', 'type']).size().unstack(fill_value=0).tail(40)
    fig, ax = plt.subplots(figsize=(11, 6))
    for col in ['Movie', 'TV Show']:
        if col in yearly: ax.plot(yearly.index, yearly[col], marker='o', linewidth=2, label=col, color=PALETTE[col])
    ax.set_title('Recent catalog releases by format', fontsize=16, weight='bold', pad=14)
    ax.set_xlabel('Release year'); ax.set_ylabel('Titles'); ax.legend(frameon=True)
    fig.tight_layout(); fig.savefig(FIG / '02_release_trend.png', dpi=180, bbox_inches='tight'); plt.close(fig)

    # 3. Genre popularity
    genres = df['listed_in'].dropna().str.split(', ').explode().value_counts().head(12).sort_values()
    save_bar(genres, 'Most common Netflix genres', 'Number of titles', '03_top_genres.png', color='#b20710', horizontal=True)

    # 4. Rating distribution
    ratings = df['rating'].value_counts().head(12).sort_values()
    save_bar(ratings, 'Content rating distribution', 'Number of titles', '04_ratings.png', color='#564d4d', horizontal=True)

    # 5. Country insights
    countries = df['primary_country'].replace('Unknown', np.nan).dropna().value_counts().head(12).sort_values()
    save_bar(countries, 'Leading countries by title count', 'Number of titles', '05_countries.png', color='#e87c03', horizontal=True)

    # 6. Movie duration
    movies = df.loc[df['type'].eq('Movie') & df['duration_num'].notna()]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(movies['duration_num'], bins=30, kde=True, color='#e50914', ax=ax)
    ax.axvline(movies['duration_num'].median(), color='#221f1f', linestyle='--', label=f"Median: {movies['duration_num'].median():.0f} min")
    ax.set_title('Movie duration distribution', fontsize=16, weight='bold', pad=14)
    ax.set_xlabel('Duration (minutes)'); ax.set_ylabel('Movies'); ax.legend()
    fig.tight_layout(); fig.savefig(FIG / '06_movie_duration.png', dpi=180, bbox_inches='tight'); plt.close(fig)

    # Summary tables for reproducibility
    summary = pd.DataFrame({
        'metric': ['total_titles','movies','tv_shows','date_added_coverage','median_movie_minutes','median_release_year'],
        'value': [len(df), int((df.type=='Movie').sum()), int((df.type=='TV Show').sum()), int(df.date_added.notna().sum()), float(movies.duration_num.median()), float(df.release_year.median())]
    })
    summary.to_csv(OUT / 'summary_metrics.csv', index=False)
    genres.rename_axis('genre').reset_index(name='titles').to_csv(OUT / 'top_genres.csv', index=False)
    countries.rename_axis('country').reset_index(name='titles').to_csv(OUT / 'top_countries.csv', index=False)
    ratings.rename_axis('rating').reset_index(name='titles').to_csv(OUT / 'rating_counts.csv', index=False)
    return summary


if __name__ == '__main__':
    df = load_and_clean()
    summary = run(df)
    print(summary.to_string(index=False))
