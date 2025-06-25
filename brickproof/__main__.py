import sys
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import brickproof.cli as cli


def main():
    args = sys.argv

    if len(args) == 1:
        # list possible commands here....
        print("Welcome to Brickproof")
        print("Commands to run:")
        print(
            "\t- init: initializes brickproof project by writing new brickproof toml file"
        )
        print("\t- configure: configures databricks environment interactively.")
        print("\t- run: runs brickproof testing job")
        print("\t- version: prints current brickproof version")

        return 0

    # version commmand
    if args[1] == "version" or args[1] == "Version":
        cli.version()
        return 0

    # init command
    if args[1] == "init" or args[1] == "Init":
        cli.init("./brickproof.toml")
        return 0

    # TODO run command
    if args[1] == "run" or args[1] == "Run":
        profile = "default"
        if len(args) == 3:
            if args[2] == "--p" or args[2] == "--profile":
                profile = str(args[3])

        cli.run(profile=profile, file_path="./.bprc")
        return 0

    # configure command
    if args[1] == "configure" or args[1] == "Configure":
        cli.configure()
        return 0

    return 0


if __name__ == "__main__":

    main()