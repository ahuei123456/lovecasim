Feature: Ability Conditions
    As a player
    I want ability conditions to be checked correctly
    So that abilities only trigger when valid

    Scenario: Group Filter Condition
        Given a condition requiring group "Aqours"
        And a member card of group "Aqours"
        When the condition is checked for the member
        Then the result should be True

    Scenario: Cost Check Condition
        Given a condition requiring cost LE 3
        And a member card with cost 3
        When the condition is checked for the member
        Then the result should be True

    Scenario: Opponent Has Member Condition
        Given a condition requiring opponent to have a member
        And the opponent has a member on stage
        When the condition is checked
        Then the result should be True
