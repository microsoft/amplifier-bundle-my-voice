"""Profile storage management - handles git sync for voice profiles."""

import asyncio
import os
import time
from pathlib import Path
from typing import Optional

# Staleness threshold - pull if last sync was more than this many seconds ago
STALENESS_THRESHOLD = 300  # 5 minutes


class ProfileStore:
    """Manages voice profile storage with git sync."""

    def __init__(self, config: dict):
        self.profile_source = config.get("profile_source", "unconfigured")
        self.local_path = Path(
            config.get(
                "local_path", os.path.expanduser("~/.amplifier/my-voice/profiles")
            )
        )
        self._last_sync: float = 0
        self._initialized = False

    @property
    def is_configured(self) -> bool:
        """Check if profile storage is configured."""
        return self.profile_source not in ("unconfigured", None, "")

    @property
    def is_git_source(self) -> bool:
        """Check if using git remote storage."""
        return self.profile_source.startswith("git+")

    @property
    def git_url(self) -> Optional[str]:
        """Extract git URL from profile_source."""
        if not self.is_git_source:
            return None
        # git+https://github.com/user/repo -> https://github.com/user/repo
        return self.profile_source[4:]

    @property
    def is_stale(self) -> bool:
        """Check if local copy might be stale (needs pull)."""
        if not self.is_git_source:
            return False
        return (time.time() - self._last_sync) > STALENESS_THRESHOLD

    @property
    def configuration_state(self) -> str:
        """Determine user's setup state for appropriate UX flow.

        Returns one of:
        - "unconfigured": No config in settings.yaml (new user OR returning user on new device)
        - "configured_needs_clone": Git config exists but repo not cloned yet
        - "configured_no_profile": Storage ready but no profile built yet
        - "ready": Profile exists and ready to use
        """
        if not self.is_configured:
            return "unconfigured"

        if self.is_git_source:
            git_dir = self.local_path / ".git"
            if not git_dir.exists():
                return "configured_needs_clone"

        # Check if any profiles exist
        profiles_dir = self.local_path / "profiles"
        if profiles_dir.exists():
            profiles = [
                p
                for p in profiles_dir.iterdir()
                if p.is_dir() and (p / "VOICE_PROFILE.md").exists()
            ]
            if profiles:
                return "ready"

        return "configured_no_profile"

    async def _run_git(
        self, *args: str, cwd: Optional[Path] = None
    ) -> tuple[int, str, str]:
        """Run a git command."""
        proc = await asyncio.create_subprocess_exec(
            "git",
            *args,
            cwd=cwd or self.local_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return proc.returncode or 0, stdout.decode(), stderr.decode()

    async def ensure_initialized(self) -> dict:
        """Ensure profile storage is initialized. Clone if needed."""
        if not self.is_configured:
            return {
                "success": False,
                "error": "Profile storage not configured. Add config.my-voice.profile_source to ~/.amplifier/settings.yaml",
            }

        # Create local path if needed
        self.local_path.mkdir(parents=True, exist_ok=True)

        if self.is_git_source:
            git_dir = self.local_path / ".git"
            if not git_dir.exists():
                # Clone the repo
                return await self._clone()

        self._initialized = True
        return {"success": True, "message": "Profile storage ready"}

    async def _clone(self) -> dict:
        """Clone the profile repo."""
        url = self.git_url
        if not url:
            return {"success": False, "error": "Invalid git URL"}

        # Clone to parent, then the repo becomes local_path
        parent = self.local_path.parent
        parent.mkdir(parents=True, exist_ok=True)

        # Remove local_path if it exists but isn't a git repo
        if self.local_path.exists():
            import shutil

            shutil.rmtree(self.local_path)

        code, stdout, stderr = await self._run_git(
            "clone", url, str(self.local_path), cwd=parent
        )

        if code != 0:
            return {"success": False, "error": f"Clone failed: {stderr}"}

        self._last_sync = time.time()
        self._initialized = True
        return {"success": True, "message": f"Cloned profile repo to {self.local_path}"}

    async def sync(self, force: bool = False) -> dict:
        """Pull latest from remote if git source and stale (or forced)."""
        init_result = await self.ensure_initialized()
        if not init_result["success"]:
            return init_result

        if not self.is_git_source:
            return {"success": True, "message": "Local storage - no sync needed"}

        if not force and not self.is_stale:
            return {"success": True, "message": "Already up to date (not stale)"}

        # Pull latest
        code, stdout, stderr = await self._run_git("pull", "--rebase")

        if code != 0:
            # Try to handle conflicts gracefully
            if "conflict" in stderr.lower():
                return {
                    "success": False,
                    "error": f"Merge conflict - manual resolution needed: {stderr}",
                }
            return {"success": False, "error": f"Pull failed: {stderr}"}

        self._last_sync = time.time()
        return {
            "success": True,
            "message": "Synced with remote",
            "output": stdout.strip(),
        }

    async def save(self, message: str = "Update voice profile") -> dict:
        """Commit and push changes if git source."""
        if not self._initialized:
            init_result = await self.ensure_initialized()
            if not init_result["success"]:
                return init_result

        if not self.is_git_source:
            return {"success": True, "message": "Local storage - changes saved locally"}

        # Check for changes
        code, stdout, _ = await self._run_git("status", "--porcelain")
        if not stdout.strip():
            return {"success": True, "message": "No changes to save"}

        # Add all changes
        code, _, stderr = await self._run_git("add", "-A")
        if code != 0:
            return {"success": False, "error": f"Add failed: {stderr}"}

        # Commit
        code, _, stderr = await self._run_git(
            "commit",
            "-m",
            message,
            "-m",
            "🤖 Generated with [Amplifier](https://github.com/microsoft/amplifier)",
            "-m",
            "Co-Authored-By: Amplifier <240397093+microsoft-amplifier@users.noreply.github.com>",
        )
        if code != 0:
            return {"success": False, "error": f"Commit failed: {stderr}"}

        # Push
        code, _, stderr = await self._run_git("push")
        if code != 0:
            return {"success": False, "error": f"Push failed: {stderr}"}

        self._last_sync = time.time()
        return {"success": True, "message": f"Saved and pushed: {message}"}

    async def read_profile(self, profile_name: str = "default") -> dict:
        """Read a voice profile, syncing first if stale."""
        # Sync if stale
        if self.is_stale:
            sync_result = await self.sync()
            if not sync_result["success"]:
                # Log warning but continue with local copy
                pass

        profile_path = self.local_path / "profiles" / profile_name / "VOICE_PROFILE.md"

        if not profile_path.exists():
            return {
                "success": False,
                "error": f"Profile not found: {profile_name}. Run voice-analyst to create one.",
                "path": str(profile_path),
            }

        content = profile_path.read_text()
        return {"success": True, "content": content, "path": str(profile_path)}

    async def write_profile(
        self, content: str, profile_name: str = "default", auto_save: bool = True
    ) -> dict:
        """Write a voice profile, optionally committing and pushing."""
        init_result = await self.ensure_initialized()
        if not init_result["success"]:
            return init_result

        profile_dir = self.local_path / "profiles" / profile_name
        profile_dir.mkdir(parents=True, exist_ok=True)

        profile_path = profile_dir / "VOICE_PROFILE.md"
        profile_path.write_text(content)

        result = {
            "success": True,
            "message": f"Wrote profile to {profile_path}",
            "path": str(profile_path),
        }

        if auto_save and self.is_git_source:
            save_result = await self.save(f"Update {profile_name} voice profile")
            result["save_result"] = save_result

        return result

    async def status(self) -> dict:
        """Get current status of profile storage."""
        info = {
            "configured": self.is_configured,
            "profile_source": self.profile_source,
            "local_path": str(self.local_path),
            "is_git": self.is_git_source,
            "initialized": self._initialized,
        }

        if self.is_git_source:
            info["is_stale"] = self.is_stale
            info["seconds_since_sync"] = (
                int(time.time() - self._last_sync) if self._last_sync else None
            )

            if self._initialized:
                # Get git status
                code, stdout, _ = await self._run_git("status", "--porcelain")
                info["has_changes"] = bool(stdout.strip())

                # Get current commit
                code, stdout, _ = await self._run_git("rev-parse", "--short", "HEAD")
                info["current_commit"] = stdout.strip() if code == 0 else None

        # List available profiles
        profiles_dir = self.local_path / "profiles"
        if profiles_dir.exists():
            info["profiles"] = [p.name for p in profiles_dir.iterdir() if p.is_dir()]
        else:
            info["profiles"] = []

        return info
