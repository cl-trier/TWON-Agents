# ToDo: move schemas to external database and load during runtime

def get_explicit_agent_config():
    return {
        "model": "tiiuae/falcon-7b-instruct",
        "prompts": {
            "read": "Decide with yes or no if you would read the following text {character}: '''{content}'''",
            "like": "Decide with yes or no if you would like the following text {character}: '''{content}'''",
            "share": "Decide with yes or no if you would share the following text {character}: '''{content}'''",
            "reply": "Reply in the form of a tweet to the following text {character}: '''{content}'''"
        }
    }


def get_explicit_agent_definition():
    return {
        'base': {
            "label": "🤖 Plain Model",
            "persona": ""
        },
        "agreeing": {
            "label": "🙆 Agreeing Agent",
            "persona": "while imagining you are an individual agreeing with the content"
        },
        "disagreeing": {
            "label": "🙅 Disagreeing Agent",
            "persona": "while imagining you are an individual disagreeing with the content"
        },
        "conspiracy_theorist": {
            "label": "🛸 Conspiracy Theorist",
            "persona": "while imagining you are a conspiracy theorist"
        },
        "nobel_prize_winner": {
            "label": "🏅 Nobel Prize Winner",
            "persona": "while imagining you are a nobel prize winner"
        },
        "us_congress_member": {
            "label": "🏛️ US Congress Member",
            "persona": "while imagining you are a member of the U.S. congress"
        }
    }
