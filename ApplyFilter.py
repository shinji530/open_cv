# ApplyFilter.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ImageSliderApp(QWidget):
    def __init__(self, image_path):
        super().__init__()

        self.image_path = image_path  # Save the image file path

        # Load the image
        self.image = cv2.imread(self.image_path)

        # Check if image loading was successful
        if self.image is None:
            print(f"Error: Unable to load image from {self.image_path}.")
            sys.exit()

        # Initialize sliders and labels
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # Add a horizontal layout to arrange sliders and labels side by side
        hbox_slider = QHBoxLayout()

        # Create R, G, B sliders and labels
        self.createSlider('R', hbox_slider)
        self.createSlider('G', hbox_slider)
        self.createSlider('B', hbox_slider)

        vbox.addLayout(hbox_slider)

        # Create a label for displaying the image
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.label)

        # Display the initial image
        self.updateImage()

        # Create a Reset button and connect it to the resetSliders function
        reset_button = QPushButton('Reset', self)
        reset_button.clicked.connect(self.resetSliders)
        vbox.addWidget(reset_button)

        # Create buttons for color vision deficiencies (protanopia, deuteranopia, tritanopia) and connect them to corresponding functions
        protanopia_button = QPushButton('Protanopia', self)
        protanopia_button.clicked.connect(self.increaseRed)
        deuteranopia_button = QPushButton('Deuteranopia', self)
        deuteranopia_button.clicked.connect(self.increaseGreen)
        tritanopia_button = QPushButton('Tritanopia', self)
        tritanopia_button.clicked.connect(self.increaseBlue)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(protanopia_button)
        hbox_buttons.addWidget(deuteranopia_button)
        hbox_buttons.addWidget(tritanopia_button)
        vbox.addLayout(hbox_buttons)

        self.setLayout(vbox)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Slider')
        self.show()

    def createSlider(self, label, layout):
        label_widget = QLabel(f'{label}: 0', self)
        layout.addWidget(label_widget)

        slider = QSlider(Qt.Horizontal, self)
        slider.setMaximum(255)
        slider.setMinimum(-255)  # Allow negative values

        # Connect the valueChanged signal of each slider to the sliderChanged function with the corresponding channel
        if label == 'R':
            slider.valueChanged[int].connect(lambda value: self.sliderChanged(value, 'R'))
        elif label == 'G':
            slider.valueChanged[int].connect(lambda value: self.sliderChanged(value, 'G'))
        elif label == 'B':
            slider.valueChanged[int].connect(lambda value: self.sliderChanged(value, 'B'))

        layout.addWidget(slider)
        self.__dict__[f'{label}_slider'] = slider
        self.__dict__[f'{label}_label'] = label_widget

    def sliderChanged(self, value, channel):
        # Update the image display
        self.updateImage()

    def resetSliders(self):
        # Reset all sliders to 0
        for label in ['R', 'G', 'B']:
            slider = self.__dict__[f'{label}_slider']
            slider.setValue(0)

    def increaseRed(self):
        # Increase the red slider value by 50
        self.R_slider.setValue(self.R_slider.value() + 50)

    def increaseGreen(self):
        # Increase the green slider value by 50
        self.G_slider.setValue(self.G_slider.value() + 50)

    def increaseBlue(self):
        # Increase the blue slider value by 50
        self.B_slider.setValue(self.B_slider.value() + 50)

    def updateImage(self):
        # Get the current values of the sliders
        r = self.R_slider.value()
        g = self.G_slider.value()
        b = self.B_slider.value()

        # Update the labels with the current slider values
        self.R_label.setText(f'R: {r}')
        self.G_label.setText(f'G: {g}')
        self.B_label.setText(f'B: {b}')

        # Create a copy of the original image
        frame = self.image.copy().astype(np.int32)

        # Adjust pixel values based on slider values for each channel
        if b > 0:
            frame[:, :, 0] = np.where(frame[:, :, 0] >= 128, frame[:, :, 0] + b, frame[:, :, 0])
        else:
            frame[:, :, 0] = np.where(frame[:, :, 0] < 128, frame[:, :, 0] + b, frame[:, :, 0])
        if g > 0:
            frame[:, :, 1] = np.where(frame[:, :, 1] >= 128, frame[:, :, 1] + g, frame[:, :, 1])
        else:
            frame[:, :, 1] = np.where(frame[:, :, 1] < 128, frame[:, :, 1] + g, frame[:, :, 1])
        if r > 0:
            frame[:, :, 2] = np.where(frame[:, :, 2] >= 128, frame[:, :, 2] + r, frame[:, :, 2])
        else:
            frame[:, :, 2] = np.where(frame[:, :, 2] < 128, frame[:, :, 2] + r, frame[:, :, 2])

        # Clip pixel values to the range [0, 255]
        frame[:, :, 0] = np.clip(frame[:, :, 0], 0, 255)
        frame[:, :, 1] = np.clip(frame[:, :, 1], 0, 255)
        frame[:, :, 2] = np.clip(frame[:, :, 2], 0, 255)

        frame = frame.astype(np.uint8)

        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w

        # Create a QImage with modified constructor
        q_image = QImage(rgb_image.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        # Update the image label
        self.label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create an ImageSliderApp with the image file path as an argument
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        ex = ImageSliderApp(image_path)
    else:
        print("Image file path not provided.")
        sys.exit()

    sys.exit(app.exec_())
