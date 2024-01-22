The route processes a provided JSON payload (defined below) and returns the agents response.

## Thread

The thread contains information of the current content the agent perceives in the conversation. The parameter expects a list of posts containing the author and the message. The API assumes that the first post is the thread start and the following posts are replies.

```
"thread": {
    "posts": [
        {"author": "human_user", "message": "I like cookies!"},
        {"author": "cookie_monster", "message": "Me Love to Eat Cookies."}
    ]
}
```
