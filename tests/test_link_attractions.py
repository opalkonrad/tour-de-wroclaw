import pytest

from src.algorithm.link_attractions import check_if_weld
from src.graph.path_schema import AttractionNode


@pytest.fixture
def sample_attractions_list():
    return [
        (
            AttractionNode(id=1, pos=(17.0, 51.0)),
            AttractionNode(id=2, pos=(17.1, 51.2)),
            1,
        ),
        (
            AttractionNode(id=3, pos=(17.2, 51.3)),
            AttractionNode(id=4, pos=(17.3, 51.1)),
            1, 
        ),
        (
            AttractionNode(id=5, pos=(17.3, 51.1)),
            AttractionNode(id=6, pos=(17.3, 51.1)),
            1,
        ),
    ]

@pytest.mark.parametrize(
    "pair, distance, expected_index",
    [
        (
            (AttractionNode(id=1, pos=(17.0, 51.0)), AttractionNode(id=2, pos=(17.1, 51.2))), 0.1, 0
        ),
        (
            (AttractionNode(id=3, pos=(17.2000005, 51.30000001)), AttractionNode(id=4, pos=(17.3, 51.100003))), 0.4, 1
        ),
        (
            (AttractionNode(id=4, pos=(17.3, 51.100003)), AttractionNode(id=3, pos=(17.2000005, 51.30000001))), 0.4, 1
        ),
        (
            (AttractionNode(id=1, pos=(17.7, 51.4)), AttractionNode(id=2, pos=(17.1, 51.2))), 0.1, None
        ),
    ]
)
def test_check_if_weld(sample_attractions_list, pair, distance, expected_index):
    index = check_if_weld(sample_attractions_list, pair, distance)

    assert index == expected_index
