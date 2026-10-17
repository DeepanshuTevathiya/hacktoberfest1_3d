import pytest
from app.demo import microwave
from app.schemas import Blueprint

def test_demo_blueprint_is_valid():
    assert microwave().slug == 'microwave_oven'

def test_duplicate_slot_is_rejected():
    data = microwave().model_dump(); data['parts'][1]['slot'] = 'top'
    data['parts'][3]['slot'] = 'top'
    with pytest.raises(ValueError): Blueprint.model_validate(data)

def test_unknown_reference_is_rejected():
    data = microwave().model_dump(); data['flow'][0] = 'not_a_part'
    with pytest.raises(ValueError): Blueprint.model_validate(data)
