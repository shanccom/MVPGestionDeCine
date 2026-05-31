import tkinter as tk
from tkinter import messagebox, ttk

from ui.pelicula_ui import PeliculaUI
from ui.venta_ui import VentaUI


class VentanaPrincipal(ttk.Frame):
    def __init__(self, master=None):
        self._root = master or tk.Tk()
        super().__init__(self._root)
        self._root.title("Sistema de Gestion de Cine")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self._construir_ui()

    def _construir_ui(self):
        ttk.Label(
            self,
            text="Gestion de Cine",
            font=("TkDefaultFont", 12, "bold"),
        ).pack(pady=10)

        botones = ttk.Frame(self)
        botones.pack(pady=10)

        ttk.Button(botones, text="Peliculas", command=self._abrir_peliculas).grid(
            row=0, column=0, padx=5, pady=5, sticky="ew"
        )
        ttk.Button(botones, text="Salas", command=self._no_disponible).grid(
            row=0, column=1, padx=5, pady=5, sticky="ew"
        )
        ttk.Button(botones, text="Funciones", command=self._no_disponible).grid(
            row=0, column=2, padx=5, pady=5, sticky="ew"
        )
        ttk.Button(botones, text="Ventas", command=self._abrir_ventas).grid(
            row=0, column=3, padx=5, pady=5, sticky="ew"
        )

        for col in range(4):
            botones.grid_columnconfigure(col, weight=1)

        ttk.Button(self, text="Salir", command=self._root.destroy).pack(pady=10)

    def _abrir_peliculas(self):
        ventana = tk.Toplevel(self._root)
        PeliculaUI(master=ventana)

    def _abrir_ventas(self):
        ventana = tk.Toplevel(self._root)
        VentaUI(master=ventana)

    def _no_disponible(self):
        messagebox.showinfo("Modulo no disponible", "Este modulo aun no esta implementado.")


def lanzar_aplicacion():
    app = VentanaPrincipal()
    app._root.mainloop()


if __name__ == "__main__":
    lanzar_aplicacion()