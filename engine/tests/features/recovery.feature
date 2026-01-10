Feature: Recovery Effects
    Relationships between effects and discard recovery logic

    Scenario: Recover a live card from discard
        Given a player with a discard pile
        And the discard pile contains a live card "LiveA" with ID 300
        And the discard pile contains a live card "LiveB" with ID 301
        When the player activates an effect to recover a live card
        And the player selects "LiveA" from the recovery choices
        Then "LiveA" should be in the player's hand
        And "LiveA" should not be in the player's discard
        And the player's hand size should increase by 1

    Scenario: Recover a member card from discard
        Given a player with a discard pile
        And the discard pile contains a member card "MemberA" with ID 400
        When the player activates an effect to recover a member card
        And the player selects "MemberA" from the recovery choices
        Then "MemberA" should be in the player's hand
        And "MemberA" should not be in the player's discard

    Scenario: Recover a member with filters (Group and Cost)
        Given a player with a discard pile
        And the discard pile contains the test members for filtering
        When the player activates an effect to recover a member with group "μ's" and max cost 4
        Then the recovery choices should include "Kotori"
        And the recovery choices should not include "Honoka"
        And the recovery choices should not include "Chika"
        When the player selects "Kotori" from the recovery choices
        Then "Kotori" should be in the player's hand
