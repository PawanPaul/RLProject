import pytest
import RLAIMainFunc

def test_answer():
    assert RLAIMainFunc.block_init(3,4,5) == [3, 4, 5, RLAIMainFunc.Block.unknown, RLAIMainFunc.MineType.unknown, {}, [], RLAIMainFunc.CraftType.unknown, []]

test_answer()