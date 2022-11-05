import gradio as gr
from game import *


def img_to_letter(img):
    return img

class MyInterface:

    def __init__(self):
        self.word = "abcde"
        self.game = LearningToSpell()
        self.game.set_word(self.word)
        self.colors = ["grey" if i>0 else "blue" for i in range(len(self.word))]
        self.images = ["" for _ in range(len(self.word))]
        self.current_letter_index = 0
        self.font_size = 40 # font size in px
        self.basic_style = """
        <style>
            .mydiv {
            float:left;
            display:flex;
            justify-content: center;
            align-items: center;
            background-color: gray;
            width: 3em;
            height: 3em;
            margin: .5em;
            font-size: 40px;}

            .blue {
                background-color: gray;
            }

        </style>
        """
        self.set_first_html()
    
    def update_status(self):
        status = self.game.get_current_state()
        self.word = status["word"]
        self.colors = status["colors"]
        self.current_letter_index = status["current_letter"]

    def input_img(self, img):
        letter = img_to_letter(img)
        self.input_letter(letter)
        html = self.html
        return html
    
    def set_first_html(self):
        new_html = self.basic_style
        len_word = len(self.word)
        # self.update_status()
        for i in range(len_word):
            new_html += f"""
                <div class='mydiv' style='background-color:{self.game.colors[i]}; 
                """

            if i==len_word:
                new_html += f"""clear:both;"""
                
            new_html += f""" '>
                <p>{self.game.word[i]}</p>
                </div>
                """
        self.html = new_html

    def input_letter(self, letter):
        """
        Inputs a letter as the next letter and updates it's own html
        If the letter was right, the html shows it and self.current_letter goes up by 1
        Else, the html shows the letter was wrond and self.current_letter stays the same        
        """
        # if letter == self.word[self.current_letter_index]:
        #     self.colors[self.current_letter_index] = 'green'
        #     self.current_letter_index += 1
        #     if self.current_letter_index<len(self.word):
        #         self.colors[self.current_letter_index] = 'blue'
        # else:
        #     self.colors[self.current_letter_index] = 'red'
        new_html = self.basic_style
        self.game.try_word(letter)
        # self.update_status()
        len_word = len(self.word)
        for i in range(len_word):
            new_html += f"""
                <div class='mydiv' style='background-color:{self.game.colors[i]}; 
                """

            if i==len_word:
                new_html += f"""clear:both;"""

            new_html += f""" '>
                <p>{letter[i]}</p>
                </div>
                """
        # print(new_html)
        self.html = new_html

with gr.Blocks() as app:
    my_interface = MyInterface()
    html = gr.HTML(value = my_interface.html)
    text = gr.Textbox(label="Palavra")
    button = gr.Button(value="Enviar")

    button.click(fn=my_interface.input_img, inputs=text, outputs=html)

app.launch()