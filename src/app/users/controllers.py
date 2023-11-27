from flask import request
from flask_restful import Resource

from app.users.services.session_token import SessionTokenService
from core.utils import Response


class AuthController(Resource):
    token_service = SessionTokenService()

    def post(self):
        data = request.json
        [err, data, status_code] = self.token_service.generate_token(data)
        if err:
            return Response(success=False, message=data, status_code=status_code)

        return Response(
            success=True, message="Login Successful", data=data, status_code=status_code
        )
