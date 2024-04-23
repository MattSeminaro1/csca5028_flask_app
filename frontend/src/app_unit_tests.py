import unittest
from flask_testing import TestCase
from app import app, get_pitchers, get_batters, get_summary_statistics
import psycopg2

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
    
    def test_database_connection(self):
        # Define connection parameters
        conn_params = {
            'dbname': 'db_init',
            'user': 'csca5028',
            'password': 'csca5028',
            'host': 'csca5028-db-instance.c1a04q2cyd4h.us-east-1.rds.amazonaws.com',
            'port': '5432'
        }

        # Attempt to connect to the database
        try:
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()

            # Check if the connection is successful
            self.assertTrue(conn is not None)
            self.assertTrue(cursor is not None)

            # Close the cursor and connection
            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            # If connection fails, fail the test
            self.fail(f"Database connection failed: {e}")

if __name__ == '__main__':
    unittest.main()
