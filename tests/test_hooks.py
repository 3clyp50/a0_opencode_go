import pytest
from git import GitCommandError, Repo

import hooks


def test_pre_update_unblocks_thumbnail_pull(tmp_path, monkeypatch):
    source_dir = tmp_path / "source"
    with Repo.init(source_dir, initial_branch="main") as source:
        (source_dir / "plugin.yaml").write_text("name: a0_opencode_go\n")
        source.index.add(["plugin.yaml"])
        source.index.commit("initial plugin")
        installed_dir = tmp_path / "installed"
        with Repo.clone_from(source_dir, installed_dir) as installed:
            monkeypatch.setattr(hooks, "__file__", str(installed_dir / "hooks.py"))
            thumbnail = installed_dir / "webui" / "thumbnail.webp"
            thumbnail.parent.mkdir()
            thumbnail.write_bytes(b"downloaded artwork")
            settings = installed_dir / "config.json"
            settings.write_bytes(b"local settings")

            upstream_thumbnail = source_dir / "webui" / "thumbnail.webp"
            upstream_thumbnail.parent.mkdir()
            upstream_thumbnail.write_bytes(b"tracked artwork")
            source.index.add(["webui/thumbnail.webp"])
            source.index.commit("ship thumbnail")

            with pytest.raises(GitCommandError, match="untracked working tree files"):
                installed.remotes.origin.pull("main")
            hooks.pre_update()
            hooks.pre_update()
            installed.remotes.origin.pull("main")

            assert installed.head.commit.hexsha == source.head.commit.hexsha
            assert thumbnail.read_bytes() == b"tracked artwork"
            assert thumbnail.with_name("thumbnail.webp.pre-update-backup").read_bytes() == b"downloaded artwork"
            assert settings.read_bytes() == b"local settings"
            hooks.pre_update()
            assert thumbnail.read_bytes() == b"tracked artwork"


@pytest.mark.parametrize("state", ["zip", "tracked", "symlink", "backup_exists"])
def test_pre_update_preserves_existing_files(tmp_path, monkeypatch, state):
    monkeypatch.setattr(hooks, "__file__", str(tmp_path / "hooks.py"))
    thumbnail = tmp_path / "webui" / "thumbnail.webp"
    thumbnail.parent.mkdir()
    thumbnail.write_bytes(b"local artwork")
    backup = thumbnail.with_name("thumbnail.webp.pre-update-backup")
    if state == "zip":
        hooks.pre_update()
    else:
        with Repo.init(tmp_path, initial_branch="main") as repo:
            if state == "tracked":
                repo.index.add(["webui/thumbnail.webp"])
            elif state == "symlink":
                target = tmp_path / "original.webp"
                thumbnail.rename(target)
                thumbnail.symlink_to(target)
            elif state == "backup_exists":
                backup.write_bytes(b"earlier backup")
            if state == "backup_exists":
                with pytest.raises(FileExistsError):
                    hooks.pre_update()
                assert backup.read_bytes() == b"earlier backup"
            else:
                hooks.pre_update()
                assert not backup.exists()
            if state == "symlink":
                assert thumbnail.is_symlink()
    assert thumbnail.read_bytes() == b"local artwork"
