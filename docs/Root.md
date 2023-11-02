**TWON *(TWin of Online Social Networks)* API provides access to two components of a simulated network:** Generative Agents powered by Large Language Models that react to textual content in a personalized manner and a Content Distributor that ranks and filters a stream of content for a specific user profile.

Currently, the API serves as a structural mockup to showcase proposed endpoints and exemplary calls with Hugging Face API. The example call generates the reply of explicitly defined agents to given Posts.

## Proposed Structure (tbd)

```
├── /                     <- Redirects to API documentation (docs/)
│
├── agents/{agent_id}     <- Returns agent(s) information
│   ├── explicit/         <- {agent_interaction}
│   └── implicit/         -- Second Iteration
│
├── distributor/          
│   ├── manual/           <- {content_stream, user}
│   └── neural/           -- Second Iteration
│
├── docs/                 <- Swagger API Documentation
└── redoc/                <- Redocly API Documentation
```
