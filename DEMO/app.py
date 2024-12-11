import tkinter as tk
from tkinter import filedialog
from tkinter import Label, Button, Frame
from PIL import Image, ImageTk, ImageOps
import predict

def reset_state():
    """Reset the application to its initial state."""
    image_label.config(image="", text="No image")
    image_label.image = None
    price_label.config(text="$0")
    button.config(text="Upload", bg="#4a90e2", command=upload_image, state="normal")

def switch_model():
    """Switch the model type between 'nn' and 'rf'."""
    current_model = model_button.config('text')[-1]
    new_model = "RF" if current_model == "NN" else "NN"
    model_button.config(text=new_model)

def predict_price_action():
    """Perform prediction and update the UI with results."""
    button.config(text="Predicting...", state="disabled")
    root.update()
    
    image_path = image_label.image_path
    
    model_type = model_button.config('text')[-1]
    
    img = predict.load_and_preprocess_image(image_path)
    pred = predict.predict_all(img)
    price = int(predict.predict_price(pred, model_type)/100)
    
    price_label.config(text=f"${price}00~{price+1}00")

    button.config(text="Next", bg="#e67e22", command=reset_state, state="normal")

def upload_image():
    """Open an image, display it, and prepare for prediction."""
    button.config(text="Uploading...", state="disabled")
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        button.config(text="Upload", bg="#4a90e2", state="normal")
        return

    img = Image.open(file_path)

    # Correct image orientation based on EXIF data
    try:
        img = ImageOps.exif_transpose(img)
    except AttributeError:
        # If the image has no EXIF data, do nothing
        pass

    img.thumbnail((350, 350))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk, text="")
    image_label.image = img_tk
    image_label.image_path = file_path

    button.config(text="Predict", bg="#27ae60", command=predict_price_action, state="normal")

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
output_frame.grid(row=1, column=1, sticky="s")
output_frame.grid_propagate(False)
output_frame.config(width=400, height=120)

button_frame = Frame(output_frame, bg="#f4f4f9")
button_frame.grid(row=1, column=0)
button_frame.grid_propagate(False)
button_frame.config(width=400, height=60)

button = Button(
    button_frame, text="Upload", command=upload_image,
    width=20, bg="#4a90e2", fg="white", font=("Helvetica", 12, "bold"), relief="raised"
)
button.grid(row=0, column=0, padx=(80, 10), pady=10)

model_button = Button(
    button_frame, text="NN", command=switch_model,
    width=3, bg="black", fg="white", font=("Helvetica", 8, "bold"), relief="raised"
)
model_button.grid(row=0, column=1, pady=10)

price_frame = Frame(output_frame, bg="#f4f4f9")
price_frame.grid(row=0, column=0)
price_frame.grid_propagate(False)
price_frame.config(width=400, height=60)

price_frame.columnconfigure(0, weight=1)
price_frame.columnconfigure(1, weight=0)

price_text_label = Label(
    price_frame, text="Predicted Price:", font=("Helvetica", 16, "bold"),
    bg="#f4f4f9", fg="#333333"
)
price_text_label.grid(row=0, column=0, padx=10, pady=20, sticky="w")

price_label = Label(
    price_frame, text="$0", font=("Helvetica", 16, "bold"),
    bg="#f4f4f9", fg="#333333"
)
price_label.grid(row=0, column=1, padx=20, pady=20, sticky="e")

root.mainloop()
