import librosa
import numpy as np
import os


class MusicEngine:

    def __init__(self, music_path):
        self.music_path = music_path
        self.y = None
        self.sr = None
        self.beats = []

    # -----------------------------
    # LOAD AUDIO SAFELY
    # -----------------------------
    def load(self):

        if not os.path.exists(self.music_path):
            raise FileNotFoundError(f"Music file not found: {self.music_path}")

        try:
            self.y, self.sr = librosa.load(self.music_path, sr=None)
            print(f"🎵 Audio loaded successfully (sr={self.sr})")

        except Exception as e:
            print(f"⚠️ Audio load failed: {e}")
            self.y, self.sr = None, None

    # -----------------------------
    # DETECT BEATS (CINEMATIC FIXED)
    # -----------------------------
    def detect_beats(self):

        if self.y is None:
            print("⚠️ No audio data — using fallback beats")
            return self._fallback_beats()

        try:
            tempo, beat_frames = librosa.beat.beat_track(y=self.y, sr=self.sr)

            beats = librosa.frames_to_time(beat_frames, sr=self.sr)

            # Convert to clean Python floats
            self.beats = [float(b) for b in beats]

            print(f"🎵 Raw beats detected: {len(self.beats)}")

            # -----------------------------
            # 🔥 FIX 1: REMOVE MICRO-BEATS
            # -----------------------------
            self.beats = self._filter_beats(self.beats)

            print(f"🎬 Cinematic beats final: {len(self.beats)}")

            return self.beats

        except Exception as e:
            print(f"⚠️ Beat detection failed: {e}")
            return self._fallback_beats()

    # -----------------------------
    # 🔥 BEAT FILTER (IMPORTANT FIX)
    # -----------------------------
    def _filter_beats(self, beats):

        if not beats:
            return []

        filtered = []

        min_gap = 0.65  # seconds (controls video speed)

        last = -999

        for b in beats:
            if b - last >= min_gap:
                filtered.append(b)
                last = b

        # Safety fallback
        if len(filtered) < 5:
            return self._fallback_beats()

        return filtered

    # -----------------------------
    # FALLBACK BEATS (NO AUDIO SAFE MODE)
    # -----------------------------
    def _fallback_beats(self):

        print("🎬 Using fallback cinematic timing")

        duration = 2.0
        count = 20

        beats = [i * duration for i in range(count)]

        self.beats = beats

        return beats

    # -----------------------------
    # FRAME DURATION (OPTIONAL LEGACY SUPPORT)
    # -----------------------------
    def generate_durations(self, frames):

        if not frames:
            return []

        durations = []

        for i in range(len(frames)):

            if i % 5 == 0:
                durations.append(3.5)
            elif i % 3 == 0:
                durations.append(2.0)
            else:
                durations.append(2.5)

        return durations
    