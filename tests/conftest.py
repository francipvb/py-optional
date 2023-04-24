from pytest import fixture


@fixture(scope="session")
def anyio_backend():
    return ("asyncio", {"use_uvloop": True})
