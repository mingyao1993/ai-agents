https://agentchat.vercel.app/

uv run langgraph dev

source .venv/bin/activate
python -m ensurepip

uv pip compile --output-file requirements.txt pyproject.toml