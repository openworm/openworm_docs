PYTHON=python
install:
	$(PYTHON) -m pip install -U -r requirements.txt
check:
	$(PYTHON) -m black -l 79 --check build.py
	$(PYTHON) -m flake8 --count --statistics --show-source build.py
build:
	$(PYTHON) build.py
	$(PYTHON) -m mkdocs build
