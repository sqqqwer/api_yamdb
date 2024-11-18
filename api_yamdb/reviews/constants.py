from typing import Final

STR_OUTPUT_LIMIT: Final[int] = 30
NAME_MAX_LENGTH: Final[int] = 256
SLUG_MAX_LENGTH: Final[int] = 50
PASSWORD_MAX_LENGTH: Final[int] = 254
EMAIL_MAX_LENGTH: Final[int] = 254
ROLE_INDEX: Final[int] = 0
ROLE_USER: Final[str] = 'user'
ROLE_MODERATOR: Final[str] = 'moderator'
ROLE_ADMIN: Final[str] = 'admin'
DEFAULT_ROLE: Final[str] = ROLE_USER
MAX_SCORE_VALUE: Final[int] = 10
MIN_SCORE_VALUE: Final[int] = 1
USERNAME_MAX_LENGTH: Final[int] = 150
DEFAULT_TITLE_RATING: Final[int] = 0
BAN_USERNAME: Final[str] = 'me'
MAX_LENGTH_ROLES = 64


ROLES = (
    (ROLE_USER, 'user'),
    (ROLE_MODERATOR, 'moderator'),
    (ROLE_ADMIN, 'admin')
)

ADD_USER_FIELDS = (
    (None,
     {'fields': ('username',)}
     ),
    (("Personal info"),
     {"fields": ("first_name", "last_name", "email")}
     ),
    (("Permissions"),
     {"fields":
         (
             "is_active",
             "is_staff",
             "is_superuser",
         ),
      }
     ),
    (("Important dates"),
     {"fields": ("date_joined",)})
)
EDIT_USER_FIELDS = (
    (None,
     {'fields': (
         'first_name',
         'last_name',
         'email',
         'role',
         'bio',
         'is_staff',
         'is_active',
         'date_joined'
     )}
     )
)
