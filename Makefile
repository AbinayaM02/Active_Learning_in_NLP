# Styling
.PHONY: style
style:
	black .
	flake8
	isort .
