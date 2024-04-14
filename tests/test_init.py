import pytest

from aiosolaredge import SolarEdge


@pytest.mark.asyncio
async def test_create_object():
    """Creating an object works as expected."""
    solar_edge = SolarEdge("API_KEY")
    assert solar_edge.timeout == 10
    assert solar_edge.api_key == "API_KEY"
    assert solar_edge._created_session is True
    await solar_edge.close()
