from keras.models import Sequential
from keras.models import Model
from keras.layers import Input, Dense, Activation, Flatten, Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D, BatchNormalization
from keras.optimizers import SGD
from skimage import io
from sklearn.preprocessing import OneHotEncoder
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
import keras
import numpy as np
import cv2

def VGG_16(classify_num, weights_path=None, input_shape=[224, 224, 3]):
    img_input = Input(shape=input_shape)

    # Block 1
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)


    # Classification block
    x = Flatten(name='flatten')(x)
    x = Dense(4096, activation='relu', name='fca')(x)
    x = Dense(4096, activation='relu', name='fcb')(x)
    x = Dense(classify_num, activation='softmax', name='Classification')(x)


    inputs = img_input
    # Create model.
    model = Model(inputs=inputs, outputs=x, name='vgg16')

    if weights_path:
        model.load_weights(weights_path)

    return model

if __name__ == "__main__":
    img1 = cv2.resize(cv2.imread('1.pgm'), (224, 224)).astype(np.float32).tolist()
    img2 = cv2.resize(cv2.imread('2.pgm'), (224, 224)).astype(np.float32).tolist()
    data = np.array([img1, img2])

    encoder = OneHotEncoder()
    labels = encoder.fit_transform([[1], [2]]).toarray()

    model = VGG_16(classify_num=labels.shape[0])
    model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(lr=1e-4), metrics=['accuracy'])
    model.fit(x=data, y=labels, epochs=1)
    
    out = model.predict(np.array([img1, img2]))
    print(out)
    print(np.argmax(out, axis=1))