from datetime import datetime

class FileHandler:
    def __init__(self, filename):
        """Inicializa el manejador de archivos con el nombre de archivo dado."""
        self.filename = filename
        self.file = None

    def open_file(self):
        """Abre el archivo en modo anexar, creando el archivo si no existe."""
        self.file = open(self.filename, 'a')  # Cambia 'w' a 'a' para agregar contenido

    def write_to_file(self, content):
        """Escribe contenido en el archivo junto con la fecha y hora actual."""
        if self.file:
            # Obtiene la fecha y hora actual
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Escribe el contenido junto con el timestamp
            self.file.write(f"{timestamp} - {content}\n")  # Agrega una nueva línea después de cada entrada
        else:
            print("Error: El archivo no está abierto.")

    def close_file(self):
        """Cierra el archivo."""
        if self.file:
            self.file.close()
            self.file = None
        else:
            print("Error: El archivo no está abierto.")

# Ejemplo de uso
file_handler = FileHandler('mi_archivo.txt')
file_handler.open_file()
file_handler.write_to_file('it is amazing')
file_handler.close_file()
