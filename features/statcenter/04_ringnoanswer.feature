Feature: Stat

    Scenario: Generation of event RINGNOANSWER
        Given there are no calls running
        Given there is no agents logged
        Given there is no "RINGNOANSWER" entry in queue "q04"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 004      |   1004 | statscenter | 004          |
        Given there are queues with infos:
            | name | number | context     | agents_number |
            | q04  | 5004   | statscenter | 004           |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "004" on extension "1004@statscenter"
        Given I wait 5 seconds for the calls processing
        Given there is 1 calls to extension "5004@statscenter" then i hang up after "20s"
        Given I wait 2 seconds for the calls processing
        Given I logout agent "004" on extension "1004@statscenter"
        Given I wait 25 seconds for the calls processing
        Then I should see 1 "RINGNOANSWER" event in queue "q04" in the queue log
