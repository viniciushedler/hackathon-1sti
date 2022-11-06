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
        len_word = len(self.word) # gets the length of the word to be guessed
        # Subtracts the spaces between letters and gets
        # the total space each one will occupy
        margin = max(0, 40 - 4 * len_word)
        square_size = (100 - len_word + 1) / len_word
        self.html = f"""<style>
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
        for i in range(self.game.max_attempts): # For every attempt the player may have
                                                # (can be thought of as 'for word in self.game.player_attempts')
            for j in range(len_word):   # Repeats for the size of the word to be guessed
                # Creates the div with appropriate color
                self.html += f"""
                    <div class='mydiv' style='background-color:{self.game.colors[i][j]}; 
                    """

                # If it's the first letter, make it so it's also a new line
                if j == 0:
                    self.html += f"clear: both;"
                
                # Adds the content of the div ('<p>letter</p>') and closes the div
                self.html += f""" '>
                    <p></p>
                    </div>
                    """
        self.html += "</div>"

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
        len_word = len(self.word) # gets the length of the word to be guessed
        # Subtracts the spaces between letters and gets
        # the total space each one will occupy
        margin = max(0, 40 - 4 * len_word)
        square_size = (100 - len_word + 1) / len_word
        # Starts to redefine the HTML as the basic style of the interface
        self.html = f"""<style>
        .letters {{
            margin: 0 {margin}%;
        }}

        .mydiv {{
            width: {square_size}%;
        }}
        </style>
        <div class='letters'>
        """

        # 'debugging'
        print(f"Colors: {self.game.colors}")

        # Updates the game, inputting the letter
        self.game.try_letter(letter)

        # Builds the output html
        for i in range(self.game.max_attempts): # For every attempt the player may have
                                                # (can be thought of as 'for word in self.game.player_attempts')
            
            # Sets the current word, to be printed
            if i == self.game.current_attempt:
                curr_word = self.game.current_word
            else:
                curr_word = self.game.player_attempts[i]
            len_curr_word = len(curr_word)

            for j in range(len_word):   # Repeats for the size of the word to be guessed
                # Creates the div with appropriate color
                self.html += f"""
                    <div class='mydiv' style='background-color:{self.game.colors[i][j]}; 
                    """

                # If it's the first letter, make it so it's also a new line
                if j == 0:
                    self.html += f"clear:both;"

                # Adds the content of the div ('<p>letter</p>') and closes the div
                self.html += f""" '>
                    <p>{curr_word[j] if j<len_curr_word else ''}</p>
                    </div>
                    """
                    
        # 'debugging'
        # print(self.html)

        self.html += "</div>"

        return self.html
    
    def try_image(self, image):
        """
        Receives an image, translates it to a letter and inputs it into the game

        Parameters
        ----------
        image : np.ndarray of shape (height, width, 3)
            Image inputted by the user
        
        Returns
        ----------
        html : html to be rendered by a gr.HTML object
        """
        letter = get_letter_from_image(image) # gets a letter from the image
        self.html = self.add_letter(letter) # adds the letter to the game, getting back the output html

        return self.html


css = """
.letters {
    display: flex;
    height: 100%;
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

with gr.Blocks() as demo:
    my_interface = MyInterface()

    # Creates the gr.HTML element that will output most of the game interface
    # (Doesn't output the webcam or button parts)
    html = gr.HTML(value=my_interface.html)
    with gr.Row():
        # Creates the webcam object, which will input images into the game
        # 'streaming = True' means that the webcam content is live streamed to the frontend
        #   so the user can see themselves
        # 'mirror_webcam = True' flips the image horizontally for a better experience
        gr.Markdown("")
        webcam = gr.Image(source="webcam", streaming=True, mirror_webcam=True, elem_id="webcam")
        gr.Markdown("")

    # Create the buttons for the user to interact with the game
    add = gr.Button(value="Adicionar letra")
    submit = gr.Button(value="Enviar palavra")
    submit.click(fn=my_interface.try_image, inputs=webcam, outputs=html)
    add.click(fn=my_interface.add_letter, inputs=webcam, outputs=html)

demo.launch(server_port=8080)
