import sys
import io
from contextlib import redirect_stdout
from browser import URL, get_body, show  # Assuming your previous script is named 'browser.py'

# Unicode symbols for success and failure
GREEN_CHECK = '\u2705'  # ✔
RED_X = '\u274C'        # ✖

def run_tests(verbose=False):
    tests = [
        ("Test data URL with plain text", "data:text/html,Hello", "Hello", False),
        ("Test data URL with HTML entities", "data:text/html,&lt;div&gt;Hello", "<div>Hello", False),
        ("Test local file URL", "file:///Users/Sean.M.Stephenson/hello", "hello world", False),
        ("Test https URL", "https://browser.engineering/examples/example1-simple.html", 
         "This is a simple\n    web page with some\n    text in it.", False),
        ("Test view-source URL", "view-source:https://browser.engineering/examples/example1-simple.html", 
         "<html>\n  <body>\n    <div>This is a simple</div>\n    <div>web page with some</div>\n    <span>text in it.</span>\n  </body>\n</html>", True),
    ]

    for title, test_case, expected_output, view_source in tests:
        print(f"Running: {title}")
        print(f"URL: {test_case}")
        try:
            url = URL(test_case)
            result = get_body(url)

            # Capture the output of the `show` function
            with io.StringIO() as buf, redirect_stdout(buf):
                show(result, url.view_source)  # Pass view_source flag to show
                output = buf.getvalue().strip()

            if verbose:
                print(f"Output: {output}")

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
