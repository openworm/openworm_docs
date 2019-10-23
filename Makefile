PYTHON=python
install:
	$(PYTHON) -m pip install -U -r requirements.txt
check:
	$(PYTHON) -m black --check build.py
	$(PYTHON) -m flake8 --max-line-length=88 --ignore=E203 --count --statistics --show-source build.py
build:
	$(PYTHON) build.py
	$(PYTHON) -m mkdocs build
serve: build
	$(PYTHON) -m mkdocs serve
