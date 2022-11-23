from rest_framework.serializers import ModelSerializer

from pandemic.models import World, City, Player, DiseaseCard, PlayerCard


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'world_id', 'name', 'color', 'has_research_center', 'diseases', 'position', 'neighbors', 'players_in_city']


class PlayerSerializer(ModelSerializer):
    city = CitySerializer(many=False)

    class Meta:
        model = Player
        fields = ['id', 'world_id', 'name', 'city', 'next_player_id', 'is_current_player']


class DiseaseCardSerializer(ModelSerializer):
    class Meta:
        model = DiseaseCard
        fields = ['id', 'world_id', 'city_id', 'name', 'index', 'is_discarded']


class PlayerCardSerializer(ModelSerializer):
    class Meta:
        model = PlayerCard
        fields = ['id', 'world_id', 'city_id', 'name', 'index', 'player_id']


class WorldSerializer(ModelSerializer):
    # players = PlayerSerializer(many=True)
    # cities = CitySerializer(many=True)
    player_cards = PlayerCardSerializer(many=True)
    disease_cards = DiseaseCardSerializer(many=True)

    class Meta:
        model = World
        fields = ['id', 'current_spreading_rate', 'number_of_outbreak', 'are_antidotes_found', 'players',
                  'player_cards', 'disease_cards', 'cities']
