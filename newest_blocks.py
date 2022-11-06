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
    v = [(lm.x, lm.y, lm.z) for lm in results.multi_hand_landmarks[0].landmark]
    return np.array(v).reshape(1, -1)


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

    return num_to_let(model.predict(v)[0])
    

class MyInterface:

    def __init__(self):

        # Interface variables:
        self.word = "abcde"
        self.game = LearningToSpell()
        self.game.set_word(self.word)
        self.set_first_html()

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
        len_word = len(self.word)
        # Subtracts the spaces between letters and gets
        # the total space each one will occupy
        margin = max(0, 40 - 4 * len_word)
        square_size = (100 - len_word + 1) / len_word
        new_html = f"""<style>
        .mydiv {{
            width: {square_size}%;
        }}

        .letters {{
            margin: 0 {margin}%;
        }}
        </style>
        <div class='letters'>
        """
        # self.update_status()
        for i in range(self.game.max_attempts):
            for j in range(len_word):
                new_html += f"""
                    <div class='mydiv' style='background-color:{self.game.colors[i][j]}; 
                    """

                if j == len_word:
                    new_html += f"clear: both;"
                    
                new_html += f""" '>
                    <p></p>
                    </div>
                    """
        self.html = new_html + "</div>"

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
        # Preparation
        new_html = self.basic_style # Declares the 'new_html' variable as the basic style of the interface
        len_word = len(self.word) # gets the len of the word to be guessed

        # 'debugging'
        print(f"Colors: {self.game.colors}")

        # Updates the game, inputting the letter
        self.game.try_letter(letter)

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

                if j==0:
                    new_html += f"""clear:both;"""

                # Adds the content of the div ('<p>letter</p>') and closes the div
                new_html += f""" '>
                    <p>{curr_word[j] if j<len_curr_word else ''}</p>
                    </div>
                    """
                    
            # print(new_html)
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


css = """
.letters {
    display: flex;
}

.mydiv {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: gray;
    margin: 0 1%;
    aspect-ratio: 1 / 1;
}

.blue {
    background-color: gray;
}

#webcam {
    aspect-ratio: 4 / 3;
}
"""

with gr.Blocks() as app:
    my_interface = MyInterface()
    html = gr.HTML(value = my_interface.html)
    text = gr.Textbox(label="Palavra")
    with gr.Row():
        gr.Image() # todo: remove this line
        # Creates the webcam object, which will input images into the game
        # 'streaming = True' means that the webcam content is live streamed to the frontend
        #   so the user can see themselves
        # 'mirror_webcam = True' flips the image horizontally for a better experience
        webcam = gr.Image(source = "webcam", streaming = True, mirror_webcam = True)
        gr.Image() # todo: remove this line
    
    # Create the buttons for the user to 
    add = gr.Button(value="Adcionar letra")
    submit = gr.Button(value="Enviar palavra")

app.launch()
