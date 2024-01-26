import os
import project5
import sys
import pytest

@pytest.fixture
def bucket(request):
    return request.config.getoption("--bucket")

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read()

def test_project1(bucket):
    TEST_ROOT_DIR = "./project5-passoff/" + bucket
    test_filenames = [f for f in os.listdir(TEST_ROOT_DIR) if f.startswith("input")]
    passed = True
    for filename in test_filenames:
        input_file = os.path.join(TEST_ROOT_DIR, filename)
        input_contents = read_file_contents(input_file)

        answer_file = os.path.join(TEST_ROOT_DIR, filename.replace('input', 'answer'))
        answer_contents = read_file_contents(answer_file)
        output = project5.project5(input_contents)
        try:
            assert answer_contents.rstrip() == output.rstrip()
            print("\n")
            print("Passed test: " + filename)
        except AssertionError as e:
            passed = False
            print("\n")
            print("Failed input: " + filename)
            print("-" * 100)
            assertion_error = str(e)
            assertion_error = assertion_error[assertion_error.find('\n  ') + 1:]
            print(assertion_error)
            print("-" * 100)
    assert passed

