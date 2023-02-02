import graphene

from accounts.models import GenieUser, Network, Wallet
from accounts.grahpql.schema import GenieUserType


class CreateOrUpdateUserInfo(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    user_info = graphene.Field(graphene.NonNull(GenieUserType))

    class Arguments:
        discord_id = graphene.String(required=True)
        name = graphene.String(required=True)
        discriminator = graphene.Int(required=True)
        avatar = graphene.String()

    def mutate(self, _, discord_id, name, discriminator, avatar):
        user = GenieUser.objects.get_or_create(discord_id=discord_id)

        user.name = name
        user.discriminator = discriminator

        if not avatar:
            user.avatar = avatar

        user.save()

        return CreateOrUpdateUserInfo(
            success=True,
            user_info=user,
        )


class VerifyUser(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        discord_id = graphene.String(required=True)
        wallet_address = graphene.String(required=True)
        # network_title = graphene.String(required=True)

    def mutate(self, _, discord_id, wallet_address):
        user = GenieUser.get_by_discordid(discord_id)
        network = Network.objects.get(title="Aptos")

        try:
            wallet = Wallet.get_wallet(user=user, network=network, address=wallet_address)
        except Exception:
            wallet = Wallet.objects.create(
                user=user,
                network=network,
                address=wallet_address
            )

        return VerifyUser(
            success=True
        )


class AccountMutation(graphene.ObjectType):
    create_or_update_user_info = CreateOrUpdateUserInfo.Field()
    verify_user = VerifyUser.Field()