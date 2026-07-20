from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    CONTROLLER = "Controller"
    SUPERVISOR = "Supervisor"
    LOBBY_OPERATOR = "LobbyOperator"
    VIEWER = "Viewer"


class Department(str, Enum):
    DRIVER = "Driver"
    CONDUCTOR = "Conductor"
    PLATFORM_STAFF = "PlatformStaff"
    SECURITY = "Security"
    MAINTENANCE = "Maintenance"
    ADMIN_STAFF = "AdminStaff"


class ShiftType(str, Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    NIGHT = "Night"
    EXTENDED = "Extended"


class AssignmentStatus(str, Enum):
    ASSIGNED = "Assigned"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "NoShow"


class AvailabilityStatus(str, Enum):
    AVAILABLE = "Available"
    ON_LEAVE = "OnLeave"
    SICK_LEAVE = "SickLeave"
    UNAVAILABLE = "Unavailable"
