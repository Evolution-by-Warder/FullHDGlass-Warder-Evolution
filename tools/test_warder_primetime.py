"""Dependency-free unit tests for the Warder PrimeTime lookup core."""
import datetime
import unittest
from unittest.mock import Mock
from warderPrimeTime import prime_time_event, target_timestamp


class PrimeTimeTests(unittest.TestCase):
    def test_current_day_and_rollover(self):
        noon = datetime.datetime(2026, 11, 7, 12, 0).timestamp()
        evening = datetime.datetime(2026, 11, 7, 21, 0).timestamp()
        self.assertEqual(datetime.datetime.fromtimestamp(target_timestamp(noon)), datetime.datetime(2026, 11, 7, 20, 25))
        self.assertEqual(datetime.datetime.fromtimestamp(target_timestamp(evening)), datetime.datetime(2026, 11, 8, 20, 25))

    def test_clock_validation(self):
        with self.assertRaises(ValueError):
            target_timestamp(0, 25, 0)

    def test_matching_event_only(self):
        now = datetime.datetime(2026, 11, 7, 12).timestamp()
        target = target_timestamp(now)
        event = Mock()
        event.getBeginTime.return_value = target - 600
        event.getDuration.return_value = 3600
        event.getEventName.return_value = "Večerný film"
        cache = Mock()
        cache.lookupEventTime.return_value = event
        self.assertEqual(prime_time_event(cache, "service", now), (target, "Večerný film"))
        cache.lookupEventTime.assert_called_once_with("service", target)
        event.getDuration.return_value = 120
        self.assertIsNone(prime_time_event(cache, "service", now))

    def test_absent_epg(self):
        self.assertIsNone(prime_time_event(None, "service", 0))
        self.assertIsNone(prime_time_event(Mock(lookupEventTime=Mock(return_value=None)), "service", 0))


if __name__ == "__main__":
    unittest.main()
