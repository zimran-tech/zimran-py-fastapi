import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.xfail(raises=AssertionError, strict=True)
async def test(app: FastAPI) -> None:
    with TestClient(app):
        pass
