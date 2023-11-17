from typing import List

from fastapi import APIRouter, Depends
from pymongo.database import Database

from .schemas import AgentResponse, AgentSchema, AgentInteraction
from .services import hf_inference


def create_route(get_database: callable) -> APIRouter:
    router = APIRouter()

    @router.get('/agents/')
    async def get_all_agents(db: Database = Depends(get_database)) -> List[AgentSchema]:
        """
        The route returns a list of all agents in production, including their character descriptions.
        """
        return [AgentSchema(**agent) for agent in list(db.agents.find({}, {'_id': False}))]

    @router.get('/agents/{agent_id}')
    async def get_agent_by_id(agent_id: str, db: Database = Depends(get_database)) -> AgentSchema | None:
        """
        The route returns a singular agent by its ID, including the character description.
        """
        data: dict | None = db.agents.find_one({'id': agent_id}, {'_id': False})
        return AgentSchema(**data) if data else None

    @router.post("/agents/")
    async def generate_agent_interaction(
            body: AgentInteraction,
            db: Database = Depends(get_database)
    ) -> AgentResponse:
        """
        The route processes a provided JSON payload (defined below) and returns the agents action as text.

        **Payload:**
        ```python
        {
            "action": "One of our (tbd) predefined actions: reading, liking, replying",
            "agent": "One of our (tbd) described agents: Base, ..., future: (Dis-)Agreer, Debater, Troll, Hater, Fact-Checker",
            "content": "The post the agent interacts on with the defined action",
            "history": Optional: UserHistory.model_config['json_schema_extra']['examples'],
            "model": "Optional: Language Model to choose; currently external (Llama-2), for later iterations local and fine-tuned"
        }
        ```
        """
        response: dict = hf_inference(
            model=db.config.find_one({'id': 'hf_model'})['value'],
            model_args=db.config.find_one({'id': 'hf_model_args'})['value'],
            template=db.templates.find_one({'id': body.action.value})['content'],
            character=db.agents.find_one({'id': body.agent.value})['character'],
            content=body.content
        )

        db.requests.insert_one(response)
        return AgentResponse(**response)

    return router
