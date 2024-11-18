from typing import Final

STR_OUTPUT_LIMIT: Final[int] = 30
NAME_MAX_LENGTH: Final[int] = 256
SLUG_MAX_LENGTH: Final[int] = 50
FIELD_MAX_LENGTH: Final[int] = 254
CONFIRMATION_CODE_MAX_LENGTH: Final[int] = 40
DEFAULT_ROLE: Final[str] = 'user'
ROLE_INDEX: Final[int] = 0

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)
