import argparse
from engine.cli_runner import run_engine


def main():
    parser = argparse.ArgumentParser(description="Cinematic Engine CLI")

    parser.add_argument("--config", required=True, help="Path to YAML config")

    args = parser.parse_args()

    run_engine(config_path=args.config)


if __name__ == "__main__":
    main()