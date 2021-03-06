Feature: Service

    Scenario: Disabling all forwards on XiVO Client hide the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | BLFMan    | Forward  | Client      | blfman    | password   | sip      | default | 1801   | 
        Given the user "BLFMan Forward" with the following func keys:
         | blf  | destination_type | destination_forward | destination_exten |
         | true |      forward     |      noanswer       |                   |
         | true |      forward     |      noanswer       |       1234        |
         | true |      forward     |    unconditional    |                   |
         | true |      forward     |    unconditional    |       5678        |
         | true |      forward     |        busy         |                   |
         | true |      forward     |        busy         |       0912        |
        Given the "Enable forwarding on no-answer" extension is enabled
        Given the "Enable forwarding on busy" extension is enabled
        Given the "Enable unconditional forwarding" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "blfman", pass "password"
        Given I enable forwarding on no-answer with destination "1234" on XiVO Client
        Given I enable forwarding on busy with destination "5678" on XiVO Client
        Given I enable unconditional forwarding with destination "0912" on XiVO Client
        When I wait 1 seconds
        When I disable all forwards on XiVO Client
        Then the user "BLFMan Forward" has all forwards hints disabled
        Then the disable all forwards is enabled on XiVO Client
        Then the forwarding on no-answer is disabled on XiVO Client
        Then the forwarding on busy is disabled on XiVO Client
        Then the unconditional forwarding is disabled on XiVO Client

    Scenario: Enabling no-answer forward on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | NoAnswer  | Forward  | Client      | noanswer  | password   | sip      | default | 1802   | 
        Given the user "NoAnswer Forward" with the following func keys:
         | blf  | destination_type | destination_forward | destination_exten |
         | true |      forward     |      noanswer       |                   |
         | true |      forward     |      noanswer       |       1234        |
        Given the "Enable forwarding on no-answer" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "noanswer", pass "password"
        When I enable forwarding on no-answer with destination "1234" on XiVO Client
        Then the user "NoAnswer Forward" has the "noanswer" forward hint enabled
        Then the forwarding on no-answer is enabled with destination "1234" on XiVO Client

    Scenario: Enabling wrong no-answer forward on XiVO Client hide the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | WNoAnswer | Forward  | Client      | wnoanswer | password   | sip      | default | 1803   | 
        Given the user "WNoAnswer Forward" with the following func keys:
         | blf  | destination_type | destination_forward | destination_exten |
         | true |      forward     |      noanswer       |       1234        |
        Given the "Enable forwarding on no-answer" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "wnoanswer", pass "password"
        When I enable forwarding on no-answer with destination "5678" on XiVO Client
        Then the user "WNoAnswer Forward" has the "noanswer" forward hint disabled
        Then the forwarding on no-answer is enabled with destination "5678" on XiVO Client

    Scenario: Enabling busy forward on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | Busy      | Forward  | Client      | busy      | password   | sip      | default | 1804   | 
        Given the user "Busy Forward" with the following func keys:
         | blf  | destination_type | destination_forward | destination_exten |
         | true |      forward     |        busy         |                   |
         | true |      forward     |        busy         |       0912        |
        Given the "Enable forwarding on busy" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "busy", pass "password"
        When I enable forwarding on busy with destination "0912" on XiVO Client
        Then the user "Busy Forward" has the "busy" forward hint enabled
        Then the forwarding on busy is enabled with destination "0912" on XiVO Client

    Scenario: Enabling wrong busy forward on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | WBusy     | Forward  | Client      | wbusy     | password   | sip      | default | 1805   | 
        Given the user "WBusy Forward" with the following func keys:
         | blf  | destination_type | destination_forward | destination_exten |
         | true |      forward     |        busy         |       1234        |
        Given the "Enable forwarding on busy" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "wbusy", pass "password"
        When I enable forwarding on busy with destination "5678" on XiVO Client
        Then the user "WBusy Forward" has the "busy" forward hint disabled
        Then the forwarding on busy is enabled with destination "5678" on XiVO Client

    Scenario: Enabling unconditional forward on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | Uncond    | Forward  | Client      | uncond    | password   | sip      | default | 1806   | 
        Given the user "Uncond Forward" with the following func keys:
         | blf  | destination_type | destination_forward | destination_exten |
         | true |      forward     |    unconditional    |                   |
         | true |      forward     |    unconditional    |       5678        |
        Given the "Enable unconditional forwarding" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "uncond", pass "password"
        When I enable unconditional forwarding with destination "5678" on XiVO Client
        Then the user "Uncond Forward" has the "unconditional" forward hint enabled
        Then the unconditional forwarding is enabled with destination "5678" on XiVO Client

    Scenario: Enabling unconditional forward on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | WUncond   | Forward  | Client      | wuncond   | password   | sip      | default | 1807   | 
        Given the user "WUncond Forward" with the following func keys:
         | blf  | destination_type | destination_forward | destination_exten |
         | true |      forward     |    unconditional    |       1234        |
        Given the "Enable unconditional forwarding" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "wuncond", pass "password"
        When I enable unconditional forwarding with destination "5678" on XiVO Client
        Then the user "WUncond Forward" has the "unconditional" forward hint disabled
        Then the unconditional forwarding is enabled with destination "5678" on XiVO Client

    Scenario: Enabling DND on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | DND       | Service  | Client      | dnd       | password   | sip      | default | 1808   | 
        Given the user "DND Service" with the following func keys:
         | blf  | destination_type | destination_service |
         | true |      service     |    enablednd        |
        Given the "Do not disturb" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "dnd", pass "password"
        When I enable DND on XiVO Client
        Then the user "DND Service" has the "dnd" hint enabled
        Then the DND is enabled on XiVO Client

    Scenario: Disabling DND on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | DND       | Service  | Client      | dnd       | password   | sip      | default | 1809   | 
        Given the user "DND Service" with the following func keys:
         | blf  | destination_type | destination_service |
         | true |      service     |    enablednd        |
        Given the "Do not disturb" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "dnd", pass "password"
        When I disable DND on XiVO Client
        Then the user "DND Service" has the "dnd" hint disabled
        Then the DND is disabled on XiVO Client

    Scenario: Enabling incoming call filtering on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | IncallFil | Service  | Client      | incallfil | password   | sip      | default | 1810   | 
        Given the user "IncallFil Service" with the following func keys:
         | blf  | destination_type | destination_service |
         | true |      service     |    incallfilter     |
        Given the "Incoming call filtering" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "incallfil", pass "password"
        When I enable incoming call filtering on XiVO Client
        Then the user "IncallFil Service" has the "incallfilter" hint enabled
        Then the incoming call filtering is enabled on XiVO Client

    Scenario: Disabling incoming call filtering on XiVO Client show the BLF
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | protocol | context | number |
         | IncallFil | Service  | Client      | incallfil | password   | sip      | default | 1811   | 
        Given the user "IncallFil Service" with the following func keys:
         | blf  | destination_type | destination_service |
         | true |      service     |    incallfilter     |
        Given the "Incoming call filtering" extension is enabled
        Given I start the XiVO Client
        Given I log in the XiVO Client as "incallfil", pass "password"
        When I disable incoming call filtering on XiVO Client
        Then the user "IncallFil Service" has the "incallfilter" hint disabled
        Then the incoming call filtering is disabled on XiVO Client
