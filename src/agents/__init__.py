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

    @router.get('/agents/', tags=["agents"])
    async def get_all_agents() -> List[AgentSchema]:
        """
        The route returns a list of all agents in production, including their character descriptions.
        """
        return [AgentSchema(**agent) for agent in get_agents().values()]

    @router.get('/agents/{agent_id}', tags=["agents"])
    async def get_agent_by_id(agent_id: str) -> AgentSchema | None:
        """
        The route returns a singular agent by its ID, including the character description.
        """
        if agent_id not in get_agents():
            raise HTTPException(status_code=404, detail=f'Agent (id: {agent_id}) not found.')

        return AgentSchema(**get_agents()[agent_id])

    @router.post("/agents/", tags=["agents"])
    async def generate_agent_interaction(body: AgentInteractionSchema) -> AgentResponseSchema:
        """
        The route processes a provided JSON payload (defined below) and returns the agents response.

        ## Request Body
        The incoming payload must contain the following parameters.

        ### Action (Select)
        The action describes the task the agent should fulfill. It determines the selection of the overall prompt template.
        They model possible interactions with the social network. Currently, we only provide the 'reply' action, where the agent reacts textually to a stream of messages.

        ### Agent (Select)
        The agent describes the persona that the language model should mimic. We provide a predefined list of agents expressed by typical social media behavior.
        The complete list, including meta information, can be retrieved with the get agent route.

        ### History (Free Text)
        The history contains the recent interaction of the select agent with the platform/thread. The parameter expects preformatted text (a textual history description)
        In our current experiment iteration, we provide the last two interactions in the following format:

        ```
        You posted: {user_history_replies[n-1]}

        You posted: {user_history_replies[n]}
        ```

        If the agent has not interacted yet, we state it explicitly:

        ```
        You have not interacted in the thread yet.
        ```

        ### Thread (Free Text)
        The thread contains information of the current content the agent perceives in the conversation. The parameter expects preformatted text (a textual thread description)
        In our current experiment interation, we provide the original post (thread starter) and the last to replies in the following format:

        ```
        Post by (thread_items[0].author): (thread_items[0].content)

        Reply by (thread_items[n-1].author): (thread_items[n-1].content)

        Reply by (thread_items[n].author): (thread_items[n].content)
        ```

        ### Endpoint (Select)
        The endpoint describes the LLM integration and model for inferencing. Currently, we maintain two endpoints:
        1) Hugging Face, with all models based on the free API tier.
        2) OpenAI, with GPT-3.5-turbo and GPT-4

        **Note:** For testing/development purposes use Hugging Face only, as inferencing OpenAI is not free.
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
