import customtkinter as ctk

def createEntry(root, text, row, col, paddingX = 0, paddingY = 10, entryText = ""):
    label = ctk.CTkLabel(root, text=text, font=("Roboto", 16), text_color="#F5F5F5")
    label.grid(row=row, column=col, padx=paddingX, pady=paddingY)

    entry = ctk.CTkEntry(root, textvariable=ctk.StringVar(value=entryText))
    entry.grid(row=row, column=col+1)

    return label, entry
