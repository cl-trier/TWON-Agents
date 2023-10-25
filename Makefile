# --- --- ---

install:
	@python3 -m pip install -r requirements.txt

update:
	git pull
	sudo supervisorctl restart fastapi-app-twon-api

# --- --- ---

dev:
	uvicorn setup:app --reload

serve:
	uvicorn setup:app
