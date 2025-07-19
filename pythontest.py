import asyncio
from unittest.mock import AsyncMock


async def greet():
    return "hello"


mock = AsyncMock(return_value="hi")
print(asyncio.run(mock()))
