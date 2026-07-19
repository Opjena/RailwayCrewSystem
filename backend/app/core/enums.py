from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    CONTROLLER = "Controller"
    SUPERVISOR = "Supervisor"
    LOBBY_OPERATOR = "LobbyOperator"
    VIEWER = "Viewer"