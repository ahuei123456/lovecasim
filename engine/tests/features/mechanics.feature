Feature: Game Mechanics
    As a player
    I want to use game mechanics like Baton Touch and Cost Reduction
    So that I can play cards efficiently

    Scenario: Baton Touch reduces cost
        Given a player has a member on stage with cost 3
        And the player has a member in hand with cost 4
        And the player has 1 energy
        When the player plays the hand member onto the stage member
        Then the play should be successful
        And the energy used should be 1
        And the baton touch count should be 1

    Scenario: Baton Touch limit
        Given a player
        And a player has performed a baton touch this turn
        And the player has another member in hand
        When the player attempts another baton touch
        Then the cost should not be reduced

    Scenario: Cost Reduction for Member
        Given a player
        And a player has a cost reduction effect of 1
        And the player has a member in hand with cost 4
        And the player has 3 energy
        When the player plays the member
        Then the play should be successful
        And the energy used should be 3

    Scenario: Placement Restriction
        Given a player has a "placement" restriction
        When the player attempts to play a member
        Then the action should be illegal
