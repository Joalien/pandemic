# TODO add cheat cards
class CheatCard:

    def __init__(self, capacity: str):
        self.name: str = capacity

    def __str__(self):
        return f'CheatCard({self.name}'

    def __repr__(self):
        return self.__str__()
