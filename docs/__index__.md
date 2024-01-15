**TWON *(TWin of Online Social Networks)* API provides access to two components of a simulated network:** Generative Agents powered by Large Language Models that react to textual content in a personalized manner and a Content Distributor that ranks and filters a stream of content for a specific user profile.

Currently, the API provides only the agent interaction part. We define agents as simulated social network users modeled through large language models capable of performing all interactions a human user is capable of. We design the interaction solely on prompts and receive the agent's response as unrestricted text.

## Structure (tbd)

```
├── /                     <- Redirects to API documentation (docs/)
│   
├── personas/             <- (get) Returns a list of all personas
│ 
├── generate/             <- (post) Generate a new post
├── reply/                <- (post) Replies to a given thread
├── like/                 <- (post) Decides whether to like a post or not
│ 
├── docs/                 <- Swagger API Documentation
└── redoc/                <- Redocly API Documentation
```

The source code is available on GitHub: <https://github.com/smnmnkr/TWON-API>

## Request Body

The provided payload for all action must contain the following parameters:

### Personas

The persona describes behavior that the language model should mimic. We provide a predefined list of personas expressed by typical social media behavior and political agenda. The complete list, including meta information, can be retrieved with the get agent route. The request can contain more than one persona. Multiple personas will be merged into a stacked persona.

```
"personas": [ "expert" ]
"personas": [ "liberal", "expert" ]
```

### Integration (optional, default: Hugging Face)

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

### Language (optional, default: English)
todo

### Network (optional, default: Twitter)
todo

### History (optional, default: None)

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
