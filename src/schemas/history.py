from typing import List

from pydantic import BaseModel


class Interaction(BaseModel):
    action: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action": "liked", "message": "Sweets make the world go round!"},
                {"action": "wrote", "message": "As a kid, I fell into a jar of honey."}
            ]
        }
    }

    def __str__(self):
        return f'You {self.action} the message: {self.message}'.strip()


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
            return "You have not interacted in the network yet."

        return '\n\n'.join([str(interaction) for interaction in self.interactions[-2:]])
