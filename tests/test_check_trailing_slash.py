import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


async def test(app: FastAPI) -> None:
    with pytest.raises(AssertionError):
        with TestClient(app):
            pass
