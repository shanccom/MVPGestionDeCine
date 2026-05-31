"""Interfaz grafica Tkinter para el modulo de venta de entradas.

La interfaz consume el backend autocontenido de modulo_venta_entradas.py sin
depender de otros modulos del MVP.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from modulo_venta_entradas import ModuloVentaEntradas, VentaError


class InterfazVentaEntradas:
    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        self.raiz.title("MVP Gestion de Cine - Venta de Entradas")
        self.raiz.geometry("920x620")
        self.raiz.minsize(860, 560)

        self.modulo = ModuloVentaEntradas()

        self.funcion_id_var = tk.StringVar()
        self.capacidad_sala_var = tk.StringVar(value="100")
        self.cantidad_entradas_var = tk.StringVar(value="1")
        self.precio_unitario_var = tk.StringVar(value="15.00")
        self.venta_id_var = tk.StringVar()

        self._construir_interfaz()
        self.actualizar_tabla()

        self.raiz.protocol("WM_DELETE_WINDOW", self.cerrar)

    def _construir_interfaz(self) -> None:
        self.raiz.configure(bg="#101820")

        contenedor = ttk.Frame(self.raiz, padding=16)
        contenedor.pack(fill="both", expand=True)

        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", pady=(0, 12))

        titulo = ttk.Label(
            encabezado,
            text="Venta de Entradas",
            font=("Segoe UI", 20, "bold"),
        )
        titulo.pack(anchor="w")

        subtitulo = ttk.Label(
            encabezado,
            text="Registro, consulta y cancelacion de ventas con control de aforo",
            font=("Segoe UI", 10),
        )
        subtitulo.pack(anchor="w", pady=(4, 0))

        cuerpo = ttk.Frame(contenedor)
        cuerpo.pack(fill="both", expand=True)

        panel_formulario = ttk.LabelFrame(cuerpo, text="Registrar venta", padding=14)
        panel_formulario.pack(side="left", fill="y", padx=(0, 12))

        self._crear_campo(panel_formulario, "Funcion ID", self.funcion_id_var, 0)
        self._crear_campo(panel_formulario, "Capacidad sala", self.capacidad_sala_var, 1)
        self._crear_campo(panel_formulario, "Cantidad entradas", self.cantidad_entradas_var, 2)
        self._crear_campo(panel_formulario, "Precio unitario", self.precio_unitario_var, 3)

        ttk.Button(
            panel_formulario,
            text="Vender entradas",
            command=self.registrar_venta,
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 4))

        ttk.Separator(panel_formulario, orient="horizontal").grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=12
        )

        ttk.Label(panel_formulario, text="Venta ID para cancelar").grid(
            row=6, column=0, sticky="w", pady=(0, 4)
        )
        ttk.Entry(panel_formulario, textvariable=self.venta_id_var, width=20).grid(
            row=7, column=0, columnspan=2, sticky="ew"
        )

        ttk.Button(
            panel_formulario,
            text="Cancelar venta",
            command=self.cancelar_venta,
        ).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(8, 4))

        ttk.Button(
            panel_formulario,
            text="Actualizar listado",
            command=self.actualizar_tabla,
        ).grid(row=9, column=0, columnspan=2, sticky="ew", pady=(4, 0))

        for indice in range(10):
            panel_formulario.grid_rowconfigure(indice, weight=0)
        panel_formulario.grid_columnconfigure(1, weight=1)

        panel_listado = ttk.LabelFrame(cuerpo, text="Ventas registradas", padding=10)
        panel_listado.pack(side="right", fill="both", expand=True)

        columnas = ("id", "funcion", "cantidad", "total", "fecha", "estado")
        self.tabla = ttk.Treeview(panel_listado, columns=columnas, show="headings", height=18)
        self.tabla.heading("id", text="ID")
        self.tabla.heading("funcion", text="Funcion")
        self.tabla.heading("cantidad", text="Entradas")
        self.tabla.heading("total", text="Total")
        self.tabla.heading("fecha", text="Fecha venta")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("funcion", width=90, anchor="center")
        self.tabla.column("cantidad", width=90, anchor="center")
        self.tabla.column("total", width=90, anchor="e")
        self.tabla.column("fecha", width=180, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")

        barra_scroll = ttk.Scrollbar(panel_listado, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra_scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")

        self.estado_var = tk.StringVar(value="Listo para registrar ventas.")
        barra_estado = ttk.Label(contenedor, textvariable=self.estado_var, anchor="w")
        barra_estado.pack(fill="x", pady=(10, 0))

    def _crear_campo(self, padre: ttk.LabelFrame, etiqueta: str, variable: tk.StringVar, fila: int) -> None:
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=(0, 4))
        ttk.Entry(padre, textvariable=variable, width=22).grid(row=fila, column=1, sticky="ew", pady=(0, 8))

    def registrar_venta(self) -> None:
        try:
            funcion_id = self._obtener_entero(self.funcion_id_var.get(), "Funcion ID")
            capacidad_sala = self._obtener_entero(self.capacidad_sala_var.get(), "Capacidad sala")
            cantidad_entradas = self._obtener_entero(self.cantidad_entradas_var.get(), "Cantidad entradas")
            precio_unitario = self._obtener_decimal(self.precio_unitario_var.get(), "Precio unitario")

            venta = self.modulo.vender_entradas(
                funcion_id=funcion_id,
                capacidad_sala=capacidad_sala,
                cantidad_entradas=cantidad_entradas,
                precio_unitario=precio_unitario,
            )
        except VentaError as error:
            self.estado_var.set(str(error))
            messagebox.showerror("Error de venta", str(error))
            return
        except ValueError as error:
            self.estado_var.set(str(error))
            messagebox.showerror("Dato invalido", str(error))
            return

        self.estado_var.set(
            f"Venta registrada: ID {venta.id}, total S/ {venta.total:.2f}, estado {venta.estado}."
        )
        messagebox.showinfo("Venta exitosa", f"Se registro la venta {venta.id} correctamente.")
        self.actualizar_tabla()
        self.cantidad_entradas_var.set("1")
        self.venta_id_var.set(str(venta.id))

    def cancelar_venta(self) -> None:
        try:
            venta_id = self._obtener_entero(self.venta_id_var.get(), "Venta ID")
            venta = self.modulo.cancelar_venta(venta_id)
        except VentaError as error:
            self.estado_var.set(str(error))
            messagebox.showerror("Error al cancelar", str(error))
            return
        except ValueError as error:
            self.estado_var.set(str(error))
            messagebox.showerror("Dato invalido", str(error))
            return

        self.estado_var.set(f"Venta {venta.id} cancelada correctamente.")
        messagebox.showinfo("Cancelacion exitosa", f"La venta {venta.id} fue cancelada.")
        self.actualizar_tabla()

    def actualizar_tabla(self) -> None:
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        ventas = self.modulo.listar_ventas()
        for venta in ventas:
            self.tabla.insert(
                "",
                "end",
                values=(
                    venta.id,
                    venta.funcion_id,
                    venta.cantidad_entradas,
                    f"S/ {venta.total:.2f}",
                    venta.fecha_venta.strftime("%Y-%m-%d %H:%M:%S"),
                    venta.estado,
                ),
            )

        if not ventas:
            self.estado_var.set("No hay ventas registradas todavia.")

    @staticmethod
    def _obtener_entero(valor: str, nombre_campo: str) -> int:
        if valor.strip() == "":
            raise ValueError(f"El campo {nombre_campo} es obligatorio.")
        return int(valor)

    @staticmethod
    def _obtener_decimal(valor: str, nombre_campo: str) -> float:
        if valor.strip() == "":
            raise ValueError(f"El campo {nombre_campo} es obligatorio.")
        return float(valor)

    def cerrar(self) -> None:
        self.modulo.cerrar()
        self.raiz.destroy()


def ejecutar() -> None:
    raiz = tk.Tk()
    ttk.Style().theme_use("clam")
    InterfazVentaEntradas(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    ejecutar()