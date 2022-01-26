from tensorflow.keras.models import load_model
import numpy as np
import cv2
model = load_model("model.h5")

def predict(InputImg):
    image = cv2.imread(InputImg)
    image = image[:, :, 0]
    image = np.invert(image)
    image = cv2.resize(image,(28,28))
    image = image.reshape(1,28,28,1)


    return model.predict(image)[0].tolist().index(1)

