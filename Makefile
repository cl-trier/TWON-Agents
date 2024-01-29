# --- --- ---

install:
	@python3 -m pip install -r requirements.txt

update:
	git pull
	sudo supervisorctl restart twon-api

test:
	@python3 -m pytest tests/


# --- --- ---

dev:
	@python3 -m uvicorn api:app --reload

serve:
	@python3 -m uvicorn api:app
