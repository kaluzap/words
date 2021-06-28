import argparse
import pandas as pd
from numpy import random
from tkinter import *
from PIL import Image, ImageTk
from gtts import gTTS
import os
import matplotlib.pyplot as plt

TARGET_LANGUAGE = "de"  # language for dialog controls and sound

df_dictionary = pd.DataFrame()

message_status = {"correct": "richtig!!", "wrong": "falsch!!"}

gender_color = {"m": "red", "f": "blue", "n": "green", "p": "dark orange"}

article_texts = {"m": "der", "f": "die", "n": "das", "p": "die"}

data_file_name = ""

button_properties = {
    "data": {"text": "daten", "font": "Verdana 10 bold", "fg": "black", "width": 7},
    "article_m": {
        "text": "der",
        "font": "Verdana 10 bold",
        "fg": gender_color["m"],
        "width": 7,
    },
    "article_f": {
        "text": "die",
        "font": "Verdana 10 bold",
        "fg": gender_color["f"],
        "width": 7,
    },
    "article_n": {
        "text": "das",
        "font": "Verdana 10 bold",
        "fg": gender_color["n"],
        "width": 7,
    },
    "article_p": {
        "text": "die (pl)",
        "font": "Verdana 10 bold",
        "fg": gender_color["p"],
        "width": 7,
    },
    "sound": {"text": "hören", "font": "Verdana 10 bold", "fg": "black", "width": 7},
    "next": {"text": "nächste", "font": "Verdana 10 bold", "fg": "black", "width": 7},
}

label_properties = {
    "label_status": {"text": "status", "font": "Verdana 10 bold", "fg": "black"},
    "label_word": {"text": "Word", "font": "Verdana 20 bold", "fg": "black"},
    "label_translation": {
        "text": "translation",
        "font": "Verdana 10 bold",
        "fg": "gray35",
    },
    "label_full_data": {"text": "full data", "font": "Verdana 12 bold", "fg": "green"},
    "label_points": {
        "text": "points",
        "font": "Verdana 8 bold",
        "fg": "black",
        "justify": "left",
    },
}


class Window(Frame):
    def __init__(self, master=None):

        # state variables
        self.active_word = ""
        self.active_case = ""
        self.text_to_speak = ""
        self.count_good = 0
        self.count_total_clicks = 0
        self.count_total_words = 0
        self.already_tested = False
        self.allow_repetitions = IntVar()
        self.success_streak = 0
        self.success_streak_record = 0
        self.success_streak_history = []
        self.create_figure()

        # starting a word
        self.set_new_active_word_and_case()

        # Windows
        Frame.__init__(self, master)
        self.master = master

        # subframe for texts
        self.frame_texts = Frame(self.master)
        self.frame_texts.pack(side="top", padx="5", pady="5")

        self.label_status = Label(
            master=self.frame_texts, **label_properties["label_status"]
        )
        self.label_status.pack(side=TOP, padx="5", pady="5")

        self.label_word = Label(
            master=self.frame_texts, **label_properties["label_word"]
        )
        self.label_word.pack(side=TOP, padx="5", pady="5")

        self.label_translation = Label(
            master=self.frame_texts, **label_properties["label_translation"]
        )
        self.label_translation.pack(side=TOP, padx="5", pady="5")

        self.label_full_data = Label(
            master=self.frame_texts, **label_properties["label_full_data"]
        )
        self.label_full_data.pack(side=TOP, padx="5", pady="5")

        self.label_points = Label(
            master=self.frame_texts, **label_properties["label_points"]
        )
        self.label_points.pack(side=TOP, padx="5", pady="5")

        load = Image.open("success_streak.png")
        render = ImageTk.PhotoImage(load)
        self.img = Label(master=self.frame_texts, image=render)
        self.img.image = render
        self.img.pack(side=TOP, padx="5", pady="5")

        # subframe for article buttons
        self.frame_button_articles = Frame(self.master)
        self.frame_button_articles.pack(side="top", padx="5", pady="5")

        self.mButton = Button(
            master=self.frame_button_articles,
            command=self.clickmButton,
            **button_properties["article_m"],
        )
        self.mButton.pack(side=LEFT, padx="5")

        self.fButton = Button(
            master=self.frame_button_articles,
            command=self.clickfButton,
            **button_properties["article_f"],
        )
        self.fButton.pack(side=LEFT, padx="5")

        self.nButton = Button(
            master=self.frame_button_articles,
            command=self.clicknButton,
            **button_properties["article_n"],
        )
        self.nButton.pack(side=LEFT, padx="5")

        self.pButton = Button(
            master=self.frame_button_articles,
            command=self.clickpButton,
            **button_properties["article_p"],
        )
        self.pButton.pack(side=LEFT, padx="5")

        # subframe for functions buttons
        self.frame_button_functions = Frame(self.master)
        self.frame_button_functions.pack(side="top", padx="5", pady="5")

        self.CheckbuttonRepetitions = Checkbutton(
            master=self.frame_button_functions,
            text="Allow repetitions",
            variable=self.allow_repetitions,
        )
        self.CheckbuttonRepetitions.pack(side=LEFT, padx="5")

        self.dataButton = Button(
            master=self.frame_button_functions,
            command=self.clickDataButton,
            **button_properties["data"],
        )
        self.dataButton.pack(side=LEFT, padx="5")

        self.soundButton = Button(
            master=self.frame_button_functions,
            command=self.clickSoundButton,
            **button_properties["sound"],
        )
        self.soundButton.pack(side=LEFT, padx="5")

        self.nextButton = Button(
            master=self.frame_button_functions,
            command=self.clickNextButton,
            state=DISABLED,
            **button_properties["next"],
        )
        self.nextButton.pack(side=LEFT, padx="5")

    def set_new_active_word_and_case(self):
        global df_dictionary
        try:
            df_sample = df_dictionary.sample()
        except ValueError as err:
            print("No hay mas palabras!!!")
            return self.active_word, self.active_case

        self.active_word = df_sample.iloc[0].to_dict()
        if not self.allow_repetitions.get():
            df_dictionary = df_dictionary.drop(df_sample.index)
            print(f"There are {df_dictionary.shape[0]} words left.")

        self.active_case = random_case()
        if (self.active_word["plural"] == "-") and (self.active_case == "p"):
            self.active_case = "s"
        if self.active_word["singular"] == self.active_word["plural"]:
            self.active_case = "sp"
        if self.active_word["singular"] == "-":
            self.active_case = "p"

        if self.active_case == "s":
            self.text_to_speak = self.active_word["singular"]
        else:
            self.text_to_speak = self.active_word["plural"]

        label_properties["label_status"]["text"] = " "
        if self.active_case == "s":
            label_properties["label_word"]["text"] = self.active_word["singular"]
        else:
            label_properties["label_word"]["text"] = self.active_word["plural"]
        label_properties["label_translation"][
            "text"
        ] = f"({self.active_word['translation']})"
        label_properties["label_full_data"]["text"] = " "
        label_properties["label_points"]["text"] = self.count_statistics()

    def count_statistics(self):
        line = ""
        if not self.count_total_words:
            ratio_success = 0
        else:
            ratio_success = self.count_good / self.count_total_words
        line = f"Ratio success: {self.count_good}/{self.count_total_words} = {ratio_success:.5f}"
        if ratio_success > 0.9:
            line += "    :)\n"
        else:
            line += "    :(\n"

        if not self.count_total_clicks:
            ratio_attempts = 0
        else:
            ratio_attempts = self.count_good / self.count_total_clicks
        line += f"Ratio attempts: {self.count_good}/{self.count_total_clicks} = {ratio_attempts:.5f}"
        if ratio_attempts > 0.9:
            line += "    :)\n"
        else:
            line += "    :(\n"

        line += f"Success streak: {self.success_streak} ({self.success_streak_record})"

        return line

    def update_labels(self):
        self.label_status["text"] = label_properties["label_status"]["text"]
        self.label_word["text"] = label_properties["label_word"]["text"]
        self.label_word["fg"] = label_properties["label_word"]["fg"]
        self.label_translation["text"] = label_properties["label_translation"]["text"]
        self.label_full_data["text"] = label_properties["label_full_data"]["text"]
        self.label_full_data["fg"] = label_properties["label_full_data"]["fg"]
        self.label_points["text"] = label_properties["label_points"]["text"]
        img2 = ImageTk.PhotoImage(Image.open("success_streak.png"))
        self.img.configure(image=img2)
        self.img.image = img2

    def disable_next_button(self):
        self.nextButton["state"] = DISABLED

    def enable_next_button(self):
        self.nextButton["state"] = NORMAL

    def disable_article_buttons(self):
        self.mButton["state"] = DISABLED
        self.fButton["state"] = DISABLED
        self.nButton["state"] = DISABLED
        self.pButton["state"] = DISABLED

    def enable_article_buttons(self):
        self.mButton["state"] = NORMAL
        self.fButton["state"] = NORMAL
        self.nButton["state"] = NORMAL
        self.pButton["state"] = NORMAL

    def create_string_result(self):
        text = ""
        if self.active_word["singular"] == "-":
            text += "[ohne s.], "
        else:
            if "m" in self.active_word["gender"]:
                text += article_texts["m"] + " "
            if "f" in self.active_word["gender"]:
                text += article_texts["f"] + " "
            if "n" in self.active_word["gender"]:
                text += article_texts["n"] + " "
            text += self.active_word["singular"] + ", "

        if self.active_word["plural"] == "-":
            text += "[ohne pl.]"
        else:
            text += f"{article_texts['p']} {self.active_word['plural']}"
        self.text_to_speak = text
        return text

    def run_button_gender(self, gender):
        self.count_total_clicks += 1
        if self.test_word(gender):
            if not self.already_tested:
                self.count_good += 1
                self.success_streak += 1
            self.disable_article_buttons()
            self.enable_next_button()
            self.count_total_words += 1
            if self.success_streak_record < self.success_streak:
                self.success_streak_record = self.success_streak
            label_properties["label_status"]["text"] = message_status["correct"]
            label_properties["label_word"]["fg"] = gender_color[gender]
            label_properties["label_full_data"]["text"] = self.create_string_result()
            label_properties["label_full_data"]["fg"] = gender_color[gender]
        else:
            label_properties["label_status"]["text"] = message_status["wrong"]
            self.success_streak_history.append(self.success_streak)
            self.create_figure()
            self.success_streak = 0
        label_properties["label_points"]["text"] = self.count_statistics()
        self.already_tested = True
        self.update_labels()

    def create_figure(self):
        plt.rcParams["figure.figsize"] = (4.5, 1.5)
        plt.ylabel("Times", fontsize=8)
        plt.xlabel("Success Streak", fontsize=8)
        plt.rc("xtick", labelsize=6)
        plt.rc("ytick", labelsize=6)
        plt.xticks(range(0, self.success_streak_record + 1))
        if len(self.success_streak_history) != 0:
            plt.yticks(range(0, max(self.success_streak_history) + 1))
        else:
            plt.yticks(range(0, 1))
        plt.hist(
            self.success_streak_history,
            bins=self.success_streak_record + 1,
            range=(-0.5, self.success_streak_record + 0.5),
        )
        plt.savefig("success_streak.png", bbox_inches="tight")
        plt.clf()
        plt.close("all")

    def test_word(self, gender):
        if ("s" in self.active_case) and (gender in self.active_word["gender"]):
            return True
        if gender in self.active_case:
            return True
        return False

    def clickmButton(self):
        self.run_button_gender("m")

    def clickfButton(self):
        self.run_button_gender("f")

    def clicknButton(self):
        self.run_button_gender("n")

    def clickpButton(self):
        self.run_button_gender("p")

    def clickDataButton(self):
        global df_dictionary
        df_dictionary = pd.read_csv(data_file_name)
        print(f"Restarting dictionary. There are {df_dictionary.shape[0]} words.")

    def clickSoundButton(self):
        self.text_to_speak = self.text_to_speak.replace("[ohne pl.]", "")
        self.text_to_speak = self.text_to_speak.replace("[ohne s.], ", "")
        speech = gTTS(self.text_to_speak, lang=TARGET_LANGUAGE, slow=False)
        speech.save("text.mp3")
        os.system("mplayer text.mp3")

    def clickNextButton(self):
        self.set_new_active_word_and_case()
        label_properties["label_word"]["fg"] = "black"
        self.update_labels()
        self.enable_article_buttons()
        self.disable_next_button()
        self.already_tested = False


def random_case() -> str:
    x = random.rand()
    if x < 0.75:
        return "s"
    return "p"


def main():

    # load dictionary
    global df_dictionary
    try:
        df_dictionary = pd.read_csv(data_file_name)
    except:
        print(f'I cannot open the file "{data_file_name}"')
        return
    print(df_dictionary.head())

    # initialize tkinter
    root = Tk()
    app = Window(root)
    root.wm_title("WORDS!")
    root.geometry("500x500")
    root.mainloop()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Words", epilog="Example: python words.py -fd data_nouns_ge_sp.csv",
    )

    parser.add_argument(
        "--target_language",
        "-tl",
        required=False,
        type=str,
        default="de",
        help=f"Target language for the dialog control and sound (default 'de')",
    )

    parser.add_argument(
        "--file_dictionary",
        "-fd",
        required=True,
        type=str,
        help=f"File with the dictionary",
    )

    args = parser.parse_args()
    data_file_name = args.file_dictionary
    TARGET_LANGUAGE = args.target_language
    main()
