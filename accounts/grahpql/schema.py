import graphene

from accounts.models import GenieUser, Network, Wallet
from graphene_django import DjangoObjectType


class NetworkType(DjangoObjectType):
    class Meta:
        model = Network


class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet


class GenieUserType(DjangoObjectType):
    aptos_wallets = graphene.NonNull(graphene.List(graphene.NonNull(WalletType)))

    def resolve_aptos_wallets(value_obj, _):
        wallets = value_obj.wallet.filter(network__title="Aptos").order_by("-id")
        return wallets

    class Meta:
        model = GenieUser