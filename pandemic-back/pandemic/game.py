import functools
import random
from typing import List, Tuple

from pandemic.models import City, EpidemicCard, Color, Player, World, DiseaseCard, PlayerCard, \
    OutOfDiseaseCardError
from pandemic.view.InputView.DummyInputView import DummyInputView
from pandemic.view.OutputView.ConsoleOutputView import ConsoleOutputView
from pandemic.view.OutputView.OutputView import OutputView

MAX_NUMBER_OF_DISEASE: int = 24
MAX_NUMBER_OF_OUTBREAK: int = 8
MAX_NUMBER_OF_SAME_DISEASE_IN_CITY: int = 3
cities_that_spread_during_turn: List[City] = []

input_view = DummyInputView()
OutputView.INSTANCE = ConsoleOutputView()


def play_game():
    world = init_game()
    try:
        while not play_turn(world):
            pass
    except OutOfDiseaseCardError:
        OutputView.INSTANCE.show_message("You lose because all disease cards have been discarded")


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
            world.number_of_outbreak += infect_city(city, Color(city.color), MAX_NUMBER_OF_SAME_DISEASE_IN_CITY)

            random.shuffle(world.discard_disease_cards)
            for _ in range(len(world.discard_disease_cards)):
                world.disease_cards.append(world.discard_disease_cards.pop())

    world.number_of_outbreak += propagate_diseases(world)

    return next_turn(world)


def propagate_diseases(world) -> int:
    number_of_outbreak = 0
    for _ in range(world.spreading_rate):
        city: City = pick_disease_card(world)
        OutputView.INSTANCE.show_message(f'A disease happened in {city.name}')
        number_of_outbreak += infect_city(city, Color(city.color), 1)
        cities_that_spread_during_turn.clear()
    return number_of_outbreak


def next_turn(world) -> bool:
    next_player(world)
    return check_if_game_is_lost(world)


def check_if_game_is_lost(world) -> bool:
    number_of_disease = max(
        functools.reduce(merge_dict, map(lambda c: c.diseases, world.cities.all())).values())
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


def next_player(world):
    world.current_player = world.current_player.next_player
    world.save()


def infect_city(city: City, color: Color, number_of_disease: int) -> int:
    city.diseases[color] += number_of_disease
    if city.diseases[color] > MAX_NUMBER_OF_SAME_DISEASE_IN_CITY and city not in cities_that_spread_during_turn:
        # TODO test me
        OutputView.INSTANCE.show_message(f'An outbreak happened in {city.name}')
        cities_that_spread_during_turn.append(city)
        return outbreak(city, color)
    city.save()
    return 0


def outbreak(city: City, color: Color) -> int:  # éclosion
    city.diseases[color] = MAX_NUMBER_OF_SAME_DISEASE_IN_CITY
    city.save()
    return sum([infect_city(c, color, 1) for c in city.neighbors.all()])


def pick_disease_card(world) -> City:
    disease_card: DiseaseCard = world.disease_cards.all()\
        .filter(is_discarded=False)\
        .order_by('index')\
        .first()
    if disease_card is None:
        raise OutOfDiseaseCardError
    disease_card.is_discarded = True
    disease_card.save()
    return disease_card.city


def pick_first_disease_card(world) -> City:
    city_card: DiseaseCard = world.disease_cards.pop(0)
    return discard_city_card(city_card)


def discard_city_card(world, city_card) -> City:
    world.discard_disease_cards.append(city_card)
    return city_card.city


def pick_player_card(player_cards: List[PlayerCard], player: Player) -> bool:
    card: PlayerCard = player_cards\
        .filter(player=None)\
        .order_by('index')\
        .first()
    OutputView.INSTANCE.show_message(f'{player.name} picked {card}')
    if isinstance(card, EpidemicCard):
        return True
    else:
        card.player = player
        card.save()
        return False


def init_game(number_of_player=1, number_of_epidemic_card=6) -> World:
    world = World()
    world.save()
    init_cities(world)

    starting_city: City = random.choice(world.cities.all())
    starting_city.construct_research_center()

    init_players(world, number_of_player, starting_city)
    init_player_cards(world)
    init_disease_cards(world)

    infect_first_cities(world)
    init_players_hand(world)
    add_epidemic_cards(world, number_of_epidemic_card)
    return world


def init_players_hand(world, initial_number_of_cards=8):
    player: Player = world.players.first()
    for _ in range(initial_number_of_cards):
        pick_player_card(world.player_cards, player)
        player = player.next_player


def init_players(world: World, number_of_player: int, starting_city: City):
    players = [Player(world=world, name=f'Player {i}', position=starting_city) for i in range(1, number_of_player + 1)]
    for i in range(len(players)):
        players[i].save()
        players[i].next_player = players[(i + 1) % len(players)]
    [player.save() for player in players]
    world.current_player = players[0]
    world.save()


def init_cities(world: World):
    santiago = City(world=world, name="Santiago", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    lima = City(world=world, name="Lima", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    mexico = City(world=world, name="Mexico", color=Color.YELLOW, position=({'x': 125, 'y': 318}))
    los_angeles = City(world=world, name="Los Angeles", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    miami = City(world=world, name="Miami", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    bogota = City(world=world, name="Bogota", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    buenos_aires = City(world=world, name="Buenos Aires", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    sao_paulo = City(world=world, name="Sãu Paulo", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    lagos = City(world=world, name="Lagos", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    kinshasa = City(world=world, name="Kinshasa", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    khartoum = City(world=world, name="Khartoum", color=Color.YELLOW, position=({'x': 60, 'y': 294}))
    johannesburg = City(world=world, name="Johannesburg", color=Color.YELLOW, position=({'x': 60, 'y': 294}))

    santiago.save()
    lima.save()
    mexico.save()
    los_angeles.save()
    miami.save()
    bogota.save()
    buenos_aires.save()
    sao_paulo.save()
    lagos.save()
    kinshasa.save()
    khartoum.save()
    johannesburg.save()

    santiago.neighbors.add(lima)
    lima.neighbors.add(santiago, mexico, bogota)
    mexico.neighbors.add(los_angeles, miami, bogota, lima)
    los_angeles.neighbors.add(mexico)
    miami.neighbors.add(mexico, bogota)
    bogota.neighbors.add(miami, mexico, lima, sao_paulo, buenos_aires)
    buenos_aires.neighbors.add(bogota, sao_paulo)
    sao_paulo.neighbors.add(bogota, buenos_aires, lagos)
    lagos.neighbors.add(sao_paulo, kinshasa, khartoum)
    kinshasa.neighbors.add(lagos, khartoum, johannesburg)
    khartoum.neighbors.add(lagos, kinshasa, johannesburg)
    johannesburg.neighbors.add(kinshasa, khartoum)

    santiago.save()
    lima.save()
    mexico.save()
    los_angeles.save()
    miami.save()
    bogota.save()
    buenos_aires.save()
    sao_paulo.save()
    lagos.save()
    kinshasa.save()
    johannesburg.save()
    khartoum.save()


def init_disease_cards(world):
    indexes = list(range(len(world.cities.all())))
    random.shuffle(indexes)
    [DiseaseCard(world=world, city=city, index=indexes.pop()).save() for city in world.cities.all()]


def init_player_cards(world):
    indexes = list(range(len(world.cities.all())))
    random.shuffle(indexes)
    [PlayerCard(world=world, city=city, index=indexes.pop()).save() for city in world.cities.all()]


def infect_first_cities(world):
    for number_of_disease in range(1, 4):
        for _ in range(3):
            city: City = pick_disease_card(world)
            infect_city(city, Color(city.color), number_of_disease)


def add_epidemic_cards(world: World, number_of_epidemic_card: int):
    cards = world.player_cards.all().filter(player=None).all()
    indexes = list(map(lambda x: x.index, cards))
    max_index = max(indexes)
    [indexes.append(max_index + i + 1) for i in range(number_of_epidemic_card)]
    random.shuffle(indexes)

    assert len(indexes) == len(cards) + number_of_epidemic_card
    [EpidemicCard(world=world, index=indexes.pop(), name='Epidemic!').save() for _ in range(number_of_epidemic_card)]
    for c in cards:
        c.index = indexes.pop()
        c.save()

