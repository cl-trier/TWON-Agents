import pydantic


class Interaction(pydantic.BaseModel):
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
