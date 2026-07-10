"""Shared pytest configuration.

CI runs hypothesis derandomized so results are reproducible and a failure
always points at the commit that caused it; local runs keep the default
random exploration, where discovery belongs.
"""

import os

from hypothesis import settings

settings.register_profile("ci", derandomize=True)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))
