Feature: PostInstall Files

    Scenario: Debian sources list points on right mirrors
        Then the mirror list contains a line matching "mirror.xivo.io"
        Then the mirror list does not contain a line matching "avencall.com"
