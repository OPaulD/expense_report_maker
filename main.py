from typing import Annotated
import typer

app = typer.Typer()


@app.command()
def main():
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


if __name__ == "__main__":
    main()
