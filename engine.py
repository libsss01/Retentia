import Retentia.tools as t
from fsrs import Scheduler, Card, Rating, ReviewLog
import datetime
import time
from pytz import timezone
import bcrypt

# Storage Filename
json_file = "storage.json"


class Deck:
    """
        A class responsible for the deck creation and handle everything related to a deck, such as: cards, due cards, reviews... 
        with methods that enable features like searching, performing actions on the deck (delete, update),
        and a variety of statistical information
    """
    def __init__(self, user):
        self.user = user
        self.scheduler = Scheduler()

    def __str__(self):
        return f"{self.user.username}'s Deck !"
                
    def cards_due(self):
        dues = []
        user_id = t.get_user_id(self.user.username, self.user.password)
        data = t.return_user_dict(json_file, user_id)
        if t.has_review(self.user.username, self.user.password):
            current_date = datetime.datetime.now()
            for cards in data["flashcards"]:
                for review in data["reviews"]:  
                    current_date = current_date.astimezone(timezone('UTC'))
                    if current_date >= datetime.datetime.fromisoformat(review["due"]):
                        if str(review["card_id"]) in cards:
                            dues.append(cards[str(review["card_id"])])
                            break
        else:
            return None

        return dues

    def retreive_cards(self, listCard_ids):
        logObj = list()
        reviewObj = list()
        logs = dict()
        user_id = t.get_user_id(self.user.username, self.user.password)
        data = t.return_user_dict(json_file, user_id)
        for log in data["reviewLog"]:
            logs[log["card_id"]] = log
        for review in data["reviews"]:
            if review["card_id"] in listCard_ids and review["card_id"] in logs:
                reviewObj.append(review)
                logObj.append(logs[review["card_id"]])
            else:
                continue
        return reviewObj, logObj

    def review_init(self):
        """
            review method only called for innitialization (1st review) by seting first rating after creation
        """
        start_time = time.time()
        list_of_ids = list()
        list_of_id = list()
        lists_of_cards = list()
        real_time_cards = list()
        status = ""
        
        user_id = t.get_user_id(self.user.username, self.user.password)
        
        if len(self.user.lists_of_concepts) > 1:
            if not user_id:
                status = '\033[31mUnknown User\033[0m'
                return (status, [], [])
            
        data = t.return_user_dict(json_file, user_id)
            
        for concept in self.user.lists_of_concepts:
            if t.card_has_review(concept, data) or t.card_has_log(concept, data):
                continue
            else:
                real_time_cards.append(concept)
        for i in range(len(real_time_cards)):
            list_of_ids.append(list((real_time_cards[i].keys())))
        for i in range(len(list_of_ids)):
            list_of_id += list_of_ids[i]
        for Id in range(len(list_of_id)):
            card = Card(int(list_of_id[Id]))
            lists_of_cards.append(card)
        list_of_ids.clear()

        reviewsList = list()
        reviewLogList = list()

        for cardObj in lists_of_cards:
            list_of_ids.append(cardObj.card_id)
    
        data_json = t.read_file(json_file)
        for idObj in list_of_ids:
            for data in data_json:
                if data["id"] == user_id:
                    break
            for flashcards in data["flashcards"]:
                if str(idObj) in flashcards:
                    flashcardId = list(flashcards.keys())[0]
                    if str(idObj) == str(flashcardId):
                        for key, value in flashcards[str(flashcardId)].items():
                            print("\n")
                            print(key.title())
                            input("Press Enter to See answer...")
                            print("The answer is...")
                            time.sleep(0.2)
                            if type(value) == int:
                                print(value)
                            else:
                                print(value.title())
                            print("\n")
                            while True:
                                try:
                                    time.sleep(0.5)
                                    rating = int(input("What's your Rating about this card ?\n"
                                                    "1 = Again\n"
                                                    "2 = Hard\n"
                                                    "3 = Good\n"
                                                    "4 = Easy\n"))
                                    if not t.if_valid_rating(rating):
                                        continue
                                    else:
                                        break
                                except (ValueError):
                                    pass

                            end_time = time.time()
                            review_duration = end_time - start_time

                            # Casting & convertion into milliseconds
                            review_duration = int(review_duration) * 1000
                            for cardss in lists_of_cards:
                                card, review_log = self.scheduler.review_card(cardss, rating, review_duration=review_duration)
                                reviewsList.append(card.to_dict())
                                reviewLogList.append(review_log.to_dict())
                                if len(lists_of_cards) > 0:
                                    lists_of_cards.pop(0)
                                break
                                    
        status = "\033[32mCard(s) added and initialized, Successfull Review!\033[0m"
        return (status, reviewsList, reviewLogList)

    def review_cards(self):
        """
            review method for when a card is due after his initialization
            called for updating cards attribute such rating, review_datetime, review_duration and append log to the existent list of log 
        """
        start_time = time.time()
        cards_due = self.cards_due()
        ratings_list = list()
        status = ""
        time_of_next_review_session = None
        user_id = t.get_user_id(self.user.username, self.user.password)
        data = t.return_user_dict(json_file, user_id)  
        
        if not user_id:
            status = "\033[31mUser doesn't exist\033[0m"
            return (status, [], [], time_of_next_review_session)
        
        if not cards_due :
            time_of_next_review_session = t.get_next_time_card_is_due(self.user.username, self.user.password)
            status = "\033[34mYou don't have reviews yet or no Cards due Today\033[0m"
            return (status, [], [], time_of_next_review_session)
        
        card = Card()
        reviewsList = list()
        reviewLogList = list()
        list_id = list()  
        streak = t.get_streak(self.user.username, self.user.password)
        if streak > 1:
            print(f"***" + f"{streak} days Streak in a Row 🔥🔥🔥".center(50) + "***")

        else:
            print("***"+f" {streak} day Streak".center(50) + "***")
            
            
        for cards in data["flashcards"]:  
            for cardtoReview in cards_due:        
                card_ids = list(cards.keys())[0] 
                if cards[str(card_ids)] == cardtoReview:
                    for key, value in cardtoReview.items():
                            print("\n")
                            print(key.title())
                            input("Press Enter to See answer...")
                            print("The answer is ")
                            time.sleep(0.2)
                            if type(value) == int:
                                print(value)
                            else:
                                print(value.title())
                            list_id.append(int(card_ids))
                            print("\n")
                            while True:
                                try:
                                    time.sleep(0.5)
                                    rating = int(input("What's your Rating about this card ?\n"
                                                        "1 = Again\n"
                                                        "2 = Hard\n"
                                                        "3 = Good\n"
                                                        "4 = Easy\n"))
                                    if not t.if_valid_rating(rating):
                                        continue
                                    else:
                                        ratings_list.append(rating)
                                        break
                                except (ValueError):
                                    continue
                            
                            end_time = time.time()
                            review_duration = end_time - start_time

                            # Casting & convertion into milliseconds
                            review_duration = int(review_duration) * 1000
                else:
                    continue

        list_reviews, _ = self.retreive_cards(list_id)
        for review, rates in zip(list_reviews, ratings_list):
            review = card.from_dict(review)
            card, review_log = self.scheduler.review_card(review, rates, review_duration=review_duration)
            reviewsList.append(card.to_dict())
            reviewLogList.append(review_log.to_dict())

        
        status = "\033[32mSuccessfull Review!\033[0m"
        return  status, reviewsList, reviewLogList, time_of_next_review_session
            

    def search(self, concept):
        """
            A method for finding a specific card in the deck
            by displaying it (the concept/question and the answer)
        """
        found = False
        concept = concept.lower()  
        user_id = t.get_user_id(self.user.username, self.user.password)
        
        if not user_id:
            return "User not found"   
            
        data = t.return_user_dict(json_file, user_id)
        for card in data["flashcards"]:
            card_id = list(card.keys())[0]
            if concept in card[card_id]:
                found = True
                answer = card[card_id][concept]
                break
        if found:
            return concept, answer
        else:
            return "Card not found"

    def perform_actions_on_deck(self, concept, choice):
        """
            Method that's perform actions such as updating (concept, answer or both), delete a whole card on a deck
        """
        found = False
        message = ""
        concept = concept.lower()
        try:   
            user_id = t.get_user_id(self.user.username, self.user.password)
            if not user_id:
                return "User not found"
            json_data = t.read_file(json_file)
            for data in json_data:
                if data["id"] == user_id:
                    break
            for card in data["flashcards"]:
                card_id = list(card.keys())[0]
                if concept in card[card_id]:
                    found = True
                    break
                else:
                    continue
            match(choice, found):
                    case 1, True:
                        data["flashcards"].remove(card)
                        for review in data['reviews']:
                            if review["card_id"] == int(card_id):
                                data['reviews'].remove(review)
                                break
                        message = "Card deleted with success"
                    case 2, True:
                        update_choice = 0
                        print("Let's Update your cards !")
                        time.sleep(0.3)
                        while not update_choice or not int(update_choice) in [1, 2, 3]:
                            try:
                                update_choice = int(input("1. Edit an concept\n"
                                                        "2. Edit an answer\n"
                                                        "3. Edit both\n"))
                                print("\n")
                            except(ValueError):
                                print("Wrong Input !")
                                continue
                            
                        input("Press Enter to continue !\n")

                        match(update_choice):
                                case 1:
                                    new_key = input("What's your new concept ?\n").lower()
                                    card[card_id][new_key] = card[card_id].pop(concept)
                                    message = "Concept/Questions succefully changed !"
                                case 2:
                                    new_answer = input("What's your new answer for the concept ?\n").lower()
                                    card[card_id][concept] = new_answer
                                    message = "Answer succefully changed !"
                                case 3:
                                    new_key = input("Enter the new concept/Questions\n").lower()
                                    time.sleep(0.3)
                                    print("You entered the new concept : "+new_key)
                                    input("Press Enter to continue\n")
                                    new_answer = input("Enter the new answer for the associated concept\n").lower()
                                    time.sleep(0.2)
                                    print("You entered the answer "+ new_answer+" for the concept" +new_key)
                                    card[card_id] = {new_key: new_answer}
                                    message = "Concept succesfully updated" 

            if not found:
                error_message = "Card not found !"
                return error_message

            t.write_to_file(json_file, json_data)
            
            return message
        
        except (KeyboardInterrupt):
            return "\033[31mNo action was taken\033[0m"

    """
        Some statistical methods that real time information like the streak, the number of review done (per day or week), 
        the number of card grouped by raking, state and so on
    """
    
    def number_of_reviews(self):
        user_id = t.get_user_id(self.user.username, self.user.password)
        data = t.return_user_dict(json_file, user_id)
        return len(data['reviews'])
    
    def reviews_per_day(self):
        today_date = datetime.date.today()
        user_id = t.get_user_id(self.user.username, self.user.password)
        data = t.return_user_dict(json_file, user_id)
        return len([reviewlog['review_datetime'] for reviewlog in data['reviewLog'] if datetime.datetime.fromisoformat(reviewlog['review_datetime']).date() == today_date])
    
    def reviews_per_week(self):
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        user_id = t.get_user_id(self.user.username, self.user.password)
        data = t.return_user_dict(json_file, user_id)
        return len([reviewlog['review_datetime'] for reviewlog in data['reviewLog'] if datetime.datetime.fromisoformat(reviewlog['review_datetime']).date() <= today and datetime.datetime.fromisoformat(reviewlog['review_datetime']).date() >= monday])
    
    def streak(self):
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            date_of_user_last_review = t.get_last_time_connected(self.user.username, self.user.password)
    
            if date_of_user_last_review:
                date_of_user_last_review = str(date_of_user_last_review)
            
            if date_of_user_last_review is None:
                newStreak = 1
                t.update_streak(self.user.username, self.user.password, newStreak)
                return '\033[38;5;211mStreak Set\033[0m'
            
            if not t.get_number_of_cards_due_today(self.user.username, self.user.password):
                return "No Reviews for today !"
            
            elif datetime.datetime.fromisoformat(date_of_user_last_review).date() == today:
                return "\033[38;5;211mStreak Set\033[0m"
            
            elif datetime.datetime.fromisoformat(date_of_user_last_review).date() == yesterday:
                newStreak = t.get_streak(self.user.username, self.user.password)
                newStreak += 1
                t.update_streak(self.user.username, self.user.password, newStreak)
                return "\033[38;5;211mStreak Updated\033[0m"
                
            elif yesterday < datetime.datetime.fromisoformat(date_of_user_last_review).date():
                newStreak = 1
                t.update_streak(self.user.username, self.user.password, newStreak)
                return "\033[38;5;211mStreak Updated\033[0m"
    
    
    def number_of_cards(self):
        retreived = False
        user_id = t.get_user_id(self.user.username, self.user.password)
        data = t.return_user_dict(json_file, user_id)
        if data:
                retreived = True
        if retreived:
            return len(data["flashcards"])
        else:
            return None
    
    def number_of_card_by_rating(self):
            book_of_rating = t.count_card_by_rating(self.user.username, self.user.password)
    
            return (book_of_rating['number_of_card_rated_again'], book_of_rating['number_of_card_rated_difficult'], book_of_rating['number_of_card_rated_good'],book_of_rating['number_of_card_rated_easy'])
    
    def number_of_card_by_state(self):
            book_of_state = t.count_card_by_state(self.user.username, self.user.password)
    
            return (book_of_state['number_of_learning_card'], book_of_state['number_of_revised_card'], book_of_state['number_of_relearned_card'])
    
    def number_of_cards_due_today(self):
            number_of_cards = t.get_number_of_cards_due_today(self.user.username, self.user.password)
    
            return f"{number_of_cards} card(s) due Today !"
    
    def number_of_cards_upcoming(self):
            number_of_cards = t.get_number_of_cards_upcoming(self.user.username, self.user.password)
    
            return f"{number_of_cards} card(s) upcoming !"
    
    def number_of_overdue_cards(self):
            number_of_cards = t.get_number_of_cards_overdue(self.user.username, self.user.password)
    
            return f"{number_of_cards} overdue card(s) !"


class User:
    """
        Class responsible of the user creation and that implements some methods related to the user it self 
        like his dictionary creation and features like adding cards and create them
    """
    def __init__(self, username, password):
        self.__id = t.get_last_user_id()
        self.__username = username
        self.__lists_of_concepts = list()
        self.__user_dict = dict()
        self.__password = password
        self.__id_cards = 1

    def __str__(self):
        return f" My username is {self.__username} "

    # getter for private property
    @property
    def username(self):
        return self.__username
    @property
    def password(self):
        return self.__password
    @property
    def lists_of_concepts(self):
        return self.__lists_of_concepts.copy()
    
    
    def create_user_dict(self):
        """
            method that creates the user dict that will be stored as object in the JSON file
        """
        self.__password = t.encode_password(self.password)
        hashed_password = bcrypt.hashpw(self.__password, bcrypt.gensalt())
        self.__user_dict = {
                "username": self.username,
                "id": self.__id,
                "password": hashed_password.decode(),
                "last_time_connected": None,
                "streak": 0,
                "flashcards": self.__lists_of_concepts,
                "reviews": [],
                "reviewLog": []
            }
      
        return self.__user_dict

    def add_cards(self):
        user_id: int = t.get_user_id(self.username, self.password)
        id_cards = t.get_last_card_id(user_id, self.username, self.password)

        try:
            if (not id_cards.isdigit()):
                id_cards = 0
        except (AttributeError, ValueError):
            pass

        i = 0
        while i == 0:
            concept = input("What's your Concept/Question ?\n").lower()
            time.sleep(0.3)
            if concept == "":
                print("It seems like u didn't provide a concept")
                continue
            time.sleep(0.2)
            answer = input("What's the anwser ?\n").lower()
            if answer.isnumeric():
                answer = int(answer)
            if answer == "":
                print("It seems like u didn't provide a answer")
                continue

            while True:
                continue_or_not = input("Do you want to add more ? Y/N (yes/no)\n").lower()
                time.sleep(0.2)
                if continue_or_not == 'y' or continue_or_not == 'yes':
                    break
                elif continue_or_not == "n" or continue_or_not == "no":
                    i = 1
                    break
                else:
                    continue

            new = dict()
            id_cards += 1
            new[str(id_cards)] = {concept: answer}
            self.__lists_of_concepts.append(new)

        json_data = t.read_file(json_file)
        for data in json_data:
            if user_id == data["id"]:
                exist = True
                break
        if exist:
            for card in self.__lists_of_concepts:
                if card in data["flashcards"]:
                    continue
                data["flashcards"].append(card)
                
        t.write_to_file(json_file, json_data)


    def create_concept(self):
        i = 0
        while i == 0:
            concept = input("What's your Concept/Question ?\n").lower()
            time.sleep(0.4)
            if concept == "":
                print("It seems like u didn't provide a concept")
                continue
            answer = input("What's the anwser ?\n").lower()
            time.sleep(0.4)
            if answer.isnumeric():
                answer = int(answer)
            if answer == "":
                print("It seems like u didn't provide a answer")
                continue
            print("\n")
            while True:
                continue_or_not = input("Do you want to add more ? Y/N (yes/no)\n").lower()
                if continue_or_not == 'y' or continue_or_not == 'yes':
                    break
                elif continue_or_not == "n" or continue_or_not == "no":
                    i = 1
                    break
                else:
                    continue
            new = dict()
            new[str(self.__id_cards)] = {concept: answer}
            self.__id_cards += 1
            self.__lists_of_concepts.append(new)

class Manager:
    """
        class responsible for storing data directly to the JSON file. It implements methods for storing user and his review data
    """
    
    def __init__(self, user, deck):
        self.user = user
        self.user_dict = self.user.create_user_dict()
        self.deck = deck
    
    def store_user_info(self):
        json_data = t.read_file(json_file)
        json_data.append(self.user_dict)
        t.write_to_file(json_file, json_data)
        t.insert_last_user_id()
   
    def store_review_info(self, card_reviewed, LogReview):
        changeLog = False
        user_id = t.get_user_id(self.user.username, self.user.password)
        json_data = t.read_file(json_file)
        
        for data in json_data:
            if not user_id == data['id']:
                continue
            else:
                if not t.has_review(self.user.username, self.user.password):
                    changeLog = True
                else:
                    for review in card_reviewed:
                        found = False
                        for i, reviewStored in enumerate(data['reviews']):
                            if review['card_id'] == reviewStored['card_id']:
                                found = True
                                break
                        if found:
                            data['reviews'][i] = review
                        else:
                            data['reviews'].append(review)

                    for log in LogReview:
                        data['reviewLog'].append(log)

                if changeLog:
                    for cards in card_reviewed:
                        data["reviews"].append(cards)
                    for log in LogReview:
                        data["reviewLog"].append(log)

                t.write_to_file(json_file, json_data)
                self.deck.streak()    
                t.set_last_time_connected(self.user.username, self.user.password)