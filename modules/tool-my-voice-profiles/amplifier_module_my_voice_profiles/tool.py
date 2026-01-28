"""Voice profile management tool."""

import os
from pathlib import Path
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
- configure: Set up profile storage (for new users or new devices)

Examples:
- Sync profiles: {"operation": "sync"}
- Check status: {"operation": "status"}
- Read profile: {"operation": "read", "profile": "default"}
- Write profile: {"operation": "write", "profile": "default", "content": "..."}
- Save changes: {"operation": "save", "message": "Added new learnings"}
- Configure storage: {"operation": "configure", "storage_type": "github", "git_url": "https://github.com/user/my-voice-profiles"}
"""

    @property
    def input_schema(self) -> dict[str, Any]:
        """Return JSON schema for tool input."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["sync", "status", "read", "write", "save", "configure"],
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
                "storage_type": {
                    "type": "string",
                    "enum": ["github", "local"],
                    "description": "Storage type for configure operation",
                },
                "git_url": {
                    "type": "string",
                    "description": "GitHub repo URL (for configure with storage_type=github)",
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
                # Add configuration_state to status
                result["configuration_state"] = self._store.configuration_state
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
            elif operation == "configure":
                result = await self._configure_storage(input)
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

    async def _configure_storage(self, input: dict[str, Any]) -> dict[str, Any]:
        """Configure profile storage - helps users set up on first run or new device."""
        storage_type = input.get("storage_type")
        git_url = input.get("git_url")

        if not storage_type:
            return {
                "success": False,
                "error": "storage_type is required (github or local)",
            }

        # Read existing settings
        settings_path = Path(os.path.expanduser("~/.amplifier/settings.yaml"))

        if settings_path.exists():
            import yaml

            settings = yaml.safe_load(settings_path.read_text()) or {}
        else:
            settings = {}

        # Ensure nested structure exists
        if "config" not in settings:
            settings["config"] = {}
        if "my-voice" not in settings["config"]:
            settings["config"]["my-voice"] = {}

        # Configure based on storage type
        if storage_type == "local":
            settings["config"]["my-voice"]["profile_source"] = "local"
            message = "Configured local storage"
            next_step = (
                "Your profiles will be stored at ~/.amplifier/my-voice/profiles/"
            )

        elif storage_type == "github":
            if not git_url:
                return {
                    "success": False,
                    "error": "git_url is required for github storage type",
                    "hint": "Provide the URL to your voice profiles repo, e.g., https://github.com/username/my-voice-profiles",
                }

            # Normalize URL - add git+ prefix if not present
            if not git_url.startswith("git+"):
                git_url = f"git+{git_url}"

            settings["config"]["my-voice"]["profile_source"] = git_url
            message = f"Configured GitHub storage: {git_url}"
            next_step = "Run sync to pull your existing profile, or build a new one"

        else:
            return {
                "success": False,
                "error": f"Unknown storage_type: {storage_type}. Use 'github' or 'local'",
            }

        # Write settings back
        import yaml

        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(yaml.dump(settings, default_flow_style=False))

        # Reinitialize the store with new config
        self._store = ProfileStore(settings["config"]["my-voice"])

        # For GitHub, try to sync immediately
        if storage_type == "github":
            sync_result = await self._store.sync(force=True)
            if sync_result.get("success"):
                # Check if there's already a profile
                status = await self._store.status()
                if status.get("profiles"):
                    return {
                        "success": True,
                        "message": message,
                        "synced": True,
                        "profiles_found": status["profiles"],
                        "next_step": "Your existing profile is ready to use!",
                    }
                else:
                    return {
                        "success": True,
                        "message": message,
                        "synced": True,
                        "profiles_found": [],
                        "next_step": "Storage connected but no profile found. Build one with voice-analyst.",
                    }
            else:
                return {
                    "success": True,
                    "message": message,
                    "synced": False,
                    "sync_error": sync_result.get("error"),
                    "next_step": "Configuration saved but sync failed. Check the repo URL and your git credentials.",
                }

        return {
            "success": True,
            "message": message,
            "settings_path": str(settings_path),
            "next_step": next_step,
        }
