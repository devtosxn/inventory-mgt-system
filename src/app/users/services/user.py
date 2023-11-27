import bcrypt

from core.error_handlers import AppError
from core.resources.database import client
from core.utils.utils import BaseService


class UserService(BaseService):
    def get_all(self):
        try:
            users = list(client.db.users.find())
        except Exception as e:
            self.logger.error("UserService.get_all(): %s", str(e))
            raise AppError(500)

        return users

    def get(self, email):
        try:
            user = client.db.users.find_one({"email": email})
        except Exception as e:
            self.logger.error("UserService.get(): %s", str(e))
            raise AppError(500)

        if not user:
            return None

        return user

    def set_password(self, email, password):
        try:
            user = client.db.users.find_one({"email": email})
        except Exception as e:
            self.logger.error("UserService.set_password(): %s", str(e))
            raise AppError(500)

        if not user:
            self.logger.error(
                "UserService.set_password(): User not found for email: %s", email
            )
            raise AppError(404, "User not found")

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_id = user["_id"]
        client.db.users.update_one(
            {"_id": user_id}, {"$set": {"password": hashed_password.decode("utf-8")}}
        )

        return hashed_password.decode("utf-8")

    def check_password(self, email, password):
        try:
            user = client.db.users.find_one({"email": email})
        except Exception as e:
            self.logger.error("UserService.check_password(): %s", str(e))
            raise AppError(500)

        if not user:
            self.logger.error(
                "UserService.check_password(): User not found for email: %s", email
            )
            return False

        is_valid_password = bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        )
        return is_valid_password
