Feature: Modal Choices
    As a player
    I want to make choices when abilities trigger
    So that I can select the best effect

    Scenario: Select Mode
        Given a player has a card with "Select 1: Draw 1 or Add Blades"
        When the modal ability resolves
        Then a pending choice should be created for "SELECT_MODE"
        And the choice should have 2 options

    Scenario: Color Select
        Given a player has a card with "Select a Heart Color"
        When the color ability resolves
        Then a pending choice should be created for "COLOR_SELECT"
        And legal actions should be masked for color selection
