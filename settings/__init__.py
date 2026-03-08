from dataclasses import dataclass
from typing import Any, Type

modules: dict[str, dict[str, "SettingSpec"]] = dict()

TABLE_NAME = 'settings'


@dataclass(frozen=True)
class SettingSpec:
    name: str
    description: str = ""
    type: Type[Any] | None = None


def registerModule(module: str, setting_specs: list[SettingSpec] | None = None) -> None:
    """
    Register a setting module. Always includes "enabled". Optionally add more specs.
    """
    specs = {s.name: s for s in (setting_specs or [])}
    specs["enabled"] = SettingSpec(
        "enabled",
        description="Whether this module is enabled",
        type=bool,
    )
    modules[module] = specs
