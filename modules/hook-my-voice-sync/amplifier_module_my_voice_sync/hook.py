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
        """Handle session start - provide state-appropriate guidance."""
        state = self._store.configuration_state

        if state == "unconfigured":
            return HookResult(
                action="inject_context",
                context_injection=self._guidance_unconfigured(),
                context_injection_role="system",
            )

        if state == "configured_needs_clone":
            # Auto-sync for returning users on new devices
            await self._store.sync(force=True)
            self._last_check = time.time()
            return HookResult(
                action="inject_context",
                context_injection=self._guidance_synced(),
                context_injection_role="system",
            )

        if state == "configured_no_profile":
            return HookResult(
                action="inject_context",
                context_injection=self._guidance_no_profile(),
                context_injection_role="system",
            )

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

    def _guidance_unconfigured(self) -> str:
        """Guidance for unconfigured state - ASK FIRST, don't assume."""
        return """<system-reminder source="my-voice-state">
## Voice Profile Status: Not Configured

**IMPORTANT: ASK BEFORE ASSUMING.** The user may have an existing profile stored elsewhere.

When the user asks for voice-related help (clean up message, write in my voice, etc.):

**FIRST, ask this clarifying question:**

"I don't see a voice profile set up on this device. Quick question before we start:

**A) I have one stored already** (GitHub repo or another device)
**B) I'm new to this** - let me try it first  
**C) Skip setup for now** - just help with this message

Which applies to you?"

**Based on their answer:**

- **A) Has existing profile:**
  Ask: "Great! Where is it stored? (e.g., github.com/username/my-voice-profiles)"
  Then use the my_voice_profiles tool with operation="configure" to set it up
  
- **B) New user:**
  Proceed with the request using "ephemeral mode" - infer style from their message
  After delivering value, offer: "I noticed some patterns in your writing. Want me to save these for next time?"
  If yes, guide through storage setup
  
- **C) Skip:**
  Work from context only, infer style from the message itself
  Don't mention configuration again this session

**DO NOT:**
- Assume they're a new user
- Show YAML configuration unprompted
- Block them from getting help
- Proceed without asking which situation applies
</system-reminder>"""

    def _guidance_synced(self) -> str:
        """Guidance after syncing existing profile on new device."""
        return """<system-reminder source="my-voice-state">
## Voice Profile Status: Synced

Welcome back! Found and synced your voice profile from remote storage.
Your voice patterns are loaded and ready to use.

Proceed normally with any voice-related requests.
</system-reminder>"""

    def _guidance_no_profile(self) -> str:
        """Guidance when storage is configured but no profile exists."""
        return """<system-reminder source="my-voice-state">
## Voice Profile Status: Storage Ready, No Profile Yet

Storage is configured but no voice profile has been created yet.

When the user asks for voice-related help:

**Offer to build their profile first:**

"I see you have voice profile storage set up, but no profile exists yet. Would you like me to:

**A) Build a profile now** from writing samples or our conversation
**B) Work from this message** and save learnings after

Which would you prefer?"

If A: Guide them through voice-analyst to build profile
If B: Proceed with request, offer to save learnings after
</system-reminder>"""
