import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import os

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
PATH = os.path.dirname(os.path.realpath(__file__))


class App(customtkinter.CTk):

    WIDTH = 1280
    HEIGHT = 720

    def __init__(self):
        super().__init__()

        self.title("Gestor de Torneos")
        self.iconbitmap("icon.ico")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(6, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Gestor de Torneos",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Menu",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_2.grid(row=2, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Torneos",
                                                command=self.button_event)
        self.button_1.grid(row=3, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Jugadores",
                                                command=self.button_event2)
        self.button_2.grid(row=4, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Equipos",
                                                command=self.button_event3)
        self.button_2.grid(row=5, column=0, pady=10, padx=20)

        

    def mostrarTorneos(self):
        self.agregar_torneo_imagen = self.load_image("/agregar.png", 20)
        # ============ frame_right ============
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # ============ header ============
        self.header = customtkinter.CTkFrame(master=self.frame_right)
        self.header.grid(row=0, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")
        self.header.rowconfigure(0, weight=1)
        self.header.columnconfigure(0, weight=1)

        self.hlabel_1 = customtkinter.CTkLabel(master=self.header,
                                                    text="Datos",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.hlabel_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.hlabel_2 = customtkinter.CTkLabel(master=self.header,
                                                    text="En curso",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.hlabel_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.hlabel_3 = customtkinter.CTkLabel(master=self.header,
                                                    text="Tipo",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.hlabel_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.hlabel_4 = customtkinter.CTkLabel(master=self.header,
                                                    text="Accion",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.hlabel_4.grid(row=0, column=4, pady=10, padx=20, sticky="ew")
        # ============ header ============

        # ============ row ============
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=1, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")



        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Torneo Rosario #1\nTorneo zona sur de Rosario\nEquipos: 5/8",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="No",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="center")  # font name and size in px
        self.label_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="7",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                text="Gestionar",
                                                command=self.button_event)
        self.label_4.grid(row=0, column=4, pady=10, padx=20)
        # self.label_4 = customtkinter.CTkLabel(master=self.frame_info,
        #                                             text="Ingresar",
        #                                             text_font=("Roboto Medium", -16),
        #                                             anchor="w",
        #                                             justify="left")  # font name and size in px
        # self.label_4.grid(row=0, column=4, pady=10, padx=20, sticky="w")
        # ============ row ============

        # ============ row ============
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=2, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")



        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="# Titulo de Torneo\n# Descripción\n# Equipos anotados",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="17/10/2022",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="center")  # font name and size in px
        self.label_2.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="11",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="w",
                                                    justify="left")  # font name and size in px
        self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                text="Gestionar",
                                                command=self.button_event)
        self.label_4.grid(row=0, column=4, pady=10, padx=20)
        # ============ row ============

        

        # ============ frame_right ============

        self.radio_var = tkinter.IntVar(value=0)

        # self.button_2 = customtkinter.CTkButton(master=self.frame_right, image=self.agregar_torneo_imagen, text="Agregar torneo",width=130, height=60,
        #                                         compound="right", fg_color="#42AB49", hover_color="#53AB5B"
        #                                         )
        # self.button_2.grid(row=0, column=2, columnspan=1, padx=20, pady=10, sticky="")
        self.button_agregar = customtkinter.CTkButton(master=self.frame_right, image=self.agregar_torneo_imagen, text="Agregar Torneo", width=130, height=100, border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B")
        self.button_agregar.grid(row=0, column=2, columnspan=1, padx=20, pady=10, sticky="")
       


    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def mostrarJugadores(self):
        self.agregar_jugador_imagen = self.load_image("/agregar.png", 20)
        # ============ frame_right ============
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # ============ header ============
        self.header = customtkinter.CTkFrame(master=self.frame_right)
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

        # ============ row ============
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=1, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")



        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.jugador_imagen = self.load_image("/jugador-default.png", 55)
        self.jugador_imagen1 = self.load_image("/jugador1.png", 55)
        # self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
        #                                             text="Torneo Rosario #1\nTorneo zona sur de Rosario\nEquipos: 5/8",
        #                                             text_font=("Roboto Medium", -16),
        #                                             anchor="w",
        #                                             justify="left")  # font name and size in px
        # self.label_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.image_label = tkinter.Label(master=self.frame_info, image=self.jugador_imagen)
        self.image_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="John Doe",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_1.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="17",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_2.grid(row=0, column=2, pady=10, padx=20, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="1.87 m",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                text="Gestionar",
                                                command=self.button_event)
        self.label_4.grid(row=0, column=4, pady=10, padx=20)
        # self.label_4 = customtkinter.CTkLabel(master=self.frame_info,
        #                                             text="Ingresar",
        #                                             text_font=("Roboto Medium", -16),
        #                                             anchor="w",
        #                                             justify="left")  # font name and size in px
        # self.label_4.grid(row=0, column=4, pady=10, padx=20, sticky="w")
        # ============ row ============

        # ============ row ============
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=2, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")



        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.image_label = tkinter.Label(master=self.frame_info, image=self.jugador_imagen1)
        self.image_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Nicolas Acosta",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_1.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="23",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_2.grid(row=0, column=2, pady=10, padx=20, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="1.82 m",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                text="Gestionar",
                                                command=self.button_event)
        self.label_4.grid(row=0, column=4, pady=10, padx=20)

        # ============ row ============
        # ============ row ============
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=3, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.button_agregar = customtkinter.CTkButton(master=self.frame_info, image=self.agregar_jugador_imagen, text="Agregar nuevo equipo", border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#42AB49", fg_color=("gray84", "gray25"),
                                                hover_color="#53AB5B")
        self.button_agregar.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")
        # ============ row ============


    def mostrarEquipos(self):
        # ============ frame_right ============
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # ============ header ============
        self.header = customtkinter.CTkFrame(master=self.frame_right)
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

        # ============ row ============
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=1, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")



        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.equipo_imagen1 = self.load_image("/equipo-default.png", 55)
        self.equipo_imagen2 = self.load_image("/equipo1.png", 55)
        # self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
        #                                             text="Torneo Rosario #1\nTorneo zona sur de Rosario\nEquipos: 5/8",
        #                                             text_font=("Roboto Medium", -16),
        #                                             anchor="w",
        #                                             justify="left")  # font name and size in px
        # self.label_1.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.image_label = tkinter.Label(master=self.frame_info, image=self.equipo_imagen1)
        self.image_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Club Desconocido",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_1.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="13 Jugadores",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_2.grid(row=0, column=2, pady=10, padx=20, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="John Doe",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                text="Gestionar",
                                                command=self.button_event)
        self.label_4.grid(row=0, column=4, pady=10, padx=20)
        # self.label_4 = customtkinter.CTkLabel(master=self.frame_info,
        #                                             text="Ingresar",
        #                                             text_font=("Roboto Medium", -16),
        #                                             anchor="w",
        #                                             justify="left")  # font name and size in px
        # self.label_4.grid(row=0, column=4, pady=10, padx=20, sticky="w")
        # ============ row ============

        # ============ row ============
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=2, column=0, columnspan=2, rowspan=1, pady=(20, 0), padx=20, sticky="nsew")



        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.image_label = tkinter.Label(master=self.frame_info, image=self.equipo_imagen2)
        self.image_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Club Neira",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_1.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.label_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="17 Jugadores",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_2.grid(row=0, column=2, pady=10, padx=20, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Juan Rodriguez",
                                                    text_font=("Roboto Medium", -16),
                                                    anchor="center",
                                                    justify="center")  # font name and size in px
        self.label_3.grid(row=0, column=3, pady=10, padx=20, sticky="w")
        self.label_4 = customtkinter.CTkButton(master=self.frame_info,
                                                text="Gestionar",
                                                command=self.button_event)
        self.label_4.grid(row=0, column=4, pady=10, padx=20)
        # ============ row ============

        



    def button_event(self):
        self.mostrarTorneos()
        print("Button pressed")
    def button_event2(self):
        self.mostrarJugadores()
        print("Button pressed")
    def button_event3(self):
        self.mostrarEquipos()
        print("Button pressed")

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()