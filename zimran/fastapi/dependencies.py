from typing import Annotated

from fastapi import Header, HTTPException, status


def get_user_id(user_id: Annotated[int | None, Header(alias='x-zmrn-user-id')] = None) -> int:
    if user_id:
        return user_id

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
