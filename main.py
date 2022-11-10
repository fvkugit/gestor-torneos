import tkinter
import tkinter.messagebox
import customtkinter
import os
import sqlite3
from PIL import Image, ImageTk
from tkinter import Canvas, Menu
from datetime import date, datetime

# DOCUMENTATION CUSTOM TKINTER FROM GITHUB
# https://github.com/TomSchimansky/CustomTkinter/wiki

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")
PATH = os.path.dirname(os.path.realpath(__file__))

class App(customtkinter.CTk):

    WIDTH = 1280
    HEIGHT = 720
    global bd_name
    bd_name = "gestor.db"

    def __init__(self):
        super().__init__()

        self.barraMenu = Menu(self)
        self.title("Gestor de Torneos")
        self.iconbitmap("icon.ico")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.config(menu=self.barraMenu)
        self.mostrarBase()
        self.mostrarInicio()
        self.con = sqlite3.connect(bd_name)
        self.bd = self.con.cursor()

        configMenu = Menu(self.barraMenu, tearoff=0)
        configMenu.add_command(label="Base de datos", command=self.opcion_bd)
        configMenu.add_command(label="Creditos", command=self.opcion_creditos)
        self.barraMenu.add_cascade(label="Opciones", menu=configMenu)

    def opcion_bd(self):
        nuevoNombre = customtkinter.CTkInputDialog(master=self, text="Ingresa el nombre de la base de datos:", title="Configuracion")
        bd_name = nuevoNombre.get_input()
        self.con.close()
        self.con = sqlite3.connect(bd_name)
        self.bd = self.con.cursor()
    def opcion_creditos(self):
        tkinter.messagebox.showinfo(title="Creditos", message="Barral Facundo\nTrabajo Final Programación\nTerciario Urquiza DS 3ro2da")


    def agregar_jugador(self, id):
        jLista = self.bd.execute(f"SELECT * FROM jugadores WHERE id_jugador NOT IN (SELECT id_jugador FROM equipos_jugadores WHERE id_equipo = '{id}')")
        lista = []
        for j in jLista:
            lista.append("["+str(j[0])+"] " + j[1])
        
        if (len(lista) == 0):
            tkinter.messagebox.showerror(title="Error", message="No quedan jugadores disponibles para este equipo.")
            return

        self.window = customtkinter.CTkToplevel(self)
        window = self.window
        window.title("Nuevo jugador")
        window.iconbitmap("icon.ico")
        window.geometry("500x200")

        # Custom TKinter resizable method doesnt work.
        window.maxsize(500,200)
        window.minsize(500,200)

        window.columnconfigure(1, weight=1)

        self.window.label_msg = customtkinter.CTkLabel(window, text="ELIGE EL JUGADOR")
        label_msg = self.window.label_msg
        label_msg.grid(column=0, row=0, padx=20, pady=20, columnspan=2)
        

        entry_jugador = customtkinter.CTkOptionMenu(master=window, width=135, values = lista )
        entry_jugador.grid(column=0, columnspan=2, row=1, padx=5, pady=20)

        
        guardar = customtkinter.CTkButton(master=window, text="AGREGAR", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B",
                                                command=lambda x=id:self.agregar_jugador_a_equipo(x, entry_jugador.get()))
        guardar.grid(row=2, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

    def agregar_torneo(self, id):
        tLista = self.bd.execute(f"SELECT * FROM torneos WHERE id_torneo NOT IN (SELECT id_torneo FROM torneos_equipos WHERE id_equipo = '{id}')")
        lista = []
        for j in tLista:
            lista.append("["+str(j[0])+"] " + j[1])

        if (len(lista) == 0):
            tkinter.messagebox.showerror(title="Error", message="No quedan torneos disponibles para este equipo.")
            return

        self.window = customtkinter.CTkToplevel(self)
        window = self.window
        window.title("Nuevo torneo")
        window.iconbitmap("icon.ico")
        window.geometry("500x200")

        # Custom TKinter resizable method doesnt work.
        window.maxsize(500,200)
        window.minsize(500,200)

        window.columnconfigure(1, weight=1)

        self.window.label_msg = customtkinter.CTkLabel(window, text="ELIGE EL TORNEO")
        label_msg = self.window.label_msg
        label_msg.grid(column=0, row=0, padx=20, pady=20, columnspan=2)
        

        entry_torneo = customtkinter.CTkOptionMenu(master=window, width=135, values = lista )
        entry_torneo.grid(column=0, columnspan=2, row=1, padx=5, pady=20)

        
        guardar = customtkinter.CTkButton(master=window, text="AGREGAR", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B",
                                                command=lambda x=id:self.agregar_torneo_a_equipo(x, entry_torneo.get()))
        guardar.grid(row=2, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

    def agregar_partido_window(self, id):
        tLista = self.bd.execute(f"SELECT id_equipo, nombre FROM torneos_equipos LEFT JOIN equipos USING (id_equipo) WHERE id_torneo = '{id}'")
        lista = []
        for j in tLista:
            lista.append("["+str(j[0])+"] " + j[1])

        if (len(lista) == 0):
            tkinter.messagebox.showerror(title="Error", message="No hay equipos registrados en este torneo.")
            return

        self.window = customtkinter.CTkToplevel(self)
        window = self.window
        window.title("Nuevo partido")
        window.iconbitmap("icon.ico")
        window.geometry("500x425")

        # Custom TKinter resizable method doesnt work.
        window.maxsize(500,425)
        window.minsize(500,425)

        window.columnconfigure(1, weight=1)

        self.window.label_msg = customtkinter.CTkLabel(window, text="CARGAR DATOS DEL PARTIDO")
        label_msg = self.window.label_msg
        label_msg.grid(column=0, row=0, padx=20, pady=20, columnspan=2)
        
        label_equipo1 = customtkinter.CTkLabel(window, text="EQUIPO 1")
        label_equipo1.grid(column=0, row=1, padx=20, pady=20)
        entry_equipo1 = customtkinter.CTkOptionMenu(master=window, width=135, values = lista )
        entry_equipo1.grid(column=1, row=1, columnspan=2, padx=5, pady=20)
        label_golequipo1 = customtkinter.CTkLabel(window, text="GOLES EQUIPO 1")
        label_golequipo1.grid(column=0, row=2, padx=20, pady=20)
        entry_golequipo1 = customtkinter.CTkEntry(master=window,
                            placeholder_text="0",
                            width=170,
                            height=30,
                            border_width=2,
                            corner_radius=5)
        entry_golequipo1.grid(column=1, row=2, padx=30, pady=20)
        label_equipo2 = customtkinter.CTkLabel(window, text="EQUIPO 2")
        label_equipo2.grid(column=0, row=3, padx=20, pady=20)
        entry_equipo2 = customtkinter.CTkOptionMenu(master=window, width=135, values = lista )
        entry_equipo2.grid(column=1, row=3, columnspan=2, padx=5, pady=20)
        label_golequipo2 = customtkinter.CTkLabel(window, text="GOLES EQUIPO 2")
        label_golequipo2.grid(column=0, row=4, padx=20, pady=20)
        entry_golequipo2 = customtkinter.CTkEntry(master=window,
                            placeholder_text="0",
                            width=170,
                            height=30,
                            border_width=2,
                            corner_radius=5)
        entry_golequipo2.grid(column=1, row=4, padx=30, pady=20)

        
        guardar = customtkinter.CTkButton(master=window, text="AGREGAR", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B",
                                                command=lambda x=id:self.agregar_partido(x, entry_equipo1.get(), entry_equipo2.get(), entry_golequipo1.get(), entry_golequipo2.get()))
        guardar.grid(row=5, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")



    def crear_jugador(self):
            window = customtkinter.CTkToplevel(self)
            window.title("Nuevo jugador")
            window.iconbitmap("icon.ico")
            window.geometry("500x400")

            # Custom TKinter resizable method doesnt work.
            window.maxsize(500,400)
            window.minsize(500,400)


            window.columnconfigure(0, weight=1)

            label_msg = customtkinter.CTkLabel(window, text="INGRESAR DATOS DEL JUGADOR")
            label_msg.grid(column=0, row=0, padx=20, pady=20, columnspan=2)
            
            label_nombre = customtkinter.CTkLabel(window, text="Nombre completo")
            label_nombre.grid(column=0, row=1, padx=20, pady=20)
            entry_nombre = customtkinter.CTkEntry(master=window,
                               placeholder_text="John Doe",
                               width=170,
                               height=30,
                               border_width=2,
                               corner_radius=5)
            entry_nombre.grid(column=1, row=1, padx=30, pady=20)

            label_nac = customtkinter.CTkLabel(window, text="Fecha nacimiento")
            label_nac.grid(column=0, row=2, padx=5, pady=20)
            frame_nac = customtkinter.CTkFrame(master=window)
            frame_nac.grid(column=1, row=2, padx=30, pady=20)     
            entry_nac_dia = customtkinter.CTkOptionMenu(master=frame_nac, width=70, values = list(map(str, range(1,32))) )
            entry_nac_dia.grid(column=1, row=2, padx=5, pady=20)
            entry_nac_dia['values'] = list(range(1, 31))
            entry_nac_mes = customtkinter.CTkOptionMenu(master=frame_nac, width=70, values = list(map(str, range(1,13))))
            entry_nac_dia['values'] = list(range(1, 12))
            entry_nac_mes.grid(column=2, row=2, padx=5, pady=20)
            entry_nac_anio = customtkinter.CTkOptionMenu(master=frame_nac, width=70, values = list(map(str, range(1950,2023))))
            entry_nac_anio.set("2000")
            entry_nac_dia['values'] = list(range(1900, 2022))
            entry_nac_anio.grid(column=3, row=2, padx=5, pady=20)

            label_altura = customtkinter.CTkLabel(window, text="Altura")
            label_altura.grid(column=0, row=3, padx=20, pady=20)
            entry_altura = customtkinter.CTkEntry(master=window,
                               placeholder_text="1.80",
                               width=170,
                               height=30,
                               border_width=2,
                               corner_radius=5)
            entry_altura.grid(column=1, row=3, padx=30, pady=20)
            
            def accion_guardar():
                altura = entry_altura.get()
                dia = entry_nac_dia.get()
                mes = entry_nac_mes.get()
                anio = entry_nac_anio.get()
                nombre = entry_nombre.get()
                if (altura=="" or dia=="" or mes=="" or anio=="" or nombre==""):
                    label_msg.config(text_color="red",text="Error: Debes completar todos los campos")
                else:
                    label_msg.config(text_color="white",text="INGRESAR DATOS DEL JUGADOR")
                    self.guardar_jugador(nombre, dia, mes, anio, altura)
                    window.destroy()
                
            
            guardar = customtkinter.CTkButton(master=window, text="GUARDAR", border_width=2,
                                                    corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                    hover_color="#53AB5B", command=accion_guardar)
            guardar.grid(row=4, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

            
    def crear_equipo(self):
            window = customtkinter.CTkToplevel(self)
            window.title("Nuevo equipo")
            window.iconbitmap("icon.ico")
            window.geometry("500x270")

            # Custom TKinter resizable method doesnt work.
            window.maxsize(500,270)
            window.minsize(500,270)


            window.columnconfigure(0, weight=1)

            label_msg = customtkinter.CTkLabel(window, text="INGRESAR DATOS DEL EQUIPO")
            label_msg.grid(column=0, row=0, padx=20, pady=20, columnspan=2)
            
            label_nombre = customtkinter.CTkLabel(window, text="Nombre equipo")
            label_nombre.grid(column=0, row=1, padx=20, pady=20)
            entry_nombre = customtkinter.CTkEntry(master=window,
                               placeholder_text="Nuevo equipo",
                               width=170,
                               height=30,
                               border_width=2,
                               corner_radius=5)
            entry_nombre.grid(column=1, row=1, padx=30, pady=20)

            label_propietario = customtkinter.CTkLabel(window, text="Propietario")
            label_propietario.grid(column=0, row=3, padx=20, pady=20)
            entry_propietario = customtkinter.CTkEntry(master=window,
                               placeholder_text="John Doe",
                               width=170,
                               height=30,
                               border_width=2,
                               corner_radius=5)
            entry_propietario.grid(column=1, row=3, padx=30, pady=20)
            
            def accion_guardar():
                nombre = entry_nombre.get()
                propietario = entry_propietario.get()
                if (propietario=="" or nombre==""):
                    label_msg.config(text_color="red",text="Error: Debes completar todos los campos")
                else:
                    label_msg.config(text_color="white",text="INGRESAR DATOS DEL EQUIPO")
                    self.guardar_equipo(nombre, propietario)
                    window.destroy()
                
            
            guardar = customtkinter.CTkButton(master=window, text="GUARDAR", border_width=2,
                                                    corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                    hover_color="#53AB5B", command=accion_guardar)
            guardar.grid(row=4, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

            
    def crear_torneo(self):
            window = customtkinter.CTkToplevel(self)
            window.title("Nuevo torneo")
            window.iconbitmap("icon.ico")
            window.geometry("500x400")

            # Custom TKinter resizable method doesnt work.
            window.maxsize(500,400)
            window.minsize(500,400)


            window.columnconfigure(0, weight=1)

            label_msg = customtkinter.CTkLabel(window, text="INGRESAR DATOS DEL TORNEO")
            label_msg.grid(column=0, row=0, padx=20, pady=20, columnspan=2)
            
            label_nombre = customtkinter.CTkLabel(window, text="Nombre torneo")
            label_nombre.grid(column=0, row=1, padx=20, pady=20)
            entry_nombre = customtkinter.CTkEntry(master=window,
                               placeholder_text="Nuevo torneo",
                               width=170,
                               height=30,
                               border_width=2,
                               corner_radius=5)
            entry_nombre.grid(column=1, row=1, padx=30, pady=20)

            label_descripcion = customtkinter.CTkLabel(window, text="Descripcion")
            label_descripcion.grid(column=0, row=2, padx=20, pady=20)
            entry_descripcion = customtkinter.CTkEntry(master=window,
                               placeholder_text="Torneo en Rosario",
                               width=170,
                               height=30,
                               border_width=2,
                               corner_radius=5)
            entry_descripcion.grid(column=1, row=2, padx=30, pady=20)

            label_maximo = customtkinter.CTkLabel(window, text="Maximo equipos")
            label_maximo.grid(column=0, row=3, padx=20, pady=20)
            entry_maximo = customtkinter.CTkEntry(master=window,
                               placeholder_text="12",
                               width=170,
                               height=30,
                               border_width=2,
                               corner_radius=5)
            entry_maximo.grid(column=1, row=3, padx=30, pady=20)
            
            label_tipo = customtkinter.CTkLabel(window, text="Tipo de torneo")
            label_tipo.grid(column=0, row=4, padx=20, pady=20)
            entry_tipo = customtkinter.CTkEntry(master=window,
                               placeholder_text="Futbol 5",
                               width=170,
                               height=30,
                               border_width=2,
                               corner_radius=5)
            entry_tipo.grid(column=1, row=4, padx=30, pady=20)
            
            def accion_guardar():
                nombre = entry_nombre.get()
                descripcion = entry_descripcion.get()
                tipo = entry_tipo.get()
                maximo = entry_maximo.get()
                if (descripcion=="" or nombre=="" or tipo=="" or maximo==""):
                    label_msg.config(text_color="red",text="Error: Debes completar todos los campos")
                else:
                    label_msg.config(text_color="white",text="INGRESAR DATOS DEL TORNEO")
                    self.guardar_torneo(nombre, descripcion, tipo, maximo)
                    window.destroy()
                
            
            guardar = customtkinter.CTkButton(master=window, text="GUARDAR", border_width=2,
                                                    corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                    hover_color="#53AB5B", command=accion_guardar)
            guardar.grid(row=5, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

            




    def limpiarFrame(self, frame):
        if (self and hasattr(self, frame)):
            frm = getattr(self,frame)
            frm.destroy()
    
    
    def mostrarBase(self):
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.limpiarFrame('frame_right')
        self.frame_right = customtkinter.CTkFrame(master=self, bg_color="#292929")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

                # ============ frame scrolleable ============
        self.canvas_contenido = Canvas(self.frame_right, bg="#292929", bd=0, highlightthickness=0)
        self.contenido = customtkinter.CTkFrame(master=self.canvas_contenido, bg_color="#292929")
        self.canvas_scroll = customtkinter.CTkScrollbar(self.frame_right, command=self.canvas_contenido.yview)
        self.canvas_contenido.pack(side="left", fill="both", expand=True)
        self.canvas_scroll.pack(side="right", fill="both")
        self.canvas_contenido.configure(yscrollcommand=self.canvas_scroll.set)
        self.contenido.pack(fill="both", expand=True)
        self._frame_id = self.canvas_contenido.create_window((0,0),
                                 anchor='nw',
                                 window=self.contenido)
        self.contenido.bind('<Configure>', self.onFrameConfigure)
        self.canvas_contenido.bind('<Configure>', self.onCanvasConfigure)
        self.contenido.columnconfigure(0, weight=1)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(6, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Gestor de Torneos",
                                              text_font=("Roboto Medium", -16))  
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Menu",
                                              text_font=("Roboto Medium", -16)) 
        self.label_2.grid(row=2, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Torneos",
                                                command=self.boton_torneos)
        self.button_1.grid(row=3, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Jugadores",
                                                command=self.boton_jugadores)
        self.button_2.grid(row=4, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Equipos",
                                                command=self.boton_equipos)
        self.button_2.grid(row=5, column=0, pady=10, padx=20)

    # Metodos utiles
    def onFrameConfigure(self, event):       
        self.canvas_contenido.configure(scrollregion=self.contenido.bbox('all'))
    def onCanvasConfigure(self, event):
        width = event.width
        self.canvas_contenido.itemconfigure(self._frame_id, width=self.canvas_contenido.winfo_width())
    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))
    def age(self,nac):
        formated = date = datetime(year=int(nac[0:4]), month=int(nac[4:6]), day=int(nac[6:8]))
        today = date.today()
        age = today.year - formated.year - ((today.month, today.day) < (formated.month, formated.day))
        return age


    # Pantallas
    def mostrarInicio(self):
        self.mostrarBase()
        self.equipo_imagen1 = self.load_image("/logo.png", 400)
        self.image_label = tkinter.Label(master=self.contenido, image=self.equipo_imagen1, bg="#292929")
        self.image_label.grid(row=0, column=0, pady=(75,0), padx=20, sticky="nsew")
        self.titulo = customtkinter.CTkLabel(master=self.contenido,
                                                    text="Gestor de Torneos",
                                                    text_font=("Roboto Medium", 48),
                                                    anchor="center",
                                                    justify="center")
        self.titulo.grid(row=1, column=0, pady=50, padx=20, sticky="nsew")

    def mostrarTorneos(self):
        self.mostrarBase()
        self.agregar_torneo_imagen = self.load_image("/agregar.png", 20)

        # ============ tabla header ============
        self.header = customtkinter.CTkFrame(master=self.contenido)
        self.header.grid(row=0, column=0, columnspan=3, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
        self.header.rowconfigure(0, weight=1)
        self.header.columnconfigure(0, weight=1)

        self.hlabel_1 = customtkinter.CTkLabel(master=self.header,
                                                    text="Datos",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")
        self.hlabel_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.hlabel_2 = customtkinter.CTkLabel(master=self.header,
                                                    text="En curso",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="center") 
        self.hlabel_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.hlabel_3 = customtkinter.CTkLabel(master=self.header,
                                                    text="Tipo",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")
        self.hlabel_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.hlabel_4 = customtkinter.CTkLabel(master=self.header,
                                                    text="Accion",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  
        self.hlabel_4.grid(row=0, column=4, pady=10, padx=20, sticky="ew")
        # ============ / tabla header ============

        torneosLista = self.bd.execute(f"SELECT * FROM torneos")
        rowCount = 1
        for t in torneosLista:
            # ============ tabla fila ============
            self.frame_info = customtkinter.CTkFrame(master=self.contenido)
            self.frame_info.grid(row=rowCount, column=0, columnspan=3, rowspan=1, pady=(20, 10), padx=20, sticky="ew")
            self.frame_info.columnconfigure(0, weight=1)

            self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=str(t[1])+"\nMaximo: "+str(t[4])+" equipos",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="left")  # font name and size in px
            self.label_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
            self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text="No",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="center")  # font name and size in px
            self.label_2.grid(row=0, column=1, pady=10, padx=20, sticky="nsew")
            self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=t[3],
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="center")  # font name and size in px
            self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
            self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                    text="Gestionar",
                                                    command=lambda x=t[0]:self.gestionarTorneo(x))
            self.label_4.grid(row=0, column=4, pady=10, padx=20)

            rowCount += 1
            # ============ / tabla fila ============
        

        # ============ lateral derecho ============


        self.frame_info = customtkinter.CTkFrame(master=self.contenido)
        self.frame_info.grid(row=rowCount+1, column=0, columnspan=1, rowspan=2, pady=(20, 0), padx=20, sticky="nsew")

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.button_agregar = customtkinter.CTkButton(master=self.frame_info, image=self.agregar_torneo_imagen, text="Agregar nuevo torneo", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B", command=self.crear_torneo)
        self.button_agregar.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")




    def mostrarJugadores(self):
        self.mostrarBase()
        self.agregar_jugador_imagen = self.load_image("/agregar.png", 20)

        # ============ header ============
        self.header = customtkinter.CTkFrame(master=self.contenido)
        self.header.grid(row=0, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
        self.header.rowconfigure(0, weight=1)
        self.header.columnconfigure(0, weight=1)

        self.hlabel_1 = customtkinter.CTkLabel(master=self.header,
                                                    text="#",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.hlabel_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.hlabel_2 = customtkinter.CTkLabel(master=self.header,
                                                    text="Nombre y Apellido",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.hlabel_3 = customtkinter.CTkLabel(master=self.header,
                                                    text="Edad",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.hlabel_4 = customtkinter.CTkLabel(master=self.header,
                                                    text="Altura",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_4.grid(row=0, column=4, pady=10, padx=20, sticky="ew")
        self.hlabel_5 = customtkinter.CTkLabel(master=self.header,
                                                    text="Accion",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_5.grid(row=0, column=5, pady=10, padx=20, sticky="ew")
        # ============ header ============

        rowCounter = 1
        jugadoresLista = self.bd.execute("SELECT * FROM jugadores")
        self.jugador_imagen = self.load_image("/jugador-default.png", 55)
        # 0=ID, 1=NOMBRE, 2=FECHA NAC, 3=ALTURA
        for jugador in jugadoresLista:
            # ============ fila ============
            self.frame_info = customtkinter.CTkFrame(master=self.contenido)
            self.frame_info.grid(row=rowCounter, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")

            self.frame_info.rowconfigure(0, weight=1)
            self.frame_info.columnconfigure(0, weight=1)

            

            self.image_label = tkinter.Label(master=self.frame_info, image=self.jugador_imagen)
            self.image_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
            self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=jugador[1],
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  # font name and size in px
            self.label_1.grid(row=0, column=1, pady=10, padx=20, sticky="w")
            self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=self.age(str(jugador[2])),
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  # font name and size in px
            self.label_2.grid(row=0, column=2, pady=10, padx=20, sticky="w")
            self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=jugador[3],
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  # font name and size in px
            self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
            self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                    text="Eliminar", hover_color="#EE6B6E", fg_color="#F94449",
                                                    command=lambda id=jugador[0]:self.eliminar_jugador(id))
            self.label_4.grid(row=0, column=4, pady=10, padx=20)
            rowCounter += 1
            # ============ /fila ============


        self.frame_info = customtkinter.CTkFrame(master=self.contenido)
        self.frame_info.grid(row=rowCounter+1, column=0, columnspan=2, rowspan=2, pady=(20, 0), padx=20, sticky="nsew")

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.button_agregar = customtkinter.CTkButton(master=self.frame_info, image=self.agregar_jugador_imagen, text="Agregar nuevo jugador", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B", command=self.crear_jugador)
        self.button_agregar.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")
        # ============ row ============


    def mostrarEquipos(self):
        self.mostrarBase()
        self.agregar_jugador_imagen = self.load_image("/agregar.png", 20)
        # ============ header ============
        self.header = customtkinter.CTkFrame(master=self.contenido)
        self.header.grid(row=0, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
        self.header.rowconfigure(0, weight=1)
        self.header.columnconfigure(0, weight=1)

        self.hlabel_1 = customtkinter.CTkLabel(master=self.header,
                                                    text="#",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.hlabel_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.hlabel_2 = customtkinter.CTkLabel(master=self.header,
                                                    text="Equipo",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.hlabel_3 = customtkinter.CTkLabel(master=self.header,
                                                    text="Jugadores",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.hlabel_4 = customtkinter.CTkLabel(master=self.header,
                                                    text="Propietario",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_4.grid(row=0, column=4, pady=10, padx=20, sticky="ew")
        self.hlabel_5 = customtkinter.CTkLabel(master=self.header,
                                                    text="Accion",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_5.grid(row=0, column=5, pady=10, padx=20, sticky="ew")
        # ============ header ============
        
        rowCounter = 1
        equiposLista = self.bd.execute("SELECT * FROM equipos")
        asistente = self.con.cursor()
            
        self.equipo_imagen1 = self.load_image("/equipo-default.png", 55)
        # 0=ID, 1=NOMBRE, 2=FECHA NAC, 3=ALTURA
        for equipo in equiposLista:
            # ============ fila ============
            self.frame_info = customtkinter.CTkFrame(master=self.contenido)
            self.frame_info.grid(row=rowCounter, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")

            self.frame_info.rowconfigure(0, weight=1)
            self.frame_info.columnconfigure(0, weight=1)

            jugadoresReg = asistente.execute(f"SELECT count(*) FROM equipos_jugadores WHERE id_equipo = {equipo[0]}")
            jugadoresReg = jugadoresReg.fetchall()[0][0]

            self.image_label = tkinter.Label(master=self.frame_info, image=self.equipo_imagen1)
            self.image_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
            self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=equipo[1],
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  # font name and size in px
            self.label_1.grid(row=0, column=1, pady=10, padx=20, sticky="w")
            self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=f"{jugadoresReg} Jugadores",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  # font name and size in px
            self.label_2.grid(row=0, column=2, pady=10, padx=20, sticky="w")
            self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=equipo[2],
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  # font name and size in px
            self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
            self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                    text="Gestionar",
                                                    command=lambda id=equipo[0]:self.gestionarEquipo(id))
            self.label_4.grid(row=0, column=4, pady=10, padx=20)
            rowCounter += 1
            # ============ /fila ============

        self.frame_info = customtkinter.CTkFrame(master=self.contenido)
        self.frame_info.grid(row=rowCounter+1, column=0, columnspan=1, rowspan=2, pady=(20, 0), padx=20, sticky="nsew")

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.button_agregar = customtkinter.CTkButton(master=self.frame_info, image=self.agregar_jugador_imagen, text="Agregar nuevo equipo", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B", command=self.crear_equipo)
        self.button_agregar.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")
        # ============ row ============

        
    def gestionarEquipo(self, id):
        self.mostrarBase()

        self.contenido.columnconfigure((0,1), weight=1)

        # ============ torneos h ============
        equipoNombre = self.bd.execute(f"SELECT nombre FROM equipos WHERE id_equipo = {id}")
        equipoNombre = equipoNombre.fetchall()
        equipoNombre = equipoNombre[0][0]
        titulo = customtkinter.CTkLabel(master=self.contenido,
                                            text="Gestionar: " + equipoNombre,
                                            text_font=("Roboto Medium", 22),
                                            anchor="center",
                                            justify="center")
        titulo.grid(row=0, column=0, pady=(20,10), padx=20, columnspan=4, sticky="nsew")
        torneos = customtkinter.CTkLabel(master=self.contenido,
                                            text="Torneos",
                                            text_font=("Roboto Medium", 18),
                                            anchor="center",
                                            justify="center")
        torneos.grid(row=1, column=0, pady=(20,10), padx=20, sticky="nsew")
        jugadores = customtkinter.CTkLabel(master=self.contenido,
                                            text="Jugadores",
                                            text_font=("Roboto Medium", 18),
                                            anchor="center",
                                            justify="center")
        jugadores.grid(row=1, column=1, pady=(20,10), padx=20, sticky="nsew")

        self.header = customtkinter.CTkFrame(master=self.contenido)
        self.header.grid(row=2, column=0, columnspan=1, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
        self.header.columnconfigure(2, weight=1)

        self.hlabel_1 = customtkinter.CTkLabel(master=self.header,
                                                    text="Nombre",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")
        self.hlabel_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.hlabel_2 = customtkinter.CTkLabel(master=self.header,
                                                    text="Tipo",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left") 
        self.hlabel_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.hlabel_3 = customtkinter.CTkLabel(master=self.header,
                                                    text="Accion",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  
        self.hlabel_3.grid(row=0, column=2, pady=10, padx=20, sticky="ew")
        # ============ torneos h ============

        rowCounter = 3
        rowTorneos = 3
        idequipo = id
        torneosLista = self.bd.execute(f"SELECT id_torneo, nombre, tipo FROM torneos_equipos JOIN torneos USING (id_torneo) WHERE id_equipo = {idequipo}")
        # asistente = self.con.cursor()

        for torneo in torneosLista:
            # ============ tabla fila ============
            self.frame_info = customtkinter.CTkFrame(master=self.contenido)
            self.frame_info.grid(row=rowTorneos, column=0, columnspan=1, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
            self.frame_info.columnconfigure(4, weight=1)


            self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=torneo[1],
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="left")  # font name and size in px
            self.label_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
            self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                        text=torneo[2],
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="center")  # font name and size in px
            self.label_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
            self.label_3 = customtkinter.CTkButton(master=self.frame_info,
                                                    text="Eliminar", hover_color="#EE6B6E", fg_color="#F94449",
                                                    command=lambda id=torneo[0]:self.eliminar_torneo_a_equipo(id, idequipo))
            self.label_3.grid(row=0, column=4, pady=10, padx=20)

            rowTorneos += 1
            # ============ / tabla fila ============

        # ============ header ============
        self.header2 = customtkinter.CTkFrame(master=self.contenido)
        self.header2.grid(row=2, column=1, pady=(20, 0), padx=20, sticky="nsew")
        self.header2.columnconfigure(2, weight=1)

        self.hlabel_1 = customtkinter.CTkLabel(master=self.header2,
                                                    text="Nombre",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.hlabel_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.hlabel_2 = customtkinter.CTkLabel(master=self.header2,
                                                    text="Edad",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.hlabel_3 = customtkinter.CTkLabel(master=self.header2,
                                                    text="Accion",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_3.grid(row=0, column=2, pady=10, padx=20, sticky="ew")
        # ============ header ============

        idequipo = id
        jugadoresLista = self.bd.execute(f"SELECT id_jugador, nombre, fecha_nacimiento FROM equipos_jugadores JOIN jugadores USING (id_jugador) WHERE id_equipo = {idequipo}")
        # asistente = self.con.cursor()
        rowJugadores = 3

        for jugador in jugadoresLista:
            # ============ tabla fila ============
            self.fila = customtkinter.CTkFrame(master=self.contenido)
            self.fila.grid(row=rowJugadores, column=1, columnspan=1, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
            self.fila.columnconfigure(4, weight=1)
            self.hlabel_1 = customtkinter.CTkLabel(master=self.fila,
                                                        text=jugador[1],
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="left")  # font name and size in px
            self.hlabel_1.grid(row=1, column=0, pady=10, padx=20, sticky="w")
            self.hlabel_2 = customtkinter.CTkLabel(master=self.fila,
                                                        text=self.age(str(jugador[2])),
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  # font name and size in px
            self.hlabel_2.grid(row=1, column=1, pady=10, padx=20, sticky="w")
            self.hlabel_3 = customtkinter.CTkButton(master=self.fila,
                                                    text="Eliminar", hover_color="#EE6B6E", fg_color="#F94449",
                                                    command=lambda id=jugador[0]:self.eliminar_jugador_a_equipo(idequipo,id))
            self.hlabel_3.grid(row=1, column=4, pady=10, padx=20)

            rowJugadores += 1
            # ============ / tabla fila ============

        rowCounter = max(rowJugadores, rowTorneos)

        self.frame_info = customtkinter.CTkFrame(master=self.contenido)
        self.frame_info.grid(row=rowTorneos, column=0, pady=(20, 0), padx=20, sticky="nsew")
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        self.button_eliminar = customtkinter.CTkButton(master=self.frame_info, text="Agregar torneo", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B", command=lambda x=id:self.agregar_torneo(x))
        self.button_eliminar.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

        self.frame_info = customtkinter.CTkFrame(master=self.contenido)
        self.frame_info.grid(row=rowJugadores, column=1, pady=(20, 0), padx=20, sticky="nsew")
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        self.button_eliminar = customtkinter.CTkButton(master=self.frame_info, text="Agregar jugador", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B", command=lambda x=id:self.agregar_jugador(x))
        self.button_eliminar.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

        
        self.frame_info = customtkinter.CTkFrame(master=self.contenido)
        self.frame_info.grid(row=rowCounter+2, column=0, columnspan=2, rowspan=2, pady=(20, 0), padx=20, sticky="nsew")
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        self.button_eliminar = customtkinter.CTkButton(master=self.frame_info, text="Eliminar este equipo", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#FF2827", fg_color=("gray84", "gray25"),
                                                hover_color="#FF3230", command=lambda x=id:self.eliminar_equipo(x))
        self.button_eliminar.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")
    
    def gestionarTorneo(self, id):
        self.mostrarBase()
        def headerGTorneo():
            self.contenido.columnconfigure((0,1), weight=1)

            # ============ torneos h ============
            torneoNombre = self.bd.execute(f"SELECT nombre FROM torneos WHERE id_torneo = {id}")
            torneoNombre = torneoNombre.fetchall()
            torneoNombre = torneoNombre[0][0]
            verPartidos = customtkinter.CTkButton(master=self.contenido,
                                                        text="PARTIDOS",
                                                        command=lambda id=1:mostrarPartidos())
            verPartidos.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
            verTabla = customtkinter.CTkButton(master=self.contenido,
                                                        text="TABLA POSICIONES",
                                                        command=lambda id=1:mostrarTabla())
            verTabla.grid(row=1, column=1, pady=10, padx=20, sticky="nsew")
            titulo = customtkinter.CTkLabel(master=self.contenido,
                                                text="Gestionar: " + torneoNombre,
                                                text_font=("Roboto Medium", 22),
                                                anchor="center",
                                                justify="center")
            titulo.grid(row=0, column=0, pady=(20,10), padx=20, columnspan=4, sticky="nsew")
        headerGTorneo()

        def mostrarPartidos():
            self.mostrarBase()
            headerGTorneo()
            self.header = customtkinter.CTkFrame(master=self.contenido)
            self.header.grid(row=2, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
            self.header.columnconfigure((0,1), weight=1)

            self.hlabel_1 = customtkinter.CTkLabel(master=self.header,
                                                        text="Equipo 1",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="left")
            self.hlabel_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
            self.hlabel_2 = customtkinter.CTkLabel(master=self.header,
                                                        text="Equipo 2",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="left") 
            self.hlabel_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
            self.hlabel_3 = customtkinter.CTkLabel(master=self.header,
                                                        text="Resultado",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="left")  
            self.hlabel_3.grid(row=0, column=2, pady=10, padx=20, sticky="ew")
            self.hlabel_4 = customtkinter.CTkLabel(master=self.header,
                                                        text="Accion",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  
            self.hlabel_4.grid(row=0, column=3, pady=10, padx=20, sticky="ew")
            # ============ torneos h ============

            rowPartidos = 3
            idequipo = id
            partidosLista = self.bd.execute(f"SELECT p.id_partido, p.marcador_1, p.marcador_2, e1.nombre, e2.nombre FROM partidos p JOIN equipos e1 ON equipo_1 = e1.id_equipo JOIN equipos e2 ON equipo_2 = e2.id_equipo WHERE id_torneo = {id};")
            # asistente = self..cursor()


            for partido in partidosLista:
                # ============ tabla fila ============
                self.frame_info = customtkinter.CTkFrame(master=self.contenido)
                self.frame_info.grid(row=rowPartidos, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
                self.frame_info.columnconfigure((0,1), weight=1)


                self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                            text=partido[3],
                                                            text_font=("Roboto Medium", -16),
                                                            anchor="w",
                                                            justify="left")  # font name and size in px
                self.label_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
                self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                            text=partido[4],
                                                            text_font=("Roboto Medium", -16),
                                                            anchor="w",
                                                            justify="center")  # font name and size in px
                self.label_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
                self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                            text=str(partido[1]) +" - "+ str(partido[2]),
                                                            text_font=("Roboto Medium", -16),
                                                            anchor="w",
                                                            justify="center")  # font name and size in px
                self.label_3.grid(row=0, column=2, pady=10, padx=20, sticky="w")
                self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                        text="Eliminar", hover_color="#EE6B6E", fg_color="#F94449",
                                                        command=lambda id=partido[0]:self.eliminar_torneo_a_equipo(id, idequipo))
                self.label_4.grid(row=0, column=3, pady=10, padx=20)

                rowPartidos += 1
                # ============ / tabla fila ============
            self.frame_info = customtkinter.CTkFrame(master=self.contenido)
            self.frame_info.grid(row=rowPartidos, column=0, pady=(20, 0), padx=20, sticky="nsew", columnspan=2)
            self.frame_info.rowconfigure(0, weight=1)
            self.frame_info.columnconfigure(0, weight=1)
            self.button_eliminar = customtkinter.CTkButton(master=self.frame_info, text="Agregar partido", border_width=2,
                                                    corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                    hover_color="#53AB5B", command=lambda x=id:self.agregar_partido_window(x))
            self.button_eliminar.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")
        mostrarPartidos()
        def mostrarTabla():
            self.mostrarBase()
            headerGTorneo()
            self.header = customtkinter.CTkFrame(master=self.contenido)
            self.header.grid(row=2, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
            self.header.columnconfigure((0,1,2,3,4), weight=1)

            self.hlabel_1 = customtkinter.CTkLabel(master=self.header,
                                                        text="Equipo",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="w",
                                                        justify="left")
            self.hlabel_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
            self.hlabel_2 = customtkinter.CTkLabel(master=self.header,
                                                        text="Partidos Jugados",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center") 
            self.hlabel_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
            self.hlabel_3 = customtkinter.CTkLabel(master=self.header,
                                                        text="Partidos Empatados",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center") 
            self.hlabel_3.grid(row=0, column=2, pady=10, padx=20, sticky="w")
            self.hlabel_3 = customtkinter.CTkLabel(master=self.header,
                                                        text="Partidos Ganados",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center") 
            self.hlabel_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
            self.hlabel_4 = customtkinter.CTkLabel(master=self.header,
                                                        text="Puntos",
                                                        text_font=("Roboto Medium", -16),
                                                        anchor="center",
                                                        justify="center")  
            self.hlabel_4.grid(row=0, column=4, pady=10, padx=20, sticky="ew")
            # ============ torneos h ============

            rowTabla = 3
            tablaLista = self.bd.execute(f"SELECT x.id_equipo, x.nombre, ganados, jugados, IFNULL(empatados, 0) as empatados, ganados*3+IFNULL(empatados, 0) as puntos FROM (SELECT t.id_equipo, e.nombre, count(lista.nombre) as ganados FROM torneos_equipos t LEFT JOIN (SELECT p1.equipo_1, p1.id_partido, e.nombre FROM equipos e LEFT JOIN partidos p1 ON e.id_equipo = p1.equipo_1 WHERE id_torneo = {id} AND marcador_1 > marcador_2 UNION SELECT p2.equipo_2, p2.id_partido, e.nombre FROM equipos e LEFT JOIN partidos p2 ON e.id_equipo = p2.equipo_2 WHERE id_torneo = {id} AND marcador_1 < marcador_2 ) lista  ON lista.equipo_1 = t.id_equipo LEFT JOIN equipos e ON t.id_equipo = e.id_equipo WHERE t.id_torneo = {id}  GROUP BY t.id_equipo  ORDER BY count(lista.nombre) DESC) x  LEFT JOIN  	( SELECT id_equipo, count(*) as jugados FROM partidos p LEFT JOIN equipos e ON (id_equipo = p.equipo_1 OR id_equipo = p.equipo_2) WHERE id_torneo = {id} GROUP BY id_equipo ) y ON x.id_equipo = y.id_equipo LEFT JOIN 	(SELECT id_equipo, count(*) as empatados FROM partidos p  LEFT JOIN equipos e ON (p.equipo_1 = e.id_equipo OR p.equipo_2 = e.id_equipo) WHERE p.marcador_1 = p.marcador_2 AND p.id_torneo = {id} GROUP BY id_equipo) z ON x.id_equipo = z.id_equipo ORDER BY puntos DESC ")
            # asistente = self.con.cursor()

            for fila in tablaLista:
                # ============ tabla fila ============
                self.frame_info = customtkinter.CTkFrame(master=self.contenido)
                self.frame_info.grid(row=rowTabla, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
                self.frame_info.columnconfigure((0,1,2,3,4), weight=1)


                self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                            text=fila[1],
                                                            text_font=("Roboto Medium", -16),
                                                            anchor="w",
                                                            justify="left")  # font name and size in px
                self.label_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
                self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                            text=fila[3],
                                                            text_font=("Roboto Medium", -16),
                                                            anchor="center",
                                                            justify="center")  # font name and size in px
                self.label_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
                self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                            text=fila[4],
                                                            text_font=("Roboto Medium", -16),
                                                            anchor="center",
                                                            justify="center")  # font name and size in px
                self.label_3.grid(row=0, column=2, pady=10, padx=20, sticky="w")
                self.label_4 = customtkinter.CTkLabel(master=self.frame_info,
                                                            text=fila[2],
                                                            text_font=("Roboto Medium", -16),
                                                            anchor="center",
                                                            justify="center")  # font name and size in px
                self.label_4.grid(row=0, column=3, pady=10, padx=20, sticky="w")
                self.label_5 = customtkinter.CTkLabel(master=self.frame_info,
                                                            text=fila[2]*3+fila[4],
                                                            text_font=("Roboto Medium", -16),
                                                            anchor="center",
                                                            justify="center")  # font name and size in px
                self.label_5.grid(row=0, column=4, pady=10, padx=20, sticky="ew")

                rowTabla += 1
                # ============ / tabla fila ============



    def boton_torneos(self):
        self.mostrarTorneos()

    def boton_jugadores(self):
        self.mostrarJugadores()

    def boton_equipos(self):
        self.mostrarEquipos()


    def on_closing(self, event=0):
        self.con.close()
        self.destroy()

    # Gestion de datos SQLITE
    def formatFecha(self,d,m,a):
        if (len(d) == 1):
            d = "0"+d
        if (len(m) == 1):
            m = "0"+m
        return a+m+d

    def guardar_jugador(self, nombre, dia, mes, anio, altura):
        fecha = self.formatFecha(dia, mes, anio)
        query = (f"INSERT INTO jugadores VALUES (NULL, '{nombre}', '{fecha}', '{altura}')")
        self.bd.execute(query)
        self.con.commit()
        self.mostrarJugadores()
        
    def eliminar_jugador(self, id):
        if not tkinter.messagebox.askyesno(title="Confirmar acción", message="Seguro deseas eliminar este jugador?"):return
        query = (f"DELETE FROM jugadores WHERE id_jugador = {id}")
        self.bd.execute(query)
        self.con.commit()
        self.mostrarJugadores()

    def guardar_equipo(self, nombre, propietario):
        query = (f"INSERT INTO equipos VALUES (NULL, '{nombre}', '{propietario}', NULL)")
        self.bd.execute(query)
        self.con.commit()
        self.mostrarEquipos()

    def eliminar_equipo(self, id):
        if not tkinter.messagebox.askyesno(title="Confirmar acción", message="Seguro deseas eliminar este equipo?"):return
        query = (f"DELETE FROM equipos WHERE id_equipo = {id}")
        self.bd.execute(query)
        self.con.commit()
        self.mostrarEquipos()

    def guardar_torneo(self, nombre, descripcion, tipo, limite):
        query = (f"INSERT INTO torneos VALUES (NULL, '{nombre}', '{descripcion}', '{tipo}', '{limite}', DATE('now'))")
        self.bd.execute(query)
        self.con.commit()
        self.mostrarTorneos()

    def agregar_jugador_a_equipo(self,idEquipo,idj):
        idJugador = idj[idj.find("[")+1:idj.find("]")]
        query = (f"INSERT INTO equipos_jugadores VALUES ('{idEquipo}', '{idJugador}', DATE('now'))")
        try:
            self.bd.execute(query)
            self.con.commit()
            self.window.destroy()
        except sqlite3.IntegrityError as e:
            self.window.label_msg.configure(text_color="red",text="Error: El jugador ya se encuentra en el equipo")
        self.gestionarEquipo(idEquipo)
    def eliminar_jugador_a_equipo(self,idEquipo,idj):
        if not tkinter.messagebox.askyesno(title="Confirmar acción", message="Seguro deseas eliminar al jugador de este equipo?"):return
        # idJugador = idj[idj.find("[")+1:idj.find("]")]
        query = (f"DELETE FROM equipos_jugadores WHERE id_equipo = '{idEquipo}' AND id_jugador = '{idj}'")
        try:
            self.bd.execute(query)
            self.con.commit()
        except sqlite3.IntegrityError as e:
            self.window.label_msg.configure(text_color="red",text="Error: El jugador ya se encuentra en el equipo")
        self.gestionarEquipo(idEquipo)
    
    def agregar_torneo_a_equipo(self, idEquipo, idt):
        idTorneo = idt[idt.find("[")+1:idt.find("]")]
        query = (f"INSERT INTO torneos_equipos VALUES ('{idTorneo}', '{idEquipo}', DATE('now'))")
        try:
            self.bd.execute(query)
            self.con.commit()
            self.window.destroy()
        except sqlite3.IntegrityError as e:
            self.window.label_msg.configure(text_color="red",text="Error: El torneo ya se encuentra en el equipo")
        self.gestionarEquipo(idEquipo)

    def eliminar_torneo_a_equipo(self, idTorneo, idEquipo):
        if not tkinter.messagebox.askyesno(title="Confirmar acción", message="Seguro deseas eliminar el equipo de este torneo?"):return
        query = (f"DELETE FROM torneos_equipos WHERE id_torneo = '{idTorneo}' AND id_equipo = '{idEquipo}'")
        self.bd.execute(query)
        self.con.commit()
        self.gestionarEquipo(idEquipo)

    def eliminar_torneo(self, id):
        if not tkinter.messagebox.askyesno(title="Confirmar acción", message="Seguro deseas eliminar este torneo?"):return
        query = (f"DELETE FROM torneos WHERE id_torneo = {id}")
        self.bd.execute(query)
        self.con.commit()
        self.mostrarTorneos()

    def agregar_partido(self, idTorneo, ide1, ide2, ide1g, ide2g):
        idEquipo1 = ide1[ide1.find("[")+1:ide1.find("]")]
        idEquipo2 = ide2[ide2.find("[")+1:ide2.find("]")]
        query = (f"INSERT INTO partidos VALUES (NULL, '{idTorneo}', '{idEquipo1}', '{idEquipo2}', '{ide1g}', '{ide2g}', DATE('now'))")
        try:
            self.bd.execute(query)
            self.con.commit()
            self.window.destroy()
        except sqlite3.IntegrityError as e:
            self.window.label_msg.configure(text_color="red",text="Error: El torneo ya se encuentra en el equipo")
        self.gestionarTorneo(idTorneo)


if __name__ == "__main__":
    app = App()
    app.mainloop()
