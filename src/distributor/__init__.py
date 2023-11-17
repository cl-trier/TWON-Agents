import random
from typing import List

from fastapi import APIRouter

from .schemas import Post, User


def create_route() -> APIRouter:
    router = APIRouter()

    @router.post('/distributor/')
    async def generate_content_distribution(
            content_stream: List[Post],
            user: User
    ) -> List[Post]:
        return random.sample(content_stream, len(content_stream))

    return router
