PHONY: init init-from-template run hooks seed test check cfn-lint ldb migrate idb flask-deploy-dev deploy-dev

PYTHON=poetry run


run:
	FLASK_ENV=development $(PYTHON) flask run --reload

hooks:
	$(PYTHON) pre-commit install

seed:
	$(PYTHON) flask seed

test:
	$(PYTHON) pytest

check:
	$(PYTHON) flake8
	$(PYTHON) mypy .
	$(PYTHON) bento check
	$(PYTHON) pytest

# init DB
idb: dropcreatedb migrate seed

dropcreatedb:
	dropdb ocp --if-exists
	createdb ocp

migrate:
	flask db upgrade