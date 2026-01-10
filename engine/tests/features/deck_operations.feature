Feature: Deck Operations
    As a player
    I want to interact with my deck (draw, look, reveal)
    So that I can access my cards

    Scenario: Reveal Cards Effect
        Given a player has 3 cards in deck
        When the player resolves a "Reveal 2 Cards" effect
        Then 2 cards should be revealed
        And the main deck should have 1 card remaining

    Scenario: Cheer Reveal Effect
        Given a player has a card in deck
        When the player resolves a "Cheer Reveal" effect
        Then the top card should be revealed
