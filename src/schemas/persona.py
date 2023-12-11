from typing import List

from pydantic import BaseModel


class Persona(BaseModel):
    id: str
    name: str
    type: List[str]
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
                },
                {
                    "id": "expert",
                    "name": "Expert",
                    "type": "social-media-archetype",
                    "persona": "You provide insightful commentary, sharing your own well-thought-out opinions. You engage in discourses by offering analyses of political situations, encouraging public discourse, and fostering an environment where diverse opinions can coexist. You are a source of reliable information and a catalyst for constructive conversations surrounding politics.",
                    "summary": "I am a source of reliable information, offering commentary and fostering constructive political discourse by sharing well-thought-out opinions."
                }
            ]
        }
    }

    def merge(self, other: 'Persona') -> 'Persona':
        return Persona(
            id=f'{self.id}_{other.id}',
            name=f'{self.name} {other.name}',
            type=self.type + other.type,
            persona=f'{self.persona}\n\n{other.persona}',
            summary=f'{self.summary} {other.summary}',
        )
