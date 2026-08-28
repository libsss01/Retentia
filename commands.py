import typer
from Retentia.typer__app import typer_app
import Retentia.logic as l

        
"""
    file where live the command-line command, 
    allow to use all the features of the project without passing throught the menu loop
"""
@typer_app.command()
def build(ctx: typer.Context):
    """
        function that define the build command. Whose purpose is to call 
        the engine_init function that groups method to create, add cartes and at the end review them for initialization
    """
    ressources = ctx.obj
    result = l.engine_init(ressources.user_obj, ressources.deck_obj, ressources.manager_obj)
    if result:
        print(result)

@typer_app.command()
def review(ctx: typer.Context):
    """
        function that define the review command. Whose purpose is to call 
        the review_time function that wrap the method to review cards when they are due 
        and the user have already cards created throught `engine_init` function
    """
    ressources = ctx.obj
    result = l.review_time(ressources.user_obj, ressources.deck_obj, ressources.manager_obj)
    if not result:
        print("No reviews dues or unknown user")
    else:
        print(result)
    
@typer_app.command()
def show_statistics(ctx: typer.Context):
    """
        function that define the show-statistics command. Whose purpose is to call 
        the display_statistics function that wrap 
        a bunch of statistical methods that are displayed
        only if the user creates cards using the `engine_init` function
    """
    ressources = ctx.obj
    result = l.display_statistics(ressources.user_obj, ressources.deck_obj )
    print(result)

@typer_app.command()
def search(ctx: typer.Context):
    """
        function that define the search command. Whose purpose is to call 
        the search_cards function that wrap the method for searching cards by printing the concept/Question and
        answer only if the user have cards created throught the `engine_init` function
    """
    ressources = ctx.obj
    result = l.search_cards(ressources.user_obj, ressources.deck_obj)
    print(result)
    
@typer_app.command()
def make_actions(ctx: typer.Context):
    """
        function that define the make-actions command. Whose purpose is to call 
        the make_actions function that wrap the method for making actions on deck
        by deleting or updating cards of the deck only if the user have cards 
        created throught the `engine_init` function
    """
    ressources = ctx.obj
    result = l.make_actions(ressources.user_obj, ressources.deck_obj)
    print(result)
    
