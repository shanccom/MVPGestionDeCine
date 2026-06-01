import tkinter as tk
from tkinter import messagebox, ttk

from storage.salas.sala_repository import SalaRepository
from services.sala_service import SalaService


class SalaUI(ttk.Frame):
    def __init__(self, master=None, service=None):
        self._root = master or tk.Tk()
        super().__init__(self._root)
        
        # Inicialización de dependencias respetando la inyección
        if service is None:
            repo = SalaRepository()
            self._service = SalaService(repo)
        else:
            self._service = service
            
        self._id_seleccionado = None
        self._construir_ui()
        self._cargar_salas()

    def _construir_ui(self):
        self._root.title("Gestión de salas")
        self.pack(fill="both", expand=True, padx=10, pady=10)

        # Variables de control Tkinter
        self._id_var = tk.StringVar()
        self._numero_var = tk.StringVar()
        self._capacidad_var = tk.StringVar()

        # Panel de Formulario
        form = ttk.LabelFrame(self, text="Datos de sala")
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="ID").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._id_var, width=40, state="readonly").grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Label(form, text="Número").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._numero_var, width=40).grid(
            row=1, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Label(form, text="Capacidad").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self._capacidad_var, width=40).grid(
            row=2, column=1, sticky="w", padx=5, pady=5
        )

        # Panel de Acciones
        acciones = ttk.Frame(self)
        acciones.pack(fill="x", padx=5, pady=5)

        ttk.Button(acciones, text="Registrar", command=self._registrar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Editar", command=self._actualizar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Eliminar", command=self._eliminar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Listar", command=self._cargar_salas).pack(side="left", padx=5)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar).pack(side="left", padx=5)

        # Panel de Tabla
        tabla_frame = ttk.LabelFrame(self, text="Salas")
        tabla_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columnas = ("id_sala", "numero", "capacidad")
        self._tabla = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=12
        )
        self._tabla.heading("id_sala", text="ID")
        self._tabla.heading("numero", text="Número")
        self._tabla.heading("capacidad", text="Capacidad")
        
        self._tabla.column("id_sala", width=70, anchor="center")
        self._tabla.column("numero", width=150, anchor="center")
        self._tabla.column("capacidad", width=150, anchor="center")
        self._tabla.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

    # Métodos auxiliares de lectura
    def _leer_numero(self):
        try:
            return int(self._numero_var.get())
        except ValueError:
            raise ValueError("El número de sala debe ser un valor entero.")

    def _leer_capacidad(self):
        try:
            return int(self._capacidad_var.get())
        except ValueError:
            raise ValueError("La capacidad debe ser un valor entero.")

    # Operaciones CRUD conectadas al servicio
    def _registrar(self):
        try:
            sala = self._service.registrar_sala(
                numero=self._leer_numero(),
                capacidad=self._leer_capacidad()
            )
            self._cargar_salas()
            self._limpiar()
            self._id_var.set(str(sala.id_sala))
            messagebox.showinfo("Éxito", "Sala registrada exitosamente.")
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Error de Validación", str(exc))

    def _actualizar(self):
        if not self._id_seleccionado:
            messagebox.showerror("Error", "Seleccione una sala de la tabla para editar.")
            return
        try:
            sala = self._service.actualizar_sala(
                id_sala=self._id_seleccionado,
                numero=self._leer_numero(),
                capacidad=self._leer_capacidad()
            )
            self._cargar_salas()
            self._id_seleccionado = sala.id_sala
            self._id_var.set(str(sala.id_sala))
            messagebox.showinfo("Éxito", "Sala actualizada exitosamente.")
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Error de Validación", str(exc))

    def _eliminar(self):
        if not self._id_seleccionado:
            messagebox.showerror("Error", "Seleccione una sala para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar la sala seleccionada?"):
            return
        try:
            self._service.eliminar_sala(self._id_seleccionado)
            self._cargar_salas()
            self._limpiar()
            messagebox.showinfo("Éxito", "Sala eliminada exitosamente.")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def _cargar_salas(self):
        for item in self._tabla.get_children():
            self._tabla.delete(item)
        for sala in self._service.listar_salas():
            self._tabla.insert(
                "", "end",
                values=(
                    sala.id_sala,
                    sala.numero,
                    sala.capacidad,
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
        self._numero_var.set(valores[1])
        self._capacidad_var.set(valores[2])
        self._id_seleccionado = int(valores[0])

    def _limpiar(self):
        self._id_var.set("")
        self._numero_var.set("")
        self._capacidad_var.set("")
        self._id_seleccionado = None
        self._tabla.selection_remove(self._tabla.selection())


def lanzar_sala_ui():
    ui = SalaUI()
    ui._root.mainloop()


if __name__ == "__main__":
    lanzar_sala_ui()