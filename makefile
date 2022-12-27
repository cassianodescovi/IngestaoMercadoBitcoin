clean:
	rm -rf .venv day-summary *.checkpoints .pytest_cache .coverage

init: clean
	pip install poetry
	poetry install

test:
	poetry run python -m pytest

## CI/CD
ci-setup:
	pip install poetry
	poetry install

ci-test:
	poetry run python -m pytest