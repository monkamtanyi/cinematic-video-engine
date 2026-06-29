from setuptools import setup

setup(
    name="cinematic",
    version="1.0",
    packages=["engine"],
    entry_points={
        "console_scripts": [
            "cinematic=engine.cli:main"
        ]
    }
)