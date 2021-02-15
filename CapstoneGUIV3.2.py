import tensorflow as tf
import keras
from tkinter import Tk, Label, Button, StringVar
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import cv2
import numpy as np

IMAGE_RES = 150

def res_print(resul, predictions):
    for i in range(0, len(predictions[0])):
        Label(root, text= str(resul[i]).upper() + ': ' + 
              str(round(float(predictions[0][i])*100, 3)) + '%').pack()
        
def cvprepare(filepath):
    img_array = cv2.imread(filepath)
    r = cv2.selectROI('Selection', img_array)
    imCrop = img_array[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    cv2.destroyWindow('Selection')
    new_array = cv2.resize(img_array, (100, 150))
    if imCrop.size > 0:
        new_array = cv2.resize(imCrop, (100, IMAGE_RES))
    else:
        new_array = cv2.resize(img_array, (100, IMAGE_RES))
    new_array = cv2.resize(imCrop, (100, IMAGE_RES))
    new_array = new_array[...,::-1].astype(np.float32)
    return new_array.reshape(-1, 100, IMAGE_RES, 3)/255.0
    
def prepare(filepath):
    img_array = keras.preprocessing.image.load_img(filepath, target_size=(150,150))
    img_array = keras.preprocessing.image.img_to_array(img_array)
    img_array = tf.expand_dims(img_array, 0)
    img_array /= 255
    return img_array

export_path_sm = './Feb8Model'#'./1609881635'
modelo = tf.keras.models.load_model(
  export_path_sm)

class CapstoneGUI:
    LABEL_TEXT = [
        "Machine Learning Project for Altalink"
    ]

    def __init__(self, master):
        self.master = master
        master.title("Altalink Thermal Protection")
        self.label_index = 0
        self.label_text = StringVar()
        self.label_text.set(self.LABEL_TEXT[self.label_index])
        self.label = Label(master, textvariable=self.label_text)
        self.label.pack()
        
        self.Open_button = Button(master, text="Open", command=self.open_file)
        self.Open_button.place(relx=0, rely=0.89, height=50, width=65)

        self.close_button = Button(master, text="Close", command=master.destroy)
        self.close_button.place(relx=0.815, rely=0.89, height=50, width=65)

    def open_file(self): 
        file = askopenfile(title = 'Please select an image file', filetypes =[('Image Files', ['.jpg', '.jpeg', '.png'])]) 
        if file is not None: 
            #print(file.name)
            image = Image.open(file.name)
            # tkimage = ImageTk.PhotoImage(image)
            # myvar = Label(root, image = tkimage)
            #image = cv2.imread(file.name)
            tkimage = ImageTk.PhotoImage(image)
            myvar = Label(root, image = tkimage)
            myvar.image = tkimage
            pred = modelo.predict(cvprepare(file.name))
            #rez = tf.keras.applications.modelo.decode_predictions(pred)
            #print(rez)
            sx1 = pred[0,0]
            oh2 = pred[0,1]
            mf3 = pred[0,2]
            cf4 = pred[0,3]
            eb5 = pred[0,4]
            rez = ["1SX", "2OH", "3MF", "4CF", "5EB"]
            var = {sx1: "1SX", oh2: "2OH", mf3: "3MF", cf4: "4CF", eb5: "5EB"}
            peak = var.get(max(var))
            if peak == "1SX":
                result = 'This is a 1SX failure case'
                myvar.label_text = StringVar()
                myvar.label_text.set(result)
                myvar.label = Label(root, textvariable=myvar.label_text)
                res_print(rez, pred)
                myvar.label.pack()
                myvar.place(relx = 0.05, rely = 0.32)
            elif peak == "2OH": 
                result = 'This is a 2OH failure case'
                myvar.label_text = StringVar()
                myvar.label_text.set(result)
                myvar.label = Label(root, textvariable=myvar.label_text)
                res_print(rez, pred)
                myvar.label.pack()
                myvar.place(relx = 0.05, rely = 0.32)
            elif peak == "3MF": 
                result = 'This is a 3MF failure case'
                myvar.label_text = StringVar()
                myvar.label_text.set(result)
                myvar.label = Label(root, textvariable=myvar.label_text)
                res_print(rez, pred)
                myvar.label.pack()
                myvar.place(relx = 0.05, rely = 0.32)
            elif peak == "4CF": 
                result = 'This is a 4CF failure case'
                myvar.label_text = StringVar()
                myvar.label_text.set(result)
                myvar.label = Label(root, textvariable=myvar.label_text)
                res_print(rez, pred)
                myvar.label.pack()
                myvar.place(relx = 0.05, rely = 0.32)
            elif peak == "5EB": 
                result = 'This is a 5EB failure case'
                myvar.label_text = StringVar()
                myvar.label_text.set(result)
                myvar.label = Label(root, textvariable=myvar.label_text)
                res_print(rez, pred)
                myvar.label.pack()
                myvar.place(relx = 0.05, rely = 0.32)
            print(pred)

root = Tk()
root.geometry("350x450")
my_gui = CapstoneGUI(root)
root.mainloop()