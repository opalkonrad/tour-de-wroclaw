# tour-de-wroclaw

## Local setup

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Testing
```shell
pytest tests/
```

## Running

There are several scripts and notebook here which sums to complete analysis

### Preparing data

```shell
python src/prepare_data.py  --osm-lines="data/lines.shp" --osm-points="data/points.shp" \
 --bike-paths="data/TrasyRowerowe/TrasyRowerowe.shp" --output="datatest/" --merge-attraction
```
### Calculating paths and saving them to json
```shell
python src/calculate_paths.py --attractions="data/attractions.pickle" --roads="data/roads_w_attractions.pickle" \
 --bike-paths="data/bikepaths_w_attractions.pickle" --output="out"
```

### Converting results to shapefiles
```shell
jupyter notebook
```
then use code in Report.ipynb

Data is not delivered with this repository
