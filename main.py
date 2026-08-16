from dataclasses import dataclass
from datetime import date
import typer
from imap_tools import MailBox, AND
from rich.console import Console
from rich.table import Table
# import pandas as pd


app = typer.Typer(help="Gmail invoice scanner")
console = Console()


@dataclass
class Credentials:
    email: str
    password: str


def get_credentials():
    typer.secho(
        "Please authenticate to access your Gmail mailbox.",
        fg=typer.colors.CYAN,
        bold=True,
    )
    typer.echo("Please provide your email address.\n")
    email_adress = typer.prompt("Enter your email address:")
    password = typer.prompt(
        "Enter your password", hide_input=True, confirmation_prompt=True
    )
    return Credentials(email=email_adress, password=password)


class MailboxItem:
    def __init__(self, email: str, password: str, host: str = "imap.gmail.com"):
        self.email = email
        self.password = password
        self.host = host
        self.mailbox = MailBox(self.host)
        self.connect()

    def connect(self):
        typer.secho("Opening portal to mailbox ", fg=typer.colors.MAGENTA, bold=True)
        self.mailbox.login(self.email, self.password)

    def close_connection(self):
        try:
            self.mailbox.logout()
            typer.echo("Connection closed.")
        except Exception as e:
            typer.echo(f"Disconnect failed with error: {e}")


def connect_to_mailbox(mailbox: MailboxItem):
    folder = typer.prompt("Please provide folder/subfolder name:", default="INBOX")
    start_date_str = typer.prompt("Please provide start date in yyyy-mm-dd format")
    end_date_str = typer.prompt("Please provide end date in yyyy-mm-dd format")
    start_date = date.fromisoformat(start_date_str)
    end_date = date.fromisoformat(end_date_str)

    try:
        mailbox.mailbox.folder.set(folder)
        criteria = AND(subject="trip with Uber", date_gte=start_date, date_lt=end_date)
        mail_list = list(mailbox.mailbox.fetch(criteria, limit=6))

        if not mail_list:
            typer.echo(f"No mails in {folder} match the search criteria")
            return

        table = Table(title="Invoices found summary")
        table.add_column("Date", style="green")
        table.add_column("Subject", style="green")
        table.add_column("Ammount", style="magenta")

        for msg in mail_list:
            table.add_row(
                msg.date.strftime("%Y-%m-%d"),
                msg.subject[:41],
                "Placeholder until HTML parser is done",
            )

        console.print(table)
    except Exception as e:
        typer.echo(f"Failed with error: {e}")


@app.command()
def start_app():
    creds = get_credentials()
    mailbox = MailboxItem(email=creds.email, password=creds.password)

    try:
        while True:
            typer.echo("Connecting to mailbox")
            connect_to_mailbox(mailbox)

    finally:
        mailbox.close_connection()


if __name__ == "__main__":
    start_app()
