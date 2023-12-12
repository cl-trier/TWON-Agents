# --- --- ---

install:
	@python3 -m pip install -r requirements.txt

update:
	git pull
	sudo supervisorctl restart twon-api

test:
	@python3 -m pytest tests/  -W ignore::DeprecationWarning


# --- --- ---

dev:
	uvicorn setup:app --reload

serve:
	uvicorn setup:app
