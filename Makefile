.PHONY: setup lint test docs

setup:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

lint:
	python -m py_compile src/agents/main_agent.py src/data/feature_engineering.py src/models/churn_model.py src/services/api.py

test:
	pytest

docs:
	@echo "Open docs/ARCHITECTURE.md and docs/ROADMAP.md for project documentation."
