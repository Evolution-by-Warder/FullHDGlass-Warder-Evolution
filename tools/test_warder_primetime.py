"""Dependency-free unit tests for the Warder PrimeTime lookup core."""
import datetime
import unittest
from unittest.mock import Mock
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPrimeTime.py"
spec = spec_from_file_location("warderPrimeTime", MODULE)
warder = module_from_spec(spec)
spec.loader.exec_module(warder)
prime_time_event = warder.prime_time_event
target_timestamp = warder.target_timestamp


class PrimeTimeTests(unittest.TestCase):
    def test_current_day_and_rollover(self):
        noon = datetime.datetime(2026, 11, 7, 12, 0).timestamp()
        evening = datetime.datetime(2026, 11, 7, 21, 0).timestamp()
        self.assertEqual(datetime.datetime.fromtimestamp(target_timestamp(noon)), datetime.datetime(2026, 11, 7, 20, 25))
        self.assertEqual(datetime.datetime.fromtimestamp(target_timestamp(evening)), datetime.datetime(2026, 11, 8, 20, 25))

    def test_exact_cutoff_still_uses_todays_event(self):
        cutoff = datetime.datetime(2026, 11, 7, 20, 25, 0).timestamp()
        self.assertEqual(target_timestamp(cutoff), int(cutoff))
        after = cutoff + 1
        self.assertEqual(
            datetime.datetime.fromtimestamp(target_timestamp(after)),
            datetime.datetime(2026, 11, 8, 20, 25),
        )

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

    def test_event_at_exact_start_and_end_boundaries(self):
        now = datetime.datetime(2026, 11, 7, 12).timestamp()
        target = target_timestamp(now)
        event = Mock()
        event.getBeginTime.return_value = target
        event.getDuration.return_value = 1800
        event.getEventName.return_value = "Prime Time film"
        cache = Mock(lookupEventTime=Mock(return_value=event))
        self.assertEqual(prime_time_event(cache, "channel-a", now), (target, "Prime Time film"))
        event.getBeginTime.return_value = target - 1800
        self.assertIsNone(prime_time_event(cache, "channel-a", now))
        event.getBeginTime.return_value = target - 1801
        self.assertIsNone(prime_time_event(cache, "channel-a", now))

    def test_empty_invalid_and_zero_length_events_are_ignored(self):
        now = datetime.datetime(2026, 11, 7, 12).timestamp()
        target = target_timestamp(now)
        event = Mock()
        event.getBeginTime.return_value = target
        event.getDuration.return_value = 0
        event.getEventName.return_value = "Invalid"
        cache = Mock(lookupEventTime=Mock(return_value=event))
        self.assertIsNone(prime_time_event(cache, "channel-a", now))
        event.getDuration.return_value = 60
        event.getEventName.return_value = ""
        self.assertIsNone(prime_time_event(cache, "channel-a", now))
        cache.lookupEventTime.side_effect = RuntimeError("EPG cache unavailable")
        self.assertIsNone(prime_time_event(cache, "channel-a", now))

    def test_selected_service_is_passed_to_epg_cache(self):
        now = datetime.datetime(2026, 11, 7, 12).timestamp()
        cache = Mock(lookupEventTime=Mock(return_value=None))
        for ref in ("channel-a", "channel-b"):
            self.assertIsNone(prime_time_event(cache, ref, now, 21, 15))
            cache.lookupEventTime.assert_called_with(ref, target_timestamp(now, 21, 15))
        self.assertEqual(cache.lookupEventTime.call_count, 2)

    def test_absent_epg(self):
        self.assertIsNone(prime_time_event(None, "service", 0))
        self.assertIsNone(prime_time_event(Mock(lookupEventTime=Mock(return_value=None)), "service", 0))


if __name__ == "__main__":
    unittest.main()
