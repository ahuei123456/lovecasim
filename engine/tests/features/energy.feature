Feature: Energy Mechanics
    As a player
    I want to charge energy from deck and hand
    So that I can pay for costs

    Scenario: Charge energy from deck
        Given a player with a deck
        When the player uses an ability to charge energy from deck
        Then the player's energy zone should increase by 1
        And the player's deck size should decrease by 1
        And the new energy card should be untapped

    Scenario: Charge energy from hand
        Given a player with a hand
        When the player uses an ability to charge energy from hand
        Then a pending choice should be created for "TARGET_HAND"
