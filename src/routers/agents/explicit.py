from typing import List

from fastapi import APIRouter, Depends
from pymongo.database import Database

from ...database import get_database
from ...services import hf_inference
from ...schemas.agents import AgentResponse, AgentSchema, AgentInteraction


def create_route() -> APIRouter:
    router = APIRouter()

    @router.get('/agents/explicit')
    async def get_all_agents(db: Database = Depends(get_database)) -> List[AgentSchema]:
        return [AgentSchema(**agent) for agent in list(db.agents.find({}, {'_id': False}))]

    @router.get('/agents/explicit/{agent_id}')
    async def get_agent_by_id(agent_id: str, db: Database = Depends(get_database)) -> AgentSchema | None:
        data: dict | None = db.agents.find_one({'id': agent_id}, {'_id': False})
        return AgentSchema(**data) if data else None

    @router.post("/agents/explicit/")
    async def generate_agent_interaction(
            body: AgentInteraction,
            db: Database = Depends(get_database)
    ) -> AgentResponse:
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
