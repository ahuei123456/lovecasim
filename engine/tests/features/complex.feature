Feature: Complex Effect Sequences
    Testing sequences of effects interrupted by choices

    Scenario: Effect Sequence Interrupted by Choice
        Given a player has a "Complex Member" with ability "Order -> Tap -> Draw"
        And the opponent has a member on stage at slot 0
        And the player's deck has 5 cards
        When the player activates the ability of "Complex Member"
        Then the player should be prompted to select an opponent member
        And the pending effects should contain "DRAW"
        When the player selects the opponent member at slot 0
        Then the opponent member at slot 0 should be tapped
        And the player should draw 1 card
        And the pending effects should be empty
