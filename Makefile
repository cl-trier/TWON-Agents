ENV := ./.venv/bin/python
DEVICE := 2


debug:
	${ENV} ./pipeline/train/debug.py

train:
	${ENV} ./pipeline/train/de/task_post.py --device ${DEVICE}
	${ENV} ./pipeline/train/de/task_reply.py --device ${DEVICE}
	${ENV} ./pipeline/train/en/task_post.py --device ${DEVICE}
	${ENV} ./pipeline/train/en/task_reply.py --device ${DEVICE}

eval:
	${ENV} ./pipeline/train/de/task_post.py --no-train --device ${DEVICE}
	${ENV} ./pipeline/train/de/task_reply.py --no-train --device ${DEVICE}
	${ENV} ./pipeline/train/en/task_post.py --no-train --device ${DEVICE}
	${ENV} ./pipeline/train/en/task_reply.py --no-train --device ${DEVICE}