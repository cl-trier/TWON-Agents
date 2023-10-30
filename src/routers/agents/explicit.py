from typing import List

from fastapi import APIRouter, Depends
from pymongo.database import Database

from ...database import get_database
from ...services import hf_inference
from ...schemas.agents import AgentResponse, AgentNames, AgentSchema, AgentsActions


def create_route():
    router = APIRouter()

    @router.get('/agents/explicit')
    async def get_explicit_agents(db: Database = Depends(get_database)) -> List[AgentSchema]:
        return [AgentSchema(**agent) for agent in list(db.agents.find({}, {'_id': False}))]

    @router.get("/agents/explicit/")
    async def get_explicit_agent(
            content: str,
            name: AgentNames,
            action: AgentsActions,
            db: Database = Depends(get_database)
    ) -> AgentResponse:
        response: dict = hf_inference(
            model=db.config.find_one({'id': 'hf_model'})['value'],
            model_args=db.config.find_one({'id': 'hf_model_args'})['value'],
            template=db.templates.find_one({'id': action.value})['content'],
            character=db.agents.find_one({'id': name.value})['character'],
            content=content
        )

        db.requests.insert_one(response)
        return AgentResponse(**response)

    return router
