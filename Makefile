ENV := ./.venv/bin/python

debug:
	${ENV} ./pipeline/train/debug.py

train:
	${ENV} ./pipeline/train/de/task_post.py
	${ENV} ./pipeline/train/de/task_reply.py
	${ENV} ./pipeline/train/en/task_reply.py