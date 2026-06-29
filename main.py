from engine.cli_runner import run_engine


def main():
    try:
        run_engine("config.yaml")
    except Exception as e:
        print(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    main()