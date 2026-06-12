from enum import Enum, IntEnum


class TaskStatusEnum(IntEnum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
