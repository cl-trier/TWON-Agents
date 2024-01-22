from typing import List

from pydantic import BaseModel

from .interaction import Interaction


class History(BaseModel):
    interactions: List[Interaction] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "interactions": [
                        Interaction.model_config["json_schema_extra"]["examples"][0],
                        Interaction.model_config["json_schema_extra"]["examples"][1]
                    ]
                }
            ]
        }
    }

    def __len__(self) -> int:
        return len(self.interactions)

    def __str__(self) -> str:
        if not self.interactions:
            return "You have not interacted in the platform yet."

        return '\n'.join([str(interaction) for interaction in self.interactions[-2:]])
