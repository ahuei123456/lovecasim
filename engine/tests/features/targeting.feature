Feature: Interactive Targeting
    As a player
    I want to target specific cards
    So that I can apply effects to them

    Scenario: Tap Opponent Member
        Given an opponent has a member on stage
        When the player uses "Tap Opponent" effect
        Then a pending choice should be created for "TARGET_OPPONENT_MEMBER"
        And the opponent's member should be a valid target
