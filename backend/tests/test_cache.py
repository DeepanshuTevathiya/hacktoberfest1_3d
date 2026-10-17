from app.cache import BlueprintCache
from app.demo import television

def test_cache_round_trip(tmp_path):
    cache = BlueprintCache(tmp_path / 'cache.db'); expected = television(); cache.put(expected)
    assert cache.get(expected.slug).object_name == expected.object_name
