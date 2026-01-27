"""Voice profile sync hook module."""

from typing import Any


async def mount(coordinator: Any, config: dict[str, Any] | None = None):
    """Mount function - register hook handlers."""
    from .hook import MyVoiceSyncHook

    hook = MyVoiceSyncHook(config or {})

    # Register handlers with the hook registry
    unregister_session = coordinator.hooks.register(
        "session:start", hook.handle_session_start, priority=10, name="my-voice-sync"
    )
    unregister_prompt = coordinator.hooks.register(
        "prompt:submit", hook.handle_prompt, priority=10, name="my-voice-sync"
    )

    # Return cleanup function
    def cleanup():
        unregister_session()
        unregister_prompt()

    return cleanup
