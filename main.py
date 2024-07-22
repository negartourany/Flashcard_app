from tkinter import *
import pandas
import random

# window config
windows = Tk()
windows.title("Flashcard App")
BACKGROUND_COLOR = "#B1DDC6"
windows.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
random_french = ""
random_english = ""
flip_timer = NONE
try:
    df = pandas.read_csv("to_learn_words")
except FileNotFoundError:
    test = pandas.read_csv("french_words.csv")
    df = pandas.DataFrame(test)
df_dic = df.to_dict(orient="records")
my_random = {}


# ----------------------------- Button functions -------------------------#

def update_canvas():
    global random_english
    random_english = (my_random["English"])
    canvas.itemconfig(flashcard_img, image=card_b_pic)
    canvas.itemconfig(card_title, fill="#ffffff", text="English")
    canvas.itemconfig(card_text, fill="#ffffff", text=random_english)


def next_card():
    global flip_timer
    global my_random
    global random_french
    # choosing a random word
    my_random = random.choice(df_dic)
    random_french = (my_random["French"])
    windows.after_cancel(flip_timer)
    canvas.itemconfig(flashcard_img, image=card_f_pic)
    canvas.itemconfig(card_title, fill="#000000", text="French")
    canvas.itemconfig(card_text, fill="#000000", text=random_french)
    flip_timer = windows.after(3000, update_canvas)


def is_known():
    df_dic.remove(my_random)
    data = pandas.DataFrame(df_dic)
    data.to_csv("to_learn_words", index=False)
    next_card()
    print(len(df_dic))


# ---------------------------- The timer section --------------------------------#

time_function = windows.after(3000, update_canvas)

# --------------------------------canvas -------------------------------------------#
# card front config
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_f_pic = PhotoImage(file="images/card_front.png")
card_b_pic = PhotoImage(file="images/card_back.png")
flashcard_img = canvas.create_image(400, 263, image=card_f_pic)
canvas.grid(row=0, column=0, columnspan=2)
# text
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(400, 253, text="", font=("Ariel", 60, "bold"))
# --------------------------- button config-----------------------------------------#
# wrong button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_image, command=next_card)
wrong_btn.grid(row=1, column=0)
# right button
right_image = PhotoImage(file="images/right.png")
right_btn = Button(image=right_image, command=is_known)
right_btn.grid(row=1, column=1)

# ---------------------------- importing the data ----------------------------#

next_card()
windows.mainloop()
