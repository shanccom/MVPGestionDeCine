from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from services.venta_service import VentaError, VentaService


class VentaUI(ttk.Frame):
	def __init__(self, master=None, service=None):
		self._root = master or tk.Tk()
		super().__init__(self._root)
		self._service = service or VentaService()
		self._venta_seleccionada = None
		self._construir_ui()
		self._cargar_ventas()

	def _construir_ui(self):
		self._root.title("Gestion de ventas")
		self.pack(fill="both", expand=True, padx=10, pady=10)

		self._peliculas_disponibles = self._cargar_peliculas_disponibles()

		self._pelicula_var = tk.StringVar(value=self._peliculas_disponibles[0] if self._peliculas_disponibles else "")
		self._funcion_var = tk.StringVar(value="1")
		self._capacidad_var = tk.StringVar(value="100")
		self._cantidad_var = tk.StringVar(value="1")

		form = ttk.LabelFrame(self, text="Datos de venta")
		form.pack(fill="x", padx=5, pady=5)

		tk.Label(form, text="Pelicula").grid(row=0, column=0, sticky="w", padx=5, pady=5)
		self._pelicula_combo = ttk.Combobox(
			form,
			textvariable=self._pelicula_var,
			values=self._peliculas_disponibles,
			state="readonly",
			width=37,
		)
		self._pelicula_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
		self._pelicula_combo.bind("<<ComboboxSelected>>", self._actualizar_funcion_auto)

		tk.Label(form, text="Funcion ID").grid(row=1, column=0, sticky="w", padx=5, pady=5)
		tk.Entry(form, textvariable=self._funcion_var, width=40, state="readonly").grid(
			row=1, column=1, sticky="w", padx=5, pady=5
		)

		tk.Label(form, text="Capacidad sala").grid(row=2, column=0, sticky="w", padx=5, pady=5)
		ttk.Entry(form, textvariable=self._capacidad_var, width=40).grid(
			row=2, column=1, sticky="w", padx=5, pady=5
		)

		tk.Label(form, text="Cantidad entradas").grid(row=3, column=0, sticky="w", padx=5, pady=5)
		ttk.Entry(form, textvariable=self._cantidad_var, width=40).grid(
			row=3, column=1, sticky="w", padx=5, pady=5
		)

		acciones = ttk.Frame(self)
		acciones.pack(fill="x", padx=5, pady=5)

		ttk.Button(acciones, text="Registrar", command=self._registrar).pack(side="left", padx=5)
		tk.Button(acciones, text="Cancelar seleccionada", command=self._cancelar).pack(side="left", padx=5)
		ttk.Button(acciones, text="Listar", command=self._cargar_ventas).pack(side="left", padx=5)
		ttk.Button(acciones, text="Limpiar", command=self._limpiar).pack(side="left", padx=5)

		tabla_frame = ttk.LabelFrame(self, text="Ventas")
		tabla_frame.pack(fill="both", expand=True, padx=5, pady=5)

		columnas = ("id", "pelicula", "funcion", "cantidad", "total", "fecha", "estado")
		self._tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
		self._tabla.heading("id", text="ID")
		self._tabla.heading("pelicula", text="Pelicula")
		self._tabla.heading("funcion", text="Funcion")
		self._tabla.heading("cantidad", text="Cantidad")
		self._tabla.heading("total", text="Total")
		self._tabla.heading("fecha", text="Fecha")
		self._tabla.heading("estado", text="Estado")

		self._tabla.column("id", width=60, anchor="center")
		self._tabla.column("pelicula", width=160, anchor="w")
		self._tabla.column("funcion", width=140, anchor="w")
		self._tabla.column("cantidad", width=80, anchor="center")
		self._tabla.column("total", width=90, anchor="e")
		self._tabla.column("fecha", width=160)
		self._tabla.column("estado", width=90, anchor="center")
		self._tabla.pack(side="left", fill="both", expand=True)

		scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self._tabla.yview)
		self._tabla.configure(yscroll=scrollbar.set)
		scrollbar.pack(side="right", fill="y")

		self._tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

	def _registrar(self):
		try:
			venta = self._service.vender_entradas(
				pelicula=self._pelicula_var.get(),
				funcion_id=int(self._funcion_var.get()),
				capacidad_sala=int(self._capacidad_var.get()),
				cantidad_entradas=int(self._cantidad_var.get()),
			)
			self._cargar_ventas()
			messagebox.showinfo("Exito", "Venta registrada.")
		except (ValueError, VentaError) as exc:
			messagebox.showerror("Error", str(exc))

	def _cancelar(self):
		try:
			venta_id = self._venta_id_seleccionada()
			self._service.cancelar_venta(venta_id)
			self._cargar_ventas()
			messagebox.showinfo("Exito", "Venta cancelada.")
		except (ValueError, VentaError) as exc:
			messagebox.showerror("Error", str(exc))

	def _cargar_ventas(self):
		for item in self._tabla.get_children():
			self._tabla.delete(item)
		for venta in self._service.listar_ventas():
			self._tabla.insert(
				"",
				"end",
				values=(
					venta.id_venta,
					venta.pelicula,
					venta.funcion_id,
					venta.cantidad_entradas,
					f"S/ {venta.total:.2f}",
					venta.fecha_venta.strftime("%Y-%m-%d %H:%M:%S"),
					venta.estado,
				),
			)

	def _seleccionar_fila(self, _event):
		seleccion = self._tabla.selection()
		if not seleccion:
			return
		valores = self._tabla.item(seleccion[0], "values")
		if not valores:
			return
		self._pelicula_var.set(valores[1])
		self._funcion_var.set(valores[2])
		self._cantidad_var.set(valores[3])
		self._venta_seleccionada = int(valores[0])

	def _venta_id_seleccionada(self):
		if self._venta_seleccionada is not None:
			return self._venta_seleccionada
		seleccion = self._tabla.selection()
		if not seleccion:
			raise ValueError("Seleccione una venta para cancelar.")
		valores = self._tabla.item(seleccion[0], "values")
		if not valores:
			raise ValueError("Seleccione una venta para cancelar.")
		return int(valores[0])

	def _limpiar(self):
		self._funcion_var.set("")
		self._capacidad_var.set("100")
		self._cantidad_var.set("1")
		if self._peliculas_disponibles:
			self._pelicula_var.set(self._peliculas_disponibles[0])
		self._actualizar_funcion_auto()
		self._venta_seleccionada = None
		self._tabla.selection_remove(self._tabla.selection())

	def _actualizar_funcion_auto(self, _event=None):
		pelicula = self._pelicula_var.get()
		if pelicula in self._peliculas_disponibles:
			self._funcion_var.set(str(self._peliculas_disponibles.index(pelicula) + 1))
		else:
			self._funcion_var.set("1")

	def _cargar_peliculas_disponibles(self):
		ruta = Path(__file__).resolve().parents[1] / "storage" / "peliculas" / "peliculas.json"
		if not ruta.exists():
			return ["Sin peliculas"]
		try:
			datos = json.loads(ruta.read_text(encoding="utf-8"))
		except ValueError:
			return ["Sin peliculas"]
		items = datos.get("items", []) if isinstance(datos, dict) else []
		peliculas = [item.get("titulo", "") for item in items if item.get("titulo")]
		return peliculas or ["Sin peliculas"]


def lanzar_venta_ui():
	ui = VentaUI()
	ui._root.mainloop()


if __name__ == "__main__":
	lanzar_venta_ui()