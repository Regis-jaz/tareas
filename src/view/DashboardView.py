import flet as ft
from datetime import datetime

def DashboardView(page, tarea_controller):
    user = getattr(page, "user_data", None)
    
    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    fecha_limite = ft.DatePicker(
        first_date=datetime(2000, 1, 1),
        last_date=datetime(2030, 12, 31)
    )
    
    hora_limite = ft.TimePicker()
    
    page.overlay.append(fecha_limite)
    page.overlay.append(hora_limite)

    def abrir_calendario(e):
        fecha_limite.open = True
        page.update()

    def abrir_reloj(e):
        hora_limite.open = True
        page.update()
    
    btn_fecha = ft.ElevatedButton(
        "Seleccionar Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=abrir_calendario,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PINK_200,
            color=ft.Colors.WHITE,
        ),
    )
    
    btn_hora = ft.ElevatedButton(
        "Seleccionar Hora",
        icon=ft.Icons.ACCESS_TIME,
        on_click=abrir_reloj,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PINK_200,
            color=ft.Colors.WHITE,
        ),
    )
    
    txt_fecha_seleccionada = ft.Text("Fecha: No seleccionada", color=ft.Colors.PINK_200)
    txt_hora_seleccionada = ft.Text("Hora: No seleccionada", color=ft.Colors.PINK_200)
    
    def actualizar_fecha(e):
        if fecha_limite.value:
            txt_fecha_seleccionada.value = f"Fecha: {fecha_limite.value.strftime('%d/%m/%Y')}"
        else:
            txt_fecha_seleccionada.value = "Fecha: No seleccionada"
        page.update()
    
    def actualizar_hora(e):
        if hora_limite.value:
            txt_hora_seleccionada.value = f"Hora: {hora_limite.value.strftime('%H:%M')}"
        else:
            txt_hora_seleccionada.value = "Hora: No seleccionada"
        page.update()
    
    fecha_limite.on_change = actualizar_fecha
    hora_limite.on_change = actualizar_hora
    
    def eliminar_tarea(id_tarea):
        success, msg = tarea_controller.eliminar_tarea(id_tarea)
        if success:
            cargar_tareas()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.PINK_200)
            page.snack_bar.open = True
            page.update()
    
    def formatear_fecha(fecha):
        if not fecha:
            return "No disponible"
        if isinstance(fecha, datetime):
            return fecha.strftime('%d/%m/%Y %H:%M:%S')
        if isinstance(fecha, str):
            if ' ' in fecha:
                fecha_parte = fecha.split(' ')[0]
                hora_parte = fecha.split(' ')[1]
                año, mes, dia = fecha_parte.split('-')
                return f"{dia}/{mes}/{año} {hora_parte}"
            else:
                año, mes, dia = fecha.split('-')
                return f"{dia}/{mes}/{año}"
        return str(fecha)
    
    def cargar_tareas():
        if user and 'id_usuario' in user:
            lista_tareas.controls.clear()
            tareas = tarea_controller.obtener_lista(user['id_usuario'])
            
            for t in tareas:
                fecha_creacion_texto = ""
                if t.get('fecha_creacion'):
                    fecha_creacion_texto = f"\nCreada: {formatear_fecha(t['fecha_creacion'])}"
                
                fecha_limite_texto = ""
                if t.get('fecha_limite'):
                    fecha_limite_texto = f"\nFecha límite: {formatear_fecha(t['fecha_limite'])}"
                
                hora_limite_texto = ""
                if t.get('hora_limite'):
                    hora_texto = str(t['hora_limite'])
                    if len(hora_texto) > 5:
                        hora_texto = hora_texto[:5]
                    hora_limite_texto = f" - Hora: {hora_texto}"
                
                lista_tareas.controls.append(
                    ft.Card(
                        color=ft.Colors.PINK_50,
                        content=ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(t['titulo'], weight="bold", color=ft.Colors.PINK_200),
                                subtitle=ft.Text(
                                    f"{t.get('descripcion', 'Sin descripción')}\n"
                                    f"Prioridad: {t.get('prioridad', 'media')}\n"
                                    f"Categoría: {t.get('clasificacion', 'personal')}\n"
                                    f"Estado: {t.get('estado', 'pendiente')}"
                                    f"{fecha_limite_texto}{hora_limite_texto}{fecha_creacion_texto}",
                                    color=ft.Colors.PINK_200
                                ),
                                trailing=ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.PINK_200,
                                    on_click=lambda e, id_t=t['id_tarea']: eliminar_tarea(id_t)
                                )
                            ),
                            padding=10
                        )
                    )
                )
            page.update()
    
    txt_titulo = ft.TextField(label="Título", expand=True, border_color=ft.Colors.PINK_200)
    txt_descripcion = ft.TextField(label="Descripción", expand=True, multiline=True, max_lines=3, border_color=ft.Colors.PINK_200)
    
    prioridad_dropdown = ft.Dropdown(
        label="Prioridad",
        value="media",
        width=150,
        options=[
            ft.dropdown.Option("alta", "Alta"),
            ft.dropdown.Option("media", "Media"),
            ft.dropdown.Option("baja", "Baja"),
        ]
    )
    
    clasificacion_dropdown = ft.Dropdown(
        label="Clasificación",
        value="personal",
        width=150,
        options=[
            ft.dropdown.Option("personal", "Personal"),
            ft.dropdown.Option("trabajo", "Trabajo"),
            ft.dropdown.Option("estudio", "Estudio"),
            ft.dropdown.Option("hogar", "Hogar"),
            ft.dropdown.Option("salud", "Salud"),
            ft.dropdown.Option("otro", "Otro"),
        ]
    )
    
    estado_dropdown = ft.Dropdown(
        label="Estado",
        value="pendiente",
        width=150,
        options=[
            ft.dropdown.Option("pendiente", "Pendiente"),
            ft.dropdown.Option("en_progreso", "En Progreso"),
            ft.dropdown.Option("completada", "Completada"),
            ft.dropdown.Option("cancelada", "Cancelada"),
        ]
    )
    
    def agregar_tarea(e):
        if user and 'id_usuario' in user:
            if not txt_titulo.value:
                page.snack_bar = ft.SnackBar(ft.Text("El título es obligatorio"), bgcolor=ft.Colors.PINK_200)
                page.snack_bar.open = True
                page.update()
                return
            
            val_fecha = None
            val_hora = None

            if fecha_limite.value:
                val_fecha = fecha_limite.value.strftime('%Y-%m-%d')
            
            if hora_limite.value:
                val_hora = hora_limite.value.strftime('%H:%M:%S')

            success, msg = tarea_controller.guardar_nueva(
                user['id_usuario'],
                txt_titulo.value,
                txt_descripcion.value,
                prioridad_dropdown.value,
                clasificacion_dropdown.value,
                estado_dropdown.value,
                val_fecha,  
                val_hora   
            )
            
            if success:
                txt_titulo.value = ""
                txt_descripcion.value = ""
                fecha_limite.value = None
                hora_limite.value = None
                txt_fecha_seleccionada.value = "Fecha: No seleccionada"
                txt_hora_seleccionada.value = "Hora: No seleccionada"
                cargar_tareas()
                page.snack_bar = ft.SnackBar(ft.Text(msg, color="white"), bgcolor=ft.Colors.PINK_200)
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(msg, color="white"), bgcolor=ft.Colors.PINK_200)
                page.snack_bar.open = True
                page.update()
    
    def mostrar_perfil(e):
        if not user:
            return
        telefono = user.get('telefono') or 'No registrado'
        dialogo = ft.AlertDialog(
            title=ft.Text("Perfil 💗", color=ft.Colors.PINK_200),
            content=ft.Column([
                ft.Text(f"ID: {user.get('id_usuario', '')}", color=ft.Colors.PINK_200),
                ft.Text(f"Nombre: {user.get('nombre', '')}", color=ft.Colors.PINK_200),
                ft.Text(f"Apellido: {user.get('apellido', '')}", color=ft.Colors.PINK_200),
                ft.Text(f"Teléfono: {user.get('telefono', '')}", color=ft.Colors.PINK_200),
                ft.Text(f"Email: {user.get('email', '')}", color=ft.Colors.PINK_200),
                ft.Text(f"Fecha de registro: {formatear_fecha(user.get('fecha_registro'))}", color=ft.Colors.PINK_200),  
                ft.Text(f"Último acceso: {formatear_fecha(user.get('ultimo_acceso'))}", color=ft.Colors.PINK_200),
            ], tight=True)
        )
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()
        
    cargar_tareas()
    
    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Bienvenido, {user.get('nombre', 'Usuario') if user else 'Usuario'} 💗"),
                bgcolor=ft.Colors.PINK_200,
                color=ft.Colors.WHITE,
                actions=[
                    ft.IconButton(ft.Icons.PERSON, icon_color=ft.Colors.WHITE, on_click=mostrar_perfil),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color=ft.Colors.WHITE, on_click=lambda _: page.go("/"))
                ],
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Nueva Tarea 💗", size=18, weight="bold", color=ft.Colors.PINK_200),
                    ft.Row([txt_titulo, txt_descripcion]),
                    ft.Row([
                        prioridad_dropdown,
                        clasificacion_dropdown,
                        estado_dropdown,
                    ], spacing=20, wrap=True),
                    ft.Row([
                        btn_fecha,
                        btn_hora,
                    ], spacing=20, wrap=True),
                    ft.Row([
                        txt_fecha_seleccionada,
                        txt_hora_seleccionada,
                    ], spacing=20, wrap=True),
                    ft.ElevatedButton(
                        "Guardar 💗",
                        on_click=agregar_tarea,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PINK_200,
                            color=ft.Colors.WHITE,
                            padding=15,
                        ),
                    ),
                    ft.Divider(color=ft.Colors.PINK_200),
                    ft.Text("Mis Tareas 💗", size=18, weight="bold", color=ft.Colors.PINK_200),
                    lista_tareas
                ], expand=True),
                padding=20,
                expand=True
            ),
        ]
    )