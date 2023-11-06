from typing import Any

from pytest import fixture


@fixture(scope="session")
def anyio_backend() -> Any:
    return ("asyncio", {"use_uvloop": True})
