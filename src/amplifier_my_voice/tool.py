"""Voice profile management tool."""

from typing import Any, ClassVar

from amplifier_core.tools import Tool, ToolResult

from amplifier_my_voice.store import ProfileStore


class MyVoiceProfilesTool(Tool):
    """Tool for managing voice profiles with git sync."""

    name: ClassVar[str] = "my-voice-profiles"
    description: ClassVar[str] = """Manage voice profiles for the my-voice bundle.

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

    parameters: ClassVar[dict[str, Any]] = {
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
                "default": "default",
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
                "default": False,
            },
            "auto_save": {
                "type": "boolean",
                "description": "Auto-commit and push after write",
                "default": True,
            },
        },
        "required": ["operation"],
    }

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        my_voice_config = (config or {}).get("my-voice", {})
        self._store = ProfileStore(my_voice_config)

    async def run(
        self,
        operation: str,
        profile: str = "default",
        content: str | None = None,
        message: str | None = None,
        force: bool = False,
        auto_save: bool = True,
    ) -> ToolResult:
        """Execute a profile operation."""
        if operation == "sync":
            result = await self._store.sync(force=force)
        elif operation == "status":
            result = await self._store.status()
            result["success"] = True
        elif operation == "read":
            result = await self._store.read_profile(profile)
        elif operation == "write":
            if content is None:
                return ToolResult(
                    success=False,
                    output=None,
                    error="content is required for write operation",
                )
            result = await self._store.write_profile(
                content=content,
                profile_name=profile,
                auto_save=auto_save,
            )
        elif operation == "save":
            result = await self._store.save(message=message or "Update voice profile")
        else:
            return ToolResult(
                success=False,
                output=None,
                error=f"Unknown operation: {operation}",
            )

        if result.get("success"):
            return ToolResult(success=True, output=result)
        else:
            return ToolResult(success=False, output=None, error=result.get("error"))
