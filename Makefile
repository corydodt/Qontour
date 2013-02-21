all:
	#

clean:
	python -c 'from pymongo import MongoClient as MC; MC().drop_database("thumbs")'

development:
	virtualenv --relocatable .
	. bin/activate; python setup.py install
