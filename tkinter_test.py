import tkinter as tk
from tkinter import filedialog
from tkinter import Label, Button, Frame
from PIL import Image, ImageTk
import numpy as np

def preprocess_image(image_path):
    """Preprocess the image to match the input shape of the model."""
    image = Image.open(image_path).resize((224, 224))  # Adjust size to your model's requirement
    image_array = np.array(image) / 255.0  # Normalize the image
    return np.expand_dims(image_array, axis=0)  # Add batch dimension

def reset_state():
    """Reset the application to its initial state."""
    image_label.config(image="", text="Preview Area")  # Clear the image
    image_label.image = None
    price_label.config(text="Predicted Price: $0.00")
    button.config(text="Upload", bg="#4a90e2", command=upload_image, state="normal")  # Change to upload button

def predict_price_action():
    """Perform prediction and update the UI with results."""
    # Disable the button while predicting
    button.config(text="Predicting...", state="disabled")
    # Replace the next line with your model prediction logic
    price_label.config(text="Predicted Price: $123.45")  # Example predicted price
    button.config(text="Next", bg="#e67e22", command=reset_state, state="normal")  # Change to next button

def upload_image():
    """Open an image, display it, and prepare for prediction."""
    # Disable the button while uploading
    button.config(text="Uploading...", state="disabled")
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        button.config(text="Upload", bg="#4a90e2", state="normal")  # Reset button if no file selected
        return

    # Display the selected image
    img = Image.open(file_path)
    img.thumbnail((300, 300))  # Resize for display in UI
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk, text="")  # Clear previous text
    image_label.image = img_tk

    # Enable the button to start prediction
    button.config(text="Predict", bg="#27ae60", command=predict_price_action, state="normal")  # Change to predict button

# Create the main window
root = tk.Tk()
root.title("Price Prediction App")
root.geometry("800x480")
root.configure(bg="#f4f4f9")  # Set background color
root.resizable(False, False)

# Title at the top-left with style
title_label = Label(
    root, text="Price Prediction App", font=("Helvetica", 18, "bold"),
    bg="#f4f4f9", fg="#333333", anchor="w", padx=10, pady=5
)
title_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=10)

# Main frame for image preview
main_frame = Frame(root, bg="#f4f4f9")  # Remove white background
main_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="n", ipadx=5, ipady=5)
main_frame.grid_propagate(False)  # Prevent resizing based on children
main_frame.config(width=350, height=380)  # Fixed size

# Image preview area with fixed size
image_frame = Frame(main_frame, width=300, height=300, bg="#e0e0e0", relief="solid")
image_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame within main_frame

image_label = Label(image_frame, bg="#e0e0e0", text="Preview Area", font=("Helvetica", 10))
image_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the image within the frame

# Output frame for results and buttons (positioned at the bottom-right)
output_frame = Frame(root, bg="#f4f4f9")  # Remove white background
output_frame.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="se", ipadx=5, ipady=5)
output_frame.grid_propagate(False)  # Prevent resizing based on children
output_frame.config(width=350, height=380)  # Fixed size

# Shared button for all actions
button = Button(
    output_frame, text="Upload", command=upload_image,
    width=20, bg="#4a90e2", fg="white", font=("Helvetica", 12, "bold"), relief="raised"
)
button.pack(side="bottom", pady=20, anchor="se")

# Predicted price label with fixed width
price_label = Label(
    output_frame, text="Predicted Price: $0.00", font=("Helvetica", 16, "bold"),
    bg="#f4f4f9", fg="#333333", pady=10, width=30, anchor="w", justify="left"
)
price_label.pack(side="bottom", anchor="se")

# Run the application
root.mainloop()
