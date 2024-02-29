**TWON *(TWin of Online Social Networks)*** Agents API provides access to generative Agents powered by Large Language Models that generate or react to textual content in a personalized manner. We define agents as simulated social network users modeled through large language models capable of performing all interactions a human user is capable of. We design the interaction solely on prompts and receive the agent's response as unrestricted text.

## Structure

```
├── /                     <- (root) Swagger API Documentation
│   
├── personas/             <- (get) Returns a list of all personas
├── prompts/              <- (get) Returns a list of all prompts
│ 
├── generate/             <- (post) Generate a new post
├── reply/                <- (post) Replies to a given thread
├── like/                 <- (post) Decides whether to like a post or not
│ 
└── redoc/                <- Redocly API Documentation
```

The source code is available on GitHub: <https://github.com/smnmnkr/TWON-Agents>

## Request Body

The provided payload for all actions must contain the following parameters:

### Persona

The persona describes behavior that the language model should mimic. We provide a predefined list of personas expressed by typical social media behavior and political agenda. The complete list, including meta information, can be retrieved with the get agent route. The request can contain more than one persona. Multiple personas will be merged into a stacked persona.

```
"persona": [ "expert" ]
"persona": [ "liberal", "expert" ]
```

### Integration (optional, default: Hugging Face)

The endpoint describes the LLM provider and model for inferencing. Currently, we maintain two endpoints:

1) Hugging Face, with all models based on the free API tier.
2) OpenAI, with GPT-3.5-turbo and GPT-4
3) Local GPU-Server, with Ollama and a pre-selection of models

```
"integration": {
    "provider": "OpenAI",
    "model": "gpt-3.5-turbo"
}
```

**Note:** For testing/development purposes use Hugging Face only, as inferencing OpenAI is not free of charge.

### Language (optional, default: English)
The language describes the native language of the personas and prompts the action to respond in the given language. This attribute is restricted to the following values: `'English', 'German', 'Dutch', 'Italian', 'Serbian'`

### Platform (optional, default: Twitter)
The platform describes the environment in which the agent's browser and which writing style to emulate. This attribute is restricted to the following values: `['Twitter', 'Reddit', 'Facebook', 'Telegram']`


### History (optional, default: None)

The history contains the recent interaction of the selected agent with the platform. The parameter expects a list of interactions containing the action type and the message.

```
"history": {
    "interactions": [
        {"action": "liked", "message": "Sweets make the world go round!"},
        {"action": "wrote", "message": "As a kid, I fell into a jar of honey."}
    ]
}
```

If you provide no history, we fill the prompt with an explicit description of the missing interaction: `You have not interacted in the platform yet.`
