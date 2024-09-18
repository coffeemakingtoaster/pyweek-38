import random

class Review:
    review_text = "" 
    user_name = "" 

    def __init__(self, text, name, star_count) -> None:
        self.review_text = text
        self.user_name = name
        self.star_count = star_count

    def print(self):
        print(f'By \033[92m{self.user_name}\033[00m:\n\t\033[94m{self.review_text}\033[00m')

NEUTRAL_USERNAMES = list(set([
    "WillyWacker",
    "WillyWonka",
    "PyweekDestroyer",
    "NoneUndefined",
    # pyweek participants
    "python_lord",
    "daylight",
    "GlamaFlomic",
    "fox",
    "Dudnikov",
    "rikovmike",
    "Juna_Gala",
    "mr_matho",
    "RicBin",
    "RobbeF",
    "TurtleRecursion",
    "scarletkite27",
    "Tee",
    "Asher",
    "Snipy7374",
    "Peter312", 
    "Walkercito", 
    "SpookyExe", 
    "Scratcha",
    "spark_07",
    "Ununennium",
    "Stovoy",
    "alwaysencrypt",
    "jako",
    "AURR0RA",
    "skillfulbanana",
    "smoktwix",
    "Doger",
    "Pykemon010",
    "Skander_123",
    "Phantasma",
    "speedlimit35",
    "emille42",
    "greenflame41",
    "bharadwajraju",
    "TNTy100",
    "Rolliepiek",
    "coffee",
    "Heuser",
    "LavenderPixl",
    "Freezerino",
    "heybelia",
    "mit-mit",
    "Apex",
    "dowski",
    "wooster",
    "interrrp",
    "Cosine",
    "p0lygun",
    "TensionFlowed", 
    "serdonke", 
    "advik",
    "preatomicprince", 
    "Jsteele",
    "Vaugbe"
    "DR0ID",
    "Cosmologicon",
    "tabishrfx",
    "gurkwaan",
    "Herjeman",
    "Nils_W",
    "Gulbyxan", 
    "timduvet",
    "jollilala",
    "Boop",
    "Monstersammlery",
    "PyNon",
    "inkontoasty",
    "k3rnel_pan1c_a", 
    "grognak",
    "Dark-Shadow",
    "JustAnotherCode",
    "Gimpy",
    "Devvig",
    "Xrunfun",
    "SirBilby",
    "vagish", 
    "12944qwerty", 
    "sun_dream", 
    "daylight", 
    "Baratheon", 
    "Midnight", 
    "jotajota", 
    "podosci", 
    "Lord-Mistborn", 
    "1knock",
    "midget",
    "Konstantin",
    "Chuchumuru",
    "Master_cheese12",
    "HowDoICode",
    "vagish", 
    "tacchan"
]))

NEGATIVE_USERNAMES = list(set([
    "AngryMan",
    "DisgruntledUser",
    "UpsetPerson",
    "BadMoodBilly",
    "FoodloverFerdinand",
    "Hans",
    "NoTasteSteven",
    "IwriteReviews",
    "TootleReviewer",
    "DontTrustTheGovernment123",
    "FortniteEnjoyer",
    "PinapplePizzaEnjoyer",
]))

def get_user_name(is_negative_review=True):
    if not is_negative_review:
        return random.choice(NEUTRAL_USERNAMES)
    
    i = random.randrange(len(NEUTRAL_USERNAMES) + len(NEGATIVE_USERNAMES))
    if i >= len(NEUTRAL_USERNAMES):
        return NEGATIVE_USERNAMES[i - len(NEUTRAL_USERNAMES)]
    return NEUTRAL_USERNAMES[i]


POSITIVE_REVIEWS_PRETEXT = [
    "Hats off to the chef.",
    "Wow!",
    "Attention everyone!",
    "Dear review readers."
]

POSITIVE_REVIEWS_MAIN = [
    "What an amazing meal!",
    "The {} was delightful.",
    "Better than McDonalds",
    "Better than Burger King",
    "Food was nice. Next time I will get Doner Kebab instead of {} though",
    "SO EIN GUTES ESSEN! DA HAUTS MICH JA GLATT AUS DEN SOCKEN!",
    "My {} was amazing!",
    "I wish I could cook that good.",
    "My {} tasted just like when mom used to make them.",
    "Both the food and the service were better than expected",
    "I ate more than I should have.",
]

POSITIVE_REVIEWS_POSTTEXT = [
    "I will be coming in again!",
    "I will recommend it to a friend.",
    "I would recommend it to a friend...if I had any."
    "Sadly my girlfriend broke up with me during our dinner.",
    "Can I get the chefs number?",
    "I will try to cook {} at home now!"
]

NEGATIVE_REVIEWS_PRETEXT = [
    "I gotta tell you!!",
    "Horrible day!",
    "This restaurant is the reason my wife left me.",
    "Yesterday was the worst day of my life because of this restaurant!",
    "Dear Mr. Restaurant manager: I would like to make a complaint!",
    "Is this kitchen ran by rats?!"
]

NEGATIVE_REVIEWS_MAIN_TOO_MUCH_SALT=[
    "The dead sea contained less salt than my {}.",
    "My tears made my {} sweeter! That is how much salt was in there.",
]

NEGATIVE_REVIEWS_MAIN_TOO_SPICY=[
    "Why was my {} spicy? It should not be!",
    "Had to call an ambulance because it was so spicy.",
    "I drank about 5 litres of milk to counter the spice."
]

NEGATIVE_REVIEWS_MAIN_BURNED = [
    "Anakin was less burned after fighting Obi Wan",
    "The good part: I found some traces of {} in coal I was served.",
    "This might have been an assassination attempt."
]

NEGATIVE_REVIEWS_MAIN_WAIT_TOO_LONG = [
    "By the time the food arrived I had already eaten the napkin.",
    "I arrived when they opened up and received my food as they closed. Therefore I had to eat on the curb outside.",
]

NEGATIVE_REVIEWS_MAIN_SOMETHING_ELSE = [
    "This was an attempt to kill me!",
    "My food was barely recognizable as {}"
]

NEGATIVE_REVIEWS_POSTTEXT = [
    "I will sue this place!",
    "I am recommending this to my worst enemy!",
    "Getting bullied in high school was more enjoyable than eating here.",
    "I hope this place closes soon.",
    "If you like your taste buds, don't eat here."
]

'''
Things that can be wrong with the food:
- Too much salt
- Too spicy
- Burned
- Wait too long
- Wrong ingredients
'''
def get_review_for_food(
    food_name,
    too_much_salt=False,
    too_spicy=False,
    burned=False,
    delayed=False,
    something_else=False,
    is_player_food=False,
):
    
    food_shittiness_score = sum([too_much_salt, too_spicy, burned, delayed, something_else])

    # positive?
    if (is_player_food and food_shittiness_score < 3) or food_shittiness_score == 0:
        return __get_positive_review(food_name)

    # negative?
    review = []

    if __chance(3):
        review.append(random.choice(NEGATIVE_REVIEWS_PRETEXT).format(food_name))
    
    if __chance(2) and too_much_salt:
        review.append(random.choice(NEGATIVE_REVIEWS_MAIN_TOO_MUCH_SALT).format(food_name))
      
    if __chance(2) and too_spicy:
        review.append(random.choice(NEGATIVE_REVIEWS_MAIN_TOO_SPICY).format(food_name))
   
    if __chance(2) and burned:
        review.append(random.choice(NEGATIVE_REVIEWS_MAIN_BURNED).format(food_name))
   
    if __chance(2) and delayed:
        review.append(random.choice(NEGATIVE_REVIEWS_MAIN_WAIT_TOO_LONG).format(food_name))

    if __chance(2) and something_else:
        review.append(random.choice(NEGATIVE_REVIEWS_MAIN_SOMETHING_ELSE).format(food_name))

    if __chance(2) or len(review) == 0:
        review.append(random.choice(NEGATIVE_REVIEWS_POSTTEXT).format(food_name))

    return Review(' '.join(review), get_user_name(True),random.randrange(1,5)/2)

def __get_positive_review(food_name):
    review = [] 
    # 1 in 2 chance of getting a pretext
    if __chance(2):
        review.append(random.choice(POSITIVE_REVIEWS_PRETEXT).format(food_name))
    review.append(random.choice(POSITIVE_REVIEWS_MAIN).format(food_name))
    # 1 in 2 chance of getting a posttext
    if __chance(2):
        review.append(random.choice(POSITIVE_REVIEWS_POSTTEXT).format(food_name))
    return Review(' '.join(review),get_user_name(False),random.randrange(7,9)/2)

# This may be flawed...however I do not care tyvm
def __chance(a):
    return random.randrange( a + 1) == a

# used for testing only
if __name__ == "__main__":
    foods = ["Steak", "Pizza", "Icecream", "Soup"]
    for i in range(5):
        rev = get_review_for_food(
                random.choice(foods),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                True 
            )
        print(f'By \033[92m{rev.user_name}\033[00m:\n\t\033[94m{rev.review_text}\033[00m')

    for i in range(5):
        rev = get_review_for_food(
                random.choice(foods),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                False
            )
        print(f'By \033[92m{rev.user_name}\033[00m:\n\t\033[94m{rev.review_text}\033[00m')

