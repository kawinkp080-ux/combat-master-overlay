from src.Core.Models.Entity import Entity
from src.Core.Processors.ESPProcessor import ESPProcessor

IDENTITY = [1.0, 0, 0, 0,
            0, 1.0, 0, 0,
            0, 0, 1.0, 0,
            0, 0, 0, 1.0]


def test_entity_behind_camera_is_skipped():
    proc = ESPProcessor({"team_filter": False})
    ent = Entity(index=1, health=100, position=(0.0, 0.0, -5.0))
    boxes = proc.process([ent], IDENTITY)
    assert boxes == []


def test_center_entity_produces_box():
    proc = ESPProcessor({"team_filter": False})
    ent = Entity(index=2, health=80, position=(0.0, 0.0, 5.0))
    boxes = proc.process([ent], IDENTITY)
    assert len(boxes) == 1
    assert boxes[0].label == "hp80"