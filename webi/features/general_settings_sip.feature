Feature: General Settings SIP

    Scenario: Global Encryption
        I go on the General Settings > SIP Protocol page, tab "Security"
        When I enable the "Encryption" option
        Then I should see "encryption" to "yes" in "sip.conf"
        I go on the General Settings > SIP Protocol page, tab "Security"
        When I disable the "Encryption" option
        Then I should see "encryption" to "no" in "sip.conf"

    Scenario: ISDN compatibility
        I go on the General Settings > SIP Protocol page, tab "Signaling"
        When I enable the "ISDN compatibility (early media)" option
        Then I should see "prematuremedia" to "no" in "sip.conf"
        I go on the General Settings > SIP Protocol page, tab "Signaling"
        When I disable the "ISDN compatibility (early media)" option
        Then I should see "prematuremedia" to "yes" in "sip.conf"