# --- --- ---

install:
	@python3 -m pip install -r requirements.txt

# --- --- ---

dev:
	uvicorn setup:app --reload

serve:
	uvicorn setup:app
