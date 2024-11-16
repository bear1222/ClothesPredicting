import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Your model function here. For demonstration, we'll just print that an image is being processed.
def model_process(image):
    print("Model is processing the image...")

# Function to upload and display the image
def upload_image():
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )

    if file_path:
        # Open and display the image
        image = Image.open(file_path)
        image.thumbnail((300, 300))  # Resize for display purposes
        img_display = ImageTk.PhotoImage(image)
        
        # Update the label with the image
        image_label.config(image=img_display)
        image_label.image = img_display
        
        # Send the image to your model
        model_process(image)

# Set up the main Tkinter window
root = tk.Tk()
root.title("Image Upload for Model")

# Label to display the selected image
image_label = tk.Label(root)
image_label.pack()

# Button to upload an image
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

# Run the Tkinter main loop
root.mainloop()
