export OPENAI_API_KEY=fake-key
export OPENAI_MODEL_NAME=llama3.2
export OPENAI_BASE_URL=http://localhost:11434/v1

poetry run python idea_maker/app.py "$@"