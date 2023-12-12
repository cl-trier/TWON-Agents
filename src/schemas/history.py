from typing import List

from pydantic import BaseModel, computed_field


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

    def __repr__(self):
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

    def __len__(self):
        return len(self.interactions)

    @computed_field
    @property
    def summary(self):
        if not self.interactions:
            return "You have not interacted in the network yet."

        string: str = f'{self.interactions[0]}\n\n'

        for post in self.interactions[-2]:
            string += f'{post}\n\n'

        return string.strip()
