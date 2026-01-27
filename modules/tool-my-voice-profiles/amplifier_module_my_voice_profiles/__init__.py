"""Voice profile management tool module."""

from typing import Any


async def mount(coordinator: Any, config: dict[str, Any] | None = None):
    """Mount function called by amplifier-core module loader."""
    from .tool import MyVoiceProfilesTool

    tool = MyVoiceProfilesTool(config or {})
    await coordinator.mount("tools", tool, name=tool.name)
    return tool
