
import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import json
from fetch import fetch_url, get_metadata, save_metadata, load_metadata, process_url
import os

class TestFetch(unittest.TestCase):

    @patch('fetch.requests.get')
    def test_fetch_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body>Test content</body></html>"
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_get.return_value = mock_response

        content, content_type = fetch_url("https://example.com")
        self.assertEqual(content, "<html><body>Test content</body></html>")
        self.assertEqual(content_type, 'text/html')

    def test_get_metadata(self):
        content = "<html><body><a href='#'>Link</a><img src='image.jpg'></body></html>"
        url = "https://example.com"
        metadata = get_metadata(content, url)

        self.assertEqual(metadata['site'], 'example.com')
        self.assertEqual(metadata['num_links'], 1)
        self.assertEqual(metadata['images'], 1)
        self.assertIn('last_fetch', metadata)

    @patch('fetch.os.path.exists')
    @patch('fetch.open', new_callable=mock_open, read_data='{"site": "example.com", "num_links": 1, "images": 1, "last_fetch": "2023-05-10 12:00 UTC"}')
    def test_load_metadata(self, mock_file, mock_exists):
        mock_exists.return_value = True
        metadata = load_metadata('metadata.json')
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['site'], 'example.com')
        self.assertEqual(metadata['num_links'], 1)
        self.assertEqual(metadata['images'], 1)
        self.assertEqual(metadata['last_fetch'], '2023-05-10 12:00 UTC')

if __name__ == '__main__':
    unittest.main()