#!/bin/sh
SUPABASE_TEST_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYzNTAwODQ4NywiZXhwIjoxOTUwNTg0NDg3fQ.l8IgkO7TQokGSc9OJoobXIVXsOXkilXl4Ak6SCX5qI8" \
SUPABASE_TEST_URL="https://ibrydvrsxoapzgtnhpso.supabase.co" \
poetry run pytest
