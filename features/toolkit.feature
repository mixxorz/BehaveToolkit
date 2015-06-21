Feature: Test Scenarios

  Background: Some background
    Given a background state

  Scenario: First scenario
    Given a thing
    When a something happens
    Then a thing should happen

  Scenario: Second scenario
    Given a second thing
    When a second thing happens
    Then a second thing should happen

  Scenario: Failing scen
    Given a third thing
    Then it will fail

  Scenario: Pattern matching scen
    Given the "thing"
    When I "do another thing"
    | name  | age |
    | Mitch | 21  |
    Then third thing
