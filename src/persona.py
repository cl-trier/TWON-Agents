import typing

import pydantic


class Persona(pydantic.BaseModel):
    id: str
    name: str
    type: typing.List[str]
    persona: str
    summary: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "liberal",
                    "name": "Liberal",
                    "type": "social-media-archetype",
                    "persona": "You are a dedicated and passionate Liberal, fueled by a deep commitment to progressive values and social equality. Your political ideology is rooted in the belief that government can and should play a crucial role in addressing societal issues and ensuring justice for all. With an unwavering commitment to human rights, environmental sustainability, and social justice, you actively engage in advocacy efforts to promote inclusivity, diversity, and a fair distribution of resources.",
                    "summary": "I am a committed and passionate Liberal driven by a deep dedication to progressive values, advocating for government intervention to address societal issues."
                }
            ]
        }
    }

    def __str__(self) -> str:
        return self.persona

    def merge(self, other: 'Persona') -> 'Persona':
        return Persona(
            id=f'{self.id}_{other.id}',
            name=f'{self.name} {other.name}',
            type=self.type + other.type,
            persona=f'{self.persona}\n\n{other.persona}',
            summary=f'{self.summary} {other.summary}',
        )

    @classmethod
    def merge_personas(
            cls,
            language: str,
            persona_selection: typing.List[str],
            persona_pool: typing.Dict[typing.Tuple[str, str], 'Persona']
    ) -> 'Persona':
        merged_persona: Persona = persona_pool[(language, persona_selection[0])]
        for persona_id in persona_selection[1:]:
            merged_persona = merged_persona.merge(persona_pool[(language, persona_id)])

        return merged_persona
