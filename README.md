#XiVO Acceptance

xivo-acceptance is a testing framework for running automated tests on a XiVO
server. These tests are used for fixing regressions and testing features before
releasing a new version of XiVO.


#Prerequisites

For Linphone to work, you must do:

    adduser jenkins audio  #Jenkins is the user tunning the tests


#Configuration

Create a yaml local configuration file in ```~/.xivo-acceptance/default``` and
redefine only options that need to be changed. Default options can be found in
```xivo_acceptance/config.py```. Usually, you will only need to change the IP
addresses and subnets. For example:

    ;IP address of the XIVO server
    xivo_host: 192.168.0.10

    ;we need to allow access from the test machine to the server.
    ;add a subnet that includes the test machine's IP address
    prerequisites:
        subnets: 
			- 10.0.0.0/8
			- 192.168.0.0/24


#Getting Started

##Usage

	usage: xivo-acceptance [-h] [-i INTERNAL_FEATURES] [-p] [-v] [-x XIVO_HOST]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -i INTERNAL_FEATURES, --internal-features INTERNAL_FEATURES
	                        execute internal features
	  -p, --prerequisite    execute prerequisite
	  -v, --verbose         verbose mode
	  -x XIVO_HOST, --xivo-host XIVO_HOST
	                        xivo host

##Internal Features Structure

    /usr/share/xivo-acceptance/features
    |-- daily
    |   |-- backup
    |   |--...
    |   |-- user
    |   |   |-- client.feature
    |   |   |-- ...
    |   |   |-- webi.feature
    |   `-- xivo_configuration
    |-- example
    |   `-- example.feature
    `-- pre_daily
        |-- 01_post_install
        `-- 02_wizard
        ...

Launch daily features:

    $XA_CMD="xivo-acceptance -v -i daily"

Launch daily/webi features:

    $XA_CMD="xivo-acceptance -v -i daily/webi"

Launch admin_user.feature feature:

    $XA_CMD="xivo-acceptance -v -i daily/webi/admin_user"


##Requirements

We recommend running tests on a dedicated debian machine. Run the following
commands to install requirements:

    apt-get install libsasl2-dev xvfb xserver-xephyr linphone-nogtk python-dev postgresql-server-dev-all libldap2-dev lsof
    pip install -r requirements.txt

Once the requirements are installed, modify the configuration files and run the prerequisite script:

    python ./bin/xivo-acceptance -p


##XiVO Client

Tests require a local copy of the [XiVO Client](http://github.com/xivo-pbx/xivo-client-qt)
on the test machine with FUNCTESTS enabled. Here is a quick example on how to
install and compile the client:

    git clone git://github.com/xivo-pbx/xivo-client-qt
    cd xivo-client-qt
    qmake
    make FUNCTESTS=yes


##Configuration

Create a local configuration file in ```~/.xivo-acceptance/default``` and
redefine only options that need to be changed. Default options can be found in
```xivo_acceptance/config.py```. Usually, you will only need to change the IP
addresses and subnets. For example:

    browser:
        enable: True

    ;IP address of the XIVO server
    xivo_host: 192.168.0.10

    ;we need to allow access from the test machine to the server.
    ;add a subnet that includes the test machine's IP address
    prerequisites:
    	subnets:
			- 10.0.0.8/24
			- 192.168.0.0/24


#Running tests

Tests can be found in the ```features``` directory. You can run all tests:

    PYTHONPATH=path/to/xivo_acceptance XC_PATH=/path/to/xivo-client-qt/bin lettuce data/features/daily

Or only a single test file:

    PYTHONPATH=path/to/xivo_acceptance XC_PATH=/path/to/xivo-client-qt/bin lettuce data/features/group/group.feature


If you're using firefox 47 or greater you can use the selenium/standalone-firefox docker image
to run your browser.

To start the browser:

    docker run -d -p "4444:4444" selenium/standalone-firefox


To configure xivo-acceptance to use the Remote webdriver modify your xivo-acceptance configuration:

    browser:
        docker: True


If you need to see what is going on in the browser, use the `selenium/standalone-firefox-debug` image, which runs a VNC server (the password is "secret"):

    docker run -d -p 4444:4444 -p 5901:5900 selenium/standalone-firefox-debug
