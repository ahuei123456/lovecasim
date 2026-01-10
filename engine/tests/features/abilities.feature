Feature: Card Abilities and Effects
    As a game engine
    I want to execute card abilities correctly
    So that the game rules are enforced

    Scenario: Draw cards
        Given a player with a deck
        When the player draws 2 cards
        Then the player's hand size should increase by 2
        And the player's deck size should decrease by 2

    Scenario: Add Blades
        Given a member card with blades
        Then the member should have greater than 0 blades

    Scenario: Search Deck
        Given a player with a deck containing "μ's" members
        When the player searches the deck for "μ's"
        Then the player should find "μ's" members

    Scenario: Formation Change
        Given a player with members on stage
        When the player activates formation change
        And the player selects to swap member at slot 0 with slot 1
        Then the members at slot 0 and 1 should be swapped

    Scenario: Recover member from discard
        Given a player has a member in discard
        When the player recovers the member from discard
        Then the member should be in the player's hand
        And the member should not be in the player's discard

    Scenario Outline: Parse ability text
        When I parse the ability text "<text>"
        Then I should get an ability with trigger "<trigger>"
        And the ability should have an effect type "<effect>"

        Examples:
        | text | trigger | effect |
        | 【登場】 手札を1枚控え室に置いてもよい | ON_PLAY | SWAP_CARDS |
        | 【起動】 エネルギーを1枚支払う：カードを1枚引く | ACTIVATED | DRAW |
        | 【常時】 ライブの合計スコアを＋１する | CONSTANT | BOOST_SCORE |
