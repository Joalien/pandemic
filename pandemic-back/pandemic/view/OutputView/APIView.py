from typing import Tuple

from django.db import transaction
from django.http import HttpResponseBadRequest
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pandemic.model.Action.MoveToNeighborCity import MoveToNeighborCity
from pandemic.models import World, Player, City
from pandemic.serializer import WorldSerializer, PlayerSerializer, CitySerializer


# Manual API endpoint declaration. Avoid if possible
# class WorldAPIView(APIView):
#
#     def get_all(self, *args, **kwargs):
#         worlds = World.objects.all()
#         serializer = WorldSerializer(worlds, many=True)
#         return Response(serializer.data)
#
#     def get(self, world_id, **kwargs):
#         world = World.objects.get(world_id)
#         serializer = WorldSerializer(world)
#         return Response(serializer.data)


class WorldViewSet(ModelViewSet):
    serializer_class = WorldSerializer

    def get_queryset(self):
        return World.objects.all()


class PlayerViewSet(ModelViewSet):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.filter(world=self.request.GET.get('world_id'))

    @action(detail=True, methods=['PUT'], url_path='move_to/(?P<city_id>\d+)')
    def move_player_to_city(self, request, pk: int, city_id: int):
        player: Player = Player.objects.filter(id=pk).first()
        city: City = City.objects.filter(id=city_id).first()
        result: Tuple[bool, str] = MoveToNeighborCity.execute_action(player=player, city=city)
        return Response() if result[0] else HttpResponseBadRequest(result[1])


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(world=self.request.GET.get('world_id'))
