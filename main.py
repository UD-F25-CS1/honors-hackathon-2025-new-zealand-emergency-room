from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
from random import randint

from meta import *

# hide_debug_information()
# set_website_framed(False)
set_website_title("Your Drafter Website")
set_site_information(
    "author",
    """
Your description can go here.
""",
    [],
    [],
    [],
)


# - - - -
# Dataclasses
# - - - -


@dataclass
class Card:
    front: str
    back: str
    card_id: int

@dataclass
class State:
    cards: list[Card]

# - - - -
# Routes
# - - - -

@route
def index(state: State):
    return Page(state, content=[
        Header("Study"),
        Button(text="Create Cards", url="/create_cards"),
        Button(text="Quiz Yourself", url="/quiz_page"),
        ])

@route
def create_cards(state: State) -> Page:
    return Page(state, content=[
        ])

@route
def quiz_page(state: State) -> Page:
    return Page(state, content=[
        ])


test_state = State([])
start_server(test_state)
