import tensorflow as tf
import os
import numpy as np

classes = ['Cercospora', 'FungoBranco', 'Fusarium', 'Gibberella', 'nematoide']
base_dir = 'Treinamento'

caminhos_imagens = []
rotulos = []

for i, classe in enumerate(classes):
    rota_classe = os.path.join(base_dir, classe)
    caminhos_classe = [os.path.join(rota_classe, nome) for nome in os.listdir(rota_classe)]
    caminhos_imagens += caminhos_classe
    rotulos += [i] * len(caminhos_classe)

rotulos = np.array(rotulos)

imagens = []
for caminho in caminhos_imagens:
    imagem = tf.keras.preprocessing.image.load_img(caminho, target_size=(224, 224))
    imagem_array = tf.keras.preprocessing.image.img_to_array(imagem)
    imagem_array = tf.keras.applications.resnet50.preprocess_input(imagem_array)
    imagens.append(imagem_array)
imagens = np.array(imagens)

modelo_base = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

modelo_base.trainable = False

modelo = tf.keras.models.Sequential()
modelo.add(modelo_base)
modelo.add(tf.keras.layers.GlobalAveragePooling2D())
modelo.add(tf.keras.layers.Dense(128, activation='relu'))
modelo.add(tf.keras.layers.Dense(len(classes), activation='softmax'))

modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

modelo.fit(imagens, rotulos, epochs=10, batch_size=32)

modelo.save('classificador_plantas.h5')

print("Treinamento Concluído!")
