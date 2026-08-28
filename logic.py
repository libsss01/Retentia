from Retentia.engine import User, Deck, Manager
import Retentia.tools as t
import time
import Retentia.project as project 


def engine_init(user: User, deck: Deck, manager:Manager) -> str | None:
    time.sleep(0.5)
    print("\n")
    print("*" * t.fixed_length)
    print("*" + "Create/Add Cards".center(58) + "*")
    print("*" * t.fixed_length)
    print("\n")
    project.console.print("Let's Add some Concepts/Cards for your Deck !", style="bold")
    time.sleep(0.2)
    print("\n")
    while True:
        project.console.print("Notice that cards will be automatically reviewed after creation to innitialized them", style="bold red")
        try:
            input("Press Enter to continue !\n")

            # check if user already exist if no the user can only btw create concept and after our manager object
            # store data to the json file. If the user already exist he can only add cards to his deck
            if not t.check_user_exist(user.username, user.password):
                user.create_concept()
                manager.store_user_info()

            else:
                user.add_cards()

            # After the creation cards are immediately reviewed for initialization
            result, review_data, log_data = deck.review_init()
            if not review_data:
                return 
            manager.store_review_info(review_data, log_data)
            return result
        except ValueError:
            project.console.print("Something goes wrong", style="bold red")


def review_time(user: User, deck: Deck, manager:Manager) -> str | None:
    time.sleep(0.5)
    print("\n")
    print("*" * t.fixed_length)
    print("*" + "Review Cards".center(58) + "*")
    print("*" * t.fixed_length)
    print("\n")
    # user existence checking, an user that doesn't exist can't review cards since he has no cards created 
    if not t.check_user_exist(user.username, user.password):
        return "\033[31mYou can't access to this feature until you've create cards.\033[0m"

    # if the user has cards and his deck is not empty we are checking if there are cards due or overdue for review
    # if they have the user review cards and if there no cards for review we are printing the next review time and returning "You don't have cards due yet !"
    if not t.is_deck_empty(user.username, user.password):
        project.console.print("Let's Train your memory :)", style="bold")
        print("\n")
        if t.get_number_of_cards_due_today(user.username, user.password) != 0 or t.get_number_of_cards_overdue(user.username, user.password) != 0:
            result, review_data, log_data, time_next_review_session = deck.review_cards()
            if not review_data:
                if time_next_review_session:
                    project.console.print(f"Next Review session in {time_next_review_session} !!", style="yellow")
                return "\033[34mYou don't have cards due yet !\033[0m"
            manager.store_review_info(review_data, log_data)        
            return result
        time_next_review_session = t.get_next_time_card_is_due(user.username, user.password)
        project.console.print(f"Next Review session in {time_next_review_session} !!", style="yellow")
        return "\033[34mYou don't have cards due yet !\033[0m"
        
    return "\033[34mYour deck is empty !\033[0m"


def display_statistics(user:User, deck:Deck) -> str:
    time.sleep(0.5)
    print("\n")
    print("*" * t.fixed_length)
    print("*" + "Statistics".center(58) + "*")
    print("*" * t.fixed_length)
    print("\n")
    # user existence checking, an user that doesn't exist can't display statistics or even have it since he has no cards created yet
    if not t.check_user_exist(user.username, user.password):
        return "\033[31mYou can't access to this feature until you're registered\033[0m"

    # if the user hasn't a empty deck and have done at leat one review since many of the statistics are based on reviews
    # we're calling the statistical methods and after that print them nicely with a return message at the end of function execution
    
    if not t.is_deck_empty(user.username, user.password) and t.has_review(user.username, user.password):
        number_of_cards = deck.number_of_cards()
        number_of_cards_due = deck.number_of_cards_due_today()
        number_of_cards_overdue = deck.number_of_overdue_cards()
        number_of_cards_upcoming = deck.number_of_cards_upcoming()
        number_of_cards_learning, number_of_cards_reviewed, number_of_cards_relearned = deck.number_of_card_by_state()
        number_of_cards_rated_again, number_of_cards_rated_difficult, number_of_cards_rated_good, number_of_cards_rated_easy = deck.number_of_card_by_rating()
        number_of_reviews = deck.number_of_reviews()
        number_of_reviews_per_day = deck.reviews_per_day()
        number_of_reviews_per_week = deck.reviews_per_week()

        print("+" * t.fixed_length)
        print("Reviews Stats".center(60))
        print("+" * t.fixed_length)
        project.console.print(f"Number Of Reviews: {number_of_reviews}", soft_wrap=True)
        project.console.print(f"Number Of Reviews this Day: {number_of_reviews_per_day}", soft_wrap=True)
        project.console.print(f"Number Of Reviews this Week: {number_of_reviews_per_week}", soft_wrap=True)
        project.console.print(f"Number Of Cards : {number_of_cards}", soft_wrap=True)
        project.console.print(f"Number Of Cards Due : {number_of_cards_due}", soft_wrap=True)
        project.console.print(f"Number Of Cards Overdue: {number_of_cards_overdue}", soft_wrap=True)
        project.console.print(f"Number Of Cards Upcoming : {number_of_cards_upcoming}", soft_wrap=True)
        print("=====================================================")
        print("\n")
        print("+" * t.fixed_length)
        print("Number Of Cards By State".center(60))
        print("+" * t.fixed_length)
        project.console.print(f"Number Of Cards w Learning State : {number_of_cards_learning} cards", soft_wrap=True)
        project.console.print(f"Number Of Cards w Review State : {number_of_cards_reviewed} cards", soft_wrap=True)
        project.console.print(f"Number Of Cards w Relearning State : {number_of_cards_relearned} cards", soft_wrap=True)
        print("=====================================================")
        print("\n")
        
        print("+" * t.fixed_length)
        print("Number Of Cards By Rating".center(60))
        print("+" * t.fixed_length)
        project.console.print(f"Number Of Cards Rated Again : {number_of_cards_rated_again} cards", soft_wrap=True)
        project.console.print(f"Number Of Cards Rated Difficult : {number_of_cards_rated_difficult} cards", soft_wrap=True)
        project.console.print(f"Number Of Cards Rated Good: {number_of_cards_rated_good} cards", soft_wrap=True)
        project.console.print(f"Number Of Cards Rated Easy: {number_of_cards_rated_easy} cards", soft_wrap=True)

        return "\033[32mGood Job Keep Going !!\033[0m"

    return "\033[34mYour deck is empty !\033[0m"


def search_cards(user: User, deck:Deck) -> str | None:
    time.sleep(0.5)
    concept = ""
    response = ""
    quitt = False
    
    print("\n")
    print("*" * t.fixed_length)
    print("*" + "Search Cards".center(58) + "*")
    print("*" * t.fixed_length)
    print("\n")
    # user existence checking, an user that doesn't exist can't search cards that don't exist anymore
    if not t.check_user_exist(user.username, user.password):
        return "\033[31mYou can't access to this feature until you're registered\033[0m"
    # since the user has a deck with cards we are asking for the concept he search for it with empty verification
    # and after that we're calling the method charged of searching cards on deck based on the return type 
    # str -> for error message and tuple for concept retreived, we print message in the str case and print out the concept and answer otherwise
    
    if not t.is_deck_empty(user.username, user.password):
        while True:
            project.console.print("Be sure that the concept/card exists in your deck", style="bold red")
            time.sleep(0.2)
            while not concept:
                concept = input("Which concept/card do you want to search for ?\n")
                if not concept:
                    project.console.print("It seems like you don't provide a concept", style="bold red")
            input("Press Enter to continue\n")

            if type(deck.search(concept)) == str:
                message = deck.search(concept)
                print(message)
            else:
                concept_retreived, answer = deck.search(concept)
                if not type(concept_retreived) == int:
                    project.console.print(f"Concept : {concept_retreived.title()}", style="bold")
                else:
                    project.console.print(f"Concept : {concept_retreived}", style="bold")
                input("Press Enter to Continue\n")
                if not type(answer) == int:
                    project.console.print(f"Answer : {answer.title()}", style="bold")
                else:
                    project.console.print(f"Answer : {answer}", style="bold")
            while not response or response not in ["y", "n"]:
                response = input("Do you want to quit ? y/n\n").lower()
                print("\n")
                if response == "y":
                    quitt = True

            if not quitt:
                concept = ""
                response = ""
                continue
            return "\033[32mYour cards are alive !\033[0m"
    else:
        return "\033[34mYour deck is empty !\033[0m"


def make_actions(user: User, deck:Deck) -> str | None:
    time.sleep(0.5)
    concept = ""
    response = ''
    quitt = False
    
    print("\n")
    print("*" * t.fixed_length)
    print("*" + "Make action on Cards".center(58) + "*")
    print("*" * t.fixed_length)
    print("\n")
     # user existence checking, an user that doesn't exist can't search cards that don't exist anymore
    if not t.check_user_exist(user.username, user.password):
       return "\033[31mYou can't access to this feature until you're registered\033[0m"
    # since the user has a deck with card(s) he can delete or update card based on the concept he provide
    if not t.is_deck_empty(user.username, user.password):
        while True:
            project.console.print("Be sure that the concept/card exists in your deck", style="bold red")
            input("Press Enter to continue\n")
            while not concept:
                concept = input("Which concept/card do you want to take an action on?\n")
                if not concept:
                    print("It seems like you don't provide a concept")
                else:
                    input("Press Enter to continue\n")
                    project.console.print(
                          "1. Delete a concept/card\n"
                          "2. Update a concept/card", soft_wrap=True)
                    time.sleep(0.2)

                    choice = input("What's your choice ?\n")
                    input("Press Enter to continue !\n")

                    if not int(choice) in (1, 2) or not choice:
                        project.console.print("Your input do not match with choices", style="bold red")
                        continue
                    else:
                        choice = int(choice)
                        message = deck.perform_actions_on_deck(concept, choice)
                        print(message)

                    while not response or response not in ["y", "n"]:
                        response = input("Do you want to quit ? y/n\n").lower()
                        if response == "y":
                            quitt = True

            if not quitt:
                concept = ""
                response = ""
                continue
            return "\033[32mYour actions take effects !\033[0m"
    else:
        return "\033[34mYour deck is empty !\033[0m"

