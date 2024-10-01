import sys
import os
import pyqrcode
import png
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QColorDialog,
)
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt
import re


class GeneradorQR(QWidget):
    def __init__(self):
        super().__init__()
        self.modo_oscuro = False
        self.color_qr = QColor(0, 0, 0)
        self.color_fondo = QColor(255, 255, 255)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Generador de Códigos QR Avanzado")
        self.setGeometry(100, 100, 500, 600)
        self.aplicar_estilo()
        layout = QVBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ingrese la URL o texto")
        layout.addWidget(self.url_input)
        btn_layout = QHBoxLayout()
        self.generar_btn = QPushButton("Generar QR")
        self.generar_btn.clicked.connect(self.generar_qr)
        btn_layout.addWidget(self.generar_btn)
        self.guardar_btn = QPushButton("Guardar QR")
        self.guardar_btn.clicked.connect(self.guardar_qr)
        self.guardar_btn.setEnabled(False)
        btn_layout.addWidget(self.guardar_btn)
        layout.addLayout(btn_layout)

        color_layout = QHBoxLayout()
        self.color_qr_btn = QPushButton("Color QR")
        self.color_qr_btn.clicked.connect(self.cambiar_color_qr)
        color_layout.addWidget(self.color_qr_btn)
        self.color_fondo_btn = QPushButton("Color Fondo")
        self.color_fondo_btn.clicked.connect(self.cambiar_color_fondo)
        color_layout.addWidget(self.color_fondo_btn)
        layout.addLayout(color_layout)
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qr_label)
        self.modo_btn = QPushButton("Cambiar Modo")
        self.modo_btn.clicked.connect(self.cambiar_modo)
        layout.addWidget(self.modo_btn)
        self.setLayout(layout)

    def aplicar_estilo(self):
        if self.modo_oscuro:
            self.setStyleSheet(
                """        
                QWidget {
                    background-color: #2c2c2c;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                }
                QLineEdit, QPushButton {
                    padding: 10px;
                    font-size: 14px;
                    border: 1px solid #555;
                    border-radius: 5px;
                    background-color: #3c3c3c;
                }
                QPushButton {
                    background-color: #4CAF50;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """
            )
        else:
            self.setStyleSheet(
                """        
                QWidget {
                    background-color: #f0f0f0;
                    color: #000000;
                    font-family: Arial, sans-serif;
                }
                QLineEdit, QPushButton {
                    padding: 10px;
                    font-size: 14px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #ffffff;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """
            )

    def validar_url(self, url):
        patron = re.compile(
            r"^(?:http|ftp)s?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(patron, url) is not None

    def generar_qr(self):
        url = self.url_input.text().strip()
        if not url or not self.validar_url(url):
            QMessageBox.warning(self, "Error", "Por favor, ingrese una URL válida.")
            return
        qr = pyqrcode.create(url)
        temp_file = "temp_qr.png"
        qr.png(
            temp_file,
            scale=10,
            module_color=self.color_qr.name(),
            background=self.color_fondo.name(),
        )
        pixmap = QPixmap(temp_file)
        self.qr_label.setPixmap(
            pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.guardar_btn.setEnabled(True)
        self.setWindowTitle(f"Generador de Códigos QR Avanzado - {url}")
        os.remove(temp_file)
        QMessageBox.information(self, "Éxito", "Código QR generado con éxito.")

    def guardar_qr(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "No hay código QR para guardar.")
            return
        nombre_archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Código QR", "", "Imágenes PNG (*.png);;Imágenes SVG (*.svg)"
        )
        if nombre_archivo:
            try:
                qr = pyqrcode.create(url)
                if nombre_archivo.endswith(".png"):
                    qr.png(
                        nombre_archivo,
                        scale=10,
                        module_color=self.color_qr.name(),
                        background=self.color_fondo.name(),
                    )
                elif nombre_archivo.endswith(".svg"):
                    qr.svg(
                        nombre_archivo,
                        scale=10,
                        module_color=self.color_qr.name(),
                        background=self.color_fondo.name(),
                    )
                QMessageBox.information(
                    self, "Éxito", f"Código QR guardado como {nombre_archivo}"
                )
            except Exception as e:
                QMessageBox.warning(
                    self, "Error", f"Ocurrió un error al guardar el archivo: {e}"
                )

    def cambiar_color_qr(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_qr = color
            self.generar_qr()

    def cambiar_color_fondo(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_fondo = color
            self.generar_qr()

    def cambiar_modo(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_estilo()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GeneradorQR()
    ex.show()
    sys.exit(app.exec())
