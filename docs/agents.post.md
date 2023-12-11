The route processes a provided JSON payload (defined below) and returns the agents response.

## Request Body

The incoming payload must contain the following parameters:

### Action (Select)

The action describes the task the agent should fulfill. It determines the selection of the overall prompt template. They
model possible interactions with the social network. Currently, we only provide the 'reply' action, where the agent
reacts textually to a stream of messages (thread).

```
"action": "reply"
```

### Personas (List)

The persona describes behavior that the language model should mimic. We provide a predefined list of personas expressed
by typical social media behavior and political agenda. The complete list, including meta information, can be retrieved
with the get agent route. The request can contain more than one persona. Multiple personas will be merged into a stacked
persona.

```
"personas": [ "expert" ]
"personas": [ "liberal", "expert" ]
```

### History (Free Text)

The history contains the recent interaction of the select agent with the platform/thread. The parameter expects
preformatted text (a textual history description)
In our current experiment iteration, we provide the last two interactions in the following format:

```
You posted: {user_history_replies[n-1]}

You posted: {user_history_replies[n]}
```

If the agent has not interacted yet, we state it explicitly:

```
You have not interacted in the thread yet.
```

### Thread (Free Text)

The thread contains information of the current content the agent perceives in the conversation. The parameter expects
preformatted text (a textual thread description)
In our current experiment interation, we provide the original post (thread starter) and the last to replies in the
following format:

```
Post by (thread_items[0].author): (thread_items[0].content)

Reply by (thread_items[n-1].author): (thread_items[n-1].content)

Reply by (thread_items[n].author): (thread_items[n].content)
```

### Integration (Select)

The endpoint describes the LLM provider and model for inferencing. Currently, we maintain two endpoints:

1) Hugging Face, with all models based on the free API tier.
2) OpenAI, with GPT-3.5-turbo and GPT-4

**Note:** For testing/development purposes use Hugging Face only, as inferencing OpenAI is not free.

```
"integration": {
    "provider": "OpenAI",
    "model": "gpt-3.5-turbo"
}
```
