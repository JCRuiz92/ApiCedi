import jwt
import datetime
from models.login import LoginSchema


class LoginConfig:
    def __init__(
        self,
        search_field="email",
        password_field="password",
        schema=LoginSchema,
        key=None,
    ):
        self.search_field = search_field
        self.password_field = password_field
        self.schema = schema
        self.__key = key

    @property
    def key(self):
        """ get symmetric key """
        return self.__key

    @key.setter
    def key(self, key):
        """ set symmetric key """
        self.__key = key

    def create_token(self, model, auth_data: dict):
        """Create new session and execute post action(optional)

        Returns:
            token (json): jwt
        """
        search_value = auth_data[self.search_field]
        search_dict = {self.search_field: search_value}

        user = model.query.filter_by(**search_dict).first()

        if not user:
            return {"Authenticate": "Could not verify"}, 401

        password = auth_data[self.password_field]

        if user.compare_passwords(password):
            token = jwt.encode(
                {
                    "id": user.id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                },
                self.login_config.key,
            )
            return {"token": token.decode("UTF-8")}, 201
        return {"Authenticate": "Could not verify"}, 401
