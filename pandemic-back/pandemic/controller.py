import functools
import random
from typing import List, Tuple

from pandemic.View.InputView.DummyInputView import DummyInputView
from pandemic.View.OutputView.ConsoleOutputView import ConsoleOutputView
from pandemic.View.OutputView.OutputView import OutputView
from pandemic.model.Card.Card import Card
from pandemic.model.Card.CityCard import CityCard
from pandemic.model.Card.EpidemicCard import EpidemicCard
from pandemic.model.City import City
from pandemic.model.Color import Color
from pandemic.model.Player import Player
from pandemic.model.World import World

MAX_NUMBER_OF_DISEASE: int = 24
MAX_NUMBER_OF_OUTBREAK: int = 8
MAX_NUMBER_OF_SAME_DISEASE_IN_CITY: int = 3
cities_that_spread_during_turn: List[City] = []

input_view = DummyInputView()
OutputView.INSTANCE = ConsoleOutputView()


def start_game():
    world = init_game()
    play_game(world)


def play_game(world):
    while not play_turn(world):
        pass


def play_turn(world) -> bool:
    OutputView.INSTANCE.show_message(str(world))
    for _ in range(4):  # execute 4 actions
        action, arg = input_view.get_action()  # Because python does not have do-while mechanism
        while not action.execute_action(world, arg):
            action, arg = input_view.get_action()
    for _ in range(2):  # pick 2 cards
        player_picked_epidemic_card = pick_player_card(world.player_cards, world.current_player)
        if player_picked_epidemic_card:
            world.current_spreading_rate += 1

            city = pick_first_disease_card(world)
            OutputView.INSTANCE.show_message(f'An new epidemic happened in {city.name}!')
            world.number_of_outbreak += infect_city(city, city.color, MAX_NUMBER_OF_SAME_DISEASE_IN_CITY)

            random.shuffle(world.discard_disease_cards)
            for _ in range(len(world.discard_disease_cards)):
                world.disease_cards.append(world.discard_disease_cards.pop())

    world.number_of_outbreak += propagate_diseases(world)

    return next_turn(world)


def propagate_diseases(world) -> int:
    number_of_outbreak = 0
    for _ in range(world.spreading_rate):
        city: City = pick_disease_card(world)
        OutputView.INSTANCE.show_message(f'An disease happened in {city.name}')
        number_of_outbreak += infect_city(city, city.color, 1)
        cities_that_spread_during_turn.clear()
    return number_of_outbreak


def next_turn(world) -> bool:
    next_player(world.players)
    return check_if_game_is_lost(world)


def check_if_game_is_lost(world) -> bool:
    number_of_disease = max(functools.reduce(merge_dict, map(lambda c: c.diseases, world.cities)).values())
    rules: List[Tuple[bool, str]] = [
        (world.number_of_outbreak >= MAX_NUMBER_OF_OUTBREAK, "Too many outbreak"),
        (not world.player_cards, "No more player card"),
        (number_of_disease > MAX_NUMBER_OF_DISEASE, "Too many diseases")
    ]
    for rule in rules:
        if rule[0]:
            OutputView.INSTANCE.show_message(rule[1])
            return True
    return False


def merge_dict(a: dict[Color, int], b: dict[Color, int]) -> dict[Color, int]:
    for key, value in b.items():
        a[key] += value
    return a


def next_player(players: List[Player]):
    players.append(players.pop(0))


def infect_first_cities(world):
    for number_of_disease in range(1, 4):
        for _ in range(3):
            city: City = pick_disease_card(world)
            infect_city(city, city.color, number_of_disease)


def infect_city(city: City, color: Color, number_of_disease: int) -> int:
    city.diseases[color] += number_of_disease
    if city.diseases[color] > MAX_NUMBER_OF_SAME_DISEASE_IN_CITY and city not in cities_that_spread_during_turn:
        # TODO test me
        OutputView.INSTANCE.show_message(f'An outbreak happened in {city.name}')
        cities_that_spread_during_turn.append(city)
        return outbreak(city, color)
    return 0


def outbreak(city: City, color: Color) -> int:  # éclosion
    city.diseases[color] = MAX_NUMBER_OF_SAME_DISEASE_IN_CITY
    return sum([infect_city(c, color, 1) for c in city.neighbors])


def init_players_hand(world, initial_number_of_cards=8):
    for i in range(initial_number_of_cards):
        pick_player_card(world.player_cards, world.players[i % len(world.players)])


def init_game(number_of_player=1, number_of_epidemic_card=6) -> World:
    init_cities()

    starting_city: City = random.choice(City.cities)
    starting_city.construct_research_center()

    players = init_players(number_of_player, starting_city)

    world = World(City.cities, players, init_player_cards(), init_disease_cards())

    infect_first_cities(world)
    init_players_hand(world)
    add_epidemic_cards(world.player_cards, number_of_epidemic_card)
    return world


def init_players(number_of_player: int, starting_city: City) -> List[Player]:
    return [Player(f'Player {i}', starting_city) for i in range(1, number_of_player + 1)]


def init_disease_cards() -> List[CityCard]:
    disease_cards = [CityCard(c) for c in City.cities]
    random.shuffle(disease_cards)
    return disease_cards


def init_player_cards() -> List[Card]:
    player_cards: List[Card] = [CityCard(c) for c in City.cities]
    # player_cards.append(CheatCard()) // TODO add cheat cards later
    random.shuffle(player_cards)
    return player_cards


def add_epidemic_cards(player_cards: List[Card], number_of_epidemic_card: int):
    [player_cards.append(EpidemicCard()) for _ in range(number_of_epidemic_card)]
    random.shuffle(player_cards)


def init_cities():
    santiago = City("Santiago", Color.YELLOW)
    lima = City("Lima", Color.YELLOW)
    mexico = City("Mexico", Color.YELLOW)
    los_angeles = City("Los Angeles", Color.YELLOW)
    miami = City("Miami", Color.YELLOW)
    bogota = City("Bogota", Color.YELLOW)
    buenos_aires = City("Buenos Aires", Color.YELLOW)
    sao_paulo = City("Sãu Paulo", Color.YELLOW)
    lagos = City("Lagos", Color.YELLOW)
    kinshasa = City("Kinshasa", Color.YELLOW)
    khartoum = City("Khartoum", Color.YELLOW)
    johannesburg = City("Johannesburg", Color.YELLOW)

    santiago.add_neighbors(lima)
    lima.add_neighbors(santiago, mexico, bogota)
    mexico.add_neighbors(los_angeles, miami, bogota, lima)
    los_angeles.add_neighbors(mexico)
    miami.add_neighbors(mexico, bogota)
    bogota.add_neighbors(miami, mexico, lima, sao_paulo, buenos_aires)
    buenos_aires.add_neighbors(bogota, sao_paulo)
    sao_paulo.add_neighbors(bogota, buenos_aires, lagos)
    lagos.add_neighbors(sao_paulo, kinshasa, khartoum)
    kinshasa.add_neighbors(lagos, khartoum, johannesburg)
    khartoum.add_neighbors(lagos, kinshasa, johannesburg)
    johannesburg.add_neighbors(kinshasa, khartoum)


def pick_disease_card(world) -> City:
    city_card: CityCard = world.disease_cards.pop()
    return discard_city_card(city_card, world)


def pick_first_disease_card(world) -> City:
    city_card: CityCard = world.disease_cards.pop(0)
    return discard_city_card(city_card, world)


def discard_city_card(city_card, world) -> City:
    world.discard_disease_cards.append(city_card)
    return city_card.city


def pick_player_card(player_cards: List[Card], player: Player) -> bool:
    card: Card = player_cards.pop()
    OutputView.INSTANCE.show_message(f'{player.name} picked {card}')
    if isinstance(card, EpidemicCard):
        return True
    else:
        player.hand.append(card)
        return False
