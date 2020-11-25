from setuptools import setup, find_namespace_packages

setup(
    name="wc3games-subscriber",
    version="1.0.0",
    install_requires=[
        "boltons",
        "dataclass-factory",
        "discord.py",
        "requests",
        "simple-parsing",
        "SQLAlchemy",
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages("src"),
    scripts=["scripts/start_bot.py"],
)
