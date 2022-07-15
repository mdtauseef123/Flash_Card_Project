from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"


# ---------------------------- READING DATA FROM THE FILE------------------------------- #
#For the very first time file words_to_learn.csv is not created, so we will fetch data from original csv file i.e.
#french_words.csv. As the updated data is in the words_to_learn.csv file.
try:
    words_data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    words_data = pandas.read_csv("./data/french_words.csv")
#By making orient="records"
#It will convert our csv file to list of dictionary like [{column -> value}, … , {column -> value}]
#In our case [{'French': 'partie', 'English': 'part'}, {'French': 'histoire', 'English': 'history'},......]
words_list = words_data.to_dict(orient="records")
current_card = {}

# ---------------------------- DISPLAYING ENGLISH TRANSLATION------------------------------- #


def flip_card():
    """
    The flip_card() will set the different background image, and it will show English translation of the given French
    word in white font.
    """
    canvas.itemconfig(card_background, image=back_img)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=current_card["English"])

# ---------------------------- DISPLAYING NEXT CARD ------------------------------- #


"""
Now one of the bugs we might have encountered is if we clicked this button many times and we go through lots of 
different words,you see immediately, that card actually flipped.And it's because that window after three seconds is 
counting down in the background, waiting, waiting, until three seconds at which point it's going to flip the card.
It doesn't care that we've actually just gone onto a new card and we want to wait again, three seconds due to this
it will show the wrong translation and not what we expect infact it will show the translation of very first word when
we start clicking on it. 
In order to get this to work, we will use after_cancel() which will stop the previous timer until we fully wait for 
3 seconds for a particular French word.
Now It's not going to flip until we land on a card and wait for three seconds before it flips.
"""


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_list)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_title, fill="black", text="French")
    canvas.itemconfig(card_word, fill="black", text=current_card["French"])
    #The aim of the project is that it will show the French word then wait for 3 second and then call flip_card function
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------- CARD KNOWN ------------------------------- #

def card_known():
    words_list.remove(current_card)
    words_to_learn_data = pandas.DataFrame(words_list)
    """
    If the user knows the word in the card then it should remove that word from the list and then add the remaining 
    words into the new csv file words_to_learn so that next time the data will be read from the words_to_learn file
    instead of reading from french_words.csv.
    Also we have put the index=False which means that everytime the user opt for known button then data frame will be
    created thereby adding indexing everytime which makes the structure of the file very bad and hence in order to avoid
    these we use index=False attribute.
    """
    words_to_learn_data.to_csv("./data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
#Note if we create object of PhotoImage() inside any function then it will not work because at the end of the function
#the reference to that particular image will lost and hence it will not work.
back_img = PhotoImage(file="./images/card_back.png")
card_front_img = PhotoImage(file="./images/card_front.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150,  text="Title", fill="black", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263,  text="word", fill="black", font=(FONT_NAME, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

#We can also set images to the button
"""
The aim of this project is that when the user click the right button it means that the user know the meaning of that
word and if the the user click the cross button it means the user doesn't know the meaning of that particular word
so we will not removing that word from the list.
"""
unknown_img = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=unknown_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)
known_img = PhotoImage(file="./images/right.png")
known_button = Button(image=known_img, highlightthickness=0, command=card_known)
known_button.grid(row=1, column=1)

#Because initially the screen is showing title and word on the canvas which makes it little weird so before the user
#generates the new word we will pop the screen with title set to French and a random generated word.
next_card()

window.mainloop()
