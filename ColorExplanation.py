# ColorExplanation.py

import cv2
import numpy as np
import sys
from sobel_edge_detect import calculate, erode
import tkinter as tk
from tkinter import ttk

# Mapping of color names to RGB values
color_mapping = {
'maroon': (0, 0, 128),
'dark red': (0, 0, 139),
'brown': (42, 42, 165),
'firebrick': (34, 34, 178),
'crimson': (60, 20, 220),
'red': (0, 0, 255),
'tomato': (71, 99, 255),
'coral': (80, 127, 255),
'indian red': (92, 92, 205),
'light coral': (128, 128, 240),
'dark salmon': (122, 150, 233),
'salmon': (114, 128, 250),
'light salmon': (122, 160, 255),
'orange red': (0, 69, 255),
'dark orange': (0, 140, 255),
'orange': (0, 165, 255),
'gold': (0, 215, 255),
'dark golden rod': (11, 134, 184),
'golden rod': (32, 165, 218),
'pale golden rod': (170, 232, 238),
'dark khaki': (107, 183, 189),
'khaki': (140, 230, 240),
'olive': (0, 128, 128),
'yellow': (0, 255, 255),
'yellow green': (50, 205, 154),
'dark olive green': (47, 107, 85),
'olive drab': (35, 142, 107),
'lawn green': (0, 252, 124),
'chartreuse': (0, 255, 127),
'green yellow': (47, 255, 173),
'dark green': (0, 100, 0),
'green': (0, 128, 0),
'forest green': (34, 139, 34),
'lime': (0, 255, 0),
'lime green': (50, 205, 50),
'light green': (144, 238, 144),
'pale green': (152, 251, 152),
'dark sea green': (143, 188, 143),
'medium spring green': (154, 250, 0),
'spring green': (127, 255, 0),
'sea green': (87, 139, 46),
'medium aqua marine': (170, 205, 102),
'medium sea green': (113, 179, 60),
'light sea green': (170, 178, 32),
'dark slate gray': (79, 79, 47),
'teal': (128, 128, 0),
'dark cyan': (139, 139, 0),
'aqua': (255, 255, 0),
'cyan': (255, 255, 0),
'light cyan': (255, 255, 224),
'dark turquoise': (209, 206, 0),
'turquoise': (208, 224, 64),
'medium turquoise': (204, 209, 72),
'pale turquoise': (238, 238, 175),
'aqua marine': (212, 255, 127),
'powder blue': (230, 224, 176),
'cadet blue': (160, 158, 95),
'steel blue': (180, 130, 70),
'corn flower blue': (237, 149, 100),
'deep sky blue': (255, 191, 0),
'dodger blue': (255, 144, 30),
'light blue': (230, 216, 173),
'sky blue': (235, 206, 135),
'light sky blue': (250, 206, 135),
'midnight blue': (112, 25, 25),
'navy': (128, 0, 0),
'dark blue': (139, 0, 0),
'medium blue': (205, 0, 0),
'blue': (255, 0, 0),
'royal blue': (225, 105, 65),
'blue violet': (226, 43, 138),
'indigo': (130, 0, 75),
'dark slate blue': (139, 61, 72),
'slate blue': (205, 90, 106),
'medium slate blue': (238, 104, 123),
'medium purple': (219, 112, 147),
'dark magenta': (139, 0, 139),
'dark violet': (211, 0, 148),
'dark orchid': (204, 50, 153),
'medium orchid': (211, 85, 186),
'purple': (128, 0, 128),
'thistle': (216, 191, 216),
'plum': (221, 160, 221),
'violet': (238, 130, 238),
'magenta': (255, 0, 255),
'orchid': (214, 112, 218),
'medium violet red': (133, 21, 199),
'pale violet red': (147, 112, 219),
'deep pink': (147, 20, 255),
'hot pink': (180, 105, 255),
'light pink': (193, 182, 255),
'pink': (203, 192, 255),
'antique white': (215, 235, 250),
'beige': (220, 245, 245),
'bisque': (196, 228, 255),
'blanched almond': (205, 235, 255),
'wheat': (179, 222, 245),
'corn silk': (220, 248, 255),
'lemon chiffon': (205, 250, 255),
'light golden rod yellow': (210, 250, 250),
'light yellow': (224, 255, 255),
'saddle brown': (19, 69, 139),
'sienna': (45, 82, 160),
'chocolate': (30, 105, 210),
'peru': (63, 133, 205),
'sandy brown': (96, 164, 244),
'burly wood': (135, 184, 222),
'tan': (140, 180, 210),
'rosy brown': (143, 143, 188),
'moccasin': (181, 228, 255),
'navajo white': (173, 222, 255),
'peach puff': (185, 218, 255),
'misty rose': (225, 228, 255),
'lavender blush': (245, 240, 255),
'linen': (230, 240, 250),
'old lace': (230, 245, 253),
'papaya whip': (213, 239, 255),
'sea shell': (238, 245, 255),
'mint cream': (250, 255, 245),
'slate gray': (144, 128, 112),
'light slate gray': (153, 136, 119),
'light steel blue': (222, 196, 176),
'lavender': (250, 230, 230),
'floral white': (240, 250, 255),
'alice blue': (255, 248, 240),
'ghost white': (255, 248, 248),
'honeydew': (240, 255, 240),
'ivory': (240, 255, 255),
'azure': (255, 255, 240),
'snow': (250, 250, 255),
'black': (0, 0, 0),
'dim gray / dim grey': (105, 105, 105),
'gray / grey': (128, 128, 128),
'dark gray / dark grey': (169, 169, 169),
'silver': (192, 192, 192),
'light gray / light grey': (211, 211, 211),
'gainsboro': (220, 220, 220),
'white smoke': (245, 245, 245),
'white': (255, 255, 255),
'golden yellow':(0,223,255),
'metallic gold':(55,175,212),
'Old gold':(59,181,207),
'Vegas gold':(88,179,197),
'Pale gold':(138,190,230),
'Golden brown':(21,101,153),
'paleturquoise':(238,238,175),
'charcoal':(79,69,54),
'dark purple':(52,25,48),
'jet black':(52,52,52),
'licorice':(18,18,27),
'matte black':(43,40,40),
'onyx':(53,57,53),
'baby blue':(240,207,137),
'blue gray':(179,147,115),
'blue green':(143,143,8),
'bright blue':(255,150,0),
'cobalt blue':(171,71,0),
'Denim':(175, 143, 111),
'Egyptian Blue':(164, 52, 20),
'Electric Blue':(255, 249, 125),
'Glaucous':(182, 130, 96),
'Jade':(108, 163, 0),
'iris':(93,63,211),
'Navy Blue':(128, 0, 0),
'Neon Blue':(255, 81, 31),
'Pastel Blue':(231, 199, 167),
'Periwinkle':(255, 204, 204),
'Robin Egg Blue':(209, 222, 105),
'Royal Blue':(225, 105, 65),
'Sapphire Blue':(186, 82, 15),
'Seafoam Green':(191, 226, 159),
'Ultramarine':(242, 55, 4),
'Verdigris':(173, 181, 64),
'Zaffre':(168, 24, 8),
'Almond':(202, 221, 234),
'Brass':(110, 193, 225),
'Bronze':(50, 127, 205),
'Buff':(109, 160, 218),
'Burgundy':(32, 0, 128),
'Burnt Sienna':(81, 116, 233),
'Burnt Umber':(14, 38, 110),
'Camel':(107, 154, 193),
'Chestnut':(53, 69, 149),
'Cinnamon':(45, 125, 210),
'Coffee':(55, 78, 111),
'Cognac':(51, 67, 131),
'Copper':(51, 115, 184),
'Cordovan':(65, 65, 129),
'Dark Brown':(51, 64, 92),
'Dark Tan':(88, 133, 152),
'Ecru':(128, 178, 194),
'Fallow':(107, 154, 193),
'Fawn':(112, 170, 229),
'Garnet':(42, 42, 154),
'light brown':(196,164,132),
'Mocha':(105, 121, 150),
'Nude':(189, 210, 242),
'Ochre':(34, 119, 204),
'Olive Green':(0, 128, 128),
'Oxblood':(4, 4, 74),
'Puce':(104, 92, 169),
'Red Brown':(42, 42, 165),
'Red Ochre':(49, 56, 145),
'Russet':(27, 70, 127),
'Sand':(128,178,194),
'Taupe':(50,60,72),
'Tuscan Red':(48, 48, 124),
'Wine':(55, 47, 114),
'Ash Gray':(181, 190, 178),
'Glaucous':(182,130,96),
'Gunmetal Gray':(137, 133, 129),
'Pewter':(153, 148, 137),
'Platinum':(226, 228, 229),
'Sage Green':(91, 154, 138),
'Silver':(192, 192, 192),
'Smoke':(132, 136, 132),
'Steel Gray':(126, 121, 113),
'Army Green':(27, 75, 69),
'Bright Green':(0, 255, 170),
'Cadmium Green':(105, 121, 9),
'Celadon':(175, 225, 175),
'Citrine':(10, 208, 228),
'Emerald Green':(120, 200, 80),
'Eucalyptus':(117, 133, 95),
'Fern Green':(66, 121, 79),
'Grass Green':(0, 252, 124),
'Hunter Green':(59, 94, 53),
'Jungle Green':(138, 170, 42),
'Kelly Green':(23, 187, 76),
'Lincoln Green':(120, 135, 71),
'Malachite':(81, 218, 11),
'Mint Green':(152, 251, 152),
'Moss Green':(91, 154, 138),
'Neon Green':(80, 255, 15),
'Nyanza':(220, 255, 236),
'Pastel Green':(193, 225, 193),
'Pear':(63, 204, 201),
'Peridot':(36, 196, 180),
'Pistachio':(114, 197, 147),
'Shamrock Green':(96, 158, 0),
'Viridian':(109, 130, 64),
'Amber':(0, 191, 255),
'Apricot':(177, 206, 251),
'Bisque':(189, 210, 242),
'Burnt Orange':(0, 85, 204),
'Butterscotch':(62, 150, 227),
'Cadmium Orange':(40, 140, 242),
'Coral Pink':(121, 131, 248),
'Desert':(165, 213, 250),
'Gamboge':(15, 155, 228),
'Light Orange':(128, 213, 255),
'Mango':(68, 187, 244),
'Neon Orange':(31, 68, 255),
'Pastel Orange':(152, 200, 250),
'Peach':(180, 229, 255),
'Persimmon':(0, 88, 236),
'Pink Orange':(128, 152, 248),
'Poppy':(53, 83, 227),
'Pumpkin Orange':(24, 117, 255),
'Red Orange':(51, 68, 255),
'Safety Orange':(21, 95, 255),
'Seashell':(238, 245, 255),
'Sunset Orange':(85, 95, 250),
'Tangerine':(0, 128, 240),
'Terra Cotta':(94, 115, 227),
'Yellow Orange':(51, 170, 255),
'Amaranth':(104, 43, 159),
'Cerise':(99, 49, 222),
'Claret':(49, 19, 129),
'Dark Pink':(106, 51, 170),
'Dusty Rose':(166, 169, 201),
'Fuchsia':(255, 0, 255),
'Millennial Pink':(198, 207, 243),
'Mulberry':(55, 7, 119),
'Neon Pink':(240, 16, 255),
'Raspberry':(92, 11, 227),
'Red Purple':(83, 53, 149),
'Rose':(106, 58, 243),
'Rose Gold':(184, 191, 224),
'Rose Red':(86, 30, 194),
'Ruby Red':(95, 17, 224),
'Watermelon Pink':(131, 115, 227),
'Bright Purple':(191, 64, 191),
'Byzantium':(99, 41, 112),
'Eggplant':(72, 50, 72),
'Light Purple':(203, 195, 227),
'Light Violet':(207, 159, 255),
'Lilac':(170, 152, 169),
'Mauve':(224, 176, 255),
'Mauve Taupe':(145, 95, 109),
'Pastel Purple':(225, 177, 195),
'Quartz':(79, 65, 81),
'Tyrian Purple':(48, 3, 99),
'Wisteria':(213, 181, 189),
'Blood Red':(8, 8, 136),
'Brick Red':(68, 74, 170),
'Bright Red':(43, 75, 238),
'Cadmium Red':(43, 43, 210),
'Carmine':(64, 0, 215),
'Cherry':(45, 4, 210),
'Falu Red':(24, 24, 123),
'Marsala':(104, 104, 152),
'Neon Red':(49, 49, 255),
'Pastel Red':(160, 160, 250),
'Scarlet':(0,36, 255),
'Venetian Red':(4, 42, 164),
'Vermillion':(52, 66, 227),
'Alabaster':(222, 234, 237),
'Bone White':(238, 246, 249),
'CornSilk':(220, 248, 255),
'Cream':(208, 256, 255),
'Eggshell':(214, 234, 240),
'Off White':(246, 249, 250),
'Parchment':(229, 245, 252),
'Vanilla':(171, 229, 243),
'Bright Yellow':(0, 234, 255),
'Cadmium Yellow':(13, 218, 253),
'Canary Yellow':(143, 255, 255),
'Dark Yellow':(0, 128, 139),
'Flax':(130, 220, 238),
'Gold Yellow':(0, 192, 255),
'Icterine':(95, 245, 252),
'Jasmine':(126, 222, 248),
'Lemon Yellow':(51, 250, 250),
'Maize':(93, 236, 251),
'Mustard Yellow':(88, 219, 255),
'Naples Yellow':(94, 218, 250),
'Pastel Yellow':(160, 255, 236),
'Saffron':(48, 196, 244),

}

# Start and end points for drawing rectangles
start_point = None
end_point = None

# Mouse callback function
def draw_rectangle(event, x, y, flags, params):
    global start_point, end_point

    if event == cv2.EVENT_LBUTTONDOWN:
        if start_point is not None:  # Reset if the start point is already set
            start_point = None
            end_point = None
            img[...] = temp_img[...]  # Restore the image to its original state

        start_point = (x, y)  # Set the drag start point

    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)  # Set the drag end point
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)  # Draw a rectangle

        # Get the mean BGR value of the selected region
        region = img[start_point[1] + 2 :end_point[1] - 2, start_point[0] + 2:end_point[0] - 2]
        mean_bgr = np.mean(region, axis=(0, 1)).astype(int)
        print(start_point[0], start_point[1], end_point[0], end_point[1])

        # Find the closest color name based on BGR values
        min_dist = float('inf')
        closest_name = None
        for color_name, color_bgr in color_mapping.items():
            dist = pow(mean_bgr[0] - color_bgr[0], 2) + pow(mean_bgr[1] - color_bgr[1], 2) + pow(mean_bgr[2] - color_bgr[2], 2)
            if dist < min_dist:
                min_dist = dist
                closest_name = color_name

        # Display the color name on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2
        text_size = cv2.getTextSize(closest_name, font, font_scale, font_thickness)[0]
        text_x = max(start_point[0], min(end_point[0] - text_size[0], img.shape[1] - text_size[0]))
        text_y = min(end_point[1] + text_size[1] + 10, img.shape[0] - 1)

        # Check if the text exceeds the right edge of the window
        if text_x + text_size[0] > img.shape[1]:
            text_x = img.shape[1] - text_size[0]

        text_position = (int(text_x), int(text_y))
        cv2.putText(img, closest_name, text_position, font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

# Load the image
image_path = sys.argv[1] if len(sys.argv) > 1 else 'rainbow.jpg'
temp_img = cv2.imread(image_path)
img = temp_img.copy()

# Set the mouse callback function
cv2.namedWindow('Color Explanation')
cv2.setMouseCallback('Color Explanation', draw_rectangle)

# Display the image
window_closed = False
while True:
    cv2.imshow('Color Explanation', img)
    key = cv2.waitKey(1)
    
    # Check if the window is closed by clicking the 'X' button
    if cv2.getWindowProperty('Color Explanation', cv2.WND_PROP_VISIBLE) < 1:
        window_closed = True
        break

    if key == 27 or key == ord('q'):  # 27 is the ASCII value for the 'Esc' key
        window_closed = True
        break

if not window_closed:
    cv2.destroyWindow('Color Explanation')