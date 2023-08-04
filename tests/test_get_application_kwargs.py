from typing import Any

import pytest
from zimran.config import Environment

from zimran.fastapi import _get_application_kwargs, _PRODUCTION_APPLICATION_KWARGS


@pytest.mark.parametrize(
    'environment, application_kwargs',
    [
        (Environment.DEVELOPMENT, {}),
        (Environment.STAGING, {}),
        (Environment.PRODUCTION, _PRODUCTION_APPLICATION_KWARGS),
    ],
)
def test_get_application_kwargs(
    environment: Environment, application_kwargs: dict[str, Any],
) -> None:
    assert _get_application_kwargs(environment) == application_kwargs
