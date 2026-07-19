class SegmentEngine:
    """
    v1.0 Segment Router (Stable Production Logic)
    """

    def resolve(self, i, total):
        p = i / max(1, total)

        # TRUE 25% SEGMENT TIMELINE
        if p < 0.25:
            return 0   # Segment 1
        elif p < 0.50:
            return 1   # Segment 2
        elif p < 0.75:
            return 2   # Segment 3
        else:
            return 3   # Segment 4