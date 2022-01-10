from tkinter import *
import random
import pandas
from pandas import *


# Flash card game, It shows a random word in french and you need to guess it,
# if you get it right, click the Known button(green), if you got it wrong the Unknown button(red).

# ALERT
# Right know there is a bug, if you empty the words_to_learn.csv it can´t read it, so you need to delete manually.

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

current_card = {}

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    global flip_timer
    try:
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    except IndexError:
        window.after_cancel(flip_timer)
        canvas.itemconfig(card_title, text="", )
        canvas.itemconfig(card_word, text="Game finished", fill="white")
        canvas.itemconfig(card_background, image=card_back_img)


# Visual code

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3)

# Unknown button code, in case you don´t know the word
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

# Known button code, if you know the word
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=2)

next_card()

window.mainloop()



