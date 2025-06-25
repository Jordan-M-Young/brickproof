import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import brickproof.cli as cli


def main():
    parser = argparse.ArgumentParser(
        description="Brickproof CLI – Test Databricks Notebooks with Confidence"
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    # --- init command ---
    subparsers.add_parser("init", help="Initializes a new brickproof.toml config")

    # --- configure command ---
    subparsers.add_parser("configure", help="Configures your Databricks environment")

    # --- run command ---
    run_parser = subparsers.add_parser("run", help="Runs brickproof testing job")
    run_parser.add_argument("--profile", "-p", default="default", help="Profile name")
    run_parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging"
    )

    # --- version command ---
    subparsers.add_parser("version", help="Prints the current brickproof version")

    # If no args: print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args()

    # --- Dispatch based on subcommand ---
    if args.command == "version":
        cli.version()

    elif args.command == "init":
        cli.init("./brickproof.toml")

    elif args.command == "configure":
        cli.configure()

    elif args.command == "run":
        cli.run(profile=args.profile, file_path="./.bprc")

    else:
        parser.print_help()



if __name__ == "__main__":
    main()

