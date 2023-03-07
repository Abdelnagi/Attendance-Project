import cv2
import os
import numpy as np
import pandas as pd
import face_recognition
import tkinter as tk
from tkinter import filedialog
import time
from PIL import Image, ImageTk

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner


classNames = []


def enhance(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def findEncodings(images):
    encodelist = []
    for img in images:
        img = enhance(img)
        encoding = face_recognition.face_encodings(img)[0]
        encodelist.append(encoding)
    return encodelist

def add_database(directory):

    # create Codes.csv file if it doesn't exist
    if not os.path.exists('Codes.csv'):
        with open('Codes.csv', 'w') as f1:
            f1.write('ID\n')
            
    if not os.path.exists('Encodings.csv'):
        with open('Encodings.csv', 'w') as f2:
            f2.write('encoding')
            for i in range(127):
                f2.write(',encoding')
            f2.write('\n')
    # load existing codes
    
    codes_df = pd.read_csv('Codes.csv')
    existing_codes = set(codes_df['ID'].values.tolist())
    skip_counter = 0
    add_counter = 0
    IDonce = 0
    images = []
    classNames = []
    for foldername in os.listdir(directory):
        if str(foldername).strip() in [str(code).strip() for code in existing_codes]:
            skip_counter += 1 
            continue
        add_counter += 1
        folderpath = os.path.join(directory, foldername)
        if os.path.isdir(folderpath):
            for filename in os.listdir(folderpath):
                filepath = os.path.join(folderpath, filename)
                img = cv2.imread(filepath)
                images.append(img)
                classNames.append(foldername)

                


    print(f'Adding {add_counter} students.')
    print(f'Skipping {skip_counter} students.')
    if len(images) == 0:
        print('No new images found in directory.')
        return
    encodelist = findEncodings(images)
    df1 = pd.DataFrame(encodelist)
    df1.to_csv('Encodings.csv',index=False, mode='a', header = False)
    df2 = pd.DataFrame(classNames)
    df2.to_csv('Codes.csv', index=False, mode='a', header = False)
    print(f'{len(classNames)} new images added to the database.')

          
def mark_attendance(name, session_num):
    filename = f"attendanceSheet.csv"
    df = pd.read_csv(filename)
    df.loc[name, session_num] = 1  
    df.to_csv(filename, index=False)


def who_is_it(file_paths, session_num):
    for file_path in file_paths:
        encoode = pd.read_csv('Encodings.csv')
        Class = pd.read_csv('Codes.csv')
        Class = Class['ID'].tolist()
        test = face_recognition.load_image_file(file_path)
        test = enhance(test)
        loc = face_recognition.face_locations(test)
        encoodingstest = face_recognition.face_encodings(test)
        result = open("Output.txt", "w+")
        counter = 0
        for encodeFace, faceLoc in zip(encoodingstest, loc):
            matches = face_recognition.compare_faces(encoode, encodeFace)
            faceDis = face_recognition.face_distance(encoode, encodeFace)
            matchInd = np.argmin(faceDis)
            if matches[matchInd]:
                name = Class[matchInd]
                print(name)
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(test, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(test, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                mark_attendance(matchInd, session_num)
            else:
                counter += 1
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(test, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(test, 'NA', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        result.write("Found " + str(counter) + " people who are not in the database..")
      #  cv2.imshow('group', test)
     #   cv2.waitKey()


#############################################

def select_file():
    # Show a file dialog to select one or more image files
    filepaths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    num_files = len(filepaths)
    print(f"Selected {num_files} files: {filepaths}")
    return filepaths, num_files

def select_folder():
    folderpath = filedialog.askdirectory()
    print(f"Selected {folderpath}")
    return folderpath




class MyApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.5,0.25)
        self.window.pos_hint = {"center_x":0.5, "center_y":0.5}

        self.button1 = Button(text='Take Attendance',
                              on_press=self.on_button1_press,
                              size_hint = (1, 0.5),
                              font_size = 22,
                              padding = (0,200))
        
        self.button2 = Button(text='Add to Data base',
                              on_press=self.on_button2_press,
                              size_hint = (1, 0.5),
                              font_size = 22,
                              )
        self.button1.padding = (0,200)

        self.spinner = Spinner(
            text='Session 1',  # Default text displayed in the dropdown list
            values = ["Session 1", "Session 2", "Session 3", "Session 4", "Session 5", "Session 6"],  # options for session selection
            size_hint=(1, 0.5),  # Set the size of the dropdown list
            size=(100, 44),  # Set the size of the dropdown list
            font_size = 22,
            padding = (0,200),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Set the position of the dropdown list
        )

        self.window.add_widget(self.spinner)
        self.window.add_widget(self.button1)
        self.window.add_widget(self.button2)
       # selected_session = self.spinner.text        

        return self.window
    def on_button1_press(self, instance):
        who_is_it(select_file()[0],self.spinner.text)

    def on_button2_press(self, instance):
        add_database(select_folder())


if __name__ == '__main__':
    MyApp().run()



##add_database('Data_base')
##
##
##root = tk.Tk()
##root.geometry("400x200")  # Set the size of the window
##root.title("Image Selector")  # Set the title of the window
##
##
##session_options = ["Session 1", "Session 2", "Session 3", "Session 4", "Session 5", "Session 6"]  # options for session selection
##
##selected_session = tk.StringVar(root)
##
### Set the default value of the selected session to the first session number in the list
##selected_session.set(session_options[0])
##
### Create a drop down menu with the session numbers as options
##session_dropdown = tk.OptionMenu(root, selected_session, *session_options)
##session_dropdown.pack(pady=20)
##
##
##take_atten_btn = tk.Button(root, text="Take Attendance", command=lambda: who_is_it(select_file()[0],selected_session))
##take_atten_btn.pack(pady=20)
##
##add_data_btn = tk.Button(root, text="Add to data base", command=lambda: add_database(select_folder()))
##add_data_btn.pack(pady=20)
##
##
##root.mainloop()

###################

