# Retentia — A CLI Spaced-Repetition Tool

Retentia is a command-line spaced-repetition application inspired by Anki. It is designed for people who want to create flashcards, review them directly from the terminal, and keep track of their learning progress without needing a graphical interface.

The project was built as my CS50P final project and helped me practice object-oriented programming, modularity, persistence, testing, CLI design, authentication, and spaced-repetition logic.

## Main Features

- Create flashcards for concepts you want to study
- Review cards immediately after creation to initialize their scheduling
- Review cards again when they become due
- Search for cards in your deck
- Update or delete existing cards
- Display statistics about cards and reviews
- Use an interactive menu or direct CLI commands
- Persist users, cards, reviews, and review logs in JSON storage
- Hash and verify passwords with `bcrypt`
- Schedule reviews with the FSRS algorithm

## How Retentia Helps You Remember

Retentia is based on the principle of **spaced repetition**: instead of reviewing information continuously or only once, you revisit it at increasingly appropriate intervals.

The project uses the `fsrs` package to manage card states and future review dates. The idea is closely related to the Ebbinghaus forgetting curve: reviewing information before it is forgotten helps strengthen long-term retention.

Useful references:

- [Forgetting curve](https://en.wikipedia.org/wiki/Forgetting_curve)
- [Spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition)

## Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/libsss01/Retentia.git
cd Retentia
pip install -r requirements.txt
```

The storage files are created automatically by the setup logic when needed.

## Running the Project

### Interactive menu

```bash
python routing.py
```

### CLI commands

```bash
python routing.py [command]
```

Available commands include:

- `build` — create and initialize cards
- `review` — review cards that are currently due
- `show-statistics` — display statistics about your deck and reviews
- `search` — search for a specific card
- `make-actions` — update or delete a card

## Project Structure

### `project.py`

Contains the interactive menu and acts as the main entry point for the menu-based experience. It creates the core `User`, `Deck`, and `Manager` objects and delegates each feature to the application logic.

### `logic.py`

Contains the main use-case functions that coordinate user interactions with the domain objects:

- `engine_init` — creates cards, initializes their first reviews, and persists the result
- `review_time` — checks for due or overdue cards and launches a review session
- `display_statistics` — displays deck and review statistics
- `search_cards` — searches for a card by concept
- `make_actions` — updates or deletes a card

### `engine.py`

Contains the three main classes of the application.

#### `Deck`

Handles card and review behavior, including:

- retrieving due cards
- initializing reviews
- reviewing due cards
- searching cards
- updating or deleting cards
- counting reviews and cards
- computing review statistics
- tracking card states and ratings

The deck uses an FSRS `Scheduler` to calculate review scheduling.

#### `User`

Represents a Retentia user and manages user-specific information such as:

- username and password
- flashcards
- user data
- card identifiers
- creation and loading of concepts

#### `Manager`

Handles persistence of user information, cards, reviews, and review logs.

### `tools.py`

Contains helper functions used throughout the application, including:

- JSON storage operations
- retrieving statistical information
- password encoding and verification
- user and deck checks
- helper utilities shared by the other modules

### `routing.py`

Chooses how Retentia should start. If the user provides a command-line command, it routes execution to the corresponding CLI command. Otherwise, it launches the interactive menu.

### `commands.py`

Defines the command-line commands and connects them to the application logic.

### `typer__app.py`

Creates the shared Typer application object used by the CLI modules.

### `setup.py`

Ensures the JSON storage files required by Retentia exist before the application uses them.

### `tests_project.py`

Contains the automated test suite. The tests cover important behaviors such as:

- card creation and persistence
- password hashing and matching
- review behavior and side effects
- statistics
- card search
- deletion and updates

The tests use `pytest` and `monkeypatch` to simulate interactive input and verify both returned values and changes written to storage.

### `requirements.txt`

Lists the external Python packages required to run the project.

## Technologies and Concepts Used

- Python
- Object-Oriented Programming
- FSRS spaced-repetition scheduling
- Typer
- Rich
- PyFiglet
- bcrypt
- JSON persistence
- pytest
- monkeypatch-based testing
- modular application design

## Why I Built Retentia

Retentia started as a learning project, but its goal is practical: make active recall and spaced repetition accessible directly from the terminal.

More importantly, building it forced me to move beyond small isolated Python exercises and work with a larger program involving state, multiple modules, object interactions, persistence, third-party libraries, side effects, error handling, and automated tests.
