Feature: Triggers and Costs
    Testing trigger logic and optional costs

    Scenario: Optional Discard Cost (Shizuku)
        Given the player has 2 cards in hand
        And the player has a member "Shizuku" with an optional discard cost ability
        When the player activates the ability of "Shizuku"
        Then the player should be prompted to select 1 card from hand
        And the choice should be optional
        When the player chooses to skip the optional cost
        Then the player's hand size should remain 2
        And the ability effects should not execute
