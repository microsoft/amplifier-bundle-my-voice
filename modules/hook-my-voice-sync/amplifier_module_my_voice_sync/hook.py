"""Voice profile sync hook - keeps profiles fresh across long sessions."""

import time
from typing import Any

from amplifier_core import HookResult

from .store import ProfileStore, STALENESS_THRESHOLD


class MyVoiceSyncHook:
    """Hook handlers for voice profile sync.

    Note: This is NOT a subclass - hooks are just callables with handler methods.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        my_voice_config = (config or {}).get("my-voice", {})
        self._store = ProfileStore(my_voice_config)
        self._last_check: float = 0
        self._check_interval = STALENESS_THRESHOLD

    async def handle_session_start(
        self, event: str, data: dict[str, Any]
    ) -> HookResult:
        """Sync profiles on session start."""
        if not self._store.is_configured:
            return HookResult(
                action="inject_context",
                context_injection="""**Voice Profile Not Configured**

To use voice preservation features, add to ~/.amplifier/settings.yaml:

```yaml
config:
  my-voice:
    profile_source: git+https://github.com/YOUR_USER/my-voice-profiles
    # OR for local-only storage:
    profile_source: local
```

Then run: "Build a voice profile for me"
""",
                context_injection_role="system",
            )

        await self._store.sync(force=True)
        self._last_check = time.time()
        return HookResult(action="continue")

    async def handle_prompt(self, event: str, data: dict[str, Any]) -> HookResult:
        """Check staleness before each prompt."""
        if not self._store.is_configured:
            return HookResult(action="continue")

        now = time.time()
        if (now - self._last_check) > self._check_interval:
            self._last_check = now
            if self._store.is_stale:
                await self._store.sync()

        return HookResult(action="continue")
