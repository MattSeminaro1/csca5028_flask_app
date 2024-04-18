import unittest
from flask_testing import TestCase
from app import app, get_pitchers, get_batters, get_summary_statistics

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_pitching_endpoint(self):
        response = self.client.get('/pitching')
        self.assertEqual(response.status_code, 200)

    def test_batting_endpoint(self):
        response = self.client.get('/batting')
        self.assertEqual(response.status_code, 200)

    def test_select_endpoint_invalid_choice(self):
        response = self.client.get('/select/invalid_choice')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid choice', response.data)

    def test_get_pitchers(self):
        pitchers = get_pitchers()
        self.assertIsInstance(pitchers, list)
        # Add more assertions as needed

    def test_get_batters(self):
        batters = get_batters()
        self.assertIsInstance(batters, list)
        # Add more assertions as needed

    def test_get_summary_statistics_pitch(self):
        player = 'Player Name'
        num_games = 10
        summary_statistics = get_summary_statistics(player, num_games, 'pitch')
        self.assertIsInstance(summary_statistics, list)
        # Add more assertions as needed

    def test_get_summary_statistics_bat(self):
        player = 'Player Name'
        num_games = 10
        summary_statistics = get_summary_statistics(player, num_games, 'bat')
        self.assertIsInstance(summary_statistics, list)
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
