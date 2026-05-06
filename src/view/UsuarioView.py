import flet as ft

def UserView(page, auth_controller):
    page.title = "Perfil"
    user = getattr(page, "user_data", None)
    
    def formatear_fecha(fecha):
        if not fecha:
            return "No disponible"
        if isinstance(fecha, str) and ' ' in fecha:
            fecha_parte = fecha.split(' ')[0]  
            hora_parte = fecha.split(' ')[1]  
            año, mes, dia = fecha_parte.split('-')
            return f"{dia}/{mes}/{año} {hora_parte}"
        elif isinstance(fecha, str):
            año, mes, dia = fecha.split('-')
            return f"{dia}/{mes}/{año}"
        return str(fecha)
    
    nombre = ft.Text(f"Nombre: {user['nombre'] if user else 'Usuario'}", size=20, color=ft.Colors.PINK_200)
    apellido = ft.Text(f"Apellido: {user['apellido'] if user else 'Usuario'}", size=20, color=ft.Colors.PINK_200)
    telefono = ft.Text(f"Teléfono: {user['telefono'] if user else 'Usuario'}", size=20, color=ft.Colors.PINK_200)
    email = ft.Text(f"Email: {user['email'] if user else 'Usuario'}", size=20, color=ft.Colors.PINK_200)
    fecha_registro = ft.Text(f"Fecha de creación de la cuenta: {formatear_fecha(user['fecha_registro']) if user else 'Usuario'}", size=20, color=ft.Colors.PINK_200)
    ultimo_acceso = ft.Text(f"Último acceso: {formatear_fecha(user['ultimo_acceso']) if user else 'Usuario'}", size=20, color=ft.Colors.PINK_200)

    return ft.View(
        route="/perfil",
        controls=[
            ft.AppBar(
                title=ft.Text("Perfil de Usuario 💗", size=30),
                bgcolor=ft.Colors.PINK_200,
                color=ft.Colors.WHITE,
                actions=[
                    ft.IconButton(ft.Icons.BOOK, icon_color=ft.Colors.WHITE, on_click=lambda _: page.go("/dashboard")),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color=ft.Colors.WHITE, on_click=lambda _: page.go("/"))
                ],
            ),
            ft.Container(
                ft.Column([
                    ft.Icon(
                        icon=ft.Icons.AUTO_AWESOME,
                        size=60,
                        color=ft.Colors.PINK_200
                    ),

                    ft.Divider(thickness=8, color=ft.Colors.PINK_200),
                    ft.Row([nombre], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Divider(thickness=6, color=ft.Colors.PINK_200),
                    ft.Row([apellido], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Divider(thickness=6, color=ft.Colors.PINK_200),
                    ft.Row([telefono], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Divider(thickness=6, color=ft.Colors.PINK_200),
                    ft.Row([email], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Divider(thickness=8, color=ft.Colors.PINK_200),

                    ft.Row([fecha_registro], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Divider(thickness=8, color=ft.Colors.PINK_200),

                    ft.Row([ultimo_acceso], alignment=ft.MainAxisAlignment.CENTER),
                ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20, expand=True,
            ),
        ]
    )