from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox, filedialog
from pyzbar.pyzbar import decode, ZBarSymbol
import cv2
import pyautogui
import numpy as np
import threading
from PIL import Image, ImageTk, ImageDraw
import os
import pandas as pd
import serial
import time

class App:
    def __init__(self,font_video=0):
        self.active_camera = False
        #Parametros de configuracion de puerto serial
        self.port_opened=False
        self.com_port = ''
        self.arduino = serial
        self.message = ""
        self.saved_positions = []
        #Inicializacion de vectores
        self.info = []
        self.codelist = []
        self.codigo = []
        self.appName = 'Farmacia automatizada - Grupo 4'
        self.ventana = Tk()
        self.ventana.title(self.appName)
        #Definimos las posiciones guardadas
        self.pos1 = [[127, 53, 101, 103, 45], [127, 53, 101, 103, 0], [116, 53, 101, 103, 0], [109, 45, 101, 103, 0], [82, 45, 101, 103, 0], [82, 69, 101, 103, 0], [82, 69, 101, 106, 0], [61, 69, 101, 98, 19], [61, 82, 101, 98, 19], [61, 82, 101, 71, 19], [61, 82, 101, 71, 85], [109, 82, 101, 71, 85]]
        
        #Creamos el rack y los movimientos de los servos


        
        self.rack = np.ones((4,4))
        self.servo1 = 0 
        self.servo2 = 0
        self.servo3 = 0
        self.servo4 = 0
        self.servo5 = 0
        self.bandera = 0
        self.columna = 0
        self.entrada = 0
        self.ventana['bg']='white'
        self.font_video=font_video
        self.label=Label(self.ventana,text=self.appName,font=15,bg='blue',
                         fg='white').pack(side=TOP,fill=BOTH)
        self.btnSave = Button(self.ventana,text="GUARDAR INFO",bg='light blue',command=self.guardar)
        self.btnSave.pack(side=BOTTOM)
        self.cantMed1 = 0
        self.cantMed2 = 0
        self.cantMed3 = 0
        self.cantMed4 = 0
        self.display=scrolledtext.ScrolledText(self.ventana,width=100,background='snow3'
                                        ,height=4,padx=10, pady=10,font=('Arial', 10))
        self.display.pack(side=BOTTOM)
 
        self.canvas=Canvas(self.ventana,bg='white',width=640,height=600)
        self.canvas.pack()
        self.canvas2=Canvas(self.ventana,bg='black',width=640,height=0)
        self.canvas2.pack()
        self.btnCamera = Button(self.ventana,text="INICIAR LECTURA POR CAMARA",width=30,bg='goldenrod2',
                                activebackground='red',command=self.active_cam)
        self.btnCamera.pack(side=LEFT)
        self.btnLoad = Button(self.ventana,text="REVISAR STOCK",width=29,bg='goldenrod2',
                    activebackground='red',command = self.revisar_stock)
        self.btnLoad.pack(side=LEFT)
        self.btnAtras = Button(self.ventana,text="RETROCEDER",width=29,bg='goldenrod2',
                    activebackground='red',command = self.limpiar)
        self.archi1=PhotoImage(file="brazo.png")
        self.canvas.create_image(0, 0, image=self.archi1, anchor="nw")
        self.btnAtras.pack(side=LEFT)
        self.ventana.mainloop()

    ## Definimos la comunicacion por puerto serial
    def play_positions(self):
     for position in self.saved_positions:
            print("playing: "+str(position))
            self.send_positions(position);
            time.sleep(1)
    def send_positions(self,position):
        self.message = "{0:0=3d}".format(position[0])+"{0:0=3d}".format(position[1])+"{0:0=3d}".format(position[2])+"{0:0=3d}".format(position[3])+"{0:0=3d}".format(position[4])+"\n"
        self.arduino.write(str.encode(self.message))
        print(str.encode(self.message))
        print(self.message, end='')
        time.sleep(0.2)
    def set_port(self):
        global port_opened,arduino
        self.com_port = 'COM3' 
        self.arduino=serial.Serial(self.com_port,9600)
        self.port_opened=True
        print ("COM port set to: {}".format(self.com_port))
    def limpiar(self):
        self.canvas2.delete('all')
        self.canvas.delete('all')
        self.canvas2.configure(width=640,height=0,bg='white')
        self.canvas.configure(width=640,height=600,bg='white')
        self.archi1=PhotoImage(file="brazo.png")
        self.canvas.create_image(0, 0, image=self.archi1, anchor="nw")
    def revisar_stock(self):
        self.width=500
        self.height=500
        self.canvas.delete('all')
        k=120
        h = 30
        self.canvas.configure(width=self.width,height=self.height,bg='white')
        self.canvas.create_text(70,30,fill="blue",font="Arial 15 bold",text="Med 1")
        self.canvas.create_text(70+k,30,fill="blue",font="Arial 15 bold",text="Med 2")
        self.canvas.create_text(70+2*k,30,fill="blue",font="Arial 15 bold",text="Med 3")
        self.canvas.create_text(70+3*k,30,fill="blue",font="Arial 15 bold",text="Med 4")
        
        self.bandera=0
        self.aux = 0 #Variable para inicializar solo una vez el puerto serial
        if len(self.codigo)>0:
            self.entrada = self.codigo[-1]
            self.saved_positions = []
            if self.aux==0:
                self.set_port()
                self.aux=1
            if self.entrada == 'Domper : 1':
                column = 0    
                if(self.port_opened):
                    self.saved_positions = self.pos1
                    self.play_positions()
            elif self.entrada == 'Alergina : 1':
                column = 1
                if(self.port_opened):
                    self.saved_positions = self.pos1
                    self.play_positions()
            elif self.entrada == 'Kitadol 200mg : 1':
                column = 2
                if(self.port_opened):
                    self.saved_positions = self.pos1
                    self.play_positions()
            elif self.entrada == 'Medicamento 4':
                column = 3
                if(self.port_opened):
                    self.saved_positions = self.pos1
                    self.play_positions()
            
            else:
                column = 5
            self.arduino.close()
            try:
                for i in range(len(self.rack)):
                    if self.rack[i,column] == 1 and self.bandera == 0:
                        print('Medicamento encontrado en posicion {},{}'.format(i,column))
                        print('Enviando {} al usuario...'.format(self.codigo[-1]))
                        self.bandera = 1
                        self.rack[i,column]=0
                if self.rack[0][column]==0 and self.rack[1][column]==0 and self.rack[2][column]==0 and self.rack[3][column]==0:
                    print('Medicamento no disponible - Solicite reabastecimiento')
            except:
                print('Medicamento no encontrado en el rack')    
    
        self.dibujarRack()
        self.canvas2.configure(width=self.width,height=100,bg='white')
        self.cantMed1 = 0
        self.cantMed2 = 0
        self.cantMed3 = 0
        self.cantMed4 = 0
        for i in range(4):
            self.cantMed1 = int(self.rack[i][0] + self.cantMed1)
            self.cantMed2 = int(self.rack[i][1] + self.cantMed2)
            self.cantMed3 = int(self.rack[i][2] + self.cantMed3)
            self.cantMed4 = int(self.rack[i][3] + self.cantMed4)
        self.canvas2.delete('all')
        if self.cantMed1>0:
            self.canvas2.create_text(100,25,fill="black",font="Arial 12 bold",text="Med 1 - Cant:  {}".format(self.cantMed1))
        else:
            self.canvas2.create_text(100,25,fill="red",font="Arial 12 bold",text="Med 1 - Cant:  {}".format(self.cantMed1))
        if self.cantMed2>0:
            self.canvas2.create_text(400,25,fill="black",font="Arial 12 bold",text="Med 2 - Cant:  {}".format(self.cantMed2))
        else:
            self.canvas2.create_text(400,25,fill="red",font="Arial 12 bold",text="Med 2 - Cant:  {}".format(self.cantMed2))
        if self.cantMed3>0:
            self.canvas2.create_text(100,75,fill="black",font="Arial 12 bold",text="Med 3 - Cant:  {}".format(self.cantMed3))
        else:
            self.canvas2.create_text(100,75,fill="red",font="Arial 12 bold",text="Med 3 - Cant:  {}".format(self.cantMed3))
        if self.cantMed4>0:
            self.canvas2.create_text(400,75,fill="black",font="Arial 12 bold",text="Med 4 - Cant:  {}".format(self.cantMed4))  
        else:
            self.canvas2.create_text(400,75,fill="red",font="Arial 12 bold",text="Med 4 - Cant:  {}".format(self.cantMed4))     
        self.entrada = []
        self.codigo = []
        self.display.delete('1.0', END)
          
          
        

#Metodo utilizado para dibujar los cuadrados en pantalla
    def dibujarRack(self):
        k=120
        h = 30
        for i in range(4):
            if self.rack[0][i]==1:
                self.canvas.create_rectangle(30+i*k, 30+h, 100+i*k, 100+h,outline="green",fill="green")
            else:
                self.canvas.create_rectangle(30+i*k, 30+h, 100+i*k, 100+h,outline="red",fill="red")
        for i in range(4):
            if self.rack[1][i]==1:
                self.canvas.create_rectangle(30+i*k, 30+k+h, 100+i*k, 100+k+h,outline="green",fill="green")
            else:
                self.canvas.create_rectangle(30+i*k, 30+k+h, 100+i*k, 100+k+h,outline="red",fill="red")          
                
        for i in range(4):
            if self.rack[2][i]==1:
                self.canvas.create_rectangle(30+i*k, 30+2*k+h, 100+i*k, 100+2*k+h,outline="green",fill="green")
            else:
                self.canvas.create_rectangle(30+i*k, 30+2*k+h, 100+i*k, 100+2*k+h,outline="red",fill="red")      
              
        for i in range(4):
            if self.rack[3][i]==1:
                self.canvas.create_rectangle(30+i*k, 30+3*k+h, 100+i*k, 100+3*k+h,outline="green",fill="green")
            else:
                self.canvas.create_rectangle(30+i*k, 30+3*k+h, 100+i*k, 100+3*k+h,outline="red",fill="red") 

    def guardar(self):
        if len(self.display.get('1.0',END))>1:
            documento = filedialog.asksaveasfilename(initialdir="/",
                        title="Guardar en",defaultextension='.txt')
            if documento != "":
                archivo_guardar = open(documento,"w",encoding="utf-8")
                linea=""
                for c in str(self.display.get('1.0',END)):
                    linea=linea+c
                archivo_guardar.write(linea)
                archivo_guardar.close()
                messagebox.showinfo("GUARDADO","INFORMACI??N GUARDADA EN \'{}\'".format(documento))

 
    def visor(self):
        ret,frame  =self.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor=NW)
            self.ventana.after(15,self.visor)
 
    def active_cam(self):
        self.canvas2.delete('all')
        self.canvas.delete('all')
        self.canvas2.configure(width=640,height=0,bg='white')
        if self.active_camera == False:
            self.active_camera = True
            self.VideoCaptura()
            self.visor()
        else:
            self.active_camera = False
            self.codelist = []
            self.btnCamera.configure(text="INICIAR LECTURA POR CAMARA")
            self.vid.release()
            self.canvas.delete('all')
            self.canvas.configure(height=0)
            self.limpiar()
    def capta(self,frm):
        self.info = decode(frm)
        cv2.putText(frm, "Muestre la receta QR delante de la camara", (84, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if self.info != []:
            self.display.delete('1.0',END)
            for code in self.info:
                if code not in self.codelist:
                    self.codigo.append(code[0].decode('utf-8'))
                    self.codelist.append(code)
                    self.display.insert(END,(code[0].decode('utf-8'))+'\n')
                self.draw_rectangle(frm)
 
    def get_frame(self):
        if self.vid.isOpened():
            verif,frame=self.vid.read()
            if verif:
                self.btnCamera.configure(text="CERRAR CAMARA")
                self.capta(frame)
                return(verif,cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                messagebox.showwarning("CAMARA NO DISPONIBLE","""La c??mara est?? siendo utilizada por otra aplicaci??n.
                Cierrela e intentelo de nuevo.""")
                self.active_cam()
                return(verif,None)
        else:
            verif=False
            return(verif,None)
 
    def draw_rectangle(self,frm):
        codes = decode(frm)
        for code in codes:
            data = code.data.decode('ascii')
            x, y, w, h = code.rect.left, code.rect.top, \
                        code.rect.width, code.rect.height
            print('El largo es: {}'.format(w))
            print('El ancho es: {}'.format(h))
            cv2.rectangle(frm, (x,y),(x+w, y+h),(255, 0, 0), 6)
            cv2.putText(frm, code.type, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 50, 255), 2)
 
    def VideoCaptura(self):
        self.vid = cv2.VideoCapture(self.font_video)
        if self.vid.isOpened():
            self.width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.canvas.configure(width=self.width,height=self.height)
        else:
            messagebox.showwarning("CAMARA NO DISPONIBLE","El dispositivo est?? desactivado o no disponible")
            self.display.delete('1.0',END)
            self.active_camera = False
 
    def __del__(self):
        if self.active_camera == True:
            self.vid.release()
 
if __name__=="__main__":
    App()