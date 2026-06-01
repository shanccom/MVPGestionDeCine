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
		self._cantidad_var = tk.StringVar(value="0")
		self._asientos_var = tk.StringVar(value="Sin asientos seleccionados")
		self._asientos_seleccionados = []

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

		tk.Label(form, text="Asientos").grid(row=2, column=0, sticky="w", padx=5, pady=5)
		asientos_entry = ttk.Entry(form, textvariable=self._asientos_var, width=40, state="readonly")
		asientos_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
		ttk.Button(form, text="Seleccionar asientos", command=self._abrir_selector_asientos).grid(
			row=3, column=1, sticky="w", padx=5, pady=5
		)

		tk.Label(form, text="Cantidad entradas").grid(row=4, column=0, sticky="w", padx=5, pady=5)
		ttk.Entry(form, textvariable=self._cantidad_var, width=40, state="readonly").grid(
			row=4, column=1, sticky="w", padx=5, pady=5
		)

		acciones = ttk.Frame(self)
		acciones.pack(fill="x", padx=5, pady=5)

		ttk.Button(acciones, text="Registrar", command=self._registrar).pack(side="left", padx=5)
		tk.Button(acciones, text="Eliminar registro", command=self._eliminar_registro).pack(side="left", padx=5)
		tk.Button(acciones, text="Cancelar seleccionada", command=self._cancelar).pack(side="left", padx=5)
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
			pelicula = self._pelicula_var.get()
			funcion_id = int(self._funcion_var.get())
			asientos_seleccionados = tuple(self._asientos_seleccionados)

			self._service.vender_entradas(
				pelicula=pelicula,
				funcion_id=funcion_id,
				asientos_seleccionados=asientos_seleccionados,
			)
			self._limpiar_seleccion_asientos()
			self._cargar_ventas()
			messagebox.showinfo("Exito", "Venta registrada.", parent=self._root)
			self._mantener_ventana_activa()
		except (ValueError, VentaError) as exc:
			messagebox.showerror("Error", str(exc), parent=self._root)

	def _eliminar_registro(self):
		try:
			venta_id = self._venta_id_seleccionada()
			self._service.eliminar_venta(venta_id)
			self._cargar_ventas()
			self._limpiar()
			messagebox.showinfo("Exito", "Registro eliminado.")
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

	def _cargar_ventas(self, pelicula=None):
		pelicula = self._pelicula_var.get() if pelicula is None else pelicula
		for item in self._tabla.get_children():
			self._tabla.delete(item)
		# La tabla se actualiza automáticamente con la película seleccionada.
		for venta in self._service.listar_ventas(pelicula=pelicula):
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
		self._asientos_var.set(", ".join(f"A{asiento}" for asiento in self._asientos_seleccionados) if self._asientos_seleccionados else "Sin asientos seleccionados")
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
		self._cantidad_var.set("0")
		self._asientos_seleccionados = []
		self._asientos_var.set("Sin asientos seleccionados")
		if self._peliculas_disponibles:
			self._pelicula_var.set(self._peliculas_disponibles[0])
		self._actualizar_funcion_auto()
		self._venta_seleccionada = None
		self._tabla.selection_remove(self._tabla.selection())

	def _limpiar_seleccion_asientos(self):
		# Tras registrar, solo se reinician los asientos; la película se conserva.
		self._cantidad_var.set("0")
		self._asientos_seleccionados = []
		self._asientos_var.set("Sin asientos seleccionados")

	def _mantener_ventana_activa(self):
		self._root.deiconify()
		self._root.lift()
		self._root.focus_force()

	def _actualizar_funcion_auto(self, _event=None):
		pelicula = self._pelicula_var.get()
		if pelicula in self._peliculas_disponibles:
			self._funcion_var.set(str(self._peliculas_disponibles.index(pelicula) + 1))
		else:
			self._funcion_var.set("1")
		self._cargar_ventas(pelicula)

	def _abrir_selector_asientos(self):
		ventana = tk.Toplevel(self._root)
		ventana.title("Seleccionar asientos")
		ventana.transient(self._root)
		ventana.grab_set()

		ocupados = self._service.asientos_ocupados(int(self._funcion_var.get())) if hasattr(self._service, "asientos_ocupados") else set()
		tk.Label(ventana, text="Selecciona hasta 10 asientos").pack(anchor="w", padx=10, pady=(10, 6))

		contenedor = ttk.Frame(ventana, padding=10)
		contenedor.pack(fill="both", expand=True)

		seleccion_temporal = set(self._asientos_seleccionados)
		botones = {}

		def refrescar_estado():
			for asiento, boton in botones.items():
				if asiento in ocupados:
					boton.configure(text=f"A{asiento} (Ocupado)", state="disabled")
				elif asiento in seleccion_temporal:
					boton.configure(text=f"A{asiento} (Sel)", state="normal")
				else:
					boton.configure(text=f"A{asiento}", state="normal")

		def alternar(asiento):
			if asiento in ocupados:
				return
			if asiento in seleccion_temporal:
				seleccion_temporal.remove(asiento)
			else:
				if len(seleccion_temporal) >= 10:
					messagebox.showerror("Error", "No se puede comprar mas de 10 asientos.")
					return
				seleccion_temporal.add(asiento)
			refrescar_estado()

		for asiento in range(1, 21):
			boton = ttk.Button(contenedor, width=10, command=lambda valor=asiento: alternar(valor))
			boton.grid(row=(asiento - 1) // 5, column=(asiento - 1) % 5, padx=4, pady=4, sticky="ew")
			botones[asiento] = boton

		resumen = tk.StringVar()

		def actualizar_resumen():
			seleccionados = sorted(seleccion_temporal)
			resumen.set(", ".join(f"A{asiento}" for asiento in seleccionados) if seleccionados else "Sin asientos seleccionados")
			self._asientos_var.set(resumen.get())
			self._cantidad_var.set(str(len(seleccionados)))

		def aplicar_seleccion():
			self._asientos_seleccionados = sorted(seleccion_temporal)
			actualizar_resumen()

		def aceptar():
			if not seleccion_temporal:
				messagebox.showerror("Error", "Debes seleccionar al menos un asiento.")
				return
			aplicar_seleccion()
			ventana.destroy()

		def cerrar():
			if seleccion_temporal:
				aplicar_seleccion()
			ventana.destroy()

		def cancelar():
			ventana.destroy()

		refrescar_estado()
		actualizar_resumen()
		ventana.protocol("WM_DELETE_WINDOW", cerrar)
		botonera = ttk.Frame(ventana, padding=(10, 0, 10, 10))
		botonera.pack(fill="x")
		tk.Label(botonera, textvariable=resumen).pack(anchor="w", pady=(0, 8))
		acciones = ttk.Frame(botonera)
		acciones.pack(fill="x")
		ttk.Button(acciones, text="Aceptar", command=aceptar).pack(side="left", padx=(0, 6))
		ttk.Button(acciones, text="Cancelar", command=cancelar).pack(side="left")

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