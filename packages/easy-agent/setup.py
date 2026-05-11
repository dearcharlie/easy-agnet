from setuptools import setup

setup(
    name="easy-agent",
    version="0.1.0",
    packages=["easy_agent"],
    package_dir={"easy_agent": "easy_agent"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "easy-agent=easy_agent.cli:main",
        ],
    },
    install_requires=[
        "pyyaml>=6.0",
    ],
    python_requires=">=3.10",
)
