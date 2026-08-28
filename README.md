# Retentia - A CLI spaced-repetition tool

## Retentia is a project which allows to study without too much effort directly inside your terminal.

This project is a CLI tool inspired on Anki created to make easier the study for **nerds** like me or just person who want study without forgetting what you just learned in the next few minutes. 
 
It uses a lot of concept and principles like OOP, modularity...

### Principales Features  
- Create Cards for you study concept  
- Interactive menu for the user options 
- CLI Commands to use the tool without going through the menu  

- Review Cards for initialization after their creation and when there are dues  
- Statistics based on your deck and reviews  
- Delete and update question and/or answer of a card
  
### How this project help you to rembember better the information ?
> My project use the spaced repetition system inspired on the Ebbinghaus forgetting curve.  
> To know more about these you can consult theses links below :  
* https://en.wikipedia.org/wiki/Forgetting_curve
* https://en.wikipedia.org/wiki/Spaced_repetition  

But now, what will make your learning stick ?  
To explain simply, you don't learn once and that's it, now your learning is based on how you retain the information.  
Information is now learned at different and consecutive intervall before you forget it.
## Instructions 


### Run the project
Throught the menu loop (with no command line) :  

`python routing.py`

With commands line argument:

`python routing.py [command line arg]`

### Project Structure
The project is consist of 12 files each one with a specific purpose :  
#### **'requirements.txt' :**  
Text file with all packages you need to install to use this project
#### **'setup.py':**
His purpose is to create the 2 json storage files. If there already created anything happen.  
#### **'app.py' :**  
 <mark style="background-color: white"><b>main file of the project</b></mark >  
 Present the Menu with the differents options or project features to the user (create card, review cards, statistics and make actions to cards) and depends on the user choice call the function that hold the logic. Also a entry point of the project if you want to lauch the menu directly.  
#### **'logic.py' :**  
Consist of 5 functions with type hint that holds the project feature :  
- engine_init : with 3 parameters of the types object "User", "Deck", "Manager" and a str or None type hint as return type.
The principal purpose of this function is call the method for card creation(on user object) and storage (on manager object) and manage the logic of the different behaviors.
-  review_time : with 3 parameters of the types object "User", "Deck", "Manager" and a str or None type hint as return type.  
Call the review method (on the deck object) to make reviews when wards are due and store it with the method appropriate (on the manager object) and manage the logic of the different behaviors.
- display_statistics : with 2 parameters of the types object "User"and "Deck" and also a str or None type hint as return type.
Shows a wide range of state by calling some  statistical methods (on the deck object).
- search_cards : with 2 parameters of the types object "User" and "Deck" and also a str type hint as return type.  
Manage the logic under the call of the search method (on the deck object) and display the concept and his answers based on if the concept exists or not.  
- make_actions: with 2 parameters of the types object "User" and "Deck" and also a str type hint as return type.  
Manage the logic under the call of the perform_actions_on_deck method (on the deck object) method that based on the concept provide update (question or/and answer) or delete card.  
#### **'engine.py':**
File where live our 3 principales Class:  
- ***Deck*** :  Take an user object as argument.
    - Properties : 
        - **User object**
        - **Scheduler object**
    - Methods :
        - cards_due : retreive due cards.
        - retreive_cards : that's expect a list of card_id as argument. It's for retreiving cards and log for review when the review was created in another instance.
        - review_init : method for reviewing cards with a rating based immediatly after their creation.
        - review_cards : review method that allow usr to review cards when they are due.
        - search : method that takes a concept as argument which will be the subject of the search in the deck.
        - perform_actions_on_deck : method that expect a concept and a choice provided by the user. The choice define what operation the user want to do (deletion or updating) and this operation will affect the concept given.
        - number_of_reviews : method that return the number of review of the dedicated user
        - reviews_per_day : method that return the number of review per by done by the user.
        -reviews_per_week : method that return the number of review per by week by the user.
        - streak : method that set and update the streak of the user.
        - number_of_cards : method that return the number of cards of an user
        - number_of_cards_by_rating : method that return the number of cards by rating of an user
        - number_of_cards_by_state : method that return the number of cards by state of an user
        - number_of_cards_by_due_today: method that return the number of cards due today.
        - number_of_cards_upcoming : method that return the number of cards upcoming
        - number_of_overdue_cards : method that return the number of cards overdue.
- ***User*** :
    - Properties : 
        - **id** (int) : user id 
        - **username** (str)
        - **lists_of_concepts** (list) : list of concept that store cards created between instances
        - **user_dict** (dict) : dictionnaty with user and review informations
        - **password** (str) : user password
        - **id_cards** (int) : id for cards
    - Methods :
        - getter for "private property" (user, password, lists_of_concepts)
        - create_user_dict: method that set the user dict.
        - add_cards : method that add cards to the deck when the user already have card.
        - create_concept:
        method that create concept with question/answer for fresh user.

- **Manage** :  Class responsible of the storage of the data, take a user object as argument, a user_dict and a deck object.
    - Properties : 
        - **User object**
        - **user dict**
        - **deck object**
    - Methods :
        - store_user_info
        - store_user_info

#### **'tools.py' :**
File that define the helper function of the project for different purposes like :

- Interactions with storage file
- Retreive statistical informations
- Password Checking etc...
    
#### **'routing.py':**  
In purpose to give the user the possibilty to use the tool throught
the menu or the directly in the terminal by Command lines arguments.  
We create this file that receive the user input if he provide a command line arg we lauch the feature based on that command but if not we lauch the menu loop (app.py).  
#### **'commands.py'** :  
File where the commands for the command-line are defined and attached to the functions that run the logic.  
We have in this file and btw the project 5 commands :  
1. 'build' command to create cards (there are reviewed immediatly after creation)  

2. 'review' command to review cards that are actually dues.  

3. 'show-statistics' to display the user statistics based on his deck and reviews.  
4. 'search' command to search for a specific card inside your deck  

5. 'make-actions' to make action (delete or update concept or/and answer) on a specific card 
#### **'typer_app.py'**:  
Create the single and shared typer object once for the purpose of sharing the same context and object throughout the project, prevent the creation of several object and different context.
#### **'test_project.py'** :  
Consist of 14 functions that test the whole project with different purposes like (storage, side effects, behaviors...)






