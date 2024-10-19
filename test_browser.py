import unittest
from unittest.mock import patch, mock_open, MagicMock
import socket
from browser import URL, get_body

class TestBrowser(unittest.TestCase):

    @patch("socket.socket")
    @patch("ssl.SSLContext.wrap_socket")
    def test_http_request(self, mock_wrap_socket, mock_socket):
        # Mocking the socket's response to simulate an HTTP request
        mock_socket_inst = mock_socket.return_value
        mock_socket_inst.connect.return_value = None
        
        # Create a mock for makefile() that simulates file-like behavior
        mock_makefile = MagicMock()
        mock_makefile.readline.side_effect = [
            "HTTP/1.0 200 OK\r\n",
            "Content-Length: 38\r\n",
            "Connection: close\r\n",
            "\r\n"
        ]
        mock_makefile.read.return_value = "This is a simple web page with some text in it."

        # Assign the mock to the makefile method
        mock_socket_inst.makefile.return_value = mock_makefile

        # Mock SSL wrapping of the socket
        mock_wrap_socket.return_value = mock_socket_inst

        url = URL("https://browser.engineering/examples/example1-simple.html")
        body = get_body(url)

        self.assertIn("This is a simple web page with some text in it.", body)

    @patch("builtins.open", new_callable=mock_open, read_data="hello world")
    @patch("os.path.exists", return_value=True)
    def test_file_request(self, mock_exists, mock_file):
        url = URL("file:///Users/Sean.M.Stephenson/hello")
        body = get_body(url)

        self.assertEqual(body, "hello world")

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, mock_exists):
        url = URL("file:///Users/Sean.M.Stephenson/missing_file")
        body = get_body(url)

        self.assertEqual(body, "404 Not Found: File does not exist.")

if __name__ == "__main__":
    unittest.main()
