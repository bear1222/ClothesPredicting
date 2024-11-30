import tkinter as tk
from tkinter import filedialog
from tkinter import Label, Button, Frame
from PIL import Image, ImageTk
import predict  # Import the prediction module to use its functions

def reset_state():
    """Reset the application to its initial state."""
    image_label.config(image="", text="No image")  # Clear the image
    image_label.image = None
    price_label.config(text="$0")
    button.config(text="Upload", bg="#4a90e2", command=upload_image, state="normal")  # Change to upload button

def predict_price_action():
    """Perform prediction and update the UI with results."""
    # Disable the button while predicting
    button.config(text="Predicting...", state="disabled")
    root.update()
    
    # Get the file path from the image label
    image_path = image_label.image_path
    
    # Call the prediction function from predict.py
    img = predict.load_and_preprocess_image(image_path)
    # plt.imshow(img)
    pred = predict.predict_all(img)
    price_nn = int(predict.predict_price(pred, "nn")/100)
    # price_rf = int(predict.predict_price(pred, "rf")/100)
    
    # Display the predicted price
    price_label.config(text=f"${price_nn}00~{price_nn+1}00")
    # price_label.config(text=f"${price_nn} (NN) / ${price_rf} (RF)")

    # Enable the "Next" button after prediction
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
    img.thumbnail((350, 350))  # Resize for display in UI
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk, text="")  # Clear previous text
    image_label.image = img_tk
    image_label.image_path = file_path  # Store the file path

    # Enable the button to start prediction
    button.config(text="Predict", bg="#27ae60", command=predict_price_action, state="normal")  # Change to predict button

root = tk.Tk()
root.title("Price Prediction App")
root.geometry("800x480")
root.configure(bg="#f4f4f9")
root.resizable(False, False)

title_label = Label(
    root, text="Price Prediction App", font=("Helvetica", 18, "bold"),
    bg="#f4f4f9", fg="#333333", anchor="w", padx=10, pady=5
)
title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

main_frame = Frame(root, bg="#f4f4f9")
main_frame.grid(row=1, column=0)
main_frame.grid_propagate(False)
main_frame.config(width=400, height=380)

image_frame = Frame(main_frame, width=350, height=350, bg="#e0e0e0", relief="solid")
image_frame.place(relx=0.5, rely=0.5, anchor="center")

image_label = Label(image_frame, bg="#e0e0e0", text="No image", font=("Helvetica", 10))
image_label.place(relx=0.5, rely=0.5, anchor="center")

output_frame = Frame(root, bg="#f4f4f9")
output_frame.grid(row=1, column=1, pady=10, sticky="s")
output_frame.grid_propagate(False)
output_frame.config(width=400, height=120)
 # middle of frame
button = Button(
    output_frame, text="Upload", command=upload_image,
    width=20, bg="#4a90e2", fg="white", font=("Helvetica", 12, "bold"), relief="raised"
)
button.grid(row=1, column=0, columnspan=2, padx=100, pady=10)

price_text_label = Label(
    output_frame, text="Predicted Price:", font=("Helvetica", 16, "bold"),
    bg="#f4f4f9", fg="#333333", anchor="sw"
)
price_text_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

price_label = Label(
    output_frame, text="$0", font=("Helvetica", 16, "bold"),
    bg="#f4f4f9", fg="#333333", anchor="se"
)
price_label.grid(row=0, column=1, padx=30, pady=20, sticky="e")

root.mainloop()
