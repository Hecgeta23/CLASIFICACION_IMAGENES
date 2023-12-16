import tkinter as tk
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
import os

class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CAPTURA Y CLASIFICACION DE IMAGENES")
        self.root.configure(bg="#FFFFFF")

        self.header_label = tk.Label(root, text="CAPTURA Y CLASIFICACION DE IMAGENES", font=("Arial", 18, "bold"), bg="#FFFFFF")
        self.header_label.pack(pady=20)

        self.buttons_frame = tk.Frame(root, bg="#FFFFFF")
        self.buttons_frame.pack()

        self.capture_button = tk.Button(self.buttons_frame, text="CAPTURAR CONTINUAMENTE", command=self.start_continuous_capture, bg="#BDBDBD", fg="black", font=("Arial", 12))
        self.capture_button.grid(row=0, column=0, padx=10, pady=5)

        self.stop_button = tk.Button(self.buttons_frame, text="DETENER CAPTURA", command=self.stop_continuous_capture, bg="#BDBDBD", fg="black", font=("Arial", 12))
        self.stop_button.grid(row=0, column=1, padx=10, pady=5)
        self.stop_button.config(state=tk.DISABLED)

        self.show_button = tk.Button(root, text="MOSTRAR IMAGENES", command=self.show_image, bg="#BDBDBD", fg="black", font=("Arial", 12))
        self.show_button.pack(pady=10)
        self.show_button.config(state=tk.DISABLED)

        self.classify_label = tk.Label(root, text="CLASIFICAR IMAGENES COMO:", font=("Arial", 14), bg="#FFFFFF")
        self.classify_label.pack()

        self.classify_buttons_frame = tk.Frame(root, bg="#FFFFFF")
        self.classify_buttons_frame.pack()

        self.classify_a_button = tk.Button(self.classify_buttons_frame, text="A", command=lambda: self.classify_image('A'), bg="#BDBDBD", fg="white", font=("Arial", 12))
        self.classify_a_button.grid(row=0, column=0, padx=10, pady=5)
        self.classify_a_button.config(state=tk.DISABLED)

        self.classify_b_button = tk.Button(self.classify_buttons_frame, text="B", command=lambda: self.classify_image('B'), bg="#BDBDBD", fg="white", font=("Arial", 12))
        self.classify_b_button.grid(row=0, column=1, padx=10, pady=5)
        self.classify_b_button.config(state=tk.DISABLED)

        self.images = []
        self.current_index = 0
        self.is_continuous = False

        self.image_label = tk.Label(root, bg="white", borderwidth=2, relief="groove")
        self.image_label.pack(pady=10)

        self.filename_label = tk.Label(root, font=("Arial", 12), bg="#FFFFFF")
        self.filename_label.pack()

    def capture_screen(self):
        filename = f"screenshot_{len(self.images)}.png"
        im = ImageGrab.grab()
        im.save(filename)
        self.images.append(filename)

    def start_continuous_capture(self):
        self.is_continuous = True
        self.capture_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.show_button.config(state=tk.DISABLED)
        self.classify_a_button.config(state=tk.DISABLED)
        self.classify_b_button.config(state=tk.DISABLED)
        self.continuous_capture()

    def stop_continuous_capture(self):
        self.is_continuous = False
        self.capture_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.current_index < len(self.images):
            self.show_button.config(state=tk.NORMAL)

    def continuous_capture(self):
        if self.is_continuous:
            self.capture_screen()
            self.root.after(1000, self.continuous_capture)

    def show_image(self):
        if self.current_index < len(self.images):
            img = Image.open(self.images[self.current_index])
            img.thumbnail((400, 400))  # Redimensiona la imagen
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.filename_label.config(text=self.images[self.current_index])
            self.classify_a_button.config(state=tk.NORMAL)
            self.classify_b_button.config(state=tk.NORMAL)

    def classify_image(self, category):
        if self.current_index < len(self.images):
            if not os.path.exists(category):
                os.makedirs(category)
            os.rename(self.images[self.current_index], os.path.join(category, self.images[self.current_index]))
            self.current_index += 1
            self.image_label.config(image="")
            self.filename_label.config(text="")
            if self.current_index < len(self.images):
                self.show_image()
            else:
                self.show_button.config(state=tk.DISABLED)
                self.classify_a_button.config(state=tk.DISABLED)
                self.classify_b_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

