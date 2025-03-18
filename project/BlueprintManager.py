from flask import Blueprint
from project.user_auth.Members import Members

class BlueprintManager:
    def __init__(self):
        self.blueprints = {}
        self.__starter_blueprint()

    def __starter_blueprint(self):
        self.members = Members()
        self.blueprints['Members'] = self.members.get_blueprint()

    def get_blueprints(self):
        return self.blueprints