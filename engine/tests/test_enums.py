import numpy as np

from engine.game.game_state import Group, MemberCard, Unit, ensure_group_list, ensure_unit_list

# --- Group Tests ---


def test_ensure_group_list_multiline():
    input_str = (
        "ラブライブ！虹ヶ咲学園スクールアイドル同好会\nラブライブ！スーパースター!!\n蓮ノ空女学院スクールアイドルクラブ"
    )
    groups = ensure_group_list(input_str)

    assert len(groups) == 3
    assert Group.NIJIGASAKI in groups
    assert Group.LIELLA in groups
    assert Group.HASUNOSORA in groups


def test_member_card_parsing_multiline():
    card = MemberCard(
        card_id=1,
        card_no="TEST-multi",
        name="Multi Group Card",
        cost=1,
        hearts=np.zeros(6),
        blade_hearts=np.zeros(7),
        blades=1,
        groups="ラブライブ！\nラブライブ！サンシャイン!!",
    )

    assert len(card.groups) == 2
    assert Group.MUSE in card.groups
    assert Group.AQOURS in card.groups


# --- Unit Tests ---


def test_unit_enum_parsing():
    # Test specific requested mappings
    assert Unit.from_japanese_name("スリーズブーケ") == Unit.CERISE_BOUQUET
    assert Unit.from_japanese_name("みらくらぱーく!") == Unit.MIRA_CRA_PARK
    assert Unit.from_japanese_name("5yncri5e!") == Unit.SYNCRISE
    assert Unit.from_japanese_name("CYaRon！") == Unit.CYARON
    assert Unit.from_japanese_name("GuiltyKiss") == Unit.GUILTY_KISS
    assert Unit.from_japanese_name("EdelNote") == Unit.EDEL_NOTE

    # Test existing ones
    assert Unit.from_japanese_name("Printemps") == Unit.PRINTEMPS
    assert Unit.from_japanese_name("A・ZU・NA") == Unit.A_ZU_NA

    # Test unknown
    assert Unit.from_japanese_name("UnknownUnit") == Unit.OTHER


def test_ensure_unit_list():
    # Test multi-line
    input_str = "スリーズブーケ\nEdelNote"
    units = ensure_unit_list(input_str)
    assert len(units) == 2
    assert Unit.CERISE_BOUQUET in units
    assert Unit.EDEL_NOTE in units

    # Test list input
    input_list = ["GuiltyKiss", Unit.AZALEA]
    units_list = ensure_unit_list(input_list)
    assert len(units_list) == 2
    assert Unit.GUILTY_KISS in units_list
    assert Unit.AZALEA in units_list
