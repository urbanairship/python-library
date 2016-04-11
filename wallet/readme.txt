*****************************************************************
*               Urban Airship Wallet Python API                 *
*                  Documentation and Setup                      |
**********************************************************=-

+ Introduction

The Wallet Python API allows easy access to the Urban Airship
API for managing Android Pay and Apple Wallet digital wallet
templates and passes.

+ Installation

In the directory with the setup.py (python/)

python setup.py install

+ Use

wallet = Wallet()

Each member function of the wallet object corresponds to a restful
call. Consult the API documentation for more information:

http://docs.urbanairship.com/api/wallet.html

In order to access the API each user needs a private API key
Your key can be located in the Wallet UI under:
https://wallet.urbanairship.com/account (API Management)

The API key can either be passed to the Wallet constructor directly
but more conveniently each API key can be stored in your local systems
environment variables. This also makes it much more convenient to
switch between different environments.

On OSX its convenient to define your API keys in your .bash_profile
like this:

export UA_API_KEY_PROD=[Your production API key]
export UA_API_KEY_STAG=[Your staging API key]
export UA_API_KEY_LOCAL=[Your localhost API key]

+ Directory Structure

This is an overview of the wallet API directory structure

    api/      - Contains the api code and helper functions
    tests/    - Contains test suites for internal testing
    scripts/  - Other misc scripts. Feel free to check in stuff here
    examples/ - Examples using the high level API

+ High Level API

All of the object classes for the API are represented with an object model
To understand how to use them look in the examples directory and in the
API code.

+ Misc info

Functions that take a payload accepts either a high level object, a dictionary
or a string. Example: create_templates payload can accept either of them.

All functions that return JSON returns them as a dictionary


