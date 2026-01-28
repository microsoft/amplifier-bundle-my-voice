"""Voice profile sync hook - keeps profiles fresh across long sessions."""

import time
from typing import Any

from amplifier_core import HookResult

from .store import ProfileStore, STALENESS_THRESHOLD


class MyVoiceSyncHook:
    """Hook handlers for voice profile sync.

    This hook handles MECHANISMS (sync, staleness checks), not POLICY (asking questions).
    The agents themselves handle first-run onboarding and user interaction.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        my_voice_config = (config or {}).get("my-voice", {})
        self._store = ProfileStore(my_voice_config)
        self._last_check: float = 0
        self._check_interval = STALENESS_THRESHOLD

    async def handle_session_start(
        self, event: str, data: dict[str, Any]
    ) -> HookResult:
        """Handle session start - sync if configured, otherwise just continue."""
        state = self._store.configuration_state

        if state == "unconfigured":
            # Don't inject guidance - agents handle first-run onboarding themselves
            return HookResult(action="continue")

        if state == "configured_needs_clone":
            # Auto-sync for returning users on new devices
            await self._store.sync(force=True)
            self._last_check = time.time()
            return HookResult(action="continue")

        if state == "configured_no_profile":
            # Storage ready but no profile - agents will handle this
            return HookResult(action="continue")

        # Ready state - normal sync
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
