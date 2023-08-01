## Installation

```bash
pip install zimran-fastapi
```

## Usage

```python
from zimran.fastapi import create_app

app = create_app()
```

```python
from fastapi import Depends, Response
from zimran.fastapi.dependencies import get_user_id


async def handler(user_id: int = Depends(get_user_id)) -> Response:
    pass
```
