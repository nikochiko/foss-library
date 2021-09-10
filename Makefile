.PHONY: test
test:
	coverage run -m unittest tests
report:
	coverage report
