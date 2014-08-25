project_dir = 'django_comments_threaded'

test:
	python setup.py test

release:
	python setup.py sdist --format=zip,bztar,gztar register upload


flake8:
	flake8 ${project_dir}
	flake8 tests.py
	flake8 setup.py


coverage:
	coverage run --include=${project_dir}/*.py setup.py test
	coverage html


coveralls:
	coveralls --config_file=coverage.rc

clean:
	rm -rf *.egg *.egg-info
	rm -rf htmlcov
	rm -f .coverage
	find . -name "*.pyc" -exec rm -rf {} \;
