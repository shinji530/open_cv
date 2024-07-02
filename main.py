# main.py

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess  # Added subprocess module

class ColorBlindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image converter for Colorblindness")
        self.root.geometry("1200x700")

        title_label = tk.Label(self.root, text="<Image converter for Colorblindness>", font=("Helvetica", 16))
        title_label.pack(pady=150)

        start_button = tk.Button(self.root, text="Start", command=self.show_image_viewer)
        start_button.pack(side="bottom", pady=100)

    def show_image_viewer(self):
        # Display the second page of the colorblind program
        self.root.withdraw()  # Hide the current page

        # Create the second page
        image_viewer_page = tk.Toplevel(self.root)
        image_viewer_page.title("Image Viewer")

        # Initialize the image viewer
        image_viewer = ImageViewer(image_viewer_page, self.root)

        # Adjust the size of the image viewer page
        image_viewer_page.geometry("1200x700")

        # # Open file dialog to select a file
        # file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

class ImageViewer:
    def __init__(self, root, main_root):
        self.root = root
        self.main_root = main_root

        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=10, pady=10)
        self.image_label.pack_propagate(False)  # Prevent the image label from resizing

        # Add a variable to store the image file path
        self.image_path = None

        select_button = tk.Button(self.root, text="Select Image", command=self.load_image)
        select_button.pack(side="bottom", pady=100)

        button_frame = tk.Frame(self.root)
        button_frame.pack(side="top", padx=10, pady=10, anchor="nw")  # Change side to "top"

        description_button = tk.Button(button_frame, text="Color Explanation", command=self.run_color_explanation)
        description_button.pack(side="left", padx=5, pady=5)  # Set side to "left" and add padx

        filter_button = tk.Button(button_frame, text="Apply Filter", command=self.run_apply_filter)
        filter_button.pack(side="left", padx=5, pady=5)  # Set side to "left" and add padx

        # boundary_button = tk.Button(button_frame, text="Color Boundaries", command=self.show_boundary_window)
        # boundary_button.pack(side="left", padx=5, pady=5)  # Set side to "left" and add padx

        back_button = tk.Button(button_frame, text="Go Back", command=self.go_back)
        back_button.pack(side="left", padx=5, pady=5)  # Set side to "left" and add padx

        self.image_path = None  # Image file path storage variable

        # Add a BooleanVar to track the checkbox state
        self.use_contour_image_var = tk.BooleanVar(value=False)

        # Create a checkbox
        self.contour_checkbox = tk.Checkbutton(
            button_frame,
            text="contour image",
            variable=self.use_contour_image_var,
            command=self.toggle_contour_image,
        )
        self.contour_checkbox.pack(side="left", padx=5, pady=5)

    def toggle_contour_image(self):
        if self.use_contour_image_var.get():
            # Checkbox selected, run edge detection
            print("Contour image option selected.")
            
            if self.image_path:
                # Run sobel_edge_detect.py
                edge_image_path = self.run_edge_detection(self.image_path)

                # Update image label with the edge-detected image
                self.update_image_label(edge_image_path)
                self.set_image_path(edge_image_path)

        else:
            # Checkbox deselected, revert changes
            print("Contour image option deselected.")

            # Revert changes (you can implement this based on your requirements)
            # For example, you may want to show the original image again:
            if self.image_path:
                original_image_path = self.image_path.replace("_edge.", ".")

            # Update image label with the edge-detected image
            self.update_image_label(original_image_path)
            self.set_image_path(original_image_path)

    def run_edge_detection(self, image_path):
        # Run sobel_edge_detect.py file and get the edge-detected image path
        subprocess.run(["python", "sobel_edge_detect.py", image_path])
        edge_image_path = image_path.replace(".", "_edge.")
        return edge_image_path

    def update_image_label(self, image_path):
        # Load the edge-detected image and update the image label
        image = Image.open(image_path)

        # Resize the image if needed
        max_width = 600
        max_height = 600
        image.thumbnail((max_width, max_height), Image.LANCZOS)

        self.photo = ImageTk.PhotoImage(image)

        # Update the image label
        self.image_label.pack_forget()
        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack(padx=10, pady=10)
        self.image_label.pack_propagate(False)

        # Update the image path
        self.set_image_path(image_path)

    def set_image_path(self, image_path):
        self.image_path = image_path

    def load_image(self):
        # Open file dialog to select a file
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

        # Display the selected image
        if file_path:
            image = Image.open(file_path)

            # Limit the maximum size of the image
            max_width = 600
            max_height = 600

            # Resize the image
            image.thumbnail((max_width, max_height), Image.LANCZOS)

            self.photo = ImageTk.PhotoImage(image)

            # Place the image label below the button
            self.image_label.pack_forget()  # Remove the existing image label
            self.image_label = tk.Label(self.root, image=self.photo)
            self.image_label.pack(padx=10, pady=10)
            self.image_label.pack_propagate(False)  # Prevent the image label from resizing

            # Pass the image file path
            self.set_image_path(file_path)

    def run_apply_filter(self):
        if self.image_path:
            # Run ApplyFilter.py file and pass the image file path
            subprocess.run(["python", "ApplyFilter.py", self.image_path])
        else:
            # Handling when no image file is selected
            print("No image file selected.")

    def run_color_explanation(self):
        if self.image_path:
            # Run ColorExplanation.py file and pass the image file path
            subprocess.run(["python", "ColorExplanation.py", self.image_path])
        else:
            # Handling when no image file is selected
            print("No image file selected.")
    
    def show_boundary_window(self):
        if self.image_path:
            # Run sobel_edge_detect.py file and pass the image file path
            subprocess.run(["python", "sobel_edge_detect.py", self.image_path])
        else:
            # Handling when no image file is selected
            print("No image file selected.")

    def go_back(self):
        self.root.withdraw()
        self.main_root.deiconify()

class DescriptionWindow:
    def __init__(self, root, title, content):
        self.root = tk.Toplevel(root)
        self.root.title(title)

        title_label = tk.Label(self.root, text=title, font=("Helvetica", 16))
        title_label.pack(pady=20)

        content_label = tk.Label(self.root, text=content)
        content_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorBlindApp(root)
    root.mainloop()
