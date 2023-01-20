clean:
	rm -rf .venv day-summary *.checkpoints .pytest_cache .coverage

init: clean
	pip install poetry
	poetry init