from typing import Any

class InvalidCastMemberTypeException(Exception):
    def __init__(self, invalid_type: Any) -> None:
        self.cast_member_type = invalid_type
        self.message = f"Invalid cast member type {invalid_type}"
        super().__init__(self.message)