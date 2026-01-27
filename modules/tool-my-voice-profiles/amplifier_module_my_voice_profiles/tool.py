"""Voice profile management tool."""

from typing import Any

from amplifier_core import ToolResult

from .store import ProfileStore


class MyVoiceProfilesTool:
    """Tool for managing voice profiles with git sync.

    Implements the Tool protocol (structural typing, no inheritance needed).
    """

    def __init__(self, config: dict[str, Any] | None = None):
        my_voice_config = (config or {}).get("my-voice", {})
        self._store = ProfileStore(my_voice_config)

    @property
    def name(self) -> str:
        return "my_voice_profiles"

    @property
    def description(self) -> str:
        return """Manage voice profiles for the my-voice bundle.

Operations:
- sync: Pull latest profiles from remote (if git source)
- status: Get current profile storage status
- read: Read a voice profile
- write: Write/update a voice profile
- save: Commit and push changes to remote

Examples:
- Sync profiles: {"operation": "sync"}
- Check status: {"operation": "status"}
- Read profile: {"operation": "read", "profile": "default"}
- Write profile: {"operation": "write", "profile": "default", "content": "..."}
- Save changes: {"operation": "save", "message": "Added new learnings"}
"""

    @property
    def input_schema(self) -> dict[str, Any]:
        """Return JSON schema for tool input."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["sync", "status", "read", "write", "save"],
                    "description": "Operation to perform",
                },
                "profile": {
                    "type": "string",
                    "description": "Profile name (default: 'default')",
                },
                "content": {
                    "type": "string",
                    "description": "Profile content (for write operation)",
                },
                "message": {
                    "type": "string",
                    "description": "Commit message (for save operation)",
                },
                "force": {
                    "type": "boolean",
                    "description": "Force sync even if not stale",
                },
            },
            "required": ["operation"],
        }

    async def execute(self, input: dict[str, Any]) -> ToolResult:
        """Execute tool with given input."""
        operation = input.get("operation")
        profile = input.get("profile", "default")
        content = input.get("content")
        message = input.get("message")
        force = input.get("force", False)

        try:
            if operation == "sync":
                result = await self._store.sync(force=force)
            elif operation == "status":
                result = await self._store.status()
            elif operation == "read":
                result = await self._store.read_profile(profile)
            elif operation == "write":
                if content is None:
                    return ToolResult(
                        success=False,
                        error={"message": "content is required for write operation"},
                    )
                result = await self._store.write_profile(
                    content=content,
                    profile_name=profile,
                )
            elif operation == "save":
                result = await self._store.save(
                    message=message or "Update voice profile"
                )
            else:
                return ToolResult(
                    success=False,
                    error={"message": f"Unknown operation: {operation}"},
                )

            return ToolResult(success=True, output=result)

        except Exception as e:
            return ToolResult(
                success=False,
                error={"message": str(e), "type": type(e).__name__},
            )
