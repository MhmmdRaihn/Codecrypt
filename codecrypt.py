import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

def vig_enc(text, key):
    key = key.upper()
    text = text.upper()
    enc = []
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            shift = ord(key[i % len(key)]) - ord('A')
            enc.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            enc.append(char)
    return ''.join(enc)

def vig_dec(text, key):
    key = key.upper()
    text = text.upper()
    dec = []
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            shift = ord(key[i % len(key)]) - ord('A')
            dec.append(chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A')))
        else:
            dec.append(char)
    return ''.join(dec)

def playf_enc(text, key):
    text = text.upper().replace("J", "I")
    key = ''.join(sorted(set(key), key=lambda x: key.index(x))) 
    matrix = create_playfair_matrix(key)
    
    processed_text = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                b = 'X'
            else:
                i += 1
        else:
            b = 'X'
        processed_text.append(enc_pair(a, b, matrix))
        i += 1
    
    return ''.join(processed_text)

def playf_dec(text, key):
    text = text.upper().replace("J", "I")
    key = ''.join(sorted(set(key), key=lambda x: key.index(x)))
    matrix = create_playfair_matrix(key)
    
    processed_text = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                b = 'X'
            else:
                i += 1
        else:
            b = 'X'
        processed_text.append(dec_pair(a, b, matrix))
        i += 1
    
    return ''.join(processed_text)

def create_playfair_matrix(key):
    matrix = []
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    used = set()
    for char in key:
        if char not in used and char in alphabet:
            used.add(char)
            matrix.append(char)
    for char in alphabet:
        if char not in used:
            used.add(char)
            matrix.append(char)
    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def enc_pair(a, b, matrix):
    pos_a = find_position(a, matrix)
    pos_b = find_position(b, matrix)
    if pos_a[0] == pos_b[0]: 
        return matrix[pos_a[0]][(pos_a[1] + 1) % 5] + matrix[pos_b[0]][(pos_b[1] + 1) % 5]
    elif pos_a[1] == pos_b[1]: 
        return matrix[(pos_a[0] + 1) % 5][pos_a[1]] + matrix[(pos_b[0] + 1) % 5][pos_b[1]]
    else: 
        return matrix[pos_a[0]][pos_b[1]] + matrix[pos_b[0]][pos_a[1]]

def dec_pair(a, b, matrix):
    pos_a = find_position(a, matrix)
    pos_b = find_position(b, matrix)
    if pos_a[0] == pos_b[0]:  
        return matrix[pos_a[0]][(pos_a[1] - 1) % 5] + matrix[pos_b[0]][(pos_b[1] - 1) % 5]
    elif pos_a[1] == pos_b[1]:  
        return matrix[(pos_a[0] - 1) % 5][pos_a[1]] + matrix[(pos_b[0] - 1) % 5][pos_b[1]]
    else: 
        return matrix[pos_a[0]][pos_b[1]] + matrix[pos_b[0]][pos_a[1]]

def find_position(char, matrix):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return (i, j)
    return None


def hill_enc(text, key):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X'  
    matrix_key = [[ord(key[0]) - 65, ord(key[1]) - 65],
                   [ord(key[2]) - 65, ord(key[3]) - 65]]
    
    enc_text = []
    for i in range(0, len(text), 2):
        vector = [[ord(text[i]) - 65],
                  [ord(text[i + 1]) - 65]]
        result = matrix_multiply(matrix_key, vector)
        enc_text.append(chr(result[0][0] + 65))
        enc_text.append(chr(result[1][0] + 65))
    
    return ''.join(enc_text)

def hill_dec(text, key):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X' 
    matrix_key = [[ord(key[0]) - 65, ord(key[1]) - 65],
                   [ord(key[2]) - 65, ord(key[3]) - 65]]
    
    det = (matrix_key[0][0] * matrix_key[1][1] - matrix_key[0][1] * matrix_key[1][0]) % 26
    inv_det = mod_inverse(det, 26)
    
    if inv_det is None:
        return "Key Hill Cipher Invalid"

    adjugate = [[matrix_key[1][1], -matrix_key[0][1]],
                [-matrix_key[1][0], matrix_key[0][0]]]
    
    inverse_key = [[(inv_det * adjugate[0][0]) % 26, (inv_det * adjugate[0][1]) % 26],
                   [(inv_det * adjugate[1][0]) % 26, (inv_det * adjugate[1][1]) % 26]]
    
    dec_text = []
    for i in range(0, len(text), 2):
        vector = [[ord(text[i]) - 65],
                  [ord(text[i + 1]) - 65]]
        result = matrix_multiply(inverse_key, vector)
        dec_text.append(chr(result[0][0] + 65))
        dec_text.append(chr(result[1][0] + 65))
    
    return ''.join(dec_text)

def matrix_multiply(matrix, vector):
    result = [[0], [0]]
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i][0] += matrix[i][j] * vector[j][0]
    return [[x % 26 for x in row] for row in result]

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def enc():
    text = input_text.get("1.0", tk.END).strip().upper()
    key = key_entry.get().strip().upper()
    
    if len(key) < 12:
        messagebox.showwarning("Error", "Minimal Key 12 karakter.")
        return
    
    cipher_type = cipher_var.get()
    if cipher_type == "Vigenere":
        result = vig_enc(text, key)
    elif cipher_type == "Playfair":
        result = playf_enc(text, key)
    elif cipher_type == "Hill":
        result = hill_enc(text, key[:4])
    else:
        result = "Pilih metode enkripsi yang valid."
    
    disp_text.delete("1.0", tk.END)
    disp_text.insert(tk.END, result)

def dec():
    text = input_text.get("1.0", tk.END).strip().upper()
    key = key_entry.get().strip().upper()

    if len(key) < 12:
        messagebox.showwarning("Error","Minimal Key adalah 12 karakter.")
        return

    cipher_type = cipher_var.get()
    if cipher_type == "Vigenere":
        result = vig_dec(text, key)
    elif cipher_type == "Playfair":
        result = playf_dec(text, key)
    elif cipher_type == "Hill":
        result = hill_dec(text, key[:4])  
    else:
        result = "Pilih metode dekripsi yang valid."

    disp_text.delete("1.0", tk.END)
    disp_text.insert(tk.END, result)

def load_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", ".txt")])
    if file_path:
        with open(file_path, 'r') as file:
            file_content = file.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file_content)

window = tk.Tk()
window.title("Codecrypt")

input_text = scrolledtext.ScrolledText(window, width=40, height=10)
input_text.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

tk.Label(window, text="Masukkan Kunci:").grid(column=0, row=1)
key_entry = tk.Entry(window, width=40)
key_entry.grid(column=1, row=1, padx=10, pady=10)

cipher_var = tk.StringVar(window)
cipher_var.set("Vigenere") 
cipher_menu = tk.OptionMenu(window, cipher_var, "Vigenere", "Playfair", "Hill")
cipher_menu.grid(column=0, row=2, padx=10, pady=10)


disp_button = tk.Button(window, text="Encrypt", command=enc)
disp_button.grid(column=0, row=3, padx=10, pady=10)

dec_button = tk.Button(window, text="Decrypt", command=dec)
dec_button.grid(column=1, row=3, padx=10, pady=10)

load_button = tk.Button(window, text="Unggah File", command=load_from_file)
load_button.grid(column=1, row=2, padx=10, pady=10, columnspan=2)

disp_text = scrolledtext.ScrolledText(window, width=40, height=10)
disp_text.grid(column=0, row=6, padx=10, pady=10, columnspan=2)

window.mainloop()
