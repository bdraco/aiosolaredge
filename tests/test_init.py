import datetime
import re

import aiohttp
import pytest
from aioresponses import aioresponses

from aiosolaredge import SolarEdge


@pytest.mark.asyncio
async def test_create_object():
    """Creating an object works as expected."""
    solar_edge = SolarEdge("API_KEY")
    assert solar_edge.timeout == 10
    assert solar_edge.api_key == "API_KEY"
    assert solar_edge._created_session is True
    await solar_edge.close()


@pytest.mark.asyncio
async def test_create_object_passed_session():
    """Creating an object works as expected with a passed session."""
    session = aiohttp.ClientSession()
    solar_edge = SolarEdge("API_KEY", session)
    assert solar_edge.timeout == 10
    assert solar_edge.api_key == "API_KEY"
    assert solar_edge._created_session is False
    await solar_edge.close()
    await session.close()


@pytest.mark.asyncio
async def test_simple_requests() -> None:
    """Creating an object works as expected."""
    with aioresponses() as mocked:
        solar_edge = SolarEdge("API_KEY")
        assert solar_edge.timeout == 10
        assert solar_edge.api_key == "API_KEY"
        assert solar_edge._created_session is True
        mocked.get(
            "https://monitoringapi.solaredge.com/site/123/details?api_key=API_KEY",
            payload={"details": "details"},
        )
        assert await solar_edge.get_details(123) == {"details": "details"}
        mocked.get(
            "https://monitoringapi.solaredge.com/site/123/overview?api_key=API_KEY",
            payload={"overview": "overview"},
        )

        assert await solar_edge.get_overview(123) == {"overview": "overview"}
        mocked.get(
            "https://monitoringapi.solaredge.com/site/123/inventory?api_key=API_KEY",
            payload={"inventory": "inventory"},
        )
        assert await solar_edge.get_inventory(123) == {"inventory": "inventory"}

        mocked.get(
            "https://monitoringapi.solaredge.com/site/123/currentPowerFlow?api_key=API_KEY",
            payload={"currentPowerFlow": "currentPowerFlow"},
        )
        assert await solar_edge.get_current_power_flow(123) == {
            "currentPowerFlow": "currentPowerFlow"
        }

        pattern = re.compile(
            r"^https://monitoringapi\.solaredge\.com/site/123/energyDetails"
        )
        mocked.get(
            pattern,
            payload={"energyDetails": "energyDetails"},
        )
        assert await solar_edge.get_energy_details(
            123, datetime.datetime.now(), datetime.datetime.now()
        ) == {"energyDetails": "energyDetails"}

        pattern = re.compile(
            r"^https://monitoringapi\.solaredge\.com/site/123/energyDetails.*meters="
        )
        mocked.get(
            pattern,
            payload={"meters": "meters"},
        )
        assert await solar_edge.get_energy_details(
            123, datetime.datetime.now(), datetime.datetime.now(), meters=["FEEDIN"]
        ) == {"meters": "meters"}
        await solar_edge.close()
