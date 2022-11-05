import gradio as gr


def img_to_letter(img):
    return "a"

class MyInterface:

    def __init__(self):
        self.word = "abcde"
        self.colors = ["grey" if i>0 else "blue" for i in range(len(self.word))]
        self.images = ["" for _ in range(len(self.word))]
        self.current_letter_index = 0
        self.font_size = 40 # font size in px
        self.set_first_html()
    
    def input_img(self, img):
        letter = img_to_letter(img)
        self.__input_letter(letter)
        return self.html
    
    def set_first_html(self):
        new_html = f"""
        <style>
            .mydiv {{
            float:left;
            display:flex;
            justify-content: center;
            align-items: center;
            background-color: gray;
            width: 3em;
            height: 3em;
            margin: .5em;
            font-size: 40px;}}

            .blue {{
                background-color: gray;
            }}

        </style>
        """
        for i in range(len(self.word)):
            if i==len(self.word):
                new_html += f"""
                <div class='mydiv' style='background-color:{self.colors[i]}; clear:both;'>
                <p>{self.word[i]}</p>
                </div>
                """     
            new_html += f"""
            <div class='mydiv' style='background-color:{self.colors[i]};'>
            <p>{self.word[i]}</p>
            </div>
            """
        self.html = new_html

    def input_letter(self, letter):
        """
        Inputs a letter as the next letter and updates it's own html
        If the letter was right, the html shows it and self.current_letter goes up by 1
        Else, the html shows the letter was wrond and self.current_letter stays the same        
        """
        if letter == self.word[self.current_letter_index]:
            self.colors[self.current_letter_index] = 'green'
            self.current_letter_index += 1
            if self.current_letter_index<len(self.word):
                self.colors[self.current_letter_index] = 'blue'
        else:
            self.colors[self.current_letter_index] = 'red'
        new_html = f"""
        <style>
            div {{
            float:left;
            display:flex;
            justify-content: center;
            align-items: center;
            background-color: gray;
            width: 3em;
            height: 3em;
            margin: .5em;
            font-size: 40px;}}

        </style>
        """
        for i in range(len(self.word)):
            if i==len(self.word)-1:
                new_html += f"""
                <div style='color:{self.colors[i]}; clear:both;''>
                <p>{self.word[i]}</p>
                </div>
                """     
            new_html += f"""
            <div style='color:{self.colors[i]};>
            <p>{self.word[i]}</p>
            </div>
            """
        print(new_html)
        self.html = new_html

with gr.Blocks() as app:
    my_interface = MyInterface()
    html = gr.HTML(value = my_interface.html)
    text = gr.Textbox(label="Palavra")
    button = gr.Button(value="Enviar")

    button.click(fn=my_interface.input_letter, inputs=text, outputs=html)

app.launch()