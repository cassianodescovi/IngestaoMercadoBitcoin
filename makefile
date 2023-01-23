clean:
	rm -rf day-summary *.checkpoints .pytest_cache .coverage

init: clean
	pip install poetry
	poetry init
	pre-commit install

test:
	poetry run python -m pytest

## CI/CD
ci-setup:
	pip install poetry
	poetry install

ci-test:
	poetry run python -m pytest

ci-deploy:
	poetry run zappa update $(stage) || poetry run zappa deploy $(stage)
