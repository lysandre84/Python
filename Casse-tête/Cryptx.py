#!/usr/bin/env python3
"""
=====================================================================================================================================================

  /$$$$$$                                                   /$$                 /$$              
 /$$__  $$                                                 | $$                | $$              
| $$  \__/  /$$$$$$   /$$$$$$$ /$$$$$$$  /$$$$$$          /$$$$$$    /$$$$$$  /$$$$$$    /$$$$$$ 
| $$       |____  $$ /$$_____//$$_____/ /$$__  $$ /$$$$$$|_  $$_/   /$$__  $$|_  $$_/   /$$__  $$
| $$        /$$$$$$$|  $$$$$$|  $$$$$$ | $$$$$$$$|______/  | $$    | $$$$$$$$  | $$    | $$$$$$$$
| $$    $$ /$$__  $$ \____  $$\____  $$| $$_____/          | $$ /$$| $$_____/  | $$ /$$| $$_____/
|  $$$$$$/|  $$$$$$$ /$$$$$$$//$$$$$$$/|  $$$$$$$          |  $$$$/|  $$$$$$$  |  $$$$/|  $$$$$$$
 \______/  \_______/|_______/|_______/  \_______/           \___/   \_______/   \___/   \_______/
                                                                                                 
                                                                                                                                                                                  
=====================================================================================================================================================
=====================================================================================================================================================
 Script     : Cryptx.py
 Auteur     : Lysius
 Date       : 21/06/2024
 Description: Ce script propose une interface graphique (Tkinter) permettant de déchiffrer
                un message chiffré en deux étapes :
                1) Vigenère (clé de 6 lettres)
                2) Affine (a = 5, b = 8)
                L’utilisateur saisit un mot-clé Vigenère et obtient le texte clair.
=====================================================================================================================================================
"""
import string
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# --- Constantes du cryptosystème ---
ALPHABET = string.ascii_uppercase
MOD = 26
CIPHERTEXT = (
    "OYGOH QCMMJ DIYYX QYGCI UGNOF NUJQX\n"
    "FPUBH OLUJQ DOSGU NQQSB OIRMT DBQQR\n"
    "SSCKY BX"
)
A = 5  # Coefficient affine
B = 8  # Décalage affine


def affine_decrypt(text: str, a: int = A, b: int = B) -> str:
    """
    Déchiffrement affine : P = a^{-1} * (C - b) mod 26
    Retourne le texte clair en majuscules, préservant espaces et sauts de ligne.
    """
    a_inv = pow(a, -1, MOD)
    result = []
    for ch in text:
        if ch in ALPHABET:
            idx = ALPHABET.index(ch)
            p = (a_inv * (idx - b)) % MOD
            result.append(ALPHABET[p])
        else:
            result.append(ch)
    return "".join(result)


def vigenere_decrypt(text: str, key: str) -> str:
    """
    Déchiffrement Vigenère simple : C - k_i mod 26
    La clé doit contenir exactement 6 lettres (A–Z).
    """
    key = key.upper()
    if len(key) != 6 or not key.isalpha():
        raise ValueError("Clé Vigenère invalide (6 lettres requises)")

    result = []
    for i, ch in enumerate(text.replace("\n", "")):
        if ch in ALPHABET:
            shift = ALPHABET.index(key[i % len(key)])
            p = (ALPHABET.index(ch) - shift) % MOD
            result.append(ALPHABET[p])
        else:
            result.append(ch)
    return "".join(result)


class CryptXPuzzleApp(tk.Tk):
    """
    Application Tkinter pour résoudre le cryptopuzzle.
    """
    BG = "#1e1e2f"
    FG = "#ffffff"
    ACCENT = "#4a90e2"

    def __init__(self) -> None:
        super().__init__()
        self.title("CryptX – Code secret")
        self.geometry("780x560")
        self.resizable(False, False)
        self.configure(bg=self.BG)
        self._setup_styles()
        self._build_widgets()

    def _setup_styles(self) -> None:
        """Configuration du thème et des styles ttk."""
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG)
        style.configure("TLabel", background=self.BG, foreground=self.FG)
        style.configure(
            "TButton", background=self.ACCENT, foreground=self.FG,
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "TButton",
            background=[("active", "#357ab7")],
            foreground=[("active", self.FG)]
        )
        style.configure(
            "TEntry", fieldbackground="#2e2e3f",
            foreground=self.FG, insertcolor=self.FG
        )

    def _build_widgets(self) -> None:
        """Construire l’interface utilisateur."""
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        ttk.Label(
            container,
            text="CryptX – Code secret",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(0, 10))

        # Cadre du message chiffré
        ttk.Label(container, text="Texte chiffré :").pack(anchor="w")
        self.cipher_box = scrolledtext.ScrolledText(
            container, height=4, font=("Consolas", 11)
        )
        self.cipher_box.insert("1.0", CIPHERTEXT)
        self.cipher_box.configure(state="disabled")
        self.cipher_box.pack(fill="x", pady=(0, 10))

        # Entrée de la clé et boutons
        entry_frame = ttk.Frame(container)
        entry_frame.pack(anchor="w", pady=(0, 10))
        ttk.Label(
            entry_frame,
            text="Clé Vigenère (6 lettres) :"
        ).grid(row=0, column=0)
        self.key_entry = ttk.Entry(entry_frame, width=10)
        self.key_entry.grid(row=0, column=1, padx=5)
        ttk.Button(
            entry_frame,
            text="Déchiffrer",
            command=self._on_decrypt
        ).grid(row=0, column=2, padx=5)
        ttk.Button(
            entry_frame,
            text="Indice",
            command=self._show_hint
        ).grid(row=0, column=3, padx=5)

        # Résultat
        ttk.Label(container, text="Résultat :").pack(anchor="w")
        self.output_box = scrolledtext.ScrolledText(
            container, height=8, font=("Consolas", 11)
        )
        self.output_box.configure(state="disabled")
        self.output_box.pack(fill="both", expand=True)

        # Signature
        tk.Label(
            self,
            text="created by Lysius",
            bg=self.BG, fg="#ff003c",
            font=("Segoe UI", 9, "italic")
        ).place(relx=1.0, rely=1.0, x=-8, y=-6, anchor="se")

    def _on_decrypt(self) -> None:
        """Gestion du clic sur le bouton 'Déchiffrer'."""
        key = self.key_entry.get().strip()
        try:
            intermediate = affine_decrypt(CIPHERTEXT.replace("\n", ""))
            clear_text = vigenere_decrypt(intermediate, key)
        except ValueError as e:
            messagebox.showwarning("Clé invalide", str(e))
            return

        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, clear_text)
        self.output_box.configure(state="disabled")

    def _show_hint(self) -> None:
        """Affiche une fenêtre d'indice."""
        messagebox.showinfo(
            "Indice",
            "Regarde la signature rouge en bas à droite."
        )


if __name__ == "__main__":
    app = CryptXPuzzleApp()
    app.mainloop()