consistent/postoffices.geojson: consistent/postoffices-reliably-geocoded.csv
	cat $^ | csvjson --lat PRIM_LAT_DEC --lon PRIM_LONG_DEC > $@
consistent/postoffices-reliably-geocoded.csv: consistent/postoffices-geocoded.csv
	cat $^ | csvgrep -c _score -r "^\d{2}\." | csvgrep -c PRIM_LAT_DEC -r "^0$$" -i > $@
consistent/postoffices-geocoded.csv: consistent/postoffices.csv geocode.py
	python geocode.py < consistent/postoffices.csv > $@
consistent/postoffices.csv: raw/postalhistory.txt clean.py
	python clean.py < raw/postalhistory.txt > $@
raw/postalhistory.txt: scrape.py
	python scrape.py > $@

install:
	sudo pip install unicodecsv
	sudo pip install geojson
