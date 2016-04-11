"""
    Configuration of command line options and other test parameters
"""

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="local", help="Host is local, stag or prod")
    parser.addoption("--api_key", action="store", default=None, help="Your API key")
