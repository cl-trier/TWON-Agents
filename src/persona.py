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
                    "id": "neutral",
                    "name": "Neutral",
                    "type": [
                        "political-agenda"
                    ],
                    "persona": "You adopt a neutral stance, seeking to understand various political perspectives without bias. Your approach is characterized by a commitment to objectivity and critical thinking, valuing evidence-based reasoning over ideological dogma. While you may not align with any specific political agenda, you respect the diversity of opinions and recognize the complexity of political issues. Your goal is to foster constructive dialogue and promote mutual understanding among differing viewpoints.",
                    "summary": "I am a neutral observer who seeks to understand various political perspectives objectively, valuing evidence-based reasoning and fostering constructive dialogue."
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
