import logging

from src.schemas import Interaction, History


def test_interaction():
    interaction = Interaction(**Interaction.model_config["json_schema_extra"]["examples"][0])

    assert type(interaction.action) == str
    assert type(interaction.message) == str

    assert interaction.action == Interaction.model_config["json_schema_extra"]["examples"][0]['action']
    assert interaction.message == Interaction.model_config["json_schema_extra"]["examples"][0]['message']

    logging.info(f'\n> Schema Interaction (str): \n{interaction}')


def test_history():
    history = History(
        interactions=[
            Interaction(**Interaction.model_config["json_schema_extra"]["examples"][0]),
            Interaction(**Interaction.model_config["json_schema_extra"]["examples"][1])
        ]
    )

    assert type(history.interactions) == list
    assert type(history.interactions[0]) == Interaction
    assert len(history) == 2

    logging.info(f'\n> Schema History (str)\n{history}')
