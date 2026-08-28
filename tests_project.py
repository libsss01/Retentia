# test functions must have same name that's name in the project file
import pytest
import datetime
import time
import builtins
import bcrypt
from Retentia.logic import engine_init, review_time, display_statistics, search_cards, make_actions
import engine as eng
import Retentia.tools as t


def test_engine_init_password_match(monkeypatch):
    username = "Dev."
    password = "Pythoncoder2026"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
    responses = iter(["", "What's the best Programming language these days", "Rust", "y",
                         "Who is the Rust creator ?", "Graydon Hoare", "n", "", "4", "", "4"])

    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)

    engine_init(user, deck, manager)

    user_id = t.get_user_id(username, password)

    data = t.return_user_dict("storage.json", user_id)

    passsword_retreived = t.encode_password(data['password'])
    password = t.encode_password(password)
    
    second_password = t.encode_password("randompassword2024")

    assert bcrypt.checkpw(second_password, passsword_retreived) == False
    assert bcrypt.checkpw(password, passsword_retreived) == True

def test_engine_init_success(monkeypatch):
    username = "coder"
    password = "PythonDev2026"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)


    responses = iter(["", "What's the best Programming language of all time ?", "C", "y",
                     "Who is the C creator ?", "Dennis Ritchie at Bell Labs", "n", "", "4", "", "4"])

    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)

    assert engine_init(user, deck, manager) == "\033[32mCard(s) added and initialized, Successfull Review!\033[0m"

    expected_dict = {
        "username": "coder",
        "id": None,
        "last_time_connected":None,
        "streak": 1,
        "flashcards": [
            {
                "1": {
                    "what's the best programming language of all time ?": "c"
                }
            },
            {
                "2": {
                    "who is the c creator ?": "dennis ritchie at bell labs"
                }
            }

        ],
        "reviews": [
            {
                "card_id": 1,
                "state": 2
            },
            {
                "card_id": 2,
                "state": 2
            }
        ],
        "reviewLog": [
            {
                "card_id": 1,
                "rating": 4,
            },
            {
                "card_id": 2,
                "rating": 4
            }
        ]
    }
    
    expected_dict["last_time_connected"] =  str(datetime.date.today())
    expected_dict["id"] = t.get_user_id(username, password) 
    
    user_id = t.get_user_id(username, password)

    data = t.return_user_dict("storage.json", user_id)
        
    data.pop("password")

    result = t.remove_keys(data)
    
    if result:
        print(result)
    
    assert data == expected_dict

def test_review_time_w_no_cards_created():
    username = "Programmer"
    password = "SoftwareEng2000_"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
    
    assert review_time(user, deck, manager) == "\033[31mYou can't access to this feature until you've create cards.\033[0m"

def test_review_time_w_no_cards_due(monkeypatch):
    username = "Fullstack Dev"
    password = "WebLover10"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)

    responses = iter(["", "What's the best JavaScript Library/Framework for Web Development", "React", "n",
                      "", "4"])

    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)
    
    engine_init(user, deck, manager)
    
    assert review_time(user, deck, manager) == "\033[34mYou don't have cards due yet !\033[0m"
    
def test_review_time_side_effect(monkeypatch):
    username = "Game Dev"
    password = "C++ Lover"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
    
    responses = iter(["", "Best Language for Game Dev ?", "C++", "y",
                     "Who is the C++ creator ?", "Bjarne Stroustrup", "y", "When The C++ Language was created ?", "It was released officially in 1985", "n", "", "1", "", "1", "", "2"])
   
    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)
        
    engine_init(user, deck, manager)
    time.sleep(1.5)
    review_time(user, deck, manager)
    
    expected_dict = {
        "username": username,
        "id": None,
        "last_time_connected":None,
        "streak": 1,
        "flashcards": [
            {
                "1": {
                    "best language for game dev ?": "c++"
                }
            },
            {
                "2": {
                    "who is the c++ creator ?": "bjarne stroustrup"
                }
            },
            {
                "3": {
                    "when the c++ language was created ?": "it was released officially in 1985"
                }
            }

        ],
        "reviews": [
            {
                "card_id": 1,
                "state": 1
            },
            {
                "card_id": 2,
                "state": 1
            }, 
            {
                "card_id": 3,
                "state": 1
            }
            
        ],
        "reviewLog": [
            {
                "card_id": 1,
                "rating": 1,
            },
            {
                "card_id": 2,
                "rating": 1
            },
            {
                "card_id": 3,
                "rating": 2
            }
        ]
    }
    
    expected_dict["last_time_connected"] =  str(datetime.date.today())
    expected_dict["id"] = t.get_user_id(username, password) 
    
    user_id = t.get_user_id(username, password)   
    data = t.return_user_dict("storage.json", user_id)
    
    data.pop("password")
    
    result = t.remove_keys(data)
        
    if result:
        print(result)

    print(data)
    print(expected_dict)
    assert data == expected_dict
    
def test_display_statistics_w_no_card_created():
    username = "Omar Marmoush"
    password = "OM22"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    
    assert display_statistics(user, deck) == "\033[31mYou can't access to this feature until you're registered\033[0m"
    
def test_display_statistics(monkeypatch):
    username = "Ismaila Sarr"
    password = "Iso"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
      
    responses = iter(["", "Actual Footnall Team ?", "Crystal Palace", "y",
                        "Shirt Number ?", "#7", "y", "Which year did you join Crystal Palace ?", "2023", "n", "", "1", "", "3", "", "2"])
       
    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)
            
    engine_init(user, deck, manager)
    
    assert deck.number_of_cards() == 3
    assert deck.number_of_card_by_rating() == (1, 1, 1, 0)
    assert deck.number_of_card_by_state() == (3, 0, 0)
    assert deck.number_of_cards_due_today() == "3 card(s) due Today !"
    assert deck.number_of_cards_upcoming() == "0 card(s) upcoming !"
    assert deck.number_of_overdue_cards() == "0 overdue card(s) !"
    assert deck.reviews_per_week() == 3
    assert deck.reviews_per_day() == 3
    assert deck.number_of_reviews() == 3
    
    
    assert display_statistics(user, deck) == "\033[32mGood Job Keep Going !!\033[0m"

def test_search_cards_w_no_cards_created():
    username = "Libss"
    password = "LM10"
    user = eng.User(username, password)
    deck = eng.Deck(user)
        
    assert search_cards(user, deck) == "\033[31mYou can't access to this feature until you're registered\033[0m"
    
def test_search_cards(monkeypatch):
    username = "Mo."
    password = "EGY"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
    responses = iter(["", "World Cup 2026 Winner ?", "Spain", "y",
                            "Best Player of the WC ?", "Rodri", "y", "Best Scorer of the WC ?", "K.Mbappe", "n", "", "1", "", "2", "", "3", "Best Player of the WC ?", "", "", "n", "Best Scorer of the WC ?", "", "", "y"])
           
    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)
                
    engine_init(user, deck, manager)
    
    assert search_cards(user, deck) == "\033[32mYour cards are alive !\033[0m"       

def test_make_actions_w_no_card_created():
    username = "O."
    password = "Ous1"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    
    assert make_actions(user, deck) == "\033[31mYou can't access to this feature until you're registered\033[0m"

def test_make_actions_deleting_functionality(monkeypatch):
    username = "Lima"
    password = "MLEng10"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
    
    responses = iter(["", "Which African Team has most CAN ?", "Egypt", "n", "", "4", "", "Which African Team has most CAN ?", "", "1", "", "y"])
    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)
    
    engine_init(user, deck, manager)
    
    make_actions(user, deck) 
    
    expected_dict = {
            "username": username,
            "id": None,
            "last_time_connected":None,
            "streak": 1,
            "flashcards": [],
            "reviews": [],
            
            "reviewLog": [
                {
                    "card_id": 1,
                    "rating": 4,
                }
            ]
        }
        
    expected_dict["last_time_connected"] =  str(datetime.date.today())
    expected_dict["id"] = t.get_user_id(username, password)
      
    user_id = t.get_user_id(username, password)
    data = t.return_user_dict("storage.json", user_id)

    data.pop("password")
         
    result = t.remove_keys(data)
        
    if result:
        print(result)
    
    assert data == expected_dict

def test_make_actions_update_concept_functionality(monkeypatch):
    username = "Haskell"
    password = "Alex10"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
    
    responses = iter(["", "Compiling vs Interpreting", "Compiling (e.g., C): Translates the entire code into an executable file before running. Interpreting (e.g., Python): Translates and executes code line by line at runtime.", "n", "", "4", "", "Compiling vs Interpreting", "", "2",  "", "1", "", "What's the difference compiling and Interpreting ?", "y"])
    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)
    
    engine_init(user, deck, manager)
    
    make_actions(user, deck)
    
    expected_dict = {
            "username": username,
            "id": None,
            "last_time_connected":None,
            "streak": 1,
            "flashcards": [
                {
                    "1": {
                                "what's the difference compiling and interpreting ?": "compiling (e.g., c): translates the entire code into an executable file before running. interpreting (e.g., python): translates and executes code line by line at runtime."
                         }
                }
            ],
            "reviews": [
                {
                    "card_id": 1,
                    "state": 2
                }
            ],
    
            "reviewLog": [
                {
                    "card_id": 1,
                    "rating": 4,
                }
            ]
        }
    
    expected_dict["last_time_connected"] =  str(datetime.date.today())
    expected_dict["id"] = t.get_user_id(username, password)
    
 
    user_id = t.get_user_id(username, password) 
    data = t.return_user_dict("storage.json", user_id)
    
    data.pop("password")
    
    result = t.remove_keys(data)
    
    if result:
        print(result)

    assert data == expected_dict

def test_make_actions_update_answer_functionality(monkeypatch):
    username = "Brooks"
    password = "bks"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
    
    responses = iter(["", "Which Team won the last CAN ?", "Morocco", "n", "", "4", "", "Which Team won the last CAN ?", "", "2",  "", "2", "", "Senegal", "y"])
    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)
    
    engine_init(user, deck, manager)
    make_actions(user, deck)
    
    expected_dict = {
            "username": username,
            "id": None,
            "last_time_connected":None,
            "streak": 1,
            "flashcards": [
                {
                    "1": {
                            "which team won the last can ?": "senegal"
                         }
                }
            ],
            "reviews": [
                {
                    "card_id": 1,
                    "state": 2
                }
            ],
    
            "reviewLog": [
                {
                    "card_id": 1,
                    "rating": 4,
                }
            ]
        }
    
    expected_dict["last_time_connected"] =  str(datetime.date.today())
    expected_dict["id"] = t.get_user_id(username, password)
    
    
    user_id = t.get_user_id(username, password)
    data = t.return_user_dict("storage.json", user_id)

    data.pop("password")
    result = t.remove_keys(data)
    
    if result:
        print(result)
            
    assert data == expected_dict   

def test_make_actions_update_concept_and_answer_functionality(monkeypatch):
    username = "Yaya"
    password = "yyy01"
    user = eng.User(username, password)
    deck = eng.Deck(user)
    manager = eng.Manager(user, deck)
    
    responses = iter(["", "The Best Python Course in Internet ?", "Python Programming MOOC", "n", "", "4","", "The Best Python Course in Internet ?", "", "2",  "", "3", "", "Which is the best Programming Course in Internet ?", "","CS50's Introduction to Programming with Python", "y"])
    def fake_input(text):
        return next(responses)
    monkeypatch.setattr(builtins, "input", fake_input)

    engine_init(user, deck, manager)
    
    make_actions(user, deck)
    expected_dict = {
            "username": username,
            "id": None,
            "last_time_connected":None,
            "streak": 1,
            "flashcards": [
                {
                    "1": {
                                "which is the best programming course in internet ?": "cs50's introduction to programming with python"
                         }
                }
            ],
            "reviews": [
                {
                    "card_id": 1,
                    "state": 2
                }
            ],
    
            "reviewLog": [
                {
                    "card_id": 1,
                    "rating": 4,
                }
            ]
        }
    
    expected_dict["last_time_connected"] =  str(datetime.date.today())
    expected_dict["id"] = t.get_user_id(username, password)
    
    user_id = t.get_user_id(username, password)  
    data = t.return_user_dict("storage.json", user_id)

    data.pop("password")    
    result = t.remove_keys(data)
    
    if result:
        print(result)
        
    assert data == expected_dict