Feature: Stat

    Scenario: Generation of event AGENTCALLBACKLOGIN
        Given there are no calls running
        Given there is no agents logged
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "007"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 007      |   1007 | statscenter | 007          |
        Given I log agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGIN" event for agent "007" in the queue log

    Scenario: Login twice using AGENTCALLBACKLOGIN
        Given there are no calls running
        Given there is no agents logged
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "007"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 007      |   1007 | statscenter | 007          |
        Given I log agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I log agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGIN" event for agent "007" in the queue log

    Scenario: Logoff when not logged in
        Given there are no calls running
        Given there is no agents logged
        Given there is no "AGENTCALLBACKLOGOFF" entry for agent "007"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 007      |   1007 | statscenter | 007          |
        Given I log agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I logout agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I logout agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGOFF" event for agent "007" in the queue log
