import unittest
import time
from app import app, get_average_altitude, calculate_health

MIN_ALTITUDE_THRESHOLD = 160  # Threshold for warning message
LOW_ORBIT_WARNING_INTERVAL = 60 # 1 minute in seconds

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_average_altitude_empty_data(self):
        # Test when data is empty, the average altitude should be 0
        data = []
        self.assertEqual(get_average_altitude(data), 0)

    def test_get_average_altitude_non_empty_data(self):
        # Test the average altitude calculation with non-empty data
        data = [
            {'altitude': 173.70318186463913, 'last_updated': 1691379870.0},
            {'altitude': 170.41987555688507, 'last_updated': 1691379880.0},
            {'altitude': 165.61909890123886, 'last_updated': 1691379890.0},
            {'altitude': 160.00000000000023, 'last_updated': 1691379900.0},
            {'altitude': 154.38090109876157, 'last_updated': 1691379910.0},
            {'altitude': 149.58012444311527, 'last_updated': 1691379920.0},
            {'altitude': 146.29681813536104, 'last_updated': 1691379930.0},
            {'altitude': 145.00913759471356, 'last_updated': 1691379940.0}
        ]
        # Expected average altitude is the sum of altitudes divided by the number of data points
        expected_average = sum(record['altitude'] for record in data) / len(data)
        self.assertEqual(get_average_altitude(data), expected_average)

    def test_health_ok(self):
        # Simulate normal altitude data
        simulated_data = [
            {'altitude': 160.0, 'last_updated': (time.time() - 45)},  # Within the last minute
            {'altitude': 165.0, 'last_updated': (time.time() - 40)},
            {'altitude': 170.0, 'last_updated': (time.time() - 35)},
            {'altitude': 160.0, 'last_updated': (time.time() - 30)},
            {'altitude': 165.0, 'last_updated': (time.time() - 25)},
        ]

        result_message = calculate_health(simulated_data, MIN_ALTITUDE_THRESHOLD, LOW_ORBIT_WARNING_INTERVAL, time.time() - 61)
        self.assertEqual(result_message, 'Altitude is A-OK')

    def test_health_low_altitude_warning(self):
        # Simulate low altitude by adding data points with altitude below the threshold
        simulated_data = [
            {'altitude': 150.0, 'last_updated': (time.time() - 45)},  # Within the warning interval
            {'altitude': 155.0, 'last_updated': (time.time() - 40)},
            {'altitude': 140.0, 'last_updated': (time.time() - 35)},
            {'altitude': 160.0, 'last_updated': (time.time() - 30)},
            {'altitude': 148.0, 'last_updated': (time.time() - 25)},
        ]

        result_message = calculate_health(simulated_data, MIN_ALTITUDE_THRESHOLD, LOW_ORBIT_WARNING_INTERVAL, time.time())
        self.assertEqual(result_message, 'WARNING: RAPID ORBITAL DECAY IMMINENT')

    def test_health_low_altitude_recovered(self):
        # Simulate low altitude warning and then wait for the recovery interval
        simulated_data = [
            {'altitude': 170.0, 'last_updated': (time.time() - 70)},  # Beyond the warning interval
            {'altitude': 175.0, 'last_updated': (time.time() - 65)},
            {'altitude': 180.0, 'last_updated': (time.time() - 60)},
            {'altitude': 185.0, 'last_updated': (time.time() - 55)},
            {'altitude': 190.0, 'last_updated': (time.time() - 50)},
        ]

        result_message = calculate_health(simulated_data, MIN_ALTITUDE_THRESHOLD, LOW_ORBIT_WARNING_INTERVAL, time.time() - 30)
        self.assertEqual(result_message, 'Sustained Low Earth Orbit Resumed')

    def test_health_response_status_code(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
