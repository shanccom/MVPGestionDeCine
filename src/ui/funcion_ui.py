import tkinter as tk
from tkinter import messagebox, ttk

from services.funcion_service import FuncionService
from storage.peliculas.pelicula_repository import PeliculaRepository
from storage.salas.sala_repository import SalaRepository


class FuncionUI(ttk.Frame):
    def __init__(
        self,
        master=None,
        service=None,
        pelicula_repository=None,
        sala_repository=None,
    ):
        self._root = master or tk.Tk()
        super().__init__(self._root)
        self._service = service or FuncionService()
        self._pelicula_repo = pelicula_repository or PeliculaRepository()
        self._sala_repo = sala_repository or SalaRepository()
        self._id_seleccionado = None
        self._peliculas_por_opcion = {}
        self._opcion_pelicula_por_id = {}
        self._salas_por_opcion = {}
        self._opcion_sala_por_id = {}
        self._cargar_catalogos()
        self._construir_ui()
        self._cargar_funciones()

    def _construir_ui(self):
        self._root.title("Gestion de funciones")
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self._id_var = tk.StringVar()
        self._pelicula_var = tk.StringVar()
        self._sala_var = tk.StringVar()
        self._fecha_var = tk.StringVar()
        self._hora_var = tk.StringVar()
        self._precio_var = tk.StringVar()

        form = ttk.LabelFrame(self, text="Datos de funcion")
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="ID").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._id_var, width=40, state="readonly").grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Label(form, text="Pelicula").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self._pelicula_combo = ttk.Combobox(
            form,
            textvariable=self._pelicula_var,
            values=list(self._peliculas_por_opcion.keys()),
            state="readonly",
            width=37,
        )
        self._pelicula_combo.grid(
            row=1, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Label(form, text="Sala").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self._sala_combo = ttk.Combobox(
            form,
            textvariable=self._sala_var,
            values=list(self._salas_por_opcion.keys()),
            state="readonly",
            width=37,
        )
        self._sala_combo.grid(
            row=2, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Label(form, text="Fecha").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._fecha_var, width=40).grid(
            row=3, column=1, sticky="w", padx=5, pady=5
        )
        ttk.Label(form, text="yyyy-mm-dd").grid(row=3, column=2, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Hora").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._hora_var, width=40).grid(
            row=4, column=1, sticky="w", padx=5, pady=5
        )
        ttk.Label(form, text="hh:mm").grid(row=4, column=2, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Precio").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._precio_var, width=40).grid(
            row=5, column=1, sticky="w", padx=5, pady=5
        )

        acciones = ttk.Frame(self)
        acciones.pack(fill="x", padx=5, pady=5)

        ttk.Button(acciones, text="Registrar", command=self._registrar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Editar", command=self._actualizar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Eliminar", command=self._eliminar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Listar", command=self._cargar_funciones).pack(side="left", padx=5)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar).pack(side="left", padx=5)

        tabla_frame = ttk.LabelFrame(self, text="Funciones")
        tabla_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columnas = ("id_funcion", "pelicula", "sala", "fecha", "hora", "precio")
        self._tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        self._tabla.heading("id_funcion", text="ID")
        self._tabla.heading("pelicula", text="Pelicula")
        self._tabla.heading("sala", text="Sala")
        self._tabla.heading("fecha", text="Fecha")
        self._tabla.heading("hora", text="Hora")
        self._tabla.heading("precio", text="Precio")
        self._tabla.column("id_funcion", width=70, anchor="center")
        self._tabla.column("pelicula", width=180)
        self._tabla.column("sala", width=140)
        self._tabla.column("fecha", width=120, anchor="center")
        self._tabla.column("hora", width=90, anchor="center")
        self._tabla.column("precio", width=90, anchor="center")
        self._tabla.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

    def _cargar_catalogos(self):
        peliculas = self._pelicula_repo.listar()
        salas = self._sala_repo.listar()

        for pelicula in peliculas:
            opcion = pelicula.titulo
            self._peliculas_por_opcion[opcion] = pelicula.id_pelicula
            self._opcion_pelicula_por_id[pelicula.id_pelicula] = opcion

        for sala in salas:
            opcion = f"Sala {sala.numero} - capacidad {sala.capacidad}"
            self._salas_por_opcion[opcion] = sala.id_sala
            self._opcion_sala_por_id[sala.id_sala] = opcion

    def _leer_pelicula(self):
        pelicula = self._peliculas_por_opcion.get(self._pelicula_var.get())
        if pelicula is None:
            raise ValueError("pelicula invalida")
        return pelicula

    def _leer_sala(self):
        sala = self._salas_por_opcion.get(self._sala_var.get())
        if sala is None:
            raise ValueError("sala invalida")
        return sala

    def _leer_precio(self):
        try:
            return float(self._precio_var.get())
        except ValueError:
            raise ValueError("precio invalido")

    def _registrar(self):
        try:
            funcion = self._service.crear_funcion(
                pelicula=self._leer_pelicula(),
                sala=self._leer_sala(),
                fecha=self._fecha_var.get(),
                hora=self._hora_var.get(),
                precio=self._leer_precio(),
            )
            self._cargar_funciones()
            self._limpiar()
            self._id_var.set(str(funcion.id_funcion))
            messagebox.showinfo("Exito", "Funcion registrada.")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def _actualizar(self):
        if not self._id_seleccionado:
            messagebox.showerror("Error", "Seleccione una funcion para editar.")
            return
        try:
            funcion = self._service.actualizar_funcion(
                id_funcion=self._id_seleccionado,
                pelicula=self._leer_pelicula(),
                sala=self._leer_sala(),
                fecha=self._fecha_var.get(),
                hora=self._hora_var.get(),
                precio=self._leer_precio(),
            )
            self._cargar_funciones()
            self._id_seleccionado = funcion.id_funcion
            self._id_var.set(str(funcion.id_funcion))
            messagebox.showinfo("Exito", "Funcion actualizada.")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def _eliminar(self):
        if not self._id_seleccionado:
            messagebox.showerror("Error", "Seleccione una funcion para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "Desea eliminar la funcion seleccionada?"):
            return
        try:
            self._service.eliminar_funcion(self._id_seleccionado)
            self._cargar_funciones()
            self._limpiar()
            messagebox.showinfo("Exito", "Funcion eliminada.")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def _cargar_funciones(self):
        for item in self._tabla.get_children():
            self._tabla.delete(item)
        for funcion in self._service.obtener_todas():
            self._tabla.insert(
                "",
                "end",
                values=(
                    funcion.id_funcion,
                    self._opcion_pelicula_por_id.get(funcion.pelicula, funcion.pelicula),
                    self._opcion_sala_por_id.get(funcion.sala, funcion.sala),
                    funcion.fecha,
                    funcion.hora,
                    f"{funcion.precio:.2f}",
                ),
            )

    def _seleccionar_fila(self, _event):
        seleccion = self._tabla.selection()
        if not seleccion:
            return
        valores = self._tabla.item(seleccion[0], "values")
        if not valores:
            return
        funcion = self._service.buscar_por_id(int(valores[0]))
        self._id_var.set(valores[0])
        self._pelicula_var.set(
            self._opcion_pelicula_por_id.get(funcion.pelicula, "")
        )
        self._sala_var.set(self._opcion_sala_por_id.get(funcion.sala, ""))
        self._fecha_var.set(valores[3])
        self._hora_var.set(valores[4])
        self._precio_var.set(valores[5])
        self._id_seleccionado = int(valores[0])

    def _limpiar(self):
        self._id_var.set("")
        self._pelicula_var.set("")
        self._sala_var.set("")
        self._fecha_var.set("")
        self._hora_var.set("")
        self._precio_var.set("")
        self._id_seleccionado = None
        self._tabla.selection_remove(self._tabla.selection())


def lanzar_funcion_ui():
    ui = FuncionUI()
    ui._root.mainloop()


if __name__ == "__main__":
    lanzar_funcion_ui()
