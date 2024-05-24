import tkinter as tk
from tkinter import simpledialog, messagebox

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    nama_user = simpledialog.askstring("Input", "Masukkan nama anda:")
    inp = simpledialog.askinteger("Input", "Masukkan jumlah data yang ingin dibeli:")
    data = []
    for x in range(inp):
        nama_barang = simpledialog.askstring("Input", f"Masukkan nama barang yang ingin dibeli {x+1}:")
        jumlah_beli = simpledialog.askinteger("Input", f"Masukkan jumlah barang yang ingin dibeli untuk {nama_barang}:")
        data.append([nama_barang, jumlah_beli])
    return nama_user, data

def show_info_message(title, message):
    messagebox.showinfo(title, message)

def show_error_message(title, message):
    messagebox.showerror(title, message)
