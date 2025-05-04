import qrcode
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Encoder/Decoder")
        self.root.geometry("400x300")
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)
        
        # Create buttons
        tk.Button(
            self.main_frame, 
            text="Encode Text to QR Code", 
            command=self.encode_text,
            width=25,
            height=2
        ).pack(pady=10)
        
        tk.Button(
            self.main_frame, 
            text="Decode QR Code from File", 
            command=self.decode_qr,
            width=25,
            height=2
        ).pack(pady=10)
        
        tk.Button(
            self.main_frame, 
            text="Exit", 
            command=root.quit,
            width=25,
            height=2
        ).pack(pady=10)
    
    def encode_text(self):
        text = simpledialog.askstring("Input", "Enter text to encode in QR code:")
        if text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save QR Code As"
            )
            
            if file_path:
                img.save(file_path)
                messagebox.showinfo("Success", f"QR code saved at:\n{file_path}")
    
    def decode_qr(self):
        file_path = filedialog.askopenfilename(
            title="Select QR Code Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                img = cv2.imread(file_path)
                detector = cv2.QRCodeDetector()
                val, _, _ = detector.detectAndDecode(img)
                
                if val:
                    messagebox.showinfo("Decoded Text", f"Decoded text:\n\n{val}")
                else:
                    messagebox.showerror("Error", "No QR code found or could not decode.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decode:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()