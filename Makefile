STATES = AL AK AS AZ AR CA CO CT DE DC FM FL GA GU HI ID IL IN IA KS KY LA ME MH MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND MP OH OK OR PW PA PR RI SC SD TN TX UT VT VI VA WA WV WI WY

consistent/postoffices.geojson: consistent/postoffices-reliably-geocoded.csv
	cat $^ | csvjson --lat PRIM_LAT_DEC --lon PRIM_LONG_DEC > $@
consistent/postoffices-reliably-geocoded.csv: $(foreach state,$(STATES),consistent/postoffices-geocoded.$(state).csv)
	csvstack $^ | csvgrep -c _score -r "^\d{2}\." | csvgrep -c PRIM_LAT_DEC -r "^0$$" -i > $@
consistent/postoffices-geocoded.%.csv: consistent/postoffices.%.csv geocode.py
	python geocode.py < $< > $@
consistent/postoffices.%.csv: raw/postalhistory.%.txt clean.py
	python clean.py < $< > $@
raw/postalhistory.%.txt: scrape.py
	python scrape.py $(subst ., ,$(suffix $(basename $(notdir $@)))) > $@

install:
	sudo pip install unicodecsv
	sudo pip install geojson
