#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# <Aplicacion para generar la guia Tkinter.>

# Copyright (c) 2013 Alejandro Alvarez <contacto@codigopython.com.ar>
# This file is part of Guia Tkinter.
#
# Guia Tkinter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Guia Tkinter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Guia Tkinter.  If not, see <http://www.gnu.org/licenses/>.

# http://www.codigopython.com.ar <contacto@codigopython.com.ar>

""".. module:: build
    :synopsis: Interfaz para generar la guia de Tkinter.
.. moduleauthor:: Alvarez Alejandro <contacto@codigopython.com.ar>
"""

"""
Requisitos:
    reportlab
        https://pypi.python.org/pypi/reportlab/
    rst2epub2
        https://pypi.python.org/pypi/rst2epub2/
    rst2pdf
        https://pypi.python.org/pypi/rst2pdf/
    glob2
        https://pypi.python.org/pypi/glob2/

TODO: Generar epub
TODO: Generar pdf

Incluir footer

Comprimir archivos

Si la salida es HTML5 incluir reproductor de video de Dailymotion
para otros formatos el link a la pagina
"""

import os
import sys
import shutil
import Tkinter
from tkFileDialog import askdirectory
from tkMessageBox import showinfo

from tools import txt2tags

try:
    import glob2
except ImportError:
    #FIXME: Mejorar salida
    raise ImportError("No se ha encontrado la libreria glob2")

modules_not_available = []
not_convert_to = []


class print_exception(Exception):
    def __init__(self, e, exc_info, need_to_run):
        self.e = e
        self.exc_info = exc_info
        str_e = str(self.e)
        self.module = str_e.split(" ")[-1]
        if not need_to_run:
            #FIXME: Evitar contenido duplicado
            modules_not_available.append(self.module)
            self.message = "No se encuentra la libreria: " + self.module
        else:
            #TODO: Implementar
            pass
        #self.inner_exception = exc_info

    def __str__(self):
        return str(self.message)

try:
    import rst2epub2
except ImportError as e:
    not_convert_to.append("epub")
    print print_exception(e, sys.exc_info(), False)
try:
    import rst2pdf
except ImportError as e:
    not_convert_to.append("pdf")
    print print_exception(e, sys.exc_info(), False)

files_convert = ("Interfaz grafica con Tkinter.txt",
        "docs/FAQ.t2t",
        "docs/Manual.t2t")

convert_dirs = ["build/html",
    "build/html/img",
    "build/rst",
    "build/rst/img",
    "build/pdf",
    "build/epub"]

images_files = glob2.glob("**/*.[pj][np]g")

base_dir = os.getcwd() + "/"
build_dir = base_dir + "build/"


class  Convert(object):
    #TODO: Documentar
    """"""
    def __init__(self,
                 files_convert,
                 output=build_dir,
                 compressed=False,
                 html=True,
                 rst=False,
                 pdf=False,
                 epub=False):
        """"""
        self.base_dir = base_dir
        self.build_dir = output
        self.base_ext = ("html", "rst")
        self.files_convert = files_convert

        self.html = html
        self.rst = rst
        self.pdf = pdf
        self.epub = epub

        self.compressed = compressed

    def check_dir(self, list_dir, image=True, base_dir=False):
        """"""
        if type(list_dir) == str:
            list_dir = (list_dir,)
        for dir_check in list_dir:
            if image:
                dir_check = os.path.dirname(dir_check)

            if base_dir:
                dir_to_check = base_dir + dir_check
            else:
                dir_to_check = dir_check

            if not os.path.exists(dir_to_check):
                os.makedirs(dir_to_check)

        return True

    def copy_image(self, images_files, ext, build_dir=None):
        """"""
        if not build_dir:
            build_dir = self.build_dir
        for image in images_files:
            src = base_dir + image
            dest = str(build_dir) + ext + "/img/" + image
            self.check_dir(dest, base_dir=False)
            shutil.copy2(src, dest)
        return True

    def convert(self, input_file, name, build_dir, target):
        """"""
        print build_dir
        print target
        if target == 'html5':
            ext = 'html'
        else:
            ext = 'rst'
        if self.copy_image(images_files, ext, build_dir):
            txt2tags.exec_command_line(user_cmdline=[
                '--target',
                target,
                "--outfile=%s%s/%s.%s" % (build_dir, ext, name, ext),
                input_file,
                ])

    def convert_pdf(self):
        """
        --config=FILE
        --output=FILE
        #--stylesheets=STYLESHEETS
        #--stylesheet-path=FOLDERLIST
        #--compressed
        #--font-path=FOLDERLIST
        #--header=HEADER
        #--footer=FOOTER
        """
        pass
        #rst2pdf.py mydocument.txt -o mydocument.pdf
        #from rst2pdf import createpdf
        #createpdf.main()

    def convert_epub(self):
        """"""
        pass

    def run_convert(self, build_dir=None, **formats):
        """
        #TODO: Usar funcion que corresponda
        """
        if not build_dir:
            build_dir = self.build_dir
        print formats
        if formats:
            self.html = formats["html"]
            self.rst = formats["rst"]
            self.pdf = formats["pdf"]
            self.epub = formats["epub"]
        for input_file in self.files_convert:
            name = os.path.basename(input_file)
            name = name[:-4]
            if self.html:
                self.convert(input_file, name, build_dir, "html5")
            if self.rst:
                self.convert(input_file, name, build_dir, "rst")
            if self.pdf:
                pass
            if self.epub:
                pass
        if self.compressed:
            #TODO: Implementar
            pass
        #TODO: Borrar todos los directorios que tengan esas extensiones
        return True


class UI(Convert):
    """Objeto que se encarga de gestionar la interfaz grafica"""
    def __init__(self, root):
        """Inicializa la interfaz grafica

        :param root: Requiere se le pase la ventana sobre la cual trabajar
        :type root: object

        :ivar root: Instancia de Tk()
        :type root: object
        :ivar build_dir: Directorio de salida para la guia
        :type build_dir: str
        :ivar html: Indica si se convierte a HTML
        :type html: bool
        :ivar rst: Indica si se convierte a RST
        :type rst: bool
        :ivar pdf: Indica si se convierte a PDF
        :type pdf: bool
        :ivar epub: Indica si se convierte a ePub
        :type epub: bool
        :ivar compressed: Indica si se genera la guia en un archivo comprimido
        :type compressed: bool
        """
        Convert.__init__(self, files_convert, output=build_dir)
        self.root = root
        #FIXME: Buscar nombre para la aplicacion
        self.root.title("Generador Guia Tkinter")
        #TODO: Establecer icono
        self.build_dir = Tkinter.StringVar(value=self.build_dir)

        self.html = Tkinter.BooleanVar(value=True)
        self.rst = Tkinter.BooleanVar()
        self.pdf = Tkinter.BooleanVar()
        self.epub = Tkinter.BooleanVar()

        self.compressed = Tkinter.BooleanVar()

    def create_gui(self):
        """Genera todos los widgets que son mostrados en pantalla
        """
        Tkinter.Label(self.root,
                      text="Archivos a convertir:").pack()
        listado = Tkinter.StringVar(value=self.files_convert)
        listbox = Tkinter.Listbox(self.root,
                        state="disabled",
                        height=0,
                        width=0,
                        listvariable=listado)
        listbox.pack()

        Tkinter.Label(self.root,
                      text="Formatos a convertir:").pack()
        Tkinter.Checkbutton(self.root,
                            text="HTML",
                            state="active",
                            variable=self.html).pack()
        Tkinter.Checkbutton(self.root,
                            text="Rst",
                            variable=self.rst).pack()
        check_pdf = Tkinter.Checkbutton(self.root,
                            text="PDF",
                            variable=self.pdf)
        check_pdf.pack()
        if "pdf" in not_convert_to:
            check_pdf.configure(state="disabled")
        check_epub = Tkinter.Checkbutton(self.root,
                            text="ePub",
                            variable=self.epub)
        check_epub.pack()
        if "epub" in not_convert_to:
            check_epub.configure(state="disabled")

        Tkinter.Label(self.root,
                      text="Directorio de salida:").pack()
        Tkinter.Entry(self.root,
                      textvariable=self.build_dir).pack()

        def choose_directory():
            """Gestiona la ventana para la eleccion del directorio de salida"""
            choose = askdirectory()
            if choose != "":
                self.build_dir.set(choose)
        Tkinter.Button(self.root,
                       text="Buscar",
                       command=choose_directory).pack()

        Tkinter.Checkbutton(self.root,
                            text="Guardar en archivo comprimido",
                            variable=self.compressed).pack()

        Tkinter.Button(self.root,
                       text="Generar",
                       command=self.exec_convert).pack()
        Tkinter.Button(self.root,
                       text="Salir",
                       command=self.exit).pack()

    def events(self, event):
        pass

    def exec_convert(self):
        if self.run_convert(build_dir=self.build_dir.get(),
                         html=self.html.get(),
                         rst=self.rst.get(),
                         pdf=self.pdf.get(),
                         epub=self.epub.get()):
            showinfo(title="Conversion realizada",
                     message="La conversion ha sido realizada con exito")
            self.exit()

    def on_start(self):
        """Gestiona todas las acciones que se deben realizar antes de \
        generar los widgets"""
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.bind("<Control-q>", self.exit)
        self.root.bind("<Control-g>", self.run_convert)
        #TODO: Verificar librerias disponibles
        #TODO: Mostrar mensaje de librerias no encontradas

    def exit(self):
        """Cierra la aplicacion"""
        #TODO: Verificar si se encuentra convirtiendo
        #TODO: Si se encuentra trabajando esperar a finalizar para cerrar
        self.root.destroy()
        sys.exit()

    def run(self):
        """Metodo para iniciar la interfaz grafica"""
        self.on_start()
        self.create_gui()
        self.root.mainloop()

if __name__ == '__main__':
    root = Tkinter.Tk()
    application = UI(root)
    application.run()
