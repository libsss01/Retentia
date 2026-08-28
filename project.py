import sys
from engine import User, Deck, Manager
import Retentia.logic as l
import Retentia.tools as t
import time
from pyfiglet import Figlet
from rich.console import Console


console = Console()
f = Figlet(font='slant')

def main():
    print(f.renderText('Welcome to Retentia'))
    time.sleep(0.5)
    console.print("The place where you can study without too much effort.", style="bold")
    time.sleep(0.5)
    username, password = t.ask_user_infos()

    # Object creation
    user = User(username, password)
    deck = Deck(user)
    manager = Manager(user, deck)

    """
        Menu loop that lauch the different feature of the application
    """
    
    while True:
        try:
            print("\n")
            print("*" * t.fixed_length)
            console.print("*" + "Menu".center(58) + "*", style="bold")
            print("*" * t.fixed_length)
            print("\n")
            console.print(
                  "1. Add concepts\n"
                  "2. Review Concepts\n"
                  "3. Statistics Summary\n"
                  "4. Concept research\n"
                  "5. Actions on concepts\n"
                  "6. Exit", soft_wrap=True)

            time.sleep(0.3)
            choice: int = int(input(f"What's your choice {username} ? \n"))


            if choice in [1, 2, 3, 4, 5, 6]:
                pass
        except (ValueError, TypeError):
            console.print("Wrong Input !", style=" bold red")
            continue

        match(choice):
            case 1:
                result = l.engine_init(user, deck, manager)
                if result:
                    print(result)
            case 2:
                result = l.review_time(user, deck, manager)
                if result:
                    print(result)
            case 3:
                result = l.display_statistics(user, deck)
                print(result)

            case 4:
                result = l.search_cards(user, deck)
                print(result)
            case 5:
                result = l.make_actions(user, deck)
                print(result)
            case 6:
                sys.exit(f"See you next time {username}👋 !")


if __name__ == "__main__":
    main()
