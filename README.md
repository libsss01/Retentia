# Retentia - A CLI spaced-repetition tool

## Retentia is a project that allows you to study without too much effort directly inside your terminal.

This project is a CLI tool inspired by Anki, created to make studying easier for **nerds** like me, or simply for people who want to study without forgetting what they just learned a few minutes later.
 
It uses a lot of concepts and principles such as OOP, modularity...

### Principal Features  
- Create cards for the concepts you want to study  
- Interactive menu for the user options  
- CLI commands to use the tool without going through the menu  
- Review cards for initialization after their creation and when they are due  
- Statistics based on your deck and reviews  
- Delete and update the question and/or answer of a card
  
### How does this project help you remember information better?
> My project uses a spaced repetition system inspired by the Ebbinghaus forgetting curve.  
> To learn more about this, you can consult the links below:  
* https://en.wikipedia.org/wiki/Forgetting_curve
* https://en.wikipedia.org/wiki/Spaced_repetition  

But now, what will make your learning stick?  
To explain it simply, you don't learn something once and that's it. Your learning is now based on how well you retain the information.  
Information is now reviewed at different and consecutive intervals before you forget it.

## Instructions 

### Run the project
Through the menu loop (with no command-line argument):  

`python routing.py`

With a command-line argument:

`python routing.py [command line arg]`

### Project Structure
The project consists of several files, each one with a specific purpose:  

#### **'requirements.txt':**  
Text file with all the packages you need to install to use this project.

#### **'setup.py':**
Its purpose is to create the 2 JSON storage files. If they are already created, nothing happens.  

#### **'project.py':**  
<mark style="background-color: white"><b>Main file of the project</b></mark>  
Presents the menu with the different options or project features to the user (create cards, review cards, statistics, and actions on cards), and depending on the user's choice, calls the function that holds the logic. It is also an entry point of the project if you want to launch the menu directly.  

#### **'logic.py':**  
Consists of 5 functions with type hints that hold the project features:  

- `engine_init`: with 3 parameters of the object types `User`, `Deck`, `Manager`, and a `str` or `None` return type hint.  
The principal purpose of this function is to call the method for card creation (on the user object) and storage (on the manager object), and manage the logic of the different behaviors.

- `review_time`: with 3 parameters of the object types `User`, `Deck`, `Manager`, and a `str` or `None` return type hint.  
Calls the review method (on the deck object) to make reviews when cards are due, stores them with the appropriate method (on the manager object), and manages the logic of the different behaviors.

- `display_statistics`: with 2 parameters of the object types `User` and `Deck`, and also a `str` or `None` return type hint.  
Shows a wide range of statistics by calling some statistical methods (on the deck object).

- `search_cards`: with 2 parameters of the object types `User` and `Deck`, and also a `str` return type hint.  
Manages the logic behind the call to the search method (on the deck object) and displays the concept and its answer depending on whether the concept exists or not.

- `make_actions`: with 2 parameters of the object types `User` and `Deck`, and also a `str` return type hint.  
Manages the logic behind the call to the `perform_actions_on_deck` method (on the deck object), which, based on the concept, provides update (question and/or answer) or delete operations.

#### **'engine.py':**
File where our 3 principal classes live:  

- ***Deck***: takes a user object as an argument.
    - Properties:  
        - **User object**  
        - **Scheduler object**  
    - Methods:  
        - `cards_due`: retrieves due cards.  
        - `retreive_cards`: expects a list of `card_id` values as an argument. It retrieves cards and logs for review when the review was created in another instance.  
        - `review_init`: method for reviewing cards with a rating immediately after their creation.  
        - `review_cards`: review method that allows the user to review cards when they are due.  
        - `search`: method that takes a concept as an argument, which will be the subject of the search in the deck.  
        - `perform_actions_on_deck`: method that expects a concept and a choice provided by the user. The choice defines what operation the user wants to do (deletion or updating), and this operation affects the given concept.  
        - `number_of_reviews`: method that returns the number of reviews of the dedicated user.  
        - `reviews_per_day`: method that returns the number of reviews per day done by the user.  
        - `reviews_per_week`: method that returns the number of reviews per week done by the user.  
        - `streak`: method that sets and updates the streak of the user.  
        - `number_of_cards`: method that returns the number of cards of a user.  
        - `number_of_cards_by_rating`: method that returns the number of cards by rating of a user.  
        - `number_of_cards_by_state`: method that returns the number of cards by state of a user.  
        - `number_of_cards_by_due_today`: method that returns the number of cards due today.  
        - `number_of_cards_upcoming`: method that returns the number of cards upcoming.  
        - `number_of_overdue_cards`: method that returns the number of overdue cards.

- ***User***:  
    - Properties:  
        - **id** (`int`): user id  
        - **username** (`str`)  
        - **lists_of_concepts** (`list`): list of concepts that stores cards created between instances  
        - **user_dict** (`dict`): dictionary with user and review information  
        - **password** (`str`): user password  
        - **id_cards** (`int`): id for cards  
    - Methods:  
        - getters for "private properties" (`user`, `password`, `lists_of_concepts`)  
        - `create_user_dict`: method that sets the user dict.  
        - `add_cards`: method that adds cards to the deck when the user already has cards.  
        - `create_concept`: method that creates a concept with a question/answer for a new user.

- **Manager**: class responsible for storing data, taking a user object, a user dict, and a deck object.  
    - Properties:  
        - **User object**  
        - **user dict**  
        - **deck object**  
    - Methods:  
        - `store_user_info`  
        - `store_review_info`

#### **'tools.py':**
File that defines the helper functions of the project for different purposes, such as:  

- Interactions with storage files  
- Retrieving statistical information  
- Password checking, etc.  
    
#### **'routing.py':**  
Its purpose is to give the user the possibility to use the tool through the menu or directly in the terminal using command-line arguments.  
We created this file to receive the user's input: if a command-line argument is provided, we launch the feature based on that command; otherwise, we launch the menu loop (`project.py`).  

#### **'commands.py':**  
File where the command-line commands are defined and attached to the functions that run the logic.  
We have 5 commands in this file and throughout the project:  

1. `build` command to create cards (they are reviewed immediately after creation)  
2. `review` command to review cards that are currently due  
3. `show-statistics` to display the user statistics based on their deck and reviews  
4. `search` command to search for a specific card inside your deck  
5. `make-actions` to make an action (delete or update concept and/or answer) on a specific card  

#### **'typer__app.py':**  
Creates the single and shared Typer object for the purpose of sharing the same context and object throughout the project, preventing the creation of several objects and different contexts.

#### **'tests_project.py':**  
Consists of 14 functions that test the whole project for different purposes such as storage, side effects, behaviors, etc.
