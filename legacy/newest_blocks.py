import gradio as gr
from game import *
import numpy as np
import mediapipe as mp
import pickle

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
model = pickle.load(open("model.data", "rb"))

def detect_hands(image):
    """
    Usa o mediapipe para detectar mãos em uma foto.
    Retorna o resultado em objeto mediapipe.
    """
    with mp_hands.Hands(min_detection_confidence=0.6, static_image_mode=True, max_num_hands=1) as hands: 
        result = hands.process(image)
    return result


def result_to_vec(results):
    """
    Transforma o objeto de análise de mãos em vetor.
    Útil para treinar modelo sktlearn.
    """
    # verifica se não há mãos no reconhecimento
    if results.multi_hand_landmarks == None:
        raise gr.Error("Não foi encontrada uma mão, tente novamente")
    # se há, cria o vetor
    v = np.array([])
    for lm in results.multi_hand_landmarks[0].landmark:
        v = np.append(v, lm.x)
        v = np.append(v, lm.y)
        v = np.append(v, lm.z)
    
    return v


def num_to_let(num):
    """
    Converte a resposta em números do modelo treinado  
    para a respectiva letra.
    """
    trad = {
        0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j',
        10:'k',11:'l',12:'m',13:'n',14:'o',15:'p',16:'q',17:'r',18:'s',
        19:'t',20:'u',21:'v',22:'w',23:'x',24:'y',25:'z'
    }
    return trad[num]

def get_letter_from_image(image):
    """
    Detecta o símbolo de libras que aparece na imagem
    e retorna a letra a que ele corresponde.
    Recebe o caminho da imagem a ser analisada.
    """

    result = detect_hands(image)
    v = result_to_vec(result)
    return num_to_let(model.predict(v.reshape((1,-1)))[0])


class MyInterface:

    def __init__(self):

        # Interface variables:
        self.word = "abcde"
        self.basic_style = """
        <style>
            .mydiv {
            float:left;
            display:flex;
            justify-content: center;
            align-items: center;
            background-color: grey;
            width: 3em;
            height: 3em;
            margin: .5em;
            font-size: 40px;}

            .blue {
                background-color: gray;
            }

        </style>
        """

        # Initial function calls
        self.game = LearningToSpell()
        self.game.set_word(self.word)
        self.set_first_html()
    
    # Deprecated?
    # def update_status(self):
    #     status = self.game.get_current_state()
    #     self.word = status["word"]
    #     self.colors = status["colors"]
    #     self.current_letter_index = status["current_letter"]

    def input_img(self, img):
        """
        Receives an image, gets a letter from it and adds the letter to the game

        Parameters
        ----------
        img : ???
            Image inputed by the user
        
        Returns
        ----------
        html: str
            A string formatted as html to be rendered by gr.HTML
        """
        letter = get_letter_from_image(img) # translates the image into a letter
        self.input_letter(letter) # inputs the letter in the game, updating the interface html
        html = self.html # gets the interface html
        return html
    
    def set_first_html(self):
        """
        Loads the html when starting the app

        Parameters
        ----------
        None
        
        Returns
        ----------
        None
        """
        new_html = self.basic_style
        len_word = len(self.word)
        # self.update_status()
        for i in range(self.game.max_attempts):
            for j in range(len_word):
                new_html += f"""
                    <div class='mydiv' style='background-color:{self.game.colors[i][j]}; 
                    """

                if j==0:
                    new_html += f"""clear:both;"""
                    
                new_html += f""" '>
                    <p></p>
                    </div>
                    """
        
        self.html = new_html

    # Deprecated?
    # def input_letter(self, letter):
    #     """
    #     Inputs a letter as the next letter and updates it's own html
    #     If the letter was right, the html shows it and self.current_letter goes up by 1
    #     Else, the html shows the letter was wrond and self.current_letter stays the same        
    #     """
    #     new_html = self.basic_style
    #     self.game.try_word(letter)
    #     # self.update_status()
    #     len_word = len(self.word)
    #     for i in range(len_word):
    #         new_html += f"""
    #             <div class='mydiv' style='background-color:{self.game.colors[i][j]}; 
    #             """

    #         if i==len_word:
    #             new_html += f"""clear:both;"""

    #         new_html += f""" '>
    #             <p>{letter[i]}</p>
    #             </div>
    #             """
    #     self.html = new_html
    
    def add_letter(self, letter):
        """
        Adds a letter to the word currently being spelled by the user
        Once the word has enough letters, the word is sent to the game and checked

        Parameters
        ----------
        letter : str
            One single letter
        
        Returns
        ----------
        html: str
            A string formatted as html to be rendered by gr.HTML
        """
        # Updates the game, inputting the letter
        self.game.try_letter(letter)
        html = self.calculate_html()
        return html

    
    def calculate_html(self):
        new_html = self.basic_style # Declares the 'new_html' variable as the basic style of the interface
        len_word = len(self.word) # gets the len of the word to be guessed

        # Builds the output html
        for i in range(self.game.max_attempts): # For every attempt the player may have
                                                # (can be thought of as 'for word in self.game.player_attempts')
            
            # Sets the current word, to be printed
            if i==self.game.current_attempt:
                curr_word = self.game.current_word
            else:
                curr_word = self.game.player_attempts[i]
            len_curr_word = len(curr_word)

            for j in range(len_word):   # Repeats for the size of the word to be guessed
                # Creates the div with appropriate color
                new_html += f"""
                    <div class='mydiv' style='background-color:{self.game.colors[i][j]}; 
                    """

                # If it's the selected letter slot, give it a border
                if j==self.game.current_letter and i==self.game.current_attempt:
                    new_html += "border-style: solid; border-width:5px; border-color:yellow;"

                # If it's the first letter, make it so it's also a new line
                if j==0:
                    new_html += "clear:both;"

                # Adds the content of the div ('<p>letter</p>') and closes the div
                new_html += f""" '>
                    <p>{curr_word[j] if j<len_curr_word else ''}</p>
                    </div>
                    """
                    
        # 'debugging'
        # print(new_html)

        # Sets the html of the interface as the 'new_html' variable
        self.html = new_html

        return new_html

    def try_image(self, image):
        """
        Receives an image, translates it to a letter and inputs it into the game

        Parameters
        ----------
        image : ???
            Image inputed by the user
        
        Returns
        ----------
        html : html to be rendered by a gr.HTML object
        """
        letter = get_letter_from_image(image) # gets a letter from the image
        html = self.add_letter(letter) # adds the letter to the game, getting back the output html

        return html
    
    def submit_word(self):
        if len(self.game.current_word) == len(self.game.word):
            self.game.submit_word()
            html = self.calculate_html()
        else:
            raise gr.Error("Palavra inválida")
        return html
    
    def move_left(self):
        self.game.move_pointer(-1)
        html = self.calculate_html()
        return html
    
    def move_right(self):
        self.game.move_pointer(1)
        html = self.calculate_html()
        return html


with gr.Blocks() as app:
    # Instanciates the MyInterface object, which will take care of the html output
    my_interface = MyInterface()

    # Creates the gr.HTML element that will output most of the game interface
    # (Doesn't output the webcam or button parts)
    html = gr.HTML(value = my_interface.html)
    
    # gr.Text element used to see elements as text when debugging
    # text = gr.Textbox(label="Palavra")

    # Creates a gr.Row, where the webcam is located
    with gr.Row():
        gr.Image() # todo: remove this line
        # Creates the webcam object, which will input images into the game
        # 'streaming = True' means that the webcam content is live streamed to the frontend
        #   so the user can see themselves
        # 'mirror_webcam = True' flips the image horizontally for a better experience
        webcam = gr.Image(source = "webcam", streaming = True, mirror_webcam = True)
        gr.Image() # todo: remove this line
    
    # Create the buttons for the user to 
    with gr.Row():
        left = gr.Button(value="Mover para a esquerda")
        with gr.Column():
            add = gr.Button(value="Adcionar letra")
            submit = gr.Button(value="Enviar palavra")
        right = gr.Button(value="Mover para a direita")

    #button.click(fn=my_interface.input_img, inputs=text, outputs=html)
    # button.click(fn=draw_landmarks, inpu ts=webcam, outputs=hand )
    add.click(fn=my_interface.try_image, inputs=webcam, outputs=html)
    submit.click(fn=my_interface.submit_word, inputs=None, outputs=html)
    left.click(fn=my_interface.move_left, inputs=None, outputs=html)
    right.click(fn=my_interface.move_right, inputs=None, outputs=html)

app.launch()