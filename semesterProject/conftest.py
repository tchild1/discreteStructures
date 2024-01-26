def pytest_addoption(parser):
    parser.addoption(
        "--bucket", action="store", help="Bucket number for testing"
    )