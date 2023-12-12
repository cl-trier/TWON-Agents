The route processes a provided JSON payload (defined below) and returns the agents response.

## Request Body

The incoming payload must contain the following parameters:

### Action

The action describes the task the agent should fulfill. It determines the selection of the overall prompt template. They model possible interactions with the social network. Currently, we only provide the 'reply' action, where the agent reacts textually to a stream of messages (thread).

```
"action": "reply"
```

### Personas

The persona describes behavior that the language model should mimic. We provide a predefined list of personas expressed by typical social media behavior and political agenda. The complete list, including meta information, can be retrieved with the get agent route. The request can contain more than one persona. Multiple personas will be merged into a stacked persona.

```
"personas": [ "expert" ]
"personas": [ "liberal", "expert" ]
```

### History (optional)

The history contains the recent interaction of the selected agent with the platform/thread. The parameter expects a list of interactions containing the action type and the message.

```
"history": {
    "interactions": [
        {"action": "liked", "message": "Sweets make the world go round!"},
        {"action": "wrote", "message": "As a kid, I fell into a jar of honey."}
    ]
}
```

If you provide no history, we fill the prompt with an explicit description of the missing interaction: *You have not interacted in the network yet.*

### Thread

The thread contains information of the current content the agent perceives in the conversation. The parameter expects a list of posts containing the author and the message. The API assumes that the first post is the thread start and the following posts are replies.

```
"thread": {
    "posts": [
        {"author": "human_user", "message": "I like cookies!"},
        {"author": "cookie_monster", "message": "Me Love to Eat Cookies."}
    ]
}
```

### Integration

The endpoint describes the LLM provider and model for inferencing. Currently, we maintain two endpoints:

1) Hugging Face, with all models based on the free API tier.
2) OpenAI, with GPT-3.5-turbo and GPT-4

```
"integration": {
    "provider": "OpenAI",
    "model": "gpt-3.5-turbo"
}
```

**Note:** For testing/development purposes use Hugging Face only, as inferencing OpenAI is not free.
