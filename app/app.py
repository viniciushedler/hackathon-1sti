import gradio as gr
from game import *
import numpy as np
import mediapipe as mp
import pickle
import secrets

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

def get_random_word():
    word_f_address = "new_valid_words.txt"
    with open(word_f_address, 'r') as f:
        word = secrets.choice(f.readlines())
        word = word[:-1]
    return word

class MyInterface:

    def __init__(self):

        # Interface variables:
        self.word = get_random_word()
        print(self.word)
        self.game = LearningToSpell()
        self.game.set_word(self.word)
        self.calculate_html()

    def reset(self):
        self.word = get_random_word()
        self.game = LearningToSpell()
        self.game.set_word(self.word)
        self.calculate_html()
        return self.html

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
        return self.html

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
        self.calculate_html()
        return self.html
    
    def calculate_html(self):
        len_word = len(self.word) # gets the length of the word to be guessed
        # Subtracts the spaces between letters and gets
        # the total space each one will occupy
        margin = max(0, 25 - 2.5 * len_word)
        square_size = (100 - len_word) / len_word
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

        # Builds the output html
        for i in range(self.game.max_attempts): # For every attempt the player may have
                                                # (can be thought of as 'for word in self.game.player_attempts')
            # Sets the current word, to be printed
            if i == self.game.current_attempt:
                curr_word = self.game.current_word
            else:
                curr_word = self.game.player_attempts[i]
            len_curr_word = len(curr_word)

            # self.html += "<br>"
            for j in range(len_word):   # Repeats for the size of the word to be guessed
                # Creates the div with appropriate color
                self.html += f"""
                    <div class='mydiv' style='background-color:{self.game.colors[i][j]};
                    """

                # If it's the first letter, make it so it's also a new line
                if j == 0:
                    self.html += "clear: both;"

                # If it's the selected letter slot, give it a border
                if j == self.game.current_letter and i == self.game.current_attempt:
                    self.html += "border-style: solid; border-width: 0.075em; border-color: yellow;"

                # Adds the content of the div ('<p>letter</p>') and closes the div
                self.html += f""" '>
                    <p>{curr_word[j].upper() if j < len_curr_word else ''}</p>
                    </div>
                    """

        self.html += "</div>"

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
        self.add_letter(letter) # adds the letter to the game, getting back the output html
        return self.html

    def submit_word(self):
        full = True
        for letter in self.game.current_word:
            if letter=='':
                full = False
        if full:
            self.game.submit_word()
            self.calculate_html()
        else:
            raise gr.Error("Palavra inválida.")
        return self.html
    
    def move_left(self):
        self.game.move_pointer(-1)
        self.calculate_html()
        return self.html
    
    def move_right(self):
        self.game.move_pointer(1)
        self.calculate_html()
        return self.html

    def check_win(self):
        if self.game.winner:
            return "<div class='message'>✨ Parabéns, você ganhou ✨</div>"
        else:
            return "<div class='message'>Bom jogo</div>"
        
    def get_word(self):
        return self.word

css = """
.mydiv {
    float: left;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: gray;
    font-size: 350%;
    margin: 0.5% 0.5%;
    aspect-ratio: 1 / 1;
}

.message {
    margin: 5% 5%;
    text-align: center;
    font-size: 350%;
    font-weight: 900;
}

#square-grid {
    align-self: center;
}

#webcam {
    aspect-ratio: 4 / 3;
}
"""

try:
    gr.close_all()
except:
    pass

with gr.Blocks(css=css) as demo:
    my_interface = MyInterface()

    # Creates the gr.HTML element that will output most of the game interface
    # (Doesn't output the webcam or button parts)
    answer = gr.HTML(my_interface.word)
    with gr.Row():
        # Creates the webcam object, which will input images into the game
        # 'streaming = True' means that the webcam content is live streamed to the frontend
        #   so the user can see themselves
        # 'mirror_webcam = True' flips the image horizontally for a better experience
        html = gr.HTML(value=my_interface.html, elem_id="square-grid")
        webcam = gr.Image(source="webcam", streaming=True, mirror_webcam=True, elem_id="webcam")

    with gr.Row():
        message = gr.HTML("<div class='message'>Bom jogo</div>")
    with gr.Row():
        # Creates empty fields for aesthetics and centering
        gr.Markdown("")
        left = gr.Button(value="Mover para a esquerda")
        add = gr.Button(value="Adicionar letra")
        submit = gr.Button(value="Enviar palavra")
        reset = gr.Button("Reiniciar jogo")
        right = gr.Button(value="Mover para a direita")
        gr.Markdown("")

    add.click(fn=my_interface.try_image, inputs=webcam, outputs=html)
    submit.click(fn=my_interface.submit_word, inputs=None, outputs=html)
    submit.click(fn=my_interface.check_win, inputs=None, outputs=message)
    left.click(fn=my_interface.move_left, inputs=None, outputs=html)
    right.click(fn=my_interface.move_right, inputs=None, outputs=html)
    reset.click(fn=my_interface.reset, inputs=None, outputs=html)
    reset.click(fn=my_interface.get_word, inputs=None, outputs=answer)

demo.launch()
