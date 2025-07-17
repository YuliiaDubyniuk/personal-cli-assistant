from src.utilities import rich_console


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            error_msg = str(e).replace('"', '')
            rich_console.print(f"[bold red]{str(error_msg)}[/bold red]")
        except IndexError:
            rich_console.print(
                "[bold red]Missing required arguments. Please provide all the arguments.[/bold red]")
        except KeyError:
            rich_console.print(
                "[bold red]Record with given name doesn't exist.[/bold red]")
        except Exception as e:
            rich_console.print(f"[bold red]Unknown error: {e}[/bold red]")
    return inner
