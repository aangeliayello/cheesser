import request
import json
import berserk

session = berserk.TokenSession("lip_1vnX8oLHQftDorNe2AiS")
client = berserk.Client(session=session)
events = client.bots.stream_incoming_events()
e = next(events)


def handle_challenge(event):
    challengers_allowed = ['aangeli']
    id = event['challenge']['id']
    challenger = event['challenge']['challenger']['id']

    if challenger in challengers_allowed:
        response = client.bots.accept_challenge(id)
        return response, id, challenger
    else:
        return None, None, None

f = open(".\lichess_api\stream_event.json")
event = json.load(f)
if event['type'] == "challenge":
    response, challenge_id, challenger = handle_challenge(event)
    challenge = client.bots.
    client.bots.stream_incoming_events()
    gse1 = client.board.stream_game_state(challenge_id)

