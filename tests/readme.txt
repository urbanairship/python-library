*****************************************************************
*       Urban Airship Wallet API Integration Test Suite         *
*                  Documentation and Setup                      |
**********************************************************=-

    setup:
        install requests and pytest modules
        cd to tests directory

    usage:

        All tests (standard):
            py.test

        Show STDOUT:
            py.test -s

        Change Environment/key:
            py.test --host prod --api_key XXX

        Verbose output:
            py.test -v

        Time tests:
            py.test --duration=50

        Run subset of tests:
            py.test -k _api
            py.test -k _object
