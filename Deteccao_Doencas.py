import tensorflow as tf
import numpy as np
import openai

modelo = tf.keras.models.load_model('classificador_plantas.h5')

def preparar_imagem(caminho_imagem):
    imagem = tf.keras.preprocessing.image.load_img(caminho_imagem, target_size=(224, 224))
    imagem_array = tf.keras.preprocessing.image.img_to_array(imagem)
    imagem_array = np.expand_dims(imagem_array, axis=0)
    imagem_preprocessada = tf.keras.applications.resnet50.preprocess_input(imagem_array)
    return imagem_preprocessada

caminho_nova_imagem = 'Teste/teste.PNG'
imagem_preparada = preparar_imagem(caminho_nova_imagem)
previsao = modelo.predict(imagem_preparada)
classe_prevista = np.argmax(previsao)

mapa_classes = {0: 'Cercospora', 1: 'FungoBranco', 2: 'Fusarium', 3: 'Gibberella', 4: 'Nematoide'}
doenca_detectada = mapa_classes[classe_prevista]

print('Doença detectada:', doenca_detectada)

resposta_usuario = input("Deseja informações sobre o tratamento desta doença? (Sim/Não): ")

def obter_resposta_gpt3(pergunta):
    openai.api_key = "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"
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pergunta,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.7
    )
    return resposta.choices[0].text.strip()

while resposta_usuario.lower() not in ["sim", "não"]:
    resposta_usuario = input("Resposta inválida. Digite 'Sim' ou 'Não': ")

if resposta_usuario.lower() == "sim":
    pergunta_para_gpt3 = f"Tenho a doença: {doenca_detectada} em minha plantação. O que isso pode causar e como posso tratá-la?"
    resposta_gpt3 = obter_resposta_gpt3(pergunta_para_gpt3)
    print("-" * 30)
    print(resposta_gpt3)

print("-" * 30)

if doenca_detectada in mapa_classes.values():
    if doenca_detectada == 'Cercospora':
        print("Nosso parceiro AgroWrap tem os melhores fungicidas do mercado perfeito para tratar Cercospora. Acesse o site e obtenha mais informações! https://www.agrowap.com.br/fungicidas")
    elif doenca_detectada == 'FungoBranco':
        print("Nosso parceiro AgroLink tem os melhores produtos de controle ambiental do mercado perfeito para tratar Fungo Branco. Acesse o site e obtenha mais informações! https://www.agrolink.com.br/agrolinkfito/")
    elif doenca_detectada == 'Fusarium':
        print("Nosso parceiro AgroWrap tem os melhores fungicidas do mercado perfeito para tratar Fusarium. Acesse o site e obtenha mais informações! https://www.agrowap.com.br/fungicidas")
    elif doenca_detectada == 'Gibberella':
        print("Nosso parceiro AgroLink tem os melhores produtos de controle ambiental do mercado perfeito para tratar Gibberella. Acesse o site e obtenha mais informações! https://www.agrolink.com.br/agrolinkfito/")
    elif doenca_detectada == 'nematoide':
        print("Nosso parceiro AgroWrap tem os melhores fungicidas do mercado perfeito para tratar Nematoide. Acesse o site e obtenha mais informações! https://www.agrowap.com.br/fungicidas")
else:
    print("Não encontramos informações específicas para a doença detectada. Recomendamos entrar em contato com um especialista em agricultura para obter orientações adicionais.")

