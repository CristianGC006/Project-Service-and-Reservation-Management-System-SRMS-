import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from client import User
from service import UserService


class ReservationApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.service = UserService()

        self.root.title("Sistema de Reservas - ProjectRSM_UNAD")
        self.root.geometry("1200x820")
        self.root.minsize(1080, 720)

        self._configurar_estilo()
        self._crear_interfaz()
        self.refrescar_todo()

    def _configurar_estilo(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        # Palette: blanco, grises y negro
        bg_main = "#FFFFFF"
        panel_bg = "#F3F4F6"
        card_bg = "#FFFFFF"
        text_color = "#111111"
        muted = "#6B7280"
        accent_bg = "#111111"  # negro
        accent_fg = "#FFFFFF"

        style.configure("TNotebook", background=bg_main, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(12, 8), font=("Segoe UI", 10, "bold"), background=bg_main)
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=text_color, background=bg_main)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 11), foreground=muted, background=bg_main)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=8, foreground=accent_fg, background=accent_bg)
        style.map("Accent.TButton", background=[("active", "#2b2b2b")], foreground=[("active", accent_fg)])
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 9), background=card_bg, fieldbackground=card_bg)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#f0f0f0")
        style.configure("Card.TFrame", background=card_bg)
        style.configure("Panel.TFrame", background=panel_bg)

        # Root background
        self.root.configure(bg=bg_main)

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=16)
        contenedor.pack(fill="both", expand=True)

        titulo = ttk.Label(contenedor, text="Sistema de Reservas y Servicios", style="Header.TLabel")
        titulo.pack(anchor="w")

        subtitulo = ttk.Label(
            contenedor,
            text="Registra usuarios, administra reservas y revisa reportes.",
            style="SubHeader.TLabel",
        )
        subtitulo.pack(anchor="w", pady=(2, 14))

        # Toolbar: búsqueda rápida y acciones
        toolbar = ttk.Frame(contenedor, style="Panel.TFrame")
        toolbar.pack(fill="x", pady=(0, 10))

        ttk.Label(toolbar, text="Buscar usuarios:").pack(side="left", padx=(0, 6))
        self.search_user_var = tk.StringVar()
        search_user = ttk.Entry(toolbar, textvariable=self.search_user_var, width=28)
        search_user.pack(side="left")
        ttk.Button(toolbar, text="Buscar", command=self._buscar_usuarios).pack(side="left", padx=6)

        ttk.Label(toolbar, text="  Buscar reservas:").pack(side="left", padx=(10, 6))
        self.search_res_var = tk.StringVar()
        search_res = ttk.Entry(toolbar, textvariable=self.search_res_var, width=28)
        search_res.pack(side="left")
        ttk.Button(toolbar, text="Buscar", command=self._buscar_reservas).pack(side="left", padx=6)

        ttk.Button(toolbar, text="Limpiar filtros", command=self._limpiar_filtros).pack(side="right")

        self.notebook = ttk.Notebook(contenedor)
        self.notebook.pack(fill="both", expand=True)

        self.tab_usuarios = ttk.Frame(self.notebook, padding=12)
        self.tab_servicios = ttk.Frame(self.notebook, padding=12)
        self.tab_reservas = ttk.Frame(self.notebook, padding=12)
        self.tab_actualizar = ttk.Frame(self.notebook, padding=12)
        self.tab_reportes = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.tab_usuarios, text="Usuarios")
        self.notebook.add(self.tab_servicios, text="Servicios")
        self.notebook.add(self.tab_reservas, text="Reservas")
        self.notebook.add(self.tab_actualizar, text="Actualizar")
        self.notebook.add(self.tab_reportes, text="Reportes")

        self._crear_tab_usuarios()
        self._crear_tab_servicios()
        self._crear_tab_reservas()
        self._crear_tab_actualizar()
        self._crear_tab_reportes()

        self.status_var = tk.StringVar(value="Listo")
        status = ttk.Label(contenedor, textvariable=self.status_var, relief="groove", anchor="w", padding=8)
        status.pack(fill="x", pady=(12, 0))

    def _crear_tab_usuarios(self):
        formulario = ttk.LabelFrame(self.tab_usuarios, text="Registrar usuario", padding=12)
        formulario.pack(fill="x", pady=(0, 12))

        self.usuario_name = tk.StringVar()
        self.usuario_email = tk.StringVar()
        self.usuario_phone = tk.StringVar()

        self._crear_campo(formulario, "Nombre", self.usuario_name, 0)
        self._crear_campo(formulario, "Email", self.usuario_email, 1)
        self._crear_campo(formulario, "Teléfono", self.usuario_phone, 2)

        botones = ttk.Frame(formulario)
        botones.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Button(botones, text="Registrar", style="Accent.TButton", command=self.registrar_usuario).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar_form_usuario).pack(side="left", padx=8)
        ttk.Button(botones, text="Actualizar lista", command=self.refrescar_usuarios).pack(side="left")

        tabla_frame = ttk.LabelFrame(self.tab_usuarios, text="Usuarios registrados", padding=12)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("Id", "Nombre", "Email", "Telefono")
        self.tree_usuarios = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tree_usuarios.heading(col, text=col)
            self.tree_usuarios.column(col, width=160, anchor="center")
        self.tree_usuarios.column("Nombre", width=220, anchor="w")
        self.tree_usuarios.column("Email", width=260, anchor="w")
        self.tree_usuarios.pack(fill="both", expand=True)
        self.tree_usuarios.tag_configure('odd', background='#ffffff')
        self.tree_usuarios.tag_configure('even', background='#f7fbff')

    def _crear_tab_servicios(self):
        formulario = ttk.LabelFrame(self.tab_servicios, text="Crear servicio de consultoría", padding=12)
        formulario.pack(fill="x", pady=(0, 12))

        self.serv_tipo = tk.StringVar(value="general")
        self.serv_nombre = tk.StringVar()
        self.serv_precio = tk.StringVar()

        ttk.Label(formulario, text="Tipo").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
        self.combo_tipo = ttk.Combobox(
            formulario,
            textvariable=self.serv_tipo,
            values=["general", "tecnica", "estrategica"],
            state="readonly",
            width=39,
        )
        self.combo_tipo.grid(row=0, column=1, sticky="we", pady=6)

        self._crear_campo(formulario, "Nombre del servicio", self.serv_nombre, 1)
        self._crear_campo(formulario, "Precio base", self.serv_precio, 2)

        botones = ttk.Frame(formulario)
        botones.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Button(botones, text="Crear servicio", style="Accent.TButton", command=self.crear_servicio).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar_form_servicio).pack(side="left", padx=8)
        ttk.Button(botones, text="Actualizar lista", command=self.refrescar_servicios).pack(side="left")

        tabla_frame = ttk.LabelFrame(self.tab_servicios, text="Servicios registrados", padding=12)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("Id", "Tipo", "Nombre", "Precio", "Descripción")
        self.tree_servicios = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tree_servicios.heading(col, text=col)
            self.tree_servicios.column(col, width=150, anchor="center")
        self.tree_servicios.column("Nombre", width=220, anchor="w")
        self.tree_servicios.column("Descripción", width=420, anchor="w")
        self.tree_servicios.pack(fill="both", expand=True)
        self.tree_servicios.tag_configure('odd', background='#ffffff')
        self.tree_servicios.tag_configure('even', background='#f7fbff')

    def _crear_tab_reservas(self):
        formulario = ttk.LabelFrame(self.tab_reservas, text="Crear reserva", padding=12)
        formulario.pack(fill="x", pady=(0, 12))

        self.res_user_id = tk.StringVar()
        self.res_servicio = tk.StringVar()
        self.res_reserva = tk.StringVar()
        self.res_mensaje = tk.StringVar()
        self.res_hora = tk.StringVar()

        self._crear_campo(formulario, "ID usuario", self.res_user_id, 0)

        ttk.Label(formulario, text="Servicio consultivo").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)
        self.combo_servicio = ttk.Combobox(formulario, textvariable=self.res_servicio, state="readonly", width=39)
        self.combo_servicio.grid(row=1, column=1, sticky="we", pady=6)

        self._crear_campo(formulario, "Reserva", self.res_reserva, 2)
        self._crear_campo(formulario, "Mensaje", self.res_mensaje, 3)
        self._crear_campo(formulario, "Hora (opcional)", self.res_hora, 4)

        botones = ttk.Frame(formulario)
        botones.grid(row=5, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Button(botones, text="Crear reserva", style="Accent.TButton", command=self.crear_reserva).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar_form_reserva).pack(side="left", padx=8)
        ttk.Button(botones, text="Actualizar lista", command=self.refrescar_reservas).pack(side="left")

        tabla_frame = ttk.LabelFrame(self.tab_reservas, text="Reservas registradas", padding=12)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("ReservationId", "UserId", "Nombre", "Servicio", "Reserva", "Hora", "Estado")
        self.tree_reservas = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tree_reservas.heading(col, text=col)
            self.tree_reservas.column(col, width=125, anchor="center")
        self.tree_reservas.column("Nombre", width=200, anchor="w")
        self.tree_reservas.column("Servicio", width=170, anchor="w")
        self.tree_reservas.column("Reserva", width=220, anchor="w")
        self.tree_reservas.pack(fill="both", expand=True)
        self.tree_reservas.tag_configure('odd', background='#ffffff')
        self.tree_reservas.tag_configure('even', background='#f7fbff')

    def _crear_tab_actualizar(self):
        formulario = ttk.LabelFrame(self.tab_actualizar, text="Reprogramar reserva", padding=12)
        formulario.pack(fill="x", pady=(0, 12))

        self.up_reservation_id = tk.StringVar()
        self.up_nueva_hora = tk.StringVar()

        self._crear_campo(formulario, "ID reserva", self.up_reservation_id, 0)
        self._crear_campo(formulario, "Nueva hora", self.up_nueva_hora, 1)

        botones = ttk.Frame(formulario)
        botones.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Button(botones, text="Actualizar", style="Accent.TButton", command=self.actualizar_reserva).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar_form_actualizar).pack(side="left", padx=8)

        ayuda = ttk.LabelFrame(self.tab_actualizar, text="Ayuda rápida", padding=12, style="Card.TFrame")
        ayuda.pack(fill="both", expand=True)
        texto = (
            "1. Registra primero un usuario.\n"
            "2. Crea al menos un servicio de consultoría.\n"
            "3. Usa el ID del usuario y selecciona el servicio para crear una reserva.\n"
            "4. Luego puedes reprogramar la hora de la reserva con su ID.\n"
            "5. Los eventos se registran automáticamente en logs.txt."
        )
        ttk.Label(ayuda, text=texto, justify="left").pack(anchor="w")

    def _crear_tab_reportes(self):
        contenedor = ttk.Frame(self.tab_reportes)
        contenedor.pack(fill="both", expand=True)

        resumen = ttk.LabelFrame(contenedor, text="Resumen general", padding=12)
        resumen.pack(fill="x", pady=(0, 12))

        self.rep_total_usuarios = tk.StringVar(value="0")
        self.rep_total_reservas = tk.StringVar(value="0")
        self.rep_total_servicios = tk.StringVar(value="0")
        self.rep_pendientes = tk.StringVar(value="0")
        self.rep_reprogramadas = tk.StringVar(value="0")

        self._crear_resumen_card(resumen, "Usuarios", self.rep_total_usuarios, 0)
        self._crear_resumen_card(resumen, "Reservas", self.rep_total_reservas, 1)
        self._crear_resumen_card(resumen, "Servicios", self.rep_total_servicios, 2)
        self._crear_resumen_card(resumen, "Pendientes", self.rep_pendientes, 3)
        self._crear_resumen_card(resumen, "Reprogramadas", self.rep_reprogramadas, 4)

        botones = ttk.Frame(contenedor)
        botones.pack(fill="x", pady=(0, 10))

        ttk.Button(botones, text="Actualizar reportes", style="Accent.TButton", command=self.refrescar_reportes).pack(side="left")
        ttk.Button(botones, text="Cargar logs", command=self.cargar_logs).pack(side="left", padx=8)

        panel = ttk.Frame(contenedor)
        panel.pack(fill="both", expand=True)

        panel_izq = ttk.LabelFrame(panel, text="Detalle del reporte", padding=12, style="Card.TFrame")
        panel_izq.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.reporte_text = scrolledtext.ScrolledText(panel_izq, height=24, font=("Consolas", 10), wrap="word", bd=0, relief="flat")
        self.reporte_text.pack(fill="both", expand=True)

        panel_der = ttk.LabelFrame(panel, text="Logs recientes", padding=12, style="Card.TFrame")
        panel_der.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self.logs_text = scrolledtext.ScrolledText(panel_der, height=24, font=("Consolas", 10), wrap="word", bd=0, relief="flat")
        self.logs_text.pack(fill="both", expand=True)

    # Simple tooltip helper
    class _ToolTip:
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tipwindow = None
            widget.bind("<Enter>", self.show)
            widget.bind("<Leave>", self.hide)

        def show(self, _event=None):
            if self.tipwindow:
                return
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + 20
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()

        def hide(self, _event=None):
            if self.tipwindow:
                self.tipwindow.destroy()
                self.tipwindow = None

    def _crear_campo(self, parent, texto, variable, fila):
        ttk.Label(parent, text=texto).grid(row=fila, column=0, sticky="w", padx=(0, 10), pady=6)
        entry = ttk.Entry(parent, textvariable=variable, width=42)
        entry.grid(row=fila, column=1, sticky="we", pady=6)
        parent.columnconfigure(1, weight=1)

    def _crear_resumen_card(self, parent, titulo, variable, columna):
        card = ttk.Frame(parent, padding=8, relief="ridge")
        card.grid(row=0, column=columna, padx=6, pady=4, sticky="nsew")
        parent.columnconfigure(columna, weight=1)

        ttk.Label(card, text=titulo, font=("Segoe UI", 9, "bold")).pack(anchor="center")
        ttk.Label(card, textvariable=variable, font=("Segoe UI", 16, "bold"), foreground="#1f3b57").pack(anchor="center", pady=(4, 0))

    def _set_status(self, mensaje: str):
        self.status_var.set(mensaje)

    def registrar_usuario(self):
        try:
            nombre = self.usuario_name.get().strip()
            email = self.usuario_email.get().strip()
            phone_text = self.usuario_phone.get().strip()

            if not phone_text.isdigit():
                raise ValueError("El teléfono debe contener solo números")

            usuario = self.service.registrar_usuario(nombre, email, int(phone_text))
            messagebox.showinfo("Éxito", f"Usuario registrado con ID {usuario['Id']}")
            self._set_status(f"Usuario registrado: {usuario['name']}")
            self.limpiar_form_usuario()
            self.refrescar_usuarios()
            self.refrescar_reportes()
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self._set_status("Error al registrar usuario")

    def crear_servicio(self):
        try:
            tipo = self.serv_tipo.get().strip()
            nombre = self.serv_nombre.get().strip()
            precio_text = self.serv_precio.get().strip()

            precio = float(precio_text)
            if precio <= 0:
                raise ValueError("El precio debe ser mayor a cero")

            servicio = self.service.crear_servicio_consultoria(tipo, nombre, precio)
            messagebox.showinfo("Éxito", f"Servicio creado con ID {servicio['id_servicio']}")
            self._set_status(f"Servicio creado: {servicio['nombre']}")
            self.limpiar_form_servicio()
            self.refrescar_servicios()
            self.refrescar_reservas()
            self.refrescar_reportes()
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self._set_status("Error al crear servicio")

    def _insert_with_stripes(self, tree: ttk.Treeview, values: tuple):
        # Insert alternating row colors
        count = len(tree.get_children())
        tag = 'even' if (count % 2 == 0) else 'odd'
        tree.insert("", "end", values=values, tags=(tag,))

    def crear_reserva(self):
        try:
            user_id = int(self.res_user_id.get().strip())
            reserva = self.res_reserva.get().strip()
            mensaje = self.res_mensaje.get().strip()
            hora = self.res_hora.get().strip()
            servicio = self.res_servicio.get().strip()

            item = self.service.crear_reserva(user_id, reserva, mensaje, hora, servicio)
            messagebox.showinfo("Éxito", f"Reserva creada con ID {item['reservation_id']}")
            self._set_status(f"Reserva creada: {item['reservation_id']}")
            self.limpiar_form_reserva()
            self.refrescar_reservas()
            self.refrescar_reportes()
        except ValueError:
            messagebox.showerror("Error", "El ID de usuario debe ser numérico")
            self._set_status("Error al crear reserva")
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self._set_status("Error al crear reserva")

    def actualizar_reserva(self):
        try:
            reservation_id = int(self.up_reservation_id.get().strip())
            nueva_hora = self.up_nueva_hora.get().strip()

            item = self.service.actualizar_hora_reserva(reservation_id, nueva_hora)
            messagebox.showinfo("Éxito", f"Reserva {item['reservation_id']} reprogramada")
            self._set_status(f"Reserva actualizada: {reservation_id}")
            self.limpiar_form_actualizar()
            self.refrescar_reservas()
            self.refrescar_reportes()
        except ValueError:
            messagebox.showerror("Error", "El ID de reserva debe ser numérico")
            self._set_status("Error al actualizar reserva")
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self._set_status("Error al actualizar reserva")

    def refrescar_usuarios(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        usuarios = User.obtener_todos_usuarios()
        for usuario in usuarios:
            self._insert_with_stripes(
                self.tree_usuarios,
                (usuario.get("Id"), usuario.get("name"), usuario.get("email"), usuario.get("Phone")),
            )

        self._set_status(f"Usuarios cargados: {len(usuarios)}")

    def refrescar_servicios(self):
        for item in self.tree_servicios.get_children():
            self.tree_servicios.delete(item)

        servicios = self.service.obtener_servicios()
        etiquetas = []
        for servicio in servicios:
            etiqueta = f"{servicio['id_servicio']} - {servicio['tipo']} - {servicio['nombre']}"
            etiquetas.append(etiqueta)
            self._insert_with_stripes(
                self.tree_servicios,
                (
                    servicio.get("id_servicio"),
                    servicio.get("tipo"),
                    servicio.get("nombre"),
                    servicio.get("precio_base"),
                    servicio.get("descripcion"),
                ),
            )

        self.combo_servicio["values"] = etiquetas
        if etiquetas and self.res_servicio.get() not in etiquetas:
            self.res_servicio.set(etiquetas[0])
        elif not etiquetas:
            self.res_servicio.set("")

        self._set_status(f"Servicios cargados: {len(servicios)}")

    def refrescar_reservas(self):
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)

        reservas = self.service.obtener_reservas()
        for reserva in reservas:
            self._insert_with_stripes(
                self.tree_reservas,
                (
                    reserva.get("reservation_id"),
                    reserva.get("user_id"),
                    reserva.get("name"),
                    reserva.get("servicio", ""),
                    reserva.get("reserva"),
                    reserva.get("hora"),
                    reserva.get("estado"),
                ),
            )

        self._set_status(f"Reservas cargadas: {len(reservas)}")

    def refrescar_reportes(self):
        resumen = self.service.obtener_resumen_reportes()

        self.rep_total_usuarios.set(str(resumen["total_usuarios"]))
        self.rep_total_reservas.set(str(resumen["total_reservas"]))
        self.rep_total_servicios.set(str(resumen["total_servicios"]))
        self.rep_pendientes.set(str(resumen["reservas_pendientes"]))
        self.rep_reprogramadas.set(str(resumen["reservas_reprogramadas"]))

        lineas = []
        lineas.append("REPORTE GENERAL DEL SISTEMA")
        lineas.append("-" * 34)
        lineas.append(f"Usuarios registrados: {resumen['total_usuarios']}")
        lineas.append(f"Servicios de consultoría: {resumen['total_servicios']}")
        lineas.append(f"Reservas totales: {resumen['total_reservas']}")
        lineas.append(f"Reservas pendientes: {resumen['reservas_pendientes']}")
        lineas.append(f"Reservas reprogramadas: {resumen['reservas_reprogramadas']}")
        lineas.append("")
        lineas.append("SERVICIOS REGISTRADOS")
        lineas.append("-" * 34)
        if resumen["servicios"]:
            for servicio in resumen["servicios"]:
                lineas.append(
                    f"#{servicio['id_servicio']} | {servicio['tipo']} | {servicio['nombre']} | ${servicio['precio_base']}"
                )
        else:
            lineas.append("Sin servicios creados todavía.")

        lineas.append("")
        lineas.append("ÚLTIMAS RESERVAS")
        lineas.append("-" * 34)
        if resumen["reservas"]:
            for reserva in resumen["reservas"][-10:]:
                lineas.append(
                    f"#{reserva.get('reservation_id')} | Usuario {reserva.get('user_id')} | {reserva.get('reserva')} | {reserva.get('estado')}"
                )
        else:
            lineas.append("Sin reservas registradas todavía.")

        self.reporte_text.delete("1.0", tk.END)
        self.reporte_text.insert(tk.END, "\n".join(lineas))

        return resumen

    # Search helpers
    def _buscar_usuarios(self):
        texto = self.search_user_var.get().strip().lower()
        if not texto:
            self.refrescar_usuarios()
            return

        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        usuarios = [u for u in User.obtener_todos_usuarios() if texto in u.get("name", "").lower() or texto in u.get("email", "").lower()]
        for usuario in usuarios:
            self._insert_with_stripes(
                self.tree_usuarios,
                (usuario.get("Id"), usuario.get("name"), usuario.get("email"), usuario.get("Phone")),
            )

    def _buscar_reservas(self):
        texto = self.search_res_var.get().strip().lower()
        if not texto:
            self.refrescar_reservas()
            return

        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)

        reservas = [r for r in self.service.obtener_reservas() if texto in str(r.get("reserva", "")).lower() or texto in str(r.get("name", "")).lower()]
        for reserva in reservas:
            self._insert_with_stripes(
                self.tree_reservas,
                (
                    reserva.get("reservation_id"),
                    reserva.get("user_id"),
                    reserva.get("name"),
                    reserva.get("servicio", ""),
                    reserva.get("reserva"),
                    reserva.get("hora"),
                    reserva.get("estado"),
                ),
            )

    def _limpiar_filtros(self):
        self.search_user_var.set("")
        self.search_res_var.set("")
        self.refrescar_todo()

    def cargar_logs(self):
        try:
            with open("logs.txt", "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()

            self.logs_text.delete("1.0", tk.END)
            self.logs_text.insert(tk.END, contenido if contenido else "Sin registros todavía.")
            self._set_status("Logs cargados")
        except FileNotFoundError:
            self.logs_text.delete("1.0", tk.END)
            self.logs_text.insert(tk.END, "logs.txt no existe todavía.")
            self._set_status("logs.txt no encontrado")

    def limpiar_form_usuario(self):
        self.usuario_name.set("")
        self.usuario_email.set("")
        self.usuario_phone.set("")

    def limpiar_form_servicio(self):
        self.serv_tipo.set("general")
        self.serv_nombre.set("")
        self.serv_precio.set("")

    def limpiar_form_reserva(self):
        self.res_user_id.set("")
        self.res_reserva.set("")
        self.res_mensaje.set("")
        self.res_hora.set("")
        if self.combo_servicio["values"]:
            self.res_servicio.set(self.combo_servicio["values"][0])
        else:
            self.res_servicio.set("")

    def limpiar_form_actualizar(self):
        self.up_reservation_id.set("")
        self.up_nueva_hora.set("")

    def refrescar_todo(self):
        self.refrescar_usuarios()
        self.refrescar_servicios()
        self.refrescar_reservas()
        self.refrescar_reportes()
        self.cargar_logs()


def main():
    root = tk.Tk()
    ReservationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()