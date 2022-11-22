from rest_framework.serializers import ModelSerializer

from pandemic.models import World, City, Player, DiseaseCard, PlayerCard


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'world_id', 'name', 'color', 'has_research_center', 'diseases', 'position', 'neighbors']


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'world_id', 'name', 'position_id', 'next_player_id']


class DiseaseCardSerializer(ModelSerializer):
    class Meta:
        model = DiseaseCard
        fields = ['id', 'world_id', 'city_id', 'name', 'index', 'card_ptr_id', 'is_discarded']


class PlayerCardSerializer(ModelSerializer):
    class Meta:
        model = PlayerCard
        fields = ['id', 'world_id', 'city_id', 'name', 'index', 'card_ptr_id', 'player_id']


class WorldSerializer(ModelSerializer):
    players = PlayerSerializer(many=True)
    cities = CitySerializer(many=True)
    player_cards = PlayerCardSerializer(many=True)
    disease_cards = DiseaseCardSerializer(many=True)

    class Meta:
        model = World
        fields = ['id', 'spreading_rate', 'number_of_outbreak', 'are_antidotes_found', 'current_player', 'players',
                  'player_cards', 'disease_cards', 'cities']
