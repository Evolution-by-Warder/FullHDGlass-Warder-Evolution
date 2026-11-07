"""Keep EPG titles inside their allocated pixels without changing user fonts."""


def fit_title_to_width(title, width, measure):
    """Return a whole or ellipsized title that fits the measured pixel width."""
    if not title or width <= 0:
        return ""
    if measure(title) <= width:
        return title
    ellipsis = "…"
    if measure(ellipsis) > width:
        return ""
    lo, hi = 0, len(title)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        candidate = title[:mid].rstrip() + ellipsis
        if measure(candidate) <= width:
            lo = mid
        else:
            hi = mid - 1
    return title[:lo].rstrip() + ellipsis
