## Installation

```bash
pip install zimran-fastapi
```

## Usage

```python
from zimran.config import CommonSettings
from zimran.fastapi import create_app


class Settings(CommonSettings):
    pass


settings = Settings()

app = create_app(settings.environment)
```

```python
from fastapi import Depends, Response
from zimran.fastapi.dependencies import get_user_id


async def handler(user_id: int = Depends(get_user_id)) -> Response:
    pass
```
