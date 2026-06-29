class SegmentEngine:

    def resolve(self, i, total):

        p = i / max(1, total)

        # 4 CLEAN CINEMATIC SEGMENTS

        if p < 0.50:
            return "field_motion"      # HERO SEGMENT (50%)

        elif p < 0.65:
            return "conveyor"          # FLOW SEGMENT (15%)

        elif p < 0.80:
            return "split_depth"       # 3D SEGMENT (15%)

        else:
            return "radial_motion"     # CLIMAX SEGMENT (20%)