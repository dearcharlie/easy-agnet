"""Configuration management for Easy-Agent."""

import os
from pathlib import Path

import yaml

DEFAULT_CONFIG = {
    "novel": {
        "projects_dir": str(Path.home() / "easy-agent-projects"),
        "default_language": "zh",
        "max_concurrency": 3,
        "chapter_word_count": 2500,
    }
}

HERMES_CONFIG_DIR = Path.home() / ".hermes"
HERMES_CONFIG_PATH = HERMES_CONFIG_DIR / "config.yaml"
HERMES_SKILLS_DIR = HERMES_CONFIG_DIR / "skills" / "novel"
PROJECTS_DIR_ENV = "EASY_AGENT_PROJECTS_DIR"


def get_config_path() -> Path:
    return HERMES_CONFIG_PATH


def load_config() -> dict:
    path = get_config_path()
    if path.exists():
        with open(path) as f:
            return {**DEFAULT_CONFIG, **(yaml.safe_load(f) or {})}
    return dict(DEFAULT_CONFIG)


def save_config(config: dict):
    path = get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)


def get_projects_dir() -> Path:
    env_dir = os.environ.get(PROJECTS_DIR_ENV)
    if env_dir:
        return Path(env_dir)
    config = load_config()
    return Path(config.get("novel", {}).get("projects_dir", DEFAULT_CONFIG["novel"]["projects_dir"]))
