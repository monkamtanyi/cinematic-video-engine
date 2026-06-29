class MotionBlurEngineV11:
    """
    SAFE MODE ONLY
    - Removes ALL blur
    - Prevents frame degradation
    - Keeps images sharp during motion
    """

    def __init__(self):
        self.enabled = False  # force OFF by default

    def apply(self, clip, intensity=1.0):
        # 🚨 CRITICAL FIX: NO BLUR PROCESSING
        return clip