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

    def __repr__(self):
        return f'Post by ${self.author}: ${self.message}'.strip()


class Thread(BaseModel):
    posts: List[Post]

    def __len__(self):
        return len(self.posts)

    def __repr__(self):
        string: str = f'{self.posts[0]}\n\n'

        for post in self.posts[-2]:
            string += f'{post}\n\n'

        return string.strip()

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
