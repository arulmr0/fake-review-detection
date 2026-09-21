.PHONY: help setup demo data experiments figures test lint clean

help:
	@echo "setup        install dependencies"
	@echo "demo         generate stand-in data, run experiments, make figures"
	@echo "data         download the real corpora (Kaggle needs a manual step)"
	@echo "experiments  run every model in every condition -> results/results.csv"
	@echo "figures      regenerate figures from results/results.csv"
	@echo "test         run the test suite"
	@echo "lint         run ruff"

setup:
	python -m pip install -r requirements.txt
	python -m pip install -e .

demo:
	python -m frd.make_synthetic --n 400
	python -m frd.experiments --human synthetic_human --machine synthetic_machine
	python -m frd.figures
	python -m frd.cli train --human synthetic_human --machine synthetic_machine

data:
	python -m frd.download

experiments:
	python -m frd.experiments

figures:
	python -m frd.figures

test:
	python -m pytest

lint:
	python -m ruff check src tests

clean:
	rm -rf .pytest_cache .ruff_cache **/__pycache__ models
