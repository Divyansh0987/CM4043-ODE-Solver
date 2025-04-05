import customtkinter as ctk

def createEntry(root, text, row, col, paddingX = 0, paddingY = 20):
    label = ctk.CTkLabel(root, text=text)
    label.grid(row=row, column=col, padx=paddingX, pady=paddingY)

    entry = ctk.CTkEntry(root)
    entry.grid(row=row, column=col+1)

    return label, entry