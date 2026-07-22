from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    CONTROLLER = "Controller"
    SUPERVISOR = "Supervisor"
    LOBBY_OPERATOR = "Lobby Operator"
    VIEWER = "Viewer"


class Department(str, Enum):
    DRIVER = "Driver"
    CONDUCTOR = "Conductor"
    PLATFORM_STAFF = "Platform Staff"
    SECURITY = "Security"
    MAINTENANCE = "Maintenance"
    ADMIN_STAFF = "Admin Staff"


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
    NO_SHOW = "No Show"


class AvailabilityStatus(str, Enum):
    AVAILABLE = "Available"
    ON_LEAVE = "On Leave"
    SICK_LEAVE = "Sick Leave"
    UNAVAILABLE = "Unavailable"


class CrewStatus(str, Enum):
    SIGNED_ON = "Signed On"
    SIGNED_OFF = "Signed Off"
    AVAILABLE = "Available"
    CALLED = "Called"
    RESTING = "Resting"
    RUNNING = "Running"
    OFF_DUTY = "Off Duty"


class ImportStatus(str, Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    PARTIAL = "Partial"
    DUPLICATE = "Duplicate"


class NotificationType(str, Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"
    SUCCESS = "Success"


class UserStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    LOCKED = "Locked"
    SUSPENDED = "Suspended"
