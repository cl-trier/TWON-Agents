import logging

from src.schemas import model


def test_interaction():
    interaction = model.Interaction(**model.Interaction.model_config["json_schema_extra"]["examples"][0])

    assert interaction.action == model.Interaction.model_config["json_schema_extra"]["examples"][0]['action']
    assert interaction.message == model.Interaction.model_config["json_schema_extra"]["examples"][0]['message']

    logging.info(f'\n> Schema Interaction (str): \n{interaction}')


def test_history():
    history = model.History(
        interactions=[
            model.Interaction(**model.Interaction.model_config["json_schema_extra"]["examples"][0]),
            model.Interaction(**model.Interaction.model_config["json_schema_extra"]["examples"][1])
        ]
    )

    assert len(history) == 2

    logging.info(f'\n> Schema History (str)\n{history}')


def test_post():
    post = model.Post(**model.Post.model_config["json_schema_extra"]["examples"][0])

    assert post.author == model.Post.model_config["json_schema_extra"]["examples"][0]['author']
    assert post.message == model.Post.model_config["json_schema_extra"]["examples"][0]['message']

    logging.info(f'\n> Schema Post (str): \n{post}')


def test_thread():
    thread = model.Thread(
        posts=[
            model.Post(**model.Post.model_config["json_schema_extra"]["examples"][0]),
            model.Post(**model.Post.model_config["json_schema_extra"]["examples"][1])
        ]
    )
    assert len(thread) == 2

    logging.info(f'\n> Schema Thread (str)\n{thread}')
