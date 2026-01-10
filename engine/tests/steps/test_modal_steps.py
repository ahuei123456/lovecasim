from pytest_bdd import given, scenario, then, when

from compiler.parser import AbilityParser


@scenario("../features/modal.feature", "Select Mode")
def test_select_mode():
    pass


@scenario("../features/modal.feature", "Color Select")
def test_color_select():
    pass


@then('a pending choice should be created for "SELECT_MODE"')
def check_choice(game_state):
    assert len(game_state.pending_choices) > 0
    assert game_state.pending_choices[0][0] == "SELECT_MODE"


@then("the choice should have 2 options")
def check_choice_options(game_state):
    _, params = game_state.pending_choices[0]
    assert len(params["options"]) == 2


@given('a player has a card with "Select a Heart Color"', target_fixture="color_ability")
def player_with_color_card(game_state):
    text = "ライブ開始時好きなハートの色を1つ指定する。"
    abilities = AbilityParser.parse_ability_text(text)
    return abilities[0]


@given('a player has a card with "Select 1: Draw 1 or Add Blades"', target_fixture="modal_ability")
def player_with_modal_card(game_state):
    # Construct ability manually or parse? Parsing is better for coverage
    text = "登場以下から1つを選ぶ。\n・1枚引く。\n・ブレードを2得る。"
    abilities = AbilityParser.parse_ability_text(text)
    return abilities[0]


@when("the modal ability resolves")
def resolve_modal_ability(game_state, modal_ability):
    eff = modal_ability.effects[0]
    # Inject options
    eff.params["options"] = modal_ability.modal_options
    game_state.pending_effects.append(eff)
    game_state._resolve_pending_effect(0)


@when("the color ability resolves")
def resolve_color_ability(game_state, color_ability):
    eff = color_ability.effects[0]
    game_state.pending_effects.append(eff)
    game_state._resolve_pending_effect(0)


@then('a pending choice should be created for "COLOR_SELECT"')
def check_color_choice(game_state):
    assert len(game_state.pending_choices) > 0
    assert game_state.pending_choices[0][0] == "COLOR_SELECT"


@then("legal actions should be masked for color selection")
def check_color_mask(game_state):
    legal = game_state.get_legal_actions()
    # range 580-585 should be true (Red, Blue, Green, Yellow, Purple, Pink)
    for i in range(580, 586):
        assert legal[i], f"Action {i} should be legal"
