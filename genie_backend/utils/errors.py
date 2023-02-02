from graphene_django.views import GraphQLView as BaseGraphQLView
from django.http import JsonResponse


class GraphQLView(BaseGraphQLView):
    @staticmethod
    def format_error(error):
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)

        try:
            formatted_error["context"] = error.original_error.context
        except AttributeError:
            pass

        return formatted_error


class GenieGraphQLException(Exception):
    message = None
    status = 200
    error_msg = None

    def __init__(
        self,
    ):
        self.context = {}

        if self.status:
            self.context["status"] = self.status

        if self.error_msg:
            self.context["error_msg"] = self.error_msg

        super().__init__(self.message)


class UserNotFound(GenieGraphQLException):
    error_code = "A00001"
    message = "Does Not Exist!!!"
    status = 400
    error_msg = "존재하지 않는 유저입니다. 다시 확인해 주세요."


class NetworkNotFound(GenieGraphQLException):
    error_code = "A00002"
    message = "Does Not Exist!!!"
    status = 400
    error_msg = "존재하지 않는 네트워크입니다. 다시 확인해 주세요."


class WalletNotFound(GenieGraphQLException):
    error_code = "A00003"
    message = "Does Not Exist!!!"
    status = 400
    error_msg = "존재하지 않는 지갑입니다. 다시 확인해 주세요."