import sys
import os
import argparse
import logging

logger = logging.getLogger(__name__)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import brickproof.cli as cli


def main():
    logging.basicConfig(filename="myapp.log", level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Brickproof CLI – Test Databricks Notebooks with Confidence"
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    # --- init command ---
    subparsers.add_parser("init", help="Initializes a new brickproof.toml config")

    # --- configure command ---
    subparsers.add_parser("configure", help="Configures your Databricks environment")

    # --- edit command ---
    edit_parser = subparsers.add_parser("edit-config", help="Edit toml config file.")
    edit_parser.add_argument(
        "-v",
        "--vars",
        nargs="+",
        help="One or more config variables in the form key=value",
    )

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
        version = cli.version()
        print(version)

    elif args.command == "init":
        cli.init("./brickproof.toml")

    elif args.command == "configure":
        cli.configure()

    elif args.command == "run":
        exit = cli.run(profile=args.profile, file_path="./.bprc", verbose=args.verbose)
        if exit == 0:
            return 0
        else:
            raise Exception

    elif args.command == "edit-config":
        print(args.vars)
        cli.edit(args.vars)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
