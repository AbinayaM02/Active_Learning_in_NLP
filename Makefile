# Styling
.PHONY: style
style:
	black .
	flake8
	isort .

# Tests
.PHONY: test
test:
	pytest --version
	pytest --cov scripts --cov-report html
