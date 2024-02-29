import pydantic


class Post(pydantic.BaseModel):
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
