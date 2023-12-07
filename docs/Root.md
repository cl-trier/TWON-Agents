**TWON *(TWin of Online Social Networks)* API provides access to two components of a simulated network:** Generative Agents powered by Large Language Models that react to textual content in a personalized manner and a Content Distributor that ranks and filters a stream of content for a specific user profile.

Currently, the API provides only the agent interaction part. We define agents as simulated social network users modeled through large language models capable of performing all interactions a human user is capable of. We design the interaction solely on prompts and receive the agent's response as unrestricted text.

## Proposed Structure (tbd)

```
├── /                     <- Redirects to API documentation (docs/)
│
├── agents/               <- Generative Agent Interaction
│   ├── get/              <- Returns a list of all agents
│   ├── get/{agent_id}    <- Returns a specific agent
│   └── post/             <- Interacts with the agent (reply)
│ 
├── docs/                 <- Swagger API Documentation
└── redoc/                <- Redocly API Documentation
```

The source code is available on GitHub: <https://github.com/smnmnkr/TWON-API>
