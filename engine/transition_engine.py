from moviepy.video import fx as vfx


class TransitionEngine:

    def __init__(self):
        self.t = 0.15

    def _safe(self, clip):
        if not hasattr(clip, "duration") or clip.duration is None:
            clip = clip.set_duration(3)
        return clip

    def apply(self, clips):

        out = []

        for c in clips:
            c = self._safe(c)

            try:
                c = c.fx(vfx.fadein, self.t).fx(vfx.fadeout, self.t)
            except:
                pass

            out.append(c)

        return out