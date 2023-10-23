**TWON *(TWin of Online Social Networks)* API provides access to two components of a simulated network:** Generative Agents powered by Large Language Models that react to textual content in a personalized manner and a Content Distributor that ranks and filters a stream of content for a specific user profile.

Currently, the API serves as a structural mockup to showcase proposed endpoints and exemplary calls with Hugging Face API. The example call generates the reply of explicitly defined agents to given Tweets.

## Proposed Structure (tbd)

```
├── /                     <- Redirects to API documentation (docs/)
│
├── agents/               <- Returns agents information (description)
│   ├── explicit/         <- {character} {action} {content}
│   └── implicit/         <- {user_history} {action} {content}
│
├── distributor/          <- Returns distributor information
│   ├── manual/           <- {content-stream}
│   └── neural/           <- {user_history} {content-stream}
│
├── docs/                 <- Swagger API Documentation
└── redoc/                <- Redocly API Documentation
```


According to the original project proposal, we will perform two simulation iterations. Thus, we propose to utilize different versions of both modules in each iteration. Explicit agents and manual distributors are suitable for the first generation phase in April 2024. They serve as a baseline for improvements during the second phase, where we utilize the implicit agents and neural distributors based on our training data.

