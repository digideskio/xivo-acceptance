Feature: REST API SIP Lines

    Scenario: Get a SIP line
        Given I have the following lines:
          | id     | username | secret | context | protocol | device_slot |
          | 553215 | toto     | abcdef | default | sip      | 1           |
        When I ask for the line_sip with id "553215"
        Then I get a response with status "200"
        Then I have a line_sip with the following parameters:
          | id     | username | secret | context |
          | 553215 | toto     | abcdef | default |
        Then I have a line_sip with the following attributes:
          | attribute              |
          | provisioning_extension |

    Scenario: Create a line with a context
        When I create a line_sip with the following parameters:
            | context | device_slot |
            | default | 1           |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a response with a link to the "lines_sip" resource
        Then I get a header with a location for the "lines_sip" resource

    Scenario: Create a line with an internal context other than default
        Given I have an internal context named "mycontext"
        When I create a line_sip with the following parameters:
            | context     | device_slot |
            | mycontext   | 1           |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a response with a link to the "lines_sip" resource
        Then I get a header with a location for the "lines_sip" resource

    Scenario: Create 2 lines in same context
        When I create a line_sip with the following parameters:
            | context | device_slot |
            | default | 1           |
        Then I get a response with status "201"
        When I create a line_sip with the following parameters:
            | context | device_slot |
            | default | 1           |
        Then I get a response with status "201"

    Scenario: Editing a line_sip that doesn't exist
        Given I have no line with id "407558"
        When I update the line_sip with id "407558" using the following parameters:
          | username |
          | toto     |
        Then I get a response with status "404"

    Scenario: Editing the username of a line_sip
        Given I have the following lines:
          |     id | username | context | protocol | device_slot |
          | 115487 | toto     | default | sip      |           1 |
        When I update the line_sip with id "115487" using the following parameters:
          | username |
          | tata     |
        Then I get a response with status "204"
        When I ask for the line_sip with id "115487"
        Then I have a line_sip with the following parameters:
          |     id | username | context |
          | 115487 | tata     | default |

    Scenario: Editing the context of a line_sip
        Given I have the following lines:
            |     id | username | context | protocol | device_slot |
            | 858494 | toto     | default | sip      |           1 |
        Given I have the following context:
            | name | numberbeg | numberend |
            | lolo | 1000      | 1999      |
        When I update the line_sip with id "858494" using the following parameters:
            | context |
            | lolo    |
        Then I get a response with status "204"
        When I ask for the line_sip with id "858494"
        Then I have a line_sip with the following parameters:
            | id | username | context |
            | 858494   | toto     | lolo    |

    Scenario: Editing the callerid of a line
        Given I have the following lines:
          |     id | username | context | callerid   | protocol | device_slot |
          | 994679 | toto     | default | Super Toto | sip      |           1 |
        Given I have the following context:
          | name | numberbeg | numberend |
          | lolo | 1000      | 1999      |
        When I update the line_sip with id "994679" using the following parameters:
          | callerid  |
          | Mega Toto |
        Then I get a response with status "204"
        When I ask for the line_sip with id "994679"
        Then I have a line_sip with the following parameters:
          |     id | username | context | callerid  |
          | 994679 | toto     | default | Mega Toto |

    Scenario: Editing the username, context, callerid of a line_sip
        Given I have the following lines:
          |     id | username | context | callerid   | protocol | device_slot |
          | 552134 | titi     | default | Super Toto | sip      |           1 |
        Given I have the following context:
          | name   | numberbeg | numberend |
          | patate | 1000      | 1999      |
        When I update the line_sip with id "552134" using the following parameters:
          | username | context | callerid   |
          | titi     | patate  | Petit Toto |
        Then I get a response with status "204"
        When I ask for the line_sip with id "552134"
        Then I have a line_sip with the following parameters:
          |     id | username | context | callerid   |
          | 552134 | titi     | patate  | Petit Toto |

    Scenario: Delete a line that doesn't exist
        Given I have no line with id "985462"
        When I delete line sip "985462"
        Then I get a response with status "404"

    Scenario: Delete a line
        Given I have the following lines:
            | id | context | protocol | device_slot |
            | 198447 | default | sip      | 1           |
        When I delete line sip "198447"
        Then I get a response with status "204"
        Then the line sip "198447" no longer exists
        Then the line "198447" no longer exists
