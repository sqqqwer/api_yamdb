from typing import Final

STR_OUTPUT_LIMIT: Final[int] = 30
NAME_MAX_LENGTH: Final[int] = 256
SLUG_MAX_LENGTH: Final[int] = 50
FIELD_MAX_LENGTH: Final[int] = 254
CONFIRMATION_CODE_MAX_LENGTH: Final[int] = 40
ROLE_INDEX: Final[int] = 0
DEFAULT_ROLE: Final[str] = 'user'
ROLE_USER: Final[str] = 'user'
ROLE_MODERATOR: Final[str] = 'moderator'
ROLE_ADMIN: Final[str] = 'admin'


ROLES = (
    (ROLE_USER, 'user'),
    (ROLE_MODERATOR, 'moderator'),
    (ROLE_ADMIN, 'admin')
)
