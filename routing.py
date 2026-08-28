import typer
from Retentia.typer__app import typer_app
import Retentia.commands as commands
import Retentia.project as project
import Retentia.tools as t
import Retentia.engine as eng
from dataclasses import dataclass
import Retentia.setup as setup


@dataclass
class objectInventory:
    """
        dataclass to store shared object between fallback and command line commands 
    """
    user_obj: object
    deck_obj : object
    manager_obj : object

  
@typer_app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
        Callback for "routing" our project based on the input of the user if he deliver a command
        with 'python routing.py' eg: 'python routing.py build' the build command is executing in background or called
        because we have imported the file where the commands lives and instead of the user run the file without commands
        we're launching the menu loop.
    """
    if ctx.invoked_subcommand is None:
        project.main() 
    else:
        username, password = t.ask_user_infos()
        user = eng.User(username, password)
        deck = eng.Deck(user)
        manager = eng.Manager(user, deck)
            
        object_inventory = objectInventory(user, deck, manager)
            
        ctx.obj = object_inventory

if __name__ == "__main__":
    setup.file_setup()
    typer_app()