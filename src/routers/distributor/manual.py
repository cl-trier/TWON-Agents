import random
from typing import List

from fastapi import APIRouter

from ...schemas.distributor import Post, User


def create_route() -> APIRouter:
    router = APIRouter()

    @router.post('/distributor/explicit/')
    async def generate_content_distribution(
            content_stream: List[Post],
            user: User
    ) -> List[Post]:
        return random.sample(content_stream, len(content_stream))

    return router
