Feature: Stat

    Scenario: Call a queue that is saturated
        Given there is no queue with name "q1"
        Given there is no queue with number "5001"
        Given there is no "FULL" entry in queue "q1"
        Given there is a queue "q1" in context "statscenter" with number "5001" that is statured
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 4 calls to extension "5001"
        Given I wait 5 seconds for the calls processing
        Then i should see 3 "FULL" event in queue "q1" in the queue log