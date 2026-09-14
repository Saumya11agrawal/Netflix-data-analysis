#!/usr/bin/env bash
set -euo pipefail
curl -L --fail --silent --show-error \
  -o data/netflix_titles.csv \
  https://raw.githubusercontent.com/prasertcbs/basic-dataset/master/netflix_titles.csv
python3 - <<'PY'
import pandas as pd
p='data/netflix_titles.csv'
df=pd.read_csv(p)
print(f'Downloaded {len(df):,} rows and {len(df.columns)} columns')
print(', '.join(df.columns))
PY
