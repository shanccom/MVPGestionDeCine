import tkinter as tk
from tkinter import messagebox, ttk

from models.pelicula import Pelicula
from services.pelicula_service import PeliculaService
from storage.peliculas.pelicula_repository import PeliculaRepository

class PeliculaUI(ttk.Frame):
    def __init__(self, master=None, service=None, repository=None):
        self._root = master or tk.Tk()
        super().__init__(self._root)
        if service is None:
            repo = repository or PeliculaRepository()
            service = PeliculaService(repository=repo)
        self._service = service
        self._titulo_seleccionado = None
        self._construir_ui()
        self._cargar_peliculas()

    def _construir_ui(self):
        self._root.title("Gestion de peliculas")
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self._id_var = tk.StringVar()
        self._titulo_var = tk.StringVar()
        self._genero_var = tk.StringVar()
        self._duracion_var = tk.StringVar()

        form = ttk.LabelFrame(self, text="Datos de pelicula")
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="ID").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._id_var, width=40, state="readonly").grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Label(form, text="Titulo").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._titulo_var, width=40).grid(
            row=1, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Label(form, text="Genero").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self._genero_combo = ttk.Combobox(
            form,
            textvariable=self._genero_var,
            values=sorted(Pelicula.GENEROS),
            state="readonly",
            width=37,
        )
        self._genero_combo.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Duracion (min)").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._duracion_var, width=40).grid(
            row=3, column=1, sticky="w", padx=5, pady=5
        )

        acciones = ttk.Frame(self)
        acciones.pack(fill="x", padx=5, pady=5)

        ttk.Button(acciones, text="Registrar", command=self._registrar).pack(
            side="left", padx=5
        )
        ttk.Button(acciones, text="Editar", command=self._actualizar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Eliminar", command=self._eliminar).pack(
            side="left", padx=5
        )
        ttk.Button(acciones, text="Limpiar", command=self._limpiar).pack(
            side="left", padx=5
        )

        tabla_frame = ttk.LabelFrame(self, text="Peliculas")
        tabla_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columnas = ("id_pelicula", "titulo", "genero", "duracion")
        self._tabla = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=12
        )
        self._tabla.heading("id_pelicula", text="ID")
        self._tabla.heading("titulo", text="Titulo")
        self._tabla.heading("genero", text="Genero")
        self._tabla.heading("duracion", text="Duracion")
        self._tabla.column("id_pelicula", width=70, anchor="center")
        self._tabla.column("titulo", width=200)
        self._tabla.column("genero", width=140)
        self._tabla.column("duracion", width=90, anchor="center")
        self._tabla.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

    def _leer_duracion(self):
        try:
            return int(self._duracion_var.get())
        except ValueError:
            raise ValueError("duracion invalida")

    def _registrar(self):
        try:
            pelicula = self._service.registrar(
                titulo=self._titulo_var.get(),
                genero=self._genero_var.get(),
                duracion=self._leer_duracion(),
            )
            self._cargar_peliculas()
            self._limpiar()
            self._id_var.set(str(pelicula.id_pelicula))
            messagebox.showinfo("Exito", "Pelicula registrada.")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def _actualizar(self):
        if not self._titulo_seleccionado:
            messagebox.showerror("Error", "Seleccione una pelicula para editar.")
            return
        try:
            pelicula = self._service.actualizar(
                self._titulo_seleccionado,
                titulo=self._titulo_var.get(),
                genero=self._genero_var.get(),
                duracion=self._leer_duracion(),
            )
            self._cargar_peliculas()
            self._titulo_seleccionado = pelicula.id_pelicula
            self._id_var.set(str(pelicula.id_pelicula))
            messagebox.showinfo("Exito", "Pelicula actualizada.")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def _eliminar(self):
        if not self._titulo_seleccionado:
            messagebox.showerror("Error", "Seleccione una pelicula para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "Desea eliminar la pelicula seleccionada?"):
            return
        try:
            self._service.eliminar(self._titulo_seleccionado)
            self._cargar_peliculas()
            self._limpiar()
            messagebox.showinfo("Exito", "Pelicula eliminada.")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def _cargar_peliculas(self):
        for item in self._tabla.get_children():
            self._tabla.delete(item)
        for pelicula in self._service.listar():
            self._tabla.insert(
                "", "end",
                values=(
                    pelicula.id_pelicula,
                    pelicula.titulo,
                    pelicula.genero,
                    pelicula.duracion,
                ),
            )

    def _seleccionar_fila(self, _event):
        seleccion = self._tabla.selection()
        if not seleccion:
            return
        valores = self._tabla.item(seleccion[0], "values")
        if not valores:
            return
        self._id_var.set(valores[0])
        self._titulo_var.set(valores[1])
        self._genero_var.set(valores[2])
        self._duracion_var.set(valores[3])
        self._titulo_seleccionado = int(valores[0])

    def _limpiar(self):
        self._id_var.set("")
        self._titulo_var.set("")
        self._genero_var.set("")
        self._duracion_var.set("")
        self._titulo_seleccionado = None
        self._tabla.selection_remove(self._tabla.selection())

def lanzar_pelicula_ui():
    ui = PeliculaUI()
    ui._root.mainloop()

if __name__ == "__main__":
    lanzar_pelicula_ui()