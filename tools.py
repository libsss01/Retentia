import json
import bcrypt
import datetime
from pytz import timezone
import math

fixed_length = 60
file_json = "storage.json"
tools_json = "tools.json"

def ask_user_infos():
    username = ""
    password = ""
    print("\n")
    print("#" * fixed_length)
    print("#" + "Sign Up/Log In".center(58) + "#")
    print("#" * fixed_length)
    print("\n")
    username: str = str(input("What's your username ? \n"))
    if username == "":
        print("Don't Want to enter a username ?")
        print("Your Default Username is user")
        username = 'user'
    while not password:
        password: str = str(input("What's your password ?\n"))

    return username, password
    
def get_user_id(username, password):
    find = False
    password = encode_password(password)
    json_data = read_file(file_json)
    for data in json_data:
        hashed_password = encode_password(data['password'])
        if data["username"] == username and check_hashed_password(password, hashed_password):
                find = True
                user_id = data["id"]
                break
    if not find:
        return None
    return user_id

def read_file(filename):
    with open(filename, "r") as f:
        json_data = json.load(f)
    return json_data

def write_to_file(filename,fileobj):
    with open(filename, "w") as f:
        json.dump(fileobj, f, indent=4)

def return_user_dict(filename, user_id):
    retreived = False
    json_data = read_file(file_json)
    for data in json_data:
        if data["id"] == user_id:
            retreived = True
            break
        else:
            continue
        
    if not retreived:
        return None
    return data

def remove_keys(data):  
    message = ""   
    for review_dict in data['reviews']:
        copy_review = list(review_dict.copy())
        for key in copy_review:
            if key in ["step", "stability", "difficulty", "due", "last_review"]:
                match (review_dict[key]):
                    case float() | int() | None:
                        review_dict.pop(key)
                    case str():
                        review_dict.pop(key)
                    case _:
                        message = " \033[31mSome data is missing \033[0m"

    for log_dict in data['reviewLog']:
        copy_log = list(log_dict.copy())
        for key in copy_log:
            if key in ["review_datetime", "review_duration"]:
                match (log_dict[key]):
                    case int():
                        log_dict.pop(key)
                    case str():
                        log_dict.pop(key)
                    case _:
                        message = " \033[32mSome data is missing \033[0m"
    
    if not message:
        message = "\033[32mKeys removed !\033[0m"
        return message
    return message 
  
def get_last_card_id(user_id, username=None, password=None):
    idFind = False
    data = return_user_dict(file_json, user_id)
    if data:
        idFind = True 
    if idFind:
        if is_deck_empty(username, password):
            return "Desck is Empty !"
        return len(data["flashcards"])
    else:
        return "User doesn't exist"
                

def insert_last_user_id():
    json_data = read_file(tools_json)
    json_data[0]["lastUserId"] += 1
    write_to_file(tools_json, json_data)

def get_last_user_id():
    data = read_file(tools_json)
    return data[0]["lastUserId"]

def is_deck_empty(username, password):
    user_id = get_user_id(username, password)
    data = return_user_dict(file_json, user_id)
    if data:
        id_find = True 
    if id_find: 
        if len(data["flashcards"]) == 0:
            return True
        return False

    
def check_user_exist(username, password):
    if_exist = False
    password = encode_password(password)
    json_data = read_file(file_json)
    for data in json_data:
        hashed_password =  encode_password(data["password"])
        if data["username"] == username and check_hashed_password(password, hashed_password):
            if_exist = True
    if if_exist:
        return True
    return False
    
def check_hashed_password(password, hashed):
    if bcrypt.checkpw(password, hashed):
        return True
    return False
    
def has_review(username, password):
    have_reviewed =  False
    user_id = get_user_id(username, password)
    data = return_user_dict(file_json, user_id)
    if len(data['reviews']) > 0  and len(data['reviewLog']) > 0:
        have_reviewed = True
    if not have_reviewed:
        return False 
    return True

def card_has_review(concept, data):
    has_review = False
    key = str(list(concept.keys())[0])
    
    for review in data['reviews']:
        if int(key) == review['card_id']:
            has_review = True
            break
        else:
            continue
    if not has_review:
        return False
    return True

def card_has_log(concept, data):
    has_log = False
    key = str(list(concept.keys())[0])
    
    for log in data['reviewLog']:
        if int(key) == log['card_id']:
            has_review = True
            break
        else:
            continue
    if not has_log:
        return False
    return True


def if_valid_rating(rates):
    return rates in [1, 2, 3, 4]
                    
def encode_password(password): 
    if not type(password) == bytes:  
        return password.encode()
    return password
      
def set_last_time_connected(username, password):
    user_id = get_user_id(username, password)
    json_data = read_file(file_json)
    for data in json_data:
        if user_id == data["id"]:
            break
    data['last_time_connected'] = datetime.date.today().isoformat()
    write_to_file(file_json, json_data)

def get_last_time_connected(username, password):
    user_id = get_user_id(username, password)
    data = return_user_dict(file_json, user_id)
    return data['last_time_connected']


def update_streak(username, password, newStreak):
    user_id = get_user_id(username, password)
    json_data = read_file(file_json)
    for data in json_data:
        if user_id == data["id"]:
            break
    data['streak'] = newStreak
    write_to_file(file_json, json_data)


def get_streak(username, password):
    user_id = get_user_id(username, password)
    data = return_user_dict(file_json, user_id)
    return data['streak']

def get_last_reviews(user_id):
    last_reviews_list = []
    data = return_user_dict(file_json, user_id)
    for review in data["reviews"]:
        last_reviews_list.append(review['last_review'])
    return last_reviews_list


def count_card_by_rating(username, password):
    counter_again = 0
    counter_difficult = 0
    counter_good = 0
    counter_easy = 0
    user_id = get_user_id(username, password)
    last_reviews = get_last_reviews(user_id)
    
    data = return_user_dict(file_json, user_id)

    for log in data['reviewLog']:
        if log['review_datetime'] in last_reviews:
            match(log['rating']):
                case 1:
                    counter_again += 1
                case 2:
                    counter_difficult += 1
                case 3:
                    counter_good += 1
                case 4:
                    counter_easy += 1
                case _:
                    print("Rating doesn't exist")
        else:
            continue

    return {"number_of_card_rated_again": counter_again,
            "number_of_card_rated_difficult": counter_difficult,
            "number_of_card_rated_good": counter_good,
            "number_of_card_rated_easy": counter_easy
            }


def count_card_by_state(username, password):

    counter_learning_state = 0
    counter_review_state = 0
    counter_relearning_state = 0
    user_id = get_user_id(username, password)
    
    data = return_user_dict(file_json, user_id)
    
    for log in data['reviews']:
        match(log['state']):
            case 1:
                counter_learning_state += 1
            case 2:
                counter_review_state += 1
            case 3:
                counter_relearning_state += 1
            case _:
                print("Weird state")

    return {"number_of_learning_card": counter_learning_state,
            "number_of_revised_card": counter_review_state,
            "number_of_relearned_card": counter_relearning_state
            }


def get_number_of_cards_due_today(username, password):
    number_of_card_due = 0
    user_id = get_user_id(username, password)
    data = return_user_dict(file_json, user_id)
    
    if has_review(username, password):
        for review in data["reviews"]:
            current_date = datetime.datetime.now().date()
            if current_date == datetime.datetime.fromisoformat(review["due"]).date():
                number_of_card_due += 1
    else:
        return "You didn't make reviews yet !"

    return number_of_card_due


def get_number_of_cards_overdue(username, password):
    number_of_card_due = 0
    user_id = get_user_id(username, password)
    data = return_user_dict(file_json, user_id)
    
    if has_review(username, password):
        for review in data["reviews"]:
            current_date = datetime.datetime.now().date()
            if current_date > datetime.datetime.fromisoformat(review["due"]).date():
                number_of_card_due += 1

    else:
        return "You didn't make reviews yet !"

    return number_of_card_due

def get_number_of_cards_upcoming(username, password):
    number_of_cards_upcoming = 0
    user_id = get_user_id(username, password)
    data = return_user_dict(file_json, user_id)
    
    if has_review(username, password):
        for review in data["reviews"]:
            current_date = datetime.datetime.now().date()
            if datetime.datetime.fromisoformat(review["due"]).date() > current_date :
                number_of_cards_upcoming += 1
    else:
        return "You didn't make reviews yet !"
    return number_of_cards_upcoming

def get_next_time_card_is_due(username, password):
    lists_of_time_differences = []
    current_date = datetime.datetime.now()
    user_id = get_user_id(username, password)
    filename = "storage.json"
    user_data = return_user_dict(filename, user_id)
    for review in user_data["reviews"]:
        current_date = current_date.astimezone(timezone('UTC'))
        if current_date < datetime.datetime.fromisoformat(review["due"]):
            lists_of_time_differences.append(datetime.datetime.fromisoformat(review["due"]) - current_date)
    smallest_time =  min(lists_of_time_differences)
    
    days = smallest_time.days
    hours = math.floor(smallest_time.seconds / 3600)
    minutes = math.floor(smallest_time.seconds / 60)

    return f"{days} day(s), {hours} hour(s) and {minutes} minute(s)"
    