"""Read the codec name from the current image, retaining older image support."""

def image_codec_name(video_type):
    try:
        from Components.SystemInfo import VideoCodec
        return VideoCodec.getName(video_type, "")
    except (ImportError, AttributeError, TypeError, ValueError):
        pass
    try:
        from Components.Converter.PliExtraInfo import codec_data
        value = codec_data.get(video_type, "")
        return value if isinstance(value, str) and "/" not in value else ""
    except (ImportError, AttributeError, TypeError, ValueError):
        return ""
