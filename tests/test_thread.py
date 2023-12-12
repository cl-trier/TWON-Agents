import logging

from src.schemas import Post, Thread


def test_post():
    post = Post(**Post.model_config["json_schema_extra"]["examples"][0])

    assert type(post.author) == str
    assert type(post.message) == str

    assert post.author == Post.model_config["json_schema_extra"]["examples"][0]['author']
    assert post.message == Post.model_config["json_schema_extra"]["examples"][0]['message']

    logging.info(f'\n> Schema Post (str): \n{post}')


def test_thread():
    thread = Thread(
        posts=[
            Post(**Post.model_config["json_schema_extra"]["examples"][0]),
            Post(**Post.model_config["json_schema_extra"]["examples"][1])
        ]
    )

    assert type(thread.posts) == list
    assert type(thread.posts[0]) == Post
    assert len(thread) == 2

    logging.info(f'\n> Schema Thread (str)\n{thread}')
