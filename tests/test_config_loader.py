from pathlib import Path

from src.Infrastructure.ConfigLoader import ConfigLoader


def test_defaults_merge(tmp_path: Path):
    cfg = tmp_path / "c.yaml"
    cfg.write_text("esp:\n  team_filter: true\n")
    loaded = ConfigLoader(cfg).load()
    assert loaded["esp"]["team_filter"] is True
    assert loaded["process"]["exe_name"] == "CombatMaster.exe"