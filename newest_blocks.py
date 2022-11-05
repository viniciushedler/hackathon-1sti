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
        letter = get_letter_from_image(img)
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
    with gr.Row():
        webcam = gr.Image(source="webcam", streaming=True, mirror_webcam=True)
        hand = gr.Image()

    button = gr.Button(value="Enviar")

    #button.click(fn=my_interface.input_img, inputs=text, outputs=html)
    # button.click(fn=draw_landmarks, inputs=webcam, outputs=hand )
    button.click(fn=get_letter_from_image, inputs=webcam, outputs=text)

app.launch()