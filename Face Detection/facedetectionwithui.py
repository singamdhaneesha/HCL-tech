import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import cv2
import os

class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection using OpenCV")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize variables
        self.input_image = None
        self.current_image_path = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=0, column=0, columnspan=3, pady=10)
        
        ttk.Button(btn_frame, text="Open Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Detect Faces", command=self.detect_faces).pack(side=tk.LEFT, padx=5)
        
        # Image labels
        self.image_labels = []
        self.text_labels = []
        titles = ["Input Image", "Grayscale Image", "Detected Faces"]
        
        for i in range(3):
            # Create placeholder for image
            label = ttk.Label(self.main_frame, borderwidth=2, relief="solid")
            label.grid(row=1, column=i, padx=10, pady=5)
            self.image_labels.append(label)
            
            # Create text label
            text_label = ttk.Label(self.main_frame, text=titles[i])
            text_label.grid(row=2, column=i, pady=5)
            self.text_labels.append(text_label)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var)
        status_bar.grid(row=3, column=0, columnspan=3, pady=10)
    
    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
            )
            if file_path:
                self.current_image_path = file_path
                self.input_image = cv2.imread(file_path)
                if self.input_image is None:
                    raise ValueError("Failed to load image")
                
                self.display_image(self.input_image, 0, "Input image loaded")
                self.process_grayscale()
                self.status_var.set("Image loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")
            self.status_var.set("Error loading image")
    
    def process_grayscale(self):
        if self.input_image is not None:
            gray_img = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
            self.display_image(gray_img, 1, "Grayscale conversion complete")
    
    def detect_faces(self):
        if self.input_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            # Load the face cascade classifier
            cascade_path = 'haarcascade_frontalface_default.xml'
            if not os.path.exists(cascade_path):
                raise FileNotFoundError("Haar cascade file not found")
            
            haar_cascade = cv2.CascadeClassifier(cascade_path)
            gray_img = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
            faces_rect = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=9)
            
            # Draw rectangles around detected faces
            output_image = self.input_image.copy()
            for (x, y, w, h) in faces_rect:
                cv2.rectangle(output_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            self.display_image(output_image, 2, f"Detected {len(faces_rect)} faces")
            self.status_var.set(f"Face detection complete - Found {len(faces_rect)} faces")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error detecting faces: {str(e)}")
            self.status_var.set("Error in face detection")
    
    def display_image(self, img, position, status_message=None):
        try:
            # Convert BGR to RGB for PIL
            if len(img.shape) == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_img = Image.fromarray(img)
            
            # Resize while maintaining aspect ratio
            display_size = (240, 240)
            pil_img.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_img)
            
            # Update label
            self.image_labels[position].configure(image=photo)
            self.image_labels[position].image = photo  # Keep a reference
            
            if status_message:
                self.status_var.set(status_message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {str(e)}")
            self.status_var.set("Error displaying image")

def main():
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()