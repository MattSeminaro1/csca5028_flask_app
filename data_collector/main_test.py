import unittest
from unittest.mock import patch, MagicMock
import main  # Assuming your script is named main.py

class TestMain(unittest.TestCase):

    @patch('main.requests.get')
    def test_find_endpoints_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = """
            <a href="/boxes/CHN/CHN202204070.shtml">Game 1</a>
            <a href="/boxes/NYN/NYN202204070.shtml">Game 2</a>
        """
        mock_get.return_value = mock_response

        endpoints = main.find_endpoints('https://www.example.com')

        self.assertEqual(endpoints, ['https://www.example.com/boxes/CHN/CHN202204070.shtml', 'https://www.example.com/boxes/NYN/NYN202204070.shtml'])

    @patch('main.webdriver.Chrome')
    def test_get_stat_data(self, mock_driver):
        mock_driver_instance = MagicMock()
        mock_driver_instance.page_source = '<div id="csv">...</div>'
        mock_driver.return_value = mock_driver_instance

        endpoints = ['https://www.example.com/game1', 'https://www.example.com/game2']
        batting_data = main.get_stat_data(endpoints, 'batting')
        pitching_data = main.get_stat_data(endpoints, 'pitching')

        self.assertEqual(len(batting_data), 2)
        self.assertEqual(len(pitching_data), 2)

if __name__ == '__main__':
    unittest.main()
