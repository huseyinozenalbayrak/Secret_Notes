import tkinter as tk
from tkinter import messagebox
import base64

FONT = ("Arial", 14, "normal")

# implements message encoding
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

# implements message decoding
def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

# If the all info is entered, it creates a file called my secrets.txt and writes the entered secret message in
# encrypted form to that file. If not, it shows an error message to the user.
def save_and_encrypt():
    if secret_text.get("1.0", tk.END).lstrip() != "" and title_entry.get().lstrip() != "" and master_key_entry.get().lstrip() != "":
        title = title_entry.get()
        message = secret_text.get("1.0", tk.END)
        master_key = master_key_entry.get()
        encrypted_message = encode(master_key, message)
        try:
            with open("my_secrets.txt", mode="a") as data_file:
                data_file.write(f"\n{title}\n{encrypted_message}")
        except FileNotFoundError:
            with open("my_secrets.txt", mode="w") as data_file:
                data_file.write(f"\n{title}\n{encrypted_message}")
        finally:
            title_entry.delete(0, tk.END)
            secret_text.delete("1.0", tk.END)
            master_key_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter all info!")

# decrypts the encrypted message if the master key is true
def decrypt():
    if secret_text.get("1.0",  tk.END).lstrip() != "" and master_key_entry.get().lstrip() != "":
        encrypted_message = secret_text.get("1.0", tk.END)
        master_key = master_key_entry.get()
        try:
            decrypted_message = decode(master_key, encrypted_message)
            master_key_entry.delete(0, tk.END)
            secret_text.delete("1.0", tk.END)
            secret_text.insert("1.0", decrypted_message)
        except:
            messagebox.showwarning("Error!", "Please enter encrypted text!")
    else:
        messagebox.showwarning("Warning", "Please enter all info!")


# user interface
win = tk.Tk()
win.geometry("500x550")
win.title("Secret Notes")
win.config(padx=20, pady=20)


title_label = tk.Label(text="Enter your title", pady=5, font=FONT)
title_label.pack()

title_entry = tk.Entry()
title_entry.pack()

secret_label = tk.Label(text="Enter your secret", pady=5, font=FONT)
secret_label.pack()

secret_text = tk.Text(width=60, height=20)
secret_text.pack()

master_key_label = tk.Label(text="Enter master key", pady=5,font=FONT)
master_key_label.pack()

master_key_entry = tk.Entry()
master_key_entry.pack()

save_encrypt_button = tk.Button(text="Save & Encrypt", font=FONT, command= save_and_encrypt)
save_encrypt_button.pack()

decrypt_button = tk.Button(text="Decrypt", font=FONT, fg="red", bg="gray", command=decrypt)
decrypt_button.pack()


tk.mainloop()