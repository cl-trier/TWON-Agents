**TWON *(TWin of Online Social Networks)* API provides access to two components of a simulated network:** Generative Agents powered by Large Language Models that react to textual content in a personalized manner and a Content Distributor that ranks and filters a stream of content for a specific user profile.

Currently, the API serves as a structural mockup to showcase proposed endpoints and exemplary calls with Hugging Face API.

## Proposed Structure (tbd)

```
├── /                     <- Redirects to API documentation (docs/)
│
├── agents/               <- Generative Agent Interaction (read, like, reply)
│   ├── get/              <- Returns a list of all agents (including persona)
│   ├── get/{agent_id}    <- Returns a specific agent information
│   └── post/             <- Handles requests to interact with the agent
│ 
├── docs/                 <- Swagger API Documentation
└── redoc/                <- Redocly API Documentation
```
