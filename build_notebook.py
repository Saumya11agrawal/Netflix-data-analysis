import json
from pathlib import Path

def md(s): return {'cell_type':'markdown','metadata':{},'source':s.splitlines(True)}
def code(s): return {'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':s.splitlines(True)}

cells=[
md('# Netflix Data Analysis\n\nA reproducible exploratory data analysis of Netflix movies and TV shows. This notebook covers data quality, catalog composition, release trends, genre popularity, ratings, movie duration, and country-wise insights.'),
md('## 1. Setup and data loading\n\nThe source file is expected at `../data/netflix_titles.csv`. Run `../fetch_dataset.sh` first if the file is not present.'),
code("from pathlib import Path\nimport sys\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nROOT = Path.cwd().parent\nsys.path.append(str(ROOT / 'src'))\nfrom analyze_netflix import load_and_clean, run\n\nsns.set_theme(style='whitegrid', context='notebook')\ndf = load_and_clean(ROOT / 'data' / 'netflix_titles.csv')\ndf.head()"),
md('## 2. Data quality and structure'),
code("print('Shape:', df.shape)\ndisplay(df.dtypes.to_frame('dtype'))\ndisplay(df.isna().sum().sort_values(ascending=False).to_frame('missing_values'))"),
md('The dataset contains both single-value and multi-value fields. The analysis keeps the raw fields and derives `primary_country` and `genre` for straightforward frequency comparisons. Missing dates and ratings are retained as unknown rather than silently discarded.'),
md('## 3. Catalog composition'),
code("display(df['type'].value_counts().rename_axis('type').to_frame('titles'))\nsns.countplot(data=df, x='type', palette={'Movie':'#e50914','TV Show':'#221f1f'})\nplt.title('Netflix catalog mix by format', weight='bold')\nplt.xlabel('Format'); plt.ylabel('Titles'); plt.show()"),
md('## 4. Release trends'),
code("trend = df.groupby(['release_year','type']).size().unstack(fill_value=0)\ntrend.tail(40).plot(figsize=(11,5), marker='o', color=['#e50914','#221f1f'])\nplt.title('Recent catalog releases by format', weight='bold')\nplt.xlabel('Release year'); plt.ylabel('Titles'); plt.show()"),
md('## 5. Genre popularity'),
code("genre_counts = df['listed_in'].dropna().str.split(', ').explode().value_counts()\ndisplay(genre_counts.head(15).to_frame('titles'))\ngenre_counts.head(12).sort_values().plot.barh(figsize=(10,6), color='#b20710')\nplt.title('Most common Netflix genres', weight='bold'); plt.xlabel('Titles'); plt.show()"),
md('## 6. Ratings distribution'),
code("rating_counts = df['rating'].value_counts()\ndisplay(rating_counts.to_frame('titles'))\nrating_counts.head(12).sort_values().plot.barh(figsize=(10,6), color='#564d4d')\nplt.title('Content rating distribution', weight='bold'); plt.xlabel('Titles'); plt.show()"),
md('## 7. Country-wise insights'),
code("country_counts = df['primary_country'].replace('Unknown', np.nan).dropna().value_counts()\ndisplay(country_counts.head(15).to_frame('titles'))\ncountry_counts.head(12).sort_values().plot.barh(figsize=(10,6), color='#e87c03')\nplt.title('Leading countries by title count', weight='bold'); plt.xlabel('Titles'); plt.show()"),
md('## 8. Movie duration'),
code("movies = df.loc[df['type'].eq('Movie') & df['duration_num'].notna()]\nprint('Median movie duration:', movies['duration_num'].median(), 'minutes')\nsns.histplot(movies['duration_num'], bins=30, kde=True, color='#e50914')\nplt.axvline(movies['duration_num'].median(), color='#221f1f', linestyle='--', label='Median')\nplt.title('Movie duration distribution', weight='bold'); plt.xlabel('Minutes'); plt.legend(); plt.show()"),
md('## 9. Reproduce all portfolio outputs\n\nThe production script writes all charts and summary CSV files to `../outputs/`. This keeps the notebook exploratory while making the final artifacts reproducible from a single command.'),
code("summary = run(df)\ndisplay(summary)"),
md('## Conclusion\n\nThis snapshot is dominated by movies, with international movies and dramas forming the largest genre groupings. TV-MA and TV-14 are the most frequent ratings, while the United States and India are the leading primary-country labels. The median movie duration is 98 minutes. These are descriptive results from a historical catalog snapshot, not current availability or causal conclusions.')
]
out={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'}},'nbformat':4,'nbformat_minor':5}
Path('/home/ubuntu/netflix-data-analysis/notebooks/netflix_analysis.ipynb').write_text(json.dumps(out, indent=2))
print('Notebook created')
