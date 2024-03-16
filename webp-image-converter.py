# Author: Vilgefortz
# Software description: Converts images to webp extension
# Contact: vilgefortzsrb@gmail.com

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import subprocess
from PIL import Image

# Global variable to store the folder path
folder_path = ""


def choose_folder():
    global folder_path  # Use the global folder_path variable
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_list = os.listdir(folder_path)
        tree.delete(*tree.get_children())  # Clear previous content
        total_images_count = len(file_list)
        total_png_count = sum(1 for file in file_list if file.lower().endswith('.png'))
        total_jpg_count = sum(1 for file in file_list if file.lower().endswith('.jpg'))

        for file in file_list:
            file_name, file_type = os.path.splitext(file)
            tree.insert("", tk.END, values=(file_name, file_type))

        # Update labels
        total_images_label.configure(text=f"Total images: {total_images_count}")
        total_png_label.configure(text=f"Total PNG images: {total_png_count}")
        total_jpg_label.configure(text=f"Total JPG images: {total_jpg_count}")

        # Show labels
        total_images_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        total_png_label.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")
        total_jpg_label.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")


def open_image(event):
    global folder_path  # Use the global folder_path variable
    item = tree.selection()[0]
    image_name = tree.item(item, "values")[0]  # Get the name of the image
    image_type = tree.item(item, "values")[1]  # Get the type of the image
    if folder_path and image_name:
        image_path = os.path.join(folder_path, f"{image_name}{image_type}")  # Get full path of the image
        image_path = image_path.replace("\\", "/")  # Replace backslashes with forward slashes
        print("Image path:", image_path)  # Print the image path
        if os.path.isfile(image_path):
            # Open the image using the default application
            os.startfile(image_path)


def convert_to_webp():
    global folder_path
    if not folder_path:
        messagebox.showerror("Error", "Please choose a folder first.")
        return

    # Ask user to select the destination folder
    destination_folder = filedialog.askdirectory()
    if not destination_folder:
        return  # User canceled the operation

    converted_count = 0  # Counter for the number of images converted
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            # Check if the file is a PNG or JPG image
            if file_name.lower().endswith('.png') or file_name.lower().endswith('.jpg'):
                # Open the image
                with Image.open(file_path) as img:
                    # Convert the image to WebP format
                    webp_path = os.path.join(destination_folder, os.path.splitext(file_name)[0] + ".webp")
                    img.save(webp_path, "WEBP")
                    converted_count += 1

    # Show conversion complete message
    messagebox.showinfo("Info", f"Conversion complete. {converted_count} image(s) converted.")


def set_treeview_style():
    style = ttk.Style()
    style.theme_use("default")  # Use the default theme
    style.configure("Treeview.Heading", background="lightgreen")  # Change the background color of the header


# Create the main window
root = tk.Tk()
root.title("Webp image converter")

# Set default width and height
window_width = 800
window_height = 500

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates for the Tk root window
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)

# Set the width and height of the window
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Create a button widget
choose_button = tk.Button(root, text="Choose", command=choose_folder, width=10, height=2)
choose_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Name", "Type"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Type", text="Type")
tree.column("Name", width=540, stretch=tk.NO)  # Adjust the width of the first column
tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Create a scrollbar widget
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.grid(row=1, column=1, sticky="ns")

# Configure the Treeview to use the scrollbar
tree.config(yscrollcommand=scrollbar.set)

# Apply custom style to the Treeview header
set_treeview_style()

# Create labels to display total number of images, PNG images, and JPEG images
total_images_label = tk.Label(root, text="Total images:")
total_png_label = tk.Label(root, text="Total PNG images:")
total_jpg_label = tk.Label(root, text="Total JPG images:")

# Create a button to convert to WebP
convert_button = tk.Button(root, command=convert_to_webp, text="Convert to Webp", bg="red", fg="white",
                           activebackground="red", activeforeground="white")
convert_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

# Bind double-click event to open_image function
tree.bind("<Double-1>", open_image)

# Run the event loop
root.mainloop()
