Feature: Stat

    Scenario: Generation of event "COMPLETECALLER"
        Given there is no queue with name "q8"
        Given there is no queue with number "5008"
        Given there is no agent with number "008"
        Given there is no user "User" "008"
        Given there is no "COMPLETECALLER" entry in queue "q8"
        Given there is a user "User" "008" in context "statscenter" with number "1008"
        Given there is a agent "Agent" "008" in context "statscenter" with number "008"
        Given there is a queue "q8" in context "statscenter" with number "5008" with agent "008"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "008" on extension "1008"
        Given I wait 5 seconds for the calls processing
        Given I wait call then wait
        Given I wait 2 seconds for the calls processing
        Given there is 1 calls to extension "5008" of a duration of 5 seconds
        Given I wait 10 seconds for the calls processing
        Then i should see 1 "COMPLETECALLER" event in queue "q8" in the queue log