import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STORE_MODULES = {
    "tool_store": REPOSITORY_ROOT
    / "modules"
    / "tool-my-voice-profiles"
    / "amplifier_module_my_voice_profiles"
    / "store.py",
    "hook_store": REPOSITORY_ROOT
    / "modules"
    / "hook-my-voice-sync"
    / "amplifier_module_my_voice_sync"
    / "store.py",
}


def load_store_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ProfileStoreGitUrlSecurityTests(unittest.IsolatedAsyncioTestCase):
    async def test_rejects_injection_urls_before_touching_storage(self):
        malicious_urls = (
            "--upload-pack=calc.exe",
            "ext::sh -c calc.exe",
            "ssh://github.com/owner/repository",
            "https://example.com/owner/repository",
        )

        for module_name, module_path in STORE_MODULES.items():
            module = load_store_module(module_name, module_path)
            for malicious_url in malicious_urls:
                with self.subTest(module=module_name, url=malicious_url):
                    with tempfile.TemporaryDirectory() as temporary_directory:
                        local_path = Path(temporary_directory) / "profiles"
                        local_path.mkdir()
                        marker = local_path / "keep.txt"
                        marker.write_text("preserve")
                        store = module.ProfileStore(
                            {
                                "profile_source": f"git+{malicious_url}",
                                "local_path": str(local_path),
                            }
                        )
                        store._run_git = AsyncMock()

                        result = await store._clone()

                        self.assertFalse(result["success"])
                        self.assertTrue(marker.exists())
                        store._run_git.assert_not_awaited()

    async def test_clones_valid_github_url_after_option_terminator(self):
        git_url = "https://github.com/owner/repository.git"

        for module_name, module_path in STORE_MODULES.items():
            module = load_store_module(module_name, module_path)
            with self.subTest(module=module_name):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    local_path = Path(temporary_directory) / "profiles"
                    store = module.ProfileStore(
                        {
                            "profile_source": f"git+{git_url}",
                            "local_path": str(local_path),
                        }
                    )
                    store._run_git = AsyncMock(return_value=(0, "", ""))

                    result = await store._clone()

                    self.assertTrue(result["success"])
                    store._run_git.assert_awaited_once_with(
                        "clone",
                        "--",
                        git_url,
                        str(local_path),
                        cwd=local_path.parent,
                    )


if __name__ == "__main__":
    unittest.main()
