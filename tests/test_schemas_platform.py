import logging

from src.schemas import platform


def test_interaction():
    interaction = platform.Interaction(**platform.Interaction.model_config["json_schema_extra"]["examples"][0])

    assert interaction.action == platform.Interaction.model_config["json_schema_extra"]["examples"][0]['action']
    assert interaction.message == platform.Interaction.model_config["json_schema_extra"]["examples"][0]['message']

    logging.info(f'\n> Schema Interaction (str): \n{interaction}')


def test_history():
    history = platform.History(
        interactions=[
            platform.Interaction(**platform.Interaction.model_config["json_schema_extra"]["examples"][0]),
            platform.Interaction(**platform.Interaction.model_config["json_schema_extra"]["examples"][1])
        ]
    )

    assert len(history) == 2

    logging.info(f'\n> Schema History (str)\n{history}')


def test_post():
    post = platform.Post(**platform.Post.model_config["json_schema_extra"]["examples"][0])

    assert post.author == platform.Post.model_config["json_schema_extra"]["examples"][0]['author']
    assert post.message == platform.Post.model_config["json_schema_extra"]["examples"][0]['message']

    logging.info(f'\n> Schema Post (str): \n{post}')


def test_thread():
    thread = platform.Thread(
        posts=[
            platform.Post(**platform.Post.model_config["json_schema_extra"]["examples"][0]),
            platform.Post(**platform.Post.model_config["json_schema_extra"]["examples"][1])
        ]
    )
    assert len(thread) == 2

    logging.info(f'\n> Schema Thread (str)\n{thread}')
