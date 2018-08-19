.PHONY: all help qa clean coverage build setup-test

# target: all - Default target. Does nothing.
all:
	@clear
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@clear
	@egrep "^# target:" [Mm]akefile

# target: qa - Run tests
qa:
	pytest

# target: clean - Delete pycache
clean:
	echo "### Cleaning *.pyc and .DS_Store files "
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '.DS_Store' -exec rm -f {} \;
	find . -name "__pycache__" -type d -exec rm -rf {} +

# target: coverage - Test coverage
coverage:
	py.test --cov=.

# target: build - Build pkg
build:
	python setup.py sdist

# target: setup-test - Test setup py
setup-test:
	python setup.py test

# target: docker-build - Build docker image with tag habrpars
docker-build:
	docker build . -t weakorm

# target: docker-test - Test code in docker
docker-test:
	docker run --rm weakorm python3 setup.py test