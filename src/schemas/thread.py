from typing import List

from pydantic import BaseModel


class Post(BaseModel):
    author: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"author": "human_user", "message": "I like cookies!"},
                {"author": "cookie_monster", "message": "Me Love to Eat Cookies."}
            ]
        }
    }

    def __str__(self) -> str:
        return f'Post by @{self.author}: {self.message}'.strip()


class Thread(BaseModel):
    posts: List[Post]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "posts": [
                        Post.model_config["json_schema_extra"]["examples"][0],
                        Post.model_config["json_schema_extra"]["examples"][1]
                    ]
                }
            ]
        }
    }

    def __len__(self) -> int:
        return len(self.posts)

    def __str__(self) -> str:
        return '\n'.join([
            str(post) for post in
            (
                self.posts if len(self) <= 2
                else self.posts[:1] + self.posts[-2:]
            )
        ])
