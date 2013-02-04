all:
	#

clean:
	python -c 'from pymongo import MongoClient as MC; MC().drop_database("thumbs")'
