"""
A simple SQLite shell.
"""

import os
import subprocess
import sys

from cli.commandline import CLI, MainEnv  # Command line interface.
from clp.commandprocessor import CLP, CommandDef  # Command line processor.
from sqli.sqli import SQLI  # SQLite interface.

NAME = "SQLiteShell"
VERSION = "v.1.0.0"
DATE = "2024"


class SQLITESHELL:
    """
    SQLITESHELL

    The SQLite3 Shell class.
    """

    def __init__(self) -> None:
        """__init__

        Initialises the SQLiteSHell.

        """
        #  Initialise the SQLite interface.

        self.sqli: SQLI = SQLI()

        #  Initialise the command line processor,
        #  and add commands to the list of recognised commands.

        self.clp: CLP = CLP()

        self.clp.add(
            CommandDef("close", "Closes the current database.", self.close, [], False)
        )

        self.clp.add(
            CommandDef(
                "create",
                "Create and opens a database.",
                self.create,
                [("database", "The name of the database to create.")],
                False,
            )
        )

        self.clp.add(
            CommandDef(
                "describe",
                "Describes a table, view, index or trigger.",
                self.sqli.describe,
                [("name", "The name of the item to describe.")],
                False,
            )
        )

        self.clp.add(
            CommandDef(
                "edit",
                "Edit a file / script.",
                self.edit,
                [("filename", "The name of the file / script to edit.")],
                False,
            )
        )

        self.clp.add(CommandDef("exit", "Exits the program.", self.exit, [], False))

        self.clp.add(
            CommandDef(
                "help",
                "Shows this list of recognisable commands.",
                self.help,
                [],
                False,
            )
        )

        self.clp.add(
            CommandDef(
                "indices",
                "Prints a list of indices in the database.",
                self.sqli.indices,
                [],
                False,
            )
        )

        self.clp.add(
            CommandDef(
                "open",
                "Opens a database.",
                self.open,
                [("database", "The name of the database to open.")],
                False,
            )
        )

        self.clp.add(
            CommandDef(
                "schema", "Prints the database schema.", self.sqli.schema, [], False
            )
        )

        self.clp.add(
            CommandDef(
                "script",
                "Runs a query from a script file. (No data returned)",
                self.sqli.script,
                [
                    (
                        "filename",
                        "The name of the file containing the query to execute.",
                    ),
                    ("[...]", "Parameters as required by the script."),
                ],
                True,
            )
        )

        self.clp.add(
            CommandDef(
                "tables",
                "Prints a list of tables in the database.",
                self.sqli.tables,
                [],
                False,
            )
        )

        self.clp.add(
            CommandDef(
                "triggers",
                "Prints a list of triggers in the database.",
                self.sqli.triggers,
                [],
                False,
            )
        )

        self.clp.add(
            CommandDef(
                "views",
                "Prints a list of views in the database.",
                self.sqli.views,
                [],
                False,
            )
        )

        #  Initialise the command line interface.

        self.cli: CLI = CLI(
            self.clp.parse,
            self.sqli.execute,
        )

        #  Configure the command line interface.

        self.cli.set_main_env(
            MainEnv(
                ">",
                f"Welcome to SQLiteShell {VERSION}",
                "Type .help for a list of commands.",
                "Thank you for using SQLiteShell.",
            )
        )

    def start(self) -> None:
        """start

        Starts the command line interface.

        """
        self.cli.start()

    def exit(self, _: dict[str, str]) -> None:
        """exit

        Exits the program.

        Args:
            _ (dict[str, str]): ignored!
        """
        self.cli.stop()

    def help(self, _: dict[str, str]) -> None:
        """help

        Prints a list of recognised commands.

        Args:
            _ (dict[str, str]): ignored!
        """
        self.clp.list()

    def create(self, parms: dict[str, str]) -> None:
        """create

        Creates a new database using the sqli interface, and updates the cli prompt.

        Args:
            parms (dict[str, str]): paramters
                "database" = name of database to create.
        """
        if self.sqli.create(parms["database"]):
            self.cli.set_prompt(f"{parms['database']} >")

    def open(self, parms: dict[str, str]) -> None:
        """open

        OPens a database using the sqli interface, and updates the cli prompt.

        Args:
            parms (dict[str, str]): paramters
                "database" = name of database to open.
        """
        if self.sqli.open(parms["database"]):
            self.cli.set_prompt(f"{parms['database']} >")

    def close(self, _: dict[str, str]) -> None:
        """close

        Closes a database using the sqli interface, and updates the cli prompt.

        Args:
            parms (dict[str, str]): ignored!
        """
        if self.sqli.close():
            self.cli.set_prompt(">")

    def edit(self, parms: dict[str, str]) -> None:
        """
        Opens the default text editor for the specified file.

        Args:
            parms (dict[str, str]): paramters
                "filename" = name of database to open.
        """
        _filename = parms["filename"]

        # Ensure the file exists

        if not os.path.exists(_filename):
            try:
                with open(_filename, "w", encoding="utf-8"):
                    pass
            except OSError as e:
                raise IOError(f"Failed to create file '{_filename}': {e}") from e

        # Try to open with the default system editor
        # This is messy as it has to work cross platform.

        try:
            if sys.platform.startswith("win"):
                # Import inside the Windows branch to avoid Pylance errors
                import os as _os  # pylint: disable=reimported. # pylint: disable=import-outside-toplevel,reimported

                _os.startfile(_filename)  # type: ignore[attr-defined]  # pylint: disable=E1101
            elif sys.platform.startswith("darwin"):
                subprocess.run(["open", _filename], check=False)
            elif sys.platform.startswith("linux"):
                subprocess.run(["xdg-open", _filename], check=False)
            else:
                raise NotImplementedError(f"Unsupported platform: {sys.platform}")
        except Exception as e:
            raise OSError(f"Could not open editor for '{_filename}': {e}") from e


def main() -> None:
    """main

    Creates and starts the sqlite shell.

    """
    sqliteshell: SQLITESHELL = SQLITESHELL()
    sqliteshell.start()


if __name__ == "__main__":
    main()
