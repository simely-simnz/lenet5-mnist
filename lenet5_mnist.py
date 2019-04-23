"""
Treina uma CNN com o dataset MNIST.
 
A CNN é inspirada na arquitetura LeNet-5, com algumas
alterações nas funções de ativação, padding e pooling.
"""
 
# importar pacotes necessários
from keras.utils import to_categorical
from keras.optimizers import SGD
from keras import backend
from keras.datasets import mnist
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np
import h5py
from cnn import LeNet5     #classe criada na pasta cnn

# importar e normalizar o dataset MNIST
# input image dimensions
img_rows, img_cols = 28, 28

print('[INFO] Download dataset')
# dividir o dataset entre train (60000) e test (10000)
(trainX, trainY), (testX, testY) =  mnist.load_data() 


print('[INFO] Padronizando imagens de acordo com a lib utilizada em backend pelo Keras (TensorFlow ou Theano)')
if backend.image_data_format() == "channels_last": #Tensorflow backend
    trainX = trainX.reshape(trainX.shape[0], img_rows, img_cols, 1)
    testX = testX.reshape(testX.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)
else: #Theano backend
    trainX = trainX.reshape(trainX.shape[0], 1, img_rows, img_cols)
    testX = testX.reshape(testX.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)

trainX = trainX.astype('float32')
testX = testX.astype('float32')
trainX /= 255
testX /= 255

# Transformar labels em vetores binarios
trainY = to_categorical(trainY, 10)
testY = to_categorical(testY, 10)

# inicializar e otimizar modelo
print("[INFO] inicializando e otimizando a CNN...")
model = LeNet5.build(28, 28, 1, 10)
model.compile(optimizer=SGD(0.01), loss="categorical_crossentropy",
              metrics=["accuracy"])
 
# treinar a CNN
print("[INFO] treinando a CNN...")
H = model.fit(trainX, trainY, batch_size=128, epochs=20, verbose=2,
          validation_data=(testX, testY))

model.save('models/trained_model.h5')

# avaliar a CNN
print("[INFO] avaliando a CNN...")
predictions = model.predict(testX, batch_size=64)
print(classification_report(testY.argmax(axis=1), predictions.argmax(axis=1),
                            target_names=[str(label) for label in range(10)]))

# plotar loss e accuracy para os datasets 'train' e 'test'
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0,20), H.history["loss"], label="train_loss")
plt.plot(np.arange(0,20), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0,20), H.history["acc"], label="train_acc")
plt.plot(np.arange(0,20), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.savefig('cnn.png', bbox_inches='tight')
