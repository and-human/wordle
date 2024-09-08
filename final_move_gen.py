import random

# TODO rather generate a random seed and print the seed so we can verify the word later.
# TODO debugging checks must be added.
# TODO input validation is done in movegen? or elsewhere?
# TODO use either uppercase or lowercase for all words.
# TODO discuss variation with Anshuman.
# TODO customization code
# TODO there needs to be dictionary of positions explored and unexplored. #Three dictionaries for black, green, and yellow.

# TODO while repeating the process, it should not even bother about the green words, and check everything but that as it will be much faster.
# random.seed(0)
# __word_list__ = [i.upper() for i in ["apple", "brick", "chair", "drive", "eagle", "flour", "giant", "horse", "ideal", "jolly",
#     "knack", "lemon", "mirth", "nifty", "ozone", "pulse", "quill", "raise", "shiny", "trade",
#     "unity", "vivid", "world", "xylen", "yeast", "zebra", "angel", "blaze", "crown", "depth",
#     "elbow", "frost", "grace", "human", "ivory", "jelly", "karma", "loyal", "music", "north",
#     "opera","lasso"]]

# read this and extract a word wordle-main/words/word_bank_5.txt
__word_list__ = []
with open("wordle-main/words/word_bank_5.txt", "r") as f:
        for line in f:
            __word_list__.append(line.strip().upper())

# __word_list__ = ['APPLE', 'BRICK', 'YEAST', 'BLAZE', 'KAREN', "CEAST"]
word_search_space = __word_list__.copy()
print(word_search_space)

# CHALLENGE_WORD = random.choice(__word_list__).upper()
CHALLENGE_WORD = "YEAST"

print(CHALLENGE_WORD)

# make a dictionary of this challenge word
LETTER_COUNT = {}
for character in set(CHALLENGE_WORD):
    LETTER_COUNT[character] = CHALLENGE_WORD.count(character)


EXPLORED_POISITIONS = {}
for character in CHALLENGE_WORD:
    EXPLORED_POISITIONS[character] = [] 

GREEN_ACHIEVED = {}
for character in set(CHALLENGE_WORD):
    GREEN_ACHIEVED[character] = 0

BLACK_LETTERS = []


def goal_test(word:str, challenge_word = CHALLENGE_WORD) -> bool:
    """ 
    Takes as input a word string and returns True if the word is the challenge word.
    Can be accomodated to include number of steps.
    """
    return word.upper() == challenge_word

def goal_test_2(word:str, challenge_word = CHALLENGE_WORD) -> bool:
    """ 
    Takes as input a word string and returns True if the word is the challenge word.
    Can be accomodated to include number of steps.
    """
    for i in range(len(word)):
        if word[i] != challenge_word[i]:
            return False
    return True


def move_gen(word:str, 
             challenge_word:str = CHALLENGE_WORD, 
             black_letters:list = BLACK_LETTERS, 
             letter_count:dict = LETTER_COUNT, 
             explored_positions:dict[list] = EXPLORED_POISITIONS,
             green_achieved = GREEN_ACHIEVED,
             word_search_space:list[str] =  word_search_space) -> list:
    """
    Takes as input a word and returns a list of all possible words that are deemed valid for future attempts based on the following rules:
    1) If the entered word is the same as the challenge word, return an empty list.

    2)  GREEN: If any character in the entered word is in the correct position in the challenge word,
        then all returned words must have that character in the same position.

    2)  YELLOW: If the word has any character that is in the challenge word but NOT in the correct position, 
        then all the returned words must have that character in any other positon except
            (a) the current position of the character in the entered word
            (b) all explored incorrect positions of the character in the challenge word.
    
    3)  BLACK: If the word has any character that is not in the challenge word, 
        then all returned words must NOT have that character in any position.

    """
    word = word.upper()
    challenge_word = challenge_word.upper()
    # global word_search_space

    if word == challenge_word:
        return []
    
    new_black_letters = [i for i in set(word) if i not in set(challenge_word) and i not in black_letters]
    print("Black Letters: ")
    print(new_black_letters)
    
    black_letters.extend(new_black_letters)

    green_positions = []
    for i in range(len(word)):
        if word[i] == challenge_word[i]:
            green_positions.append(i)
            green_achieved[word[i]] += 1
            # explored_positions[word[i]].append(i)
    
    print("Green Positions: ")
    print(green_positions)

    # yellow_positions = []
    yellow_positions = []
    for i in range(len(word)):
        if word[i] in challenge_word and i not in green_positions and letter_count[word[i]] > (green_achieved[word[i]]):
            yellow_positions.append(i)
            explored_positions[word[i]].append(i)

    print("Yellow Positions: ")
    print(yellow_positions)
    
    # get me words where the green positions are maintained, and the yellow positions cannot be in the green ones and the explored ones

    for some_word in word_search_space[:]:
        removed = False
        for i in new_black_letters:
            if i in some_word:
                word_search_space.remove(some_word)
                removed = True
                break
        
        if removed:
            continue

        for i in green_positions:
            if word[i] != some_word[i]:
                word_search_space.remove(some_word)
                removed = True
                break
        

        if removed:
            continue

        for i in yellow_positions:
            # or ya and?
            # the first if condition basically has this hard rule that the yellow word must be there in another word
            if word[i] not in some_word or word[i] in (some_word[j] for j in explored_positions[word[i]]): #get words where it is not in the explored position
                word_search_space.remove(some_word)
                removed = True
                break
    
        
    return word_search_space

while True:
    word = input("Enter your word: ")
    if word == "exit":
        break

    next_word_search_space = move_gen(word.upper())
    if next_word_search_space == []:
        print("You have guessed the word!")
        break
    print("\nWord Search Space: ")
    print(len(next_word_search_space), next_word_search_space[:10])
    print()
    print()
