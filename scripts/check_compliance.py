from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    ".env.example",
]


def main():
    missing = [path for path in REQUIRED_FILES if not Path(path).is_file()]
    if missing:
        raise SystemExit("Missing compliance files: " + ", ".join(missing))

    gitignore = Path(".gitignore").read_text(encoding="utf-8")
    if ".env" not in {line.strip() for line in gitignore.splitlines()}:
        raise SystemExit(".env must be listed in .gitignore")

    env_example = Path(".env.example").read_text(encoding="utf-8")
    if "your_google_ai_studio_key" not in env_example:
        raise SystemExit(".env.example must use placeholder values, not real secrets")


if __name__ == "__main__":
    main()
