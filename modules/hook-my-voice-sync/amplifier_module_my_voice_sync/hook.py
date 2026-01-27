"""Voice profile sync hook - keeps profiles fresh across long sessions."""

import time
from typing import Any, ClassVar

from amplifier_core.hooks import Hook, HookResult

from .store import ProfileStore, STALENESS_THRESHOLD


class MyVoiceSyncHook(Hook):
    """Hook that syncs voice profiles on session start and periodically."""

    name: ClassVar[str] = "my-voice-sync"
    description: ClassVar[str] = (
        "Syncs voice profiles from remote on session start and when stale"
    )

    # Events we care about
    SYNC_EVENTS: ClassVar[set[str]] = {
        "session:start",  # Initial sync
        "prompt:start",  # Check staleness before each prompt
    }

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        my_voice_config = (config or {}).get("my-voice", {})
        self._store = ProfileStore(my_voice_config)
        self._last_check: float = 0
        self._check_interval = STALENESS_THRESHOLD  # Same as staleness threshold

    async def __call__(self, event: str, data: dict[str, Any]) -> HookResult:
        """Handle events - sync on start, check staleness periodically."""
        if event not in self.SYNC_EVENTS:
            return HookResult(action="continue")

        # Skip if not configured
        if not self._store.is_configured:
            if event == "session:start":
                # Inject setup guidance on session start
                return HookResult(
                    action="continue",
                    inject_context={
                        "role": "system",
                        "content": """**Voice Profile Not Configured**

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
                    },
                )
            return HookResult(action="continue")

        # On session start, always sync
        if event == "session:start":
            await self._store.sync(force=True)
            self._last_check = time.time()
            return HookResult(action="continue")

        # On prompt:start, check if we should sync (for long-running sessions)
        if event == "prompt:start":
            now = time.time()
            # Only check periodically, not every prompt
            if (now - self._last_check) > self._check_interval:
                self._last_check = now
                if self._store.is_stale:
                    # Sync in background - don't block the prompt
                    await self._store.sync()

        return HookResult(action="continue")
