import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageDraw, ImageFont
import os


class Application:
    # Trying to make this a bit better look
    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry('490x270')
        self.app.title('Add watermark to you picture.')
        self.info_label = tk.Label(self.app, text='ADD your images and i will add watermarks at your pictures!',
                                   font='Verdana 10 bold').grid(row=0, column=0, columnspan=2)
        self.info_label1 = tk.Label(self.app, text='1.Select your images: ',
                                    font='Verdana 10 bold').grid(row=1, column=0, columnspan=2)
        self.upload_image_button = tk.Button(self.app, text='SELECT',
                                             font='Verdana 10 bold',
                                             command=self.load_image).grid(row=2, column=0, columnspan=2)
        self.info_label2 = tk.Label(self.app, text='2.Write text or select your watermark sign:',
                                    font='Verdana 10 bold').grid(row=3, column=0, columnspan=2)
        self.upload_watermark_button = tk.Button(self.app, text='SELECT',
                                                 font='Verdana 10 bold',
                                                 command=self.load_watermark).grid(row=4, column=0, columnspan=2)
        self.user_text_label = tk.Label(text='Watermark text:',
                                        font='Verdana 10 bold').grid(row=5, column=0)
        self.user_text = tk.Entry(self.app, width=30)
        self.user_text.grid(row=5, column=1)
        self.info_label3 = tk.Label(self.app, text='3.Specify Coordinates of watermark/text:',
                                    font='Verdana 10 bold').grid(row=6, column=0, columnspan=2)
        self.position_x_label = tk.Label(text='Position X : ',
                                         font='Verdana 10 bold').grid(row=7, column=0)
        self.position_x = tk.Entry(self.app, width=5)
        self.position_x.grid(row=8, column=0)
        self.position_y_label = tk.Label(text='Position Y : ',
                                         font='Verdana 10 bold').grid(row=7, column=1)
        self.position_y = tk.Entry(self.app, width=5)
        self.position_y.grid(row=8, column=1)
        self.info_label4 = tk.Label(text='4.What you want to do ? ',
                                    font='Verdana 10 bold').grid(row=9, column=0, columnspan=2)
        self.add_watermark_button = tk.Button(text='Add Watermarks and Save Files in cwd',
                                              font='Verdana 10 bold',
                                              command=self.add_watermark).grid(row=10, column=0)
        self.add_text_button = tk.Button(self.app, text='ADD TEXT',
                                         font='Verdana 10 bold',
                                         command=self.add_text).grid(row=10, column=1)
        self.app.mainloop()

    # Open multiple files and put them in the list (path)
    def load_image(self):
        self.images = fd.askopenfilenames(filetypes=[(' ', '*.jpg'), (' ', '*.png')])

    def load_watermark(self):
        self.watermark = Image.open(fd.askopenfilename(filetypes=[(' ', '*.jpg'), (' ', '*.png')]))

    def add_watermark(self):
        # Generate position every time when user hit button
        position = (int(self.position_x.get()), int(self.position_y.get()))
        for image in self.images:
            # Take only file name without path
            save_name = image.split('/')[-1]
            image = Image.open(image)
            width, height = image.size
            # Prepare new image that we can use png watermarks
            transparent_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            transparent_image.paste(image, (0, 0))
            transparent_image.paste(self.watermark, position, mask=self.watermark)
            self.new_file_path = os.getcwd() + f'\\{save_name[:-4]}' + '.png'
            self.check_if_file_exist(transparent_image)

    def add_text(self):
        # Generate position every time when user hit button
        position = (int(self.position_x.get()), int(self.position_y.get()))
        for image in self.images:
            # Take only file name without path
            save_name = image.split('/')[-1]
            image = Image.open(image)
            width, height = image.size
            image_edit = ImageDraw.Draw(image)
            # Make font size a bit proportional to image everytime and change font from default
            font = ImageFont.truetype('Gabriola.ttf', size=round((width/12)))
            image_edit.text(position, text=self.user_text.get(), font=font, fill=(3, 8, 12))
            self.new_file_path = os.getcwd() + f'\\{save_name[:-4]}' + '.png'
            self.check_if_file_exist(image)

    # Check if file with same name not exist. We don't want to overwrite them.
    # If there is any file with same name just add _latest :)
    def check_if_file_exist(self, image):
        while True:
            if not os.path.exists(self.new_file_path):
                image.save(self.new_file_path)
                break
            else:
                self.new_file_path = self.new_file_path[:-4] + '_latest' + '.png'


program = Application()
