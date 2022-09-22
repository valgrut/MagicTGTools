install:
	pip install -r requirements.txt

run:
	python3 -m flask run

runserver: 
	#This will check the file for any changes automatically without need to restart server after every change.
	FLASK_ENV=development flask run

deploy:
	#deploy to web server

.PHONY: install run
