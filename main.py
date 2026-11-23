import tkinter as tk
from tkinter import messagebox
import os

TIME = 1
test_words = []
test = False
user_words = list()

#load words
with open(os.getcwd() + "\\words.txt", "r") as file:
    test_words = file.read().split(" ")

# Event listener no 1: Listen for the enter key to start the test
# run a test for 1 minutes first
def start_test(*args):
    global timer, wait, test
    test = True
    timer = window.after(1000 * 60 * TIME, check_result)
    update_timer(TIME * 60)

    for word in test_words:

        wait.set(False)
        words_canvas.itemconfig(typing_word, text=word)
        in_typed_word.wait_variable(wait)

        # collect the words that the user has entered into a list
        user_words.append(in_typed_word.get())
        in_typed_word.delete(0, tk.END)        

    window.after_cancel(timer)
    check_result()

def next_word(*args):
    global test, wait
    if test:
        # can only set wait to True if the test has started
        wait.set(True)

def check_result():
    global timer, test, time_display
    window.after_cancel(timer)
    window.after_cancel(time_display)

    valid_words = list()

    for word in user_words:
        clean_word = word.replace(" ", "")
        if clean_word in test_words:
            valid_words.append(clean_word)

    score = len(valid_words)

    test = False
    user_words.clear()

    messagebox.showinfo("Score", message=f"Your typing score is {score} WPM")

def update_timer(count):
    global time_display
    if count > 0:
        time_display = window.after(1000, update_timer, count-1)
        words_canvas.itemconfig(timer_count, text=f"0:{count}")


window = tk.Tk()
window.minsize(400, 400)
window.title("Typing test program")

banner = tk.Label(window, text="Type these words (Press enter to start):", font=("Arial", 12, "normal"))
banner.pack()

words_canvas = tk.Canvas(window, width=200, height=200)
words_canvas.pack()

typing_word = words_canvas.create_text(100, 50, text="Words to be type here", font=("Arial", 12, "italic"))
# Timer display onto canvas
timer_count = words_canvas.create_text(100, 150, text="1:00", font=("Arial", 12, "italic"))

in_typed_word = tk.Entry(window, width=50)
in_typed_word.pack()
in_typed_word.focus()

# Backend
wait = tk.BooleanVar(value=False)


# Listen for space to display next word
in_typed_word.bind("<space>", next_word)

# Listen for enter word when test is set to True
window.bind_all("<Return>", start_test)



window.mainloop()