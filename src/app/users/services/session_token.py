import core.settings as config
from app.users.services.user import UserService
from core.error_handlers import AppError
from core.resources.jwt import JWTClient
from core.utils.utils import BaseService


class SessionTokenService(BaseService):
    user_service = UserService
    jwt_client = JWTClient(config)

    def generate_token(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            self.logger.error(
                "SessionTokenService.generate_token(): Email or password not provided"
            )
            err_msg = "Email and password are required"
            return [True, err_msg, 400]

        user = self.user_service.get(self, email=email)
        if not user or not self.user_service.check_password(self, email, password):
            self.logger.error(
                "SessionTokenService.generate_token(): Invalid Credentials for user: %s",
                email,
            )
            err_msg = "Invalid Credentials"
            # raise AppError(401, err_msg)
            return [True, err_msg, 401]

        jwt_token = self.jwt_client.create_token(str(user["_id"]))
        return [False, jwt_token, 200]
