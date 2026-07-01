class SegmentEngine:
    """
    v1.0 Segment Router (Stable Production Logic)
    """

    def resolve(self, i, total):
        p = i / max(1, total)

        # LOCKED SEGMENTS (your final design)
        if p < 0.50:
            return 0   # Segment A
        elif p < 0.65:
            return 1   # Segment B
        elif p < 0.80:
            return 2   # Segment C
        else:
            return 3   # Segment D