from logging import Logger

from app.Validators.base_validator import BaseValidator


class UserValidator(BaseValidator):
    def __init__(self):
        self.logger = self.create_logger()

    def create_logger(self) -> Logger:
        return Logger(__name__)
