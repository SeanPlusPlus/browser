import sys
import io
from contextlib import redirect_stdout
from browser import URL, get_body, show  # Assuming your previous script is named 'browser.py'

# Unicode symbols for success and failure
GREEN_CHECK = '\u2705'  # ✔
RED_X = '\u274C'        # ✖

def run_tests(verbose=False):
    tests = [
        ("Test data URL with plain text", "data:text/html,Hello", "Hello"),
        ("Test data URL with HTML entities", "data:text/html,&lt;div&gt;Hello", "<div>Hello"),
        ("Test local file URL", "file:///Users/Sean.M.Stephenson/hello", "hello world"),
        ("Test https URL", "https://browser.engineering/examples/example1-simple.html", 
         "This is a simple\n    web page with some\n    text in it."),
        ("Test view-source URL", "view-source:https://browser.engineering/examples/example1-simple.html", 
         "<html>\n  <body>\n    <div>This is a simple</div>\n    <div>web page with some</div>\n    <span>text in it.</span>\n  </body>\n</html>"),
        ("Test text", "https://browser.engineering/http.html", 'A web browser displays information identified by a URL.', True),
        # For this test, we're checking for a specific string in the redirected page
        ("Test 301", "http://browser.engineering/redirect", 'A web browser displays information identified by a URL.', True)
    ]

    for test in tests:
        # Unpack with a default value for `check_partial`
        title, test_case, expected_output = test[:3]
        check_partial = test[3] if len(test) > 3 else False

        print(f"Running: {title}")
        print(f"URL: {test_case}")
        try:
            url = URL(test_case)
            result = get_body(url)

            # Capture the output of the `show` function
            with io.StringIO() as buf, redirect_stdout(buf):
                show(result, url.view_source)  # Pass view_source flag to show
                output = buf.getvalue().strip()

            # Debug: Print the entire output of the test case
            if verbose:
                print(f"Full Output:\n{repr(output)}\n")  # Use repr to see any special characters
                print(f"Expected: {repr(expected_output)}\n")

            if check_partial:
                # Check if the expected string is present in the output (partial check)
                assert expected_output in output, f"Test failed for {title}. Expected output to contain: '{expected_output}', but it was not found."
            else:
                assert output == expected_output, f"Test failed for {title}. Expected: '{expected_output}', got: '{output}'"

            print(f"{title} passed. {GREEN_CHECK}\n")
        except AssertionError as e:
            print(f"{RED_X} {e}\n")
        except Exception as e:
            print(f"{RED_X} Error during {title}: {e}\n")

if __name__ == "__main__":
    # Check if --verbose flag is passed
    verbose = '--verbose' in sys.argv
    run_tests(verbose=verbose)
