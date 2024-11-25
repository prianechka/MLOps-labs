start-env:
	sudo python3 -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt

init-db:
	flask --app heart_diseases_detector init-db

run-debug:
	flask --app heart_diseases_detector run --debug