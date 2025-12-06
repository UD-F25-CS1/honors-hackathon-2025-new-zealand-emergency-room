from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
from random import randint

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


@dataclass
class Card:
    front: str
    back: str
    card_id: int
    revealed: bool

@dataclass
class State:
    cards: list[Card]
    number_of_cards: int
    current_card: int
    randomized: bool

@route
def index(state: State):
    card_check = False
    return Page(state, content=[
        Header("/Cards"),
        Button(text="Create Cards", url="/create_cards_page", arguments=Argument('check_card', card_check)),
        Button(text="View Stack", url="/view_stack"),
        Button(text="Quiz Yourself", url="/quiz_page")
        ])

@route
def card_adder(state: State, front_input: str, back_input: str) -> Page:
    card_check = bool(front_input) and bool(back_input)
    if card_check:
        state.cards.append(card_maker(state, front_input, back_input, False))
        return create_cards_page(state, not card_check)
    else:
        return create_cards_page(state, Argument('check_card', card_check))

def card_maker(state: State, front_input: str, back_input: str, reveal: bool) -> Card:
    card_number = state.number_of_cards
    state.number_of_cards += 1
    return Card(front_input, back_input, card_number, reveal)

@route
def create_cards_page(state: State, check_card: bool) -> Page:
    if check_card:
        reveal_text = "Cannot be blank"
    else:
        reveal_text = ""
    return Page(state, content=[
        Button(text="Back", url="/index"),
        "Text on Front of Card:",
        TextBox("front_input", ""),
        "Text on Back of Card:",
        TextBox("back_input", ""),
        Button(text="Add Card to Stack", url="/card_adder"),
        reveal_text
        ])
       
@route
def view_stack(state: State) -> Page:
    return Page(state, content=[
        Button(text="Back", url="/index"),
        card_viewer(state.cards)
        ])

def card_viewer(cards: list[Card]) -> PageContent:
    all_cards = []
    for card in cards:
        card_id = Argument("card_id", card.card_id)
        all_cards.append(
            [Div(
                Row("Front Side:", Text(card.front)),
                LineBreak(),
                Row("Back Side: ", Text(card.back)),
                ),
             Button(text="Remove Card", url="/remove_card", arguments=card_id)
             ]
            )
    return Table(all_cards)

@route
def remove_card(state: State, card_id: int) -> Page:
    for i, card in enumerate(state.cards):
        if card_id == card.card_id:
            state.cards.pop(i)
    return view_stack(state)

@route
def quiz_page(state: State) -> Page:
    all_cards = state.cards
    if state.randomized:
        reveal_text = "Randomized Cards!"
    else:
        reveal_text = ""
    state.randomized = False
    if not all_cards:
        return Page(state, content=[
            Row(Button(text="Back", url="/index")),
            "No Cards Made",
            ])
    current_card = all_cards[state.current_card]
    show_card = display(state, current_card)
    return Page(state, content=[
        Button(text="Back", url="/index"),
        Button(text="Randomize Cards", url="/randomize"),
        Row(reveal_text),
        Row(show_card)
        ])

@route
def randomize(state: State) -> Page:
    all_cards = state.cards
    randomized_sorted_cards = sort_cards(randomize_card_ids(all_cards))
    state.randomized = True
    state.cards = randomized_sorted_cards
    return quiz_page(state)

def display(state: State, card: Card) -> PageContent:
    all_cards = state.cards
    card_id = Argument("card_id", card.card_id)
    if not card.revealed:
        return Div(
            "Front Side",
            Row(card.front),
            Row(Button(text='Reveal Back Side', url="show_back", arguments=card_id),
                Button(text='Next Card', url="/next_card"),
                Button(text='Previous Card', url="/prev_card")
                )
            )
    else:
        return Div(
            "Back Side",
            Row(card.back),
            Row(Button(text="Reveal Front Side", url="show_front", arguments=card_id),
                Button(text="Next Card", url="/next_card"),
                Button(text="Previous Card", url="/prev_card")
                )
            )
    
@route
def next_card(state: State) -> Page:
    all_cards = state.cards
    if state.current_card< len(state.cards) - 1:
        state.current_card += 1
    all_cards[state.current_card].revealed = False
    return quiz_page(state)

@route
def prev_card(state: State) -> Page:
    all_cards = state.cards    
    if state.current_card > 0:
        state.current_card -= 1
    all_cards[state.current_card].revealed = False
    return quiz_page(state)
    
@route
def show_back(state: State, card_id: int) -> Page:
    all_cards = state.cards
    for card in all_cards:
        if card_id == card.card_id:
            card.revealed = True
            return quiz_page(state)

@route
def show_front(state: State, card_id: int) -> Page:
    all_cards = state.cards
    for card in all_cards:
        if card_id == card.card_id:
            card.revealed = False
            return quiz_page(state)

def randomize_card_ids(cards: list[Card]) -> list[Card]:
    number_of_cards = len(cards)
    numbers_used = []
    new_cards = []
    for card in cards:
        random_number = random.randint(0, number_of_cards)
        check = True
        while check:
            if random_number in numbers_used:
                random_number = random.randint(0, number_of_cards)
            else:
                check = False
                numbers_used.append(random_number) 
        card.card_id = random_number
        new_cards.append(card)
    return new_cards

def sort_cards(cards: list[Card]) -> list[Card]:
    # Iterate through each list index
    for i, card in enumerate(cards):
        j = i - 1
        # Go back through the list to find next smallest
        while j >= 0 and cards[j].card_id > card.card_id:
            # Swap element backwards
            cards[j+1] = cards[j]
            j -= 1
        # Swap that element into the target index
        cards[j+1] = card
    return cards

test_state = State([], 0, 0, False)
start_server(test_state)
