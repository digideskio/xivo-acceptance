Feature: Status related HTTP interfaces

  Scenario: User status
    Given there are users with infos:
    | firstname | lastname  | cti_profile | cti_login | cti_passwd |
    | Tyrion    | Lannister | Client      | tyrion    | tyrion     |
    Given I start the XiVO Client
    Given I log in the XiVO client as "tyrion", pass "tyrion"
    When I change my presence to "away"
    Then I should have the following user status when I query the cti:
    | user_uuid | user_id | origin_uuid | firstname | lastname  | presence |
    | yes       | yes     | yes         | Tyrion    | Lannister | away     |

  Scenario: Inexistant user
    Then I should have a "404" when I search for user "1222333" on the cti http interface

  Scenario: Infos
    When I query the infos URL on the cti http interface, I receive the uuid

  Scenario: Inexistant endpoint
    Then I should have a "404" when I search for endpoint "1222333" on the cti http interface

  Scenario: Endpoint status
    Given there are users with infos:
    | firstname | lastname  | number | context | protocol |
    | Tywin     | Lannister |   1111 | default | sip      |
    | Cersei    | Lannister |   1112 | default | sip      |
    When "Tywin Lannister" calls "1112"
    Then I should have the following endpoint status when I query the cti:
    | line_id | origin_uuid | context | number | status |
    | yes     | yes         | default |   1112 |      8 |
    When "Cersei Lannister" answers
    Then I should have the following endpoint status when I query the cti:
    | line_id | origin_uuid | context | number | status |
    | yes     | yes         | default |   1111 |      1 |
