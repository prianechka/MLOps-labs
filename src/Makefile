start-env:
	sudo python3 -m venv .venv
	. .venv/bin/activate

install-libs:
	pip install -r requirements.txt

init-db:
	flask --app heart_diseases_detector init-db

run-debug:
	flask --app heart_diseases_detector run --debug

build-run-docker:
	docker compose down --volumes
	BUILDKIT_PROGRESS=plain docker compose up --build -d

run-docker:
	docker compose down --volumes
	docker compose up