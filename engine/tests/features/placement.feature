Feature: Placement Effects
    Placing cards under members (charging energy/marker)

    Scenario: Place a card from hand under self
        Given a player with a member on stage at slot 0
        And the player has 3 cards in hand
        When the player activates an effect to place 1 card from hand under the member at slot 0
        Then the player should be prompted to select 1 card from hand
        When the player selects the first card in hand
        Then the selected card should be under the member at slot 0
        And the selected card should not be in the player's hand
