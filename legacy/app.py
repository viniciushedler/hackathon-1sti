from PIL import Image
import gradio as gr
import numpy as np
import mediapipe as mp
# Capaz de rodar uma função a cada intervalo de tempo
# from apscheduler.schedulers.background import BackgroundScheduler

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

n = 0

# Tentativa falha de criar uma função que clicasse no botão que nem deveria existir
js = """
function click() {
    // document.getElementById("component-6").click();
    // document.getElementById("component-6").innerHTML += "a";
    alert("Click");
    setTimeout(click, 5000);
}
"""

def draw_landmarks(image):
    global n
    print("Running", n)
    n += 1

    # Verifica se a imagem recebida é válida
    if type(image) != np.ndarray:
        print("Teve ruim")
        return
    with mp_hands.Hands(min_detection_confidence=0.6, static_image_mode=True, max_num_hands=2) as hands: 
        result = hands.process(image)
        # Atualiza a imagem recebida com a detecção das mãos
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
        # else:
    # Salva a imagem 
    # Image.fromarray(image).save(f"{n}.png")
    return image


with gr.Blocks(title="Teste") as demo:
    # Necessário colocar o estilo, porque o gradio ignora o tamanho da tag h1
    gr.HTML('<h1 style="font-size: 64px;">LIBRAS</h1>')
    with gr.Row():
        webcam = gr.Image(source="webcam", streaming=True)
        output = gr.Image()

    # Chama a função a cada 2 segundos, mas requer o outro jeito de dar launch
    # no aplicativo, que é significativamente mais lento e bugado, e ainda
    # não envia o output corretamente
    # dep = demo.load(fn=draw_landmarks, inputs=webcam, outputs=output, every=2)
    # dep = demo.load(draw_landmarks, webcam, output, every=2)

    btn = gr.Button("Click me")
    # Determina o comportamento do botão quando ele é clicado
    btn.click(fn=draw_landmarks, inputs=webcam, outputs=output)
    # btn.click(fn=draw_landmarks, inputs=webcam, outputs=output, cancels=[dep], every=2)
    # btn.visible = False

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=draw_landmarks, trigger="interval", seconds=2)
# scheduler.start()

demo.launch()
# if __name__ == "__main__":
#     demo.queue().launch()
