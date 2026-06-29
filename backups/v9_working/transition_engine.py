import numpy as np

from moviepy.video import fx as vfx


class TransitionEngine:

    def __init__(self):
        self.transition_time = 0.3

    # -----------------------------
    # SAFE DURATION GUARD
    # -----------------------------
    def _safe(self, clip):
        if not hasattr(clip, "duration") or clip.duration is None:
            clip = clip.set_duration(3.0)
        return clip

    # -----------------------------
    # CROSSFADE (SAFE)
    # -----------------------------
    def crossfade(self, clip):

        clip = self._safe(clip)

        try:
            return (
                clip.fx(vfx.fadein, self.transition_time)
                    .fx(vfx.fadeout, self.transition_time)
            )

        except Exception:
            # fallback: no transition if MoviePy fails
            return clip

    # -----------------------------
    # APPLY TRANSITIONS TO LIST
    # -----------------------------
    def apply(self, clips):

        if not clips:
            return clips

        processed = []

        for i, clip in enumerate(clips):

            clip = self._safe(clip)

            # only apply fade between clips (not mandatory)
            clip = self.crossfade(clip)

            processed.append(clip)

        return processed