import os
import sys
import io
from contextlib import redirect_stdout
from browser import URL, get_body, show  # Assuming your previous script is named 'browser.py'

# Unicode symbols for success and failure
GREEN_CHECK = '\u2705'  # ✔
RED_X = '\u274C'        # ✖

def run_tests(verbose=False):
    tests = [
        ("data:text/html,Hello", "Hello"),
        ("data:text/html,&lt;div&gt;Hello", "<div>Hello"),
        ("file:///Users/Sean.M.Stephenson/hello", "hello world"),
        ("https://browser.engineering/examples/example1-simple.html", "This is a simple\n    web page with some\n    text in it."),
    ]
    
    for test_case, expected_output in tests:
        print(f"Running test for URL: {test_case}")
        try:
            url = URL(test_case)
            result = get_body(url)

            # Capture the output of the `show` function
            with io.StringIO() as buf, redirect_stdout(buf):
                show(result)
                output = buf.getvalue().strip()

            if verbose:
                print(f"Output: {output}")

            assert output == expected_output, f"Test failed for URL: {test_case}. Expected: '{expected_output}', got: '{output}'"
            print(f"Test passed. {GREEN_CHECK}\n")
        except AssertionError as e:
            print(f"{RED_X} {e}\n")
        except Exception as e:
            print(f"{RED_X} Error during test: {e}\n")

if __name__ == "__main__":
    # Check if --verbose flag is passed
    verbose = '--verbose' in sys.argv
    run_tests(verbose=verbose)
