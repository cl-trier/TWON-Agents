import uuid
import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from .data import get_agents, get_prompts
from .schemas import AgentSchema, AgentInteractionSchema, AgentResponseSchema
from .inference import inference

from ..config import Config


def create_route(conf: Config) -> APIRouter:
    router = APIRouter()

    @router.get('/agents/')
    async def get_all_agents() -> List[AgentSchema]:
        """
        The route returns a list of all agents in production, including their character descriptions.
        """
        return [AgentSchema(**agent) for agent in get_agents().values()]

    @router.get('/agents/{agent_id}')
    async def get_agent_by_id(agent_id: str) -> AgentSchema | None:
        """
        The route returns a singular agent by its ID, including the character description.
        """
        if agent_id not in get_agents():
            raise HTTPException(status_code=404, detail=f'Agent (id: {agent_id}) not found.')

        return AgentSchema(**get_agents()[agent_id])

    @router.post("/agents/")
    async def generate_agent_interaction(body: AgentInteractionSchema) -> AgentResponseSchema:
        """
        The route processes a provided JSON payload (defined below) and returns the agents action as text.

        **Payload:**
        ```python
        {
            "action": "One of our (tbd) predefined actions (currently only reply)",
            "agent": "One of our (tbd) described agents: Base, ..., future: (Dis-)Agreer, Debater, Troll, Hater, Fact-Checker",
            "thread": "The thread the agent interacts on with the defined action",
            "history": "The agents behavior history",
            "endpoint": "Optional: huggingFace, OpenAI"
        }
        ```
        """
        response: AgentResponseSchema = AgentResponseSchema(
            **inference(
                template=get_prompts()[body.action.value],
                variables=dict(
                    persona=AgentSchema(**get_agents()[body.agent.value]).persona,
                    history=body.history,
                    thread=body.thread,
                ),
                endpoint=body.endpoint,
            )
              | dict(
                id=uuid.uuid1(),
                timestamp=datetime.datetime.now(),
                action=body.action.value,
                agent=body.agent.value,
                endpoint=body.endpoint,
            )
        )
        response.log(conf.logging.agent_path)

        return response

    return router
