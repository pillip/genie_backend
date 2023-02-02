import graphene

from accounts.models import GenieUser, Wallet
from accounts.grahpql.schema import GenieUserType


class AccountQuery(graphene.ObjectType):
    user_info = graphene.Field(graphene.NonNull(GenieUserType), discord_id=graphene.String(required=True))
    wallet_owner = graphene.NonNull(graphene.String, wallet_address=graphene.String(required=True))

    def resolve_user_info(self, _, **kwargs):
        discord_id = kwargs('id').strip()
        user = GenieUser.get_by_discordid(discord_id=discord_id)

        return user

    def resolve_wallet_owner(self, _, **kwargs):
        wallet_address = kwargs('id').strip()
        wallet = Wallet.get_by_address(address=wallet_address)

        return wallet.user.discord_id