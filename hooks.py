from pathlib import Path

from git import Repo


def pre_update():
    plugin_dir = Path(__file__).resolve().parent
    if not (plugin_dir / ".git").exists():
        return

    with Repo(plugin_dir) as repo:
        if "webui/thumbnail.webp" not in repo.untracked_files:
            return

    thumbnail = plugin_dir / "webui" / "thumbnail.webp"
    if thumbnail.is_symlink() or not thumbnail.is_file():
        return

    backup = thumbnail.with_name("thumbnail.webp.pre-update-backup")
    if backup.exists() or backup.is_symlink():
        raise FileExistsError(f"Move the existing thumbnail backup before updating: {backup}")
    thumbnail.rename(backup)
