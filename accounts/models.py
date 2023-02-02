from django.db import models

from genie_backend.utils.models import PrintableMixin
from genie_backend.utils import errors


class GenieUser(models.Model, PrintableMixin):
    class Meta:
        verbose_name = "디스코드 유저 정보"
        verbose_name_plural = "디스코드 유저 정보"

    discord_id = models.CharField(
        verbose_name="Discord id",
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        help_text="Discord에 기록되는 고유한 유저의 hash된 id 값",
    )

    name = models.CharField(
        verbose_name="이름",
        max_length=50,
        blank=False,
        null=False,
        help_text="Discord nickname",
    )

    discriminator = models.IntegerField(
        verbose_name="Discriminator",
        null=False,
        help_text="Discord discriminator"
    )

    avatar = models.URLField(
        verbose_name="Discord Profile",
        null=True,
        blank=True,
        default="",
        help_text="Discord Profile URL",
    )

    @classmethod
    def get_by_discordid(cls, discord_id):
        try:
            user = cls.objects.get(discord_id=discord_id)
        except cls.DoesNotExist:
            raise errors.UserNotFound

        return user

    def __str__(self):
        return f"{self.name}#{str(self.discriminator)}"


class Network(models.Model, PrintableMixin):
    class Meta:
        verbose_name = "블록체인 네트워크"
        verbose_name_plural = "블록체인 네트워크"

    title = models.CharField(
        verbose_name="이름",
        max_length=30,
        blank=False,
        null=False,
        unique=True,
        help_text="블록체인 네트워크 이름"
    )

    @classmethod
    def get_by_title(cls, title):
        try:
            network = cls.objects.get(title=title)
        except cls.DoesNotExist:
            raise errors.NetworkNotFound

        return network

    def __str__(self):
        return f"{self.title}"


class Wallet(models.Model, PrintableMixin):
    class Meta:
        verbose_name = "유저 지갑 정보"
        verbose_name_plural = "유저 지갑 정보"
        constraints = [
            models.UniqueConstraint(
                fields=["network", "address"],
                name="unique wallet address",
            ),
            models.UniqueConstraint(
                fields=["user", "network", "address"],
                name="Wallet can be owned by only one user",
            )
        ]

    user = models.ForeignKey(
        GenieUser,
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    network = models.ForeignKey(
        Network,
        on_delete=models.CASCADE,
        related_name="owns_wallet"
    )

    address = models.CharField(
        verbose_name="지갑주소",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="지갑주소"
    )

    @classmethod
    def get_wallet(cls, user, network, address):
        try:
            wallet = cls.objects.get(user=user, network=network, address=address)
        except cls.DoesNotExist:
            raise errors.WalletNotFound

        return wallet

    @classmethod
    def get_by_address(cls, address, network=None):
        if network is None:
            network = Network.objects.get(title="Aptos")

        try:
            wallet = cls.objects.get(network=network, address=address)
        except cls.DoesNotExist:
            raise errors.WalletNotFound

        return wallet

    def __str__(self):
        return f"{self.user.name} : ({self.network}){self.address}"