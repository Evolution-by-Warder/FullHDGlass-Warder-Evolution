"""Prime-time EPG lookup for the selected Enigma2 service.

Independent of the screen renderer: no change to playback, fonts or channel list.
"""
from datetime import datetime, timedelta


def target_timestamp(now, hour=20, minute=25):
    """Return the next local prime-time point, including tomorrow after cutoff."""
    hour, minute = int(hour), int(minute)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError("Invalid prime-time clock")
    local = datetime.fromtimestamp(now)
    target = local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if local > target:
        target = (local + timedelta(days=1)).replace(
            hour=hour, minute=minute, second=0, microsecond=0)
    return int(target.timestamp())


def prime_time_event(cache, service, now, hour=20, minute=25):
    """Return (timestamp, event title) or None if the selected service lacks EPG.

    lookupEventTime(ref, timestamp) returns the event spanning the instant.
    Always confirm the event contains the requested timestamp: some image APIs
    return the nearest previous event when the requested time has no listing.
    """
    if cache is None or service is None:
        return None
    target = target_timestamp(now, hour, minute)
    try:
        event = cache.lookupEventTime(service, target)
        if event is None:
            return None
        begin = int(event.getBeginTime())
        duration = int(event.getDuration())
        if duration <= 0 or not (begin <= target < begin + duration):
            return None
        title = event.getEventName()
        return (target, title) if title else None
    except (AttributeError, RuntimeError, TypeError, ValueError):
        return None
