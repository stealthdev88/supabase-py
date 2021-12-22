install:
	poetry install

install_poetry:
	curl -sSL https://install.python-poetry.org | python -
	poetry install

tests: install tests_only tests_pre_commit

tests_pre_commit:
	poetry run pre-commit run --all-files

run_tests: tests

tests_only:
	export SUPABASE_TEST_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYzNTAwODQ4NywiZXhwIjoxOTUwNTg0NDg3fQ.l8IgkO7TQokGSc9OJoobXIVXsOXkilXl4Ak6SCX5qI8" &&\
	export SUPABASE_TEST_URL="https://ibrydvrsxoapzgtnhpso.supabase.co" &&\
	poetry run pytest --cov=./ --cov-report=xml --cov-report=html -vv
