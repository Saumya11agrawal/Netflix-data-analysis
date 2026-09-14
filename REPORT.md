# Netflix Data Analysis Report

## Executive conclusion

This analysis describes a historical snapshot of 6,234 Netflix titles. Movies represent 4,265 titles, while TV shows represent 1,969 titles. The catalog is strongly international: the most frequent primary-country label is the United States, followed by India and the United Kingdom. International Movies and Dramas are the most common genre labels. TV-MA and TV-14 are the dominant content ratings. Among movies with a usable duration value, the median length is 98 minutes.

These findings are descriptive. The dataset is a catalog snapshot rather than a live Netflix feed, and the analysis does not establish why titles were added, removed, or distributed across countries and genres.

## Dataset and method

The project uses the public `netflix_titles.csv` dataset, which contains title metadata such as format, title, country, date added, release year, rating, duration, and genre tags. The cleaning pipeline parses dates, extracts numeric movie duration, derives the first listed country as `primary_country`, and splits multi-valued genre strings for frequency analysis. Missing values remain visible in the data-quality review.

The analysis uses Python with Pandas for tabular transformation, NumPy for numerical handling, Matplotlib and Seaborn for visualization, and Jupyter Notebook for interactive exploration. The production script saves every chart as a PNG and every summary table as a CSV so the report can be regenerated without manual edits.

## Key results

| Measure | Result |
|---|---:|
| Total titles | 6,234 |
| Movies | 4,265 |
| TV shows | 1,969 |
| Titles with a parsed date added | 5,583 |
| Median movie duration | 98 minutes |
| Median release year | 2016 |

### Format mix

Movies account for approximately 68.4% of the snapshot, compared with approximately 31.6% for TV shows. This imbalance matters when comparing genre and rating counts because the catalog contains substantially more movie records.

![Format mix](outputs/figures/01_format_mix.png)

### Release trends

The release-year chart shows the concentration of titles in more recent years. Release year is the original release year, not the date when a title appeared on Netflix. Therefore, the chart should be interpreted as catalog composition by title vintage rather than as a direct measure of Netflix production output.

![Release trend](outputs/figures/02_release_trend.png)

### Genre popularity

The most frequent genre labels are International Movies, Dramas, Comedies, and International TV Shows. International Movies appear 1,927 times and Dramas appear 1,623 times. Because a title can carry multiple genre labels, these counts are not mutually exclusive and should not be summed as if each title belonged to one category only.

![Top genres](outputs/figures/03_top_genres.png)

### Ratings distribution

TV-MA is the most common rating with 2,027 titles, followed by TV-14 with 1,698 titles. The result indicates that mature and teen-oriented classifications are prominent in this snapshot. Ratings are not a normalized measure of quality; they are content classifications.

![Ratings](outputs/figures/04_ratings.png)

### Country-wise insights

The United States is the leading primary-country label with 2,302 titles, followed by India with 808 and the United Kingdom with 483. The `primary_country` field uses only the first country listed in a multi-country string. This is a deliberate simplification for comparison and does not mean that co-production countries are excluded from the raw data.

![Countries](outputs/figures/05_countries.png)

### Movie duration

The median movie duration is 98 minutes. The histogram indicates a broad distribution around feature-length formats, with a smaller number of unusually short and unusually long titles. The duration field is parsed only for movies with a numeric minute value.

![Movie duration](outputs/figures/06_movie_duration.png)

## Limitations

The dataset is a historical snapshot and does not represent current availability in a particular country. Genre and country values are multi-valued, so single-label summaries simplify the underlying metadata. Date coverage is incomplete for 651 records. The analysis is exploratory and does not include causal inference, user engagement, ratings from viewers, or revenue data.

## Reproduction

From the project root, run:

```bash
bash fetch_dataset.sh
python3 src/analyze_netflix.py
```

The interactive version is available at `notebooks/netflix_analysis.ipynb`. The generated tables are stored in `outputs/` and the charts are stored in `outputs/figures/`.

## References

[1]: https://www.kaggle.com/datasets/shivamb/netflix-shows "Netflix Movies and TV Shows dataset"

[2]: https://github.com/prasertcbs/basic-dataset/blob/master/netflix_titles.csv "Public CSV mirror of Netflix titles data"
