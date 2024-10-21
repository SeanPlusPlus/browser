import os
import sys
from browser import URL, get_body  # Assuming your previous script is named 'browser.py'

# Unicode symbols for success and failure
GREEN_CHECK = '\u2705'  # ✔
RED_X = '\u274C'        # ✖

def run_tests(verbose=False):
    tests = [
        ("data:text/html,Hello", "Hello"),
        ("file:///Users/Sean.M.Stephenson/hello", "hello world"),  # Adjust this if needed based on your file content.
        ("https://browser.engineering/examples/example1-simple.html", "<html>\n  <body>\n    <div>This is a simple</div>\n    <div>web page with some</div>\n    <span>text in it.</span>\n  </body>\n</html>"),
    ]
    
    for test_case, expected_output in tests:
        print(f"Running test for URL: {test_case}")
        try:
            url = URL(test_case)
            result = get_body(url)
            
            # Handle cases where result is a list (e.g., data URLs)
            if isinstance(result, list):
                result = ''.join(result).strip()  # Join the list elements and strip whitespace
            else:
                result = result.strip()  # Just strip if it's a string

            if verbose:
                print(f"Output: {result}")
            
            assert result == expected_output, f"Test failed for URL: {test_case}. Expected: '{expected_output}', got: '{result}'"
            print(f"Test passed. {GREEN_CHECK}\n")
        except AssertionError as e:
            print(f"{RED_X} {e}\n")
        except Exception as e:
            print(f"{RED_X} Error during test: {e}\n")

if __name__ == "__main__":
    # Check if --verbose flag is passed
    verbose = '--verbose' in sys.argv
    run_tests(verbose=verbose)
