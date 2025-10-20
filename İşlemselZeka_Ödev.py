import random
import math
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QDoubleSpinBox, QPushButton, QMessageBox, QGroupBox,
    QTextEdit
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
import math

class Parcacik:
    def __init__(self, pozisyon, hiz):
        self.pozisyon = pozisyon
        self.hiz = hiz
        self.en_iyi_pozisyon = pozisyon
        self.en_iyi_uygunluk_degeri = float('inf')

class PSO:
    def __init__(self, parcacik_sayisi, w, c1, c2, min_x, max_x, max_iterasyon, uygunluk_fonksiyonu):
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.min_x = min_x
        self.max_x = max_x
        self.max_iterasyon = max_iterasyon
        self.uygunluk_fonksiyonu = uygunluk_fonksiyonu

        self.kuresel_en_iyi_pozisyon = None
        self.kuresel_en_iyi_uygunluk_degeri = float('inf')
        self.suru = []

        self._initializasyon(parcacik_sayisi)

    def _initializasyon(self, parcacik_sayisi):
        for _ in range(parcacik_sayisi):
            rastgele_pozisyon = random.uniform(self.min_x, self.max_x)
            rastgele_hiz = random.uniform(-(self.max_x - self.min_x), (self.max_x - self.min_x))
            parcacik = Parcacik(rastgele_pozisyon, rastgele_hiz)
            uygunluk = self.uygunluk_fonksiyonu(parcacik.pozisyon)
            parcacik.en_iyi_uygunluk_degeri = uygunluk
            if uygunluk < self.kuresel_en_iyi_uygunluk_degeri:
                self.kuresel_en_iyi_uygunluk_degeri = uygunluk
                self.kuresel_en_iyi_pozisyon = parcacik.pozisyon
            self.suru.append(parcacik)

    def calistir(self):
        for _ in range(self.max_iterasyon):
            for parcacik in self.suru:
                r1, r2 = random.random(), random.random()
                parcacik.hiz = (self.w * parcacik.hiz) + \
                               (self.c1 * r1 * (parcacik.en_iyi_pozisyon - parcacik.pozisyon)) + \
                               (self.c2 * r2 * (self.kuresel_en_iyi_pozisyon - parcacik.pozisyon))
                parcacik.pozisyon += parcacik.hiz
                parcacik.pozisyon = max(self.min_x, min(self.max_x, parcacik.pozisyon))
                yeni_uygunluk = self.uygunluk_fonksiyonu(parcacik.pozisyon)
                if yeni_uygunluk < parcacik.en_iyi_uygunluk_degeri:
                    parcacik.en_iyi_uygunluk_degeri = yeni_uygunluk
                    parcacik.en_iyi_pozisyon = parcacik.pozisyon
                if parcacik.en_iyi_uygunluk_degeri < self.kuresel_en_iyi_uygunluk_degeri:
                    self.kuresel_en_iyi_uygunluk_degeri = parcacik.en_iyi_uygunluk_degeri
                    self.kuresel_en_iyi_pozisyon = parcacik.en_iyi_pozisyon
            if self.kuresel_en_iyi_uygunluk_degeri < 1e-6:
                break
        return self.kuresel_en_iyi_pozisyon, self.kuresel_en_iyi_uygunluk_degeri

def ornek_uygunluk_fonksiyonu(x):
    return abs(x * x + 2 * x - 3)

class PSOArayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parçacık Sürü Optimizasyonu")
        self.setMinimumSize(600, 520)
        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f0f8ff"))
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        param_group = QGroupBox("PSO Parametreleri")
        param_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #0b58a5;
                border-radius: 12px;
                margin-top: 10px;
                background-color: #e6f2fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        param_layout = QGridLayout()
        param_layout.setVerticalSpacing(10)
        self._create_param_controls(param_layout)
        param_group.setLayout(param_layout)
        main_layout.addWidget(param_group)

        self.btn_baslat = QPushButton("Optimizasyonu Başlat")
        self.btn_baslat.setStyleSheet("""
            QPushButton {
                background-color: #0b58a5;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
                border-radius: 10px;
                border: 2px solid #09477a;
            }
            QPushButton:hover {
                background-color: #09477a;
                border: 2px solid #0b58a5;
            }
            QPushButton:pressed {
                background-color: #083a62;
            }
        """)
        self.btn_baslat.clicked.connect(self.optimizasyonu_baslat)
        main_layout.addWidget(self.btn_baslat, alignment=Qt.AlignCenter)

        result_group = QGroupBox("Sonuçlar")
        result_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #0b58a5;
                border-radius: 12px;
                background-color: #e6f2fa;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        result_layout = QGridLayout()
        result_layout.setVerticalSpacing(8)

        lbl1 = QLabel("En İyi Pozisyon (gbest):")
        lbl1.setFont(QFont("Arial", 11))
        result_layout.addWidget(lbl1, 0, 0)
        self.lbl_gbest = QLabel("N/A")
        self.lbl_gbest.setFont(QFont("Arial", 11, QFont.Bold))
        result_layout.addWidget(self.lbl_gbest, 0, 1)

        lbl2 = QLabel("En İyi Uygunluk Değeri:")
        lbl2.setFont(QFont("Arial", 11))
        result_layout.addWidget(lbl2, 1, 0)
        self.lbl_uygunluk = QLabel("N/A")
        self.lbl_uygunluk.setFont(QFont("Arial", 11, QFont.Bold))
        result_layout.addWidget(self.lbl_uygunluk, 1, 1)

        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

        self.setLayout(main_layout)

    def _create_param_controls(self, layout):
        self.spin_parcacik_sayisi = self._add_label_and_spinbox(layout, "Parçacık Sayısı:", 0, is_int=True)
        self.spin_parcacik_sayisi.setRange(1, 1000)
        self.spin_parcacik_sayisi.setValue(30)

        self.spin_max_iterasyon = self._add_label_and_spinbox(layout, "Maks. İterasyon:", 1, is_int=True)
        self.spin_max_iterasyon.setRange(1, 10000)
        self.spin_max_iterasyon.setValue(100)

        self.spin_w = self._add_label_and_spinbox(layout, "İnertya (w):", 2)
        self.spin_w.setValue(0.729)

        self.spin_c1 = self._add_label_and_spinbox(layout, "Bilişsel (c1):", 3)
        self.spin_c1.setValue(1.49445)

        self.spin_c2 = self._add_label_and_spinbox(layout, "Sosyal (c2):", 4)
        self.spin_c2.setValue(1.49445)

        self.spin_min_x = self._add_label_and_spinbox(layout, "X Min Sınırı:", 5)
        self.spin_min_x.setRange(-1000.0, 1000.0)
        self.spin_min_x.setValue(-10.0)

        self.spin_max_x = self._add_label_and_spinbox(layout, "X Max Sınırı:", 6)
        self.spin_max_x.setRange(-1000.0, 1000.0)
        self.spin_max_x.setValue(10.0)

        self.func_edit = QTextEdit()
        self.func_edit.setPlaceholderText("Örn: x**2 + 2*x - 3")
        layout.addWidget(QLabel("Uygunluk Fonksiyonu:"), 7, 0)
        layout.addWidget(self.func_edit, 7, 1)

    def _add_label_and_spinbox(self, layout, text, row, is_int=False):
        label = QLabel(text)
        label.setFont(QFont("Arial", 10))
        layout.addWidget(label, row, 0)
        spinbox = QDoubleSpinBox()
        spinbox.setRange(-float('inf'), float('inf'))
        spinbox.setDecimals(0 if is_int else 5)
        layout.addWidget(spinbox, row, 1)
        return spinbox

    def optimizasyonu_baslat(self):
        try:
            parcacik_sayisi = int(self.spin_parcacik_sayisi.value())
            max_iterasyon = int(self.spin_max_iterasyon.value())
            w = self.spin_w.value()
            c1 = self.spin_c1.value()
            c2 = self.spin_c2.value()
            min_x = self.spin_min_x.value()
            max_x = self.spin_max_x.value()

            if min_x >= max_x:
                QMessageBox.warning(self, "Hata", "Min X sınırı, Max X sınırından küçük olmalıdır.")
                return

            func_text = self.func_edit.toPlainText().strip()
            if func_text:
                try:
                    kullanici_fonksiyonu = lambda x: eval(func_text, {"__builtins__": None, "x": x, "math": math})
                    kullanici_fonksiyonu(1)
                except Exception as e:
                    QMessageBox.warning(self, "Hata", f"Fonksiyon hatalı: {e}")
                    return
            else:
                kullanici_fonksiyonu = ornek_uygunluk_fonksiyonu

            optimizer = PSO(parcacik_sayisi, w, c1, c2, min_x, max_x, max_iterasyon, kullanici_fonksiyonu)
            gbest_pozisyon, gbest_uygunluk = optimizer.calistir()

            self.lbl_gbest.setText(f"{gbest_pozisyon:.6f}")
            self.lbl_uygunluk.setText(f"{gbest_uygunluk:.6f}")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Optimizasyon sırasında bir hata oluştu: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PSOArayuz()
    ex.show()
    sys.exit(app.exec_())
