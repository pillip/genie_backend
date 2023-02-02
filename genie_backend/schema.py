import graphene

from accounts.grahpql.account_query import AccountQuery
from accounts.grahpql.account_mutation import AccountMutation


class Query(
    AccountQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    AccountMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)