from django.contrib.auth.models import User
from rest_framework import serializers

from . import models as models

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'password']
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PurchaseRequestSerializer(serializers.ModelSerializer):
    nft_token = serializers.CharField(source='nft.token', read_only=True)
    sender_id = serializers.ReadOnlyField(source='sender.id')
    receiver_id = serializers.ReadOnlyField(source='receiver.id')
    datetime_accepted = serializers.DateTimeField(read_only=True)
    is_accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.PurchaseRequest
        fields = ['nft_token', 'sender_id', 'receiver_id', 'datetime_sent', 'is_accepted', 'datetime_accepted']

class NFTCollectibleSerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source='owner.id')
    bids = serializers.ListField(child=PurchaseRequestSerializer(), read_only=True)
    class Meta:
        model = models.NFTCollectible
        fields = ['token', 'name', 'description', 'image', 'tier', 'owner_id', 'bids']

class LootboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LootboxTier
        fields = ['included_tiers', 'price']

class PlayerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    # account_id = serializers.ReadOnlyField(source='account.id')
    spacebucks = serializers.FloatField(read_only=True)
    coins = serializers.IntegerField(read_only=True)
    collectibles = NFTCollectibleSerializer(many=True, read_only=True)
    class Meta:
        model = models.Player
        fields = ['id', 'username', 'profile_image', 'spacebucks', 'coins', 'collectibles']