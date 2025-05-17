import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox
)

from models import (
    get_all_mahasiswa, add_mahasiswa_db, delete_mahasiswa_db,
    update_mahasiswa_db, get_mahasiswa_by_id
)

class MahasiswaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manajemen Mahasiswa")
        self.setGeometry(100, 100, 400, 400)

        self.list_widget = QListWidget()
        self.nama_input = QLineEdit()
        self.npm_input = QLineEdit()
        self.id_label = QLabel("")

        self.add_button = QPushButton("Tambah")
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Hapus")
        self.load_button = QPushButton("Refresh")

        layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Nama"))
        form_layout.addWidget(self.nama_input)
        form_layout.addWidget(QLabel("NPM"))
        form_layout.addWidget(self.npm_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.load_button)

        layout.addWidget(self.list_widget)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_button.clicked.connect(self.load_data)
        self.add_button.clicked.connect(self.add_mahasiswa)
        self.update_button.clicked.connect(self.update_mahasiswa)
        self.delete_button.clicked.connect(self.delete_mahasiswa)
        self.list_widget.itemClicked.connect(self.load_selected)

        self.load_data()

    def load_data(self):
        self.list_widget.clear()
        self.mahasiswa_data = get_all_mahasiswa()
        for m in self.mahasiswa_data:
            self.list_widget.addItem(f"{m['id']}: {m['nama']} ({m['npm']})")

    def load_selected(self, item):
        id_selected = int(item.text().split(":")[0])
        data = get_mahasiswa_by_id(id_selected)
        if data:
            self.id_label.setText(str(data["id"]))
            self.nama_input.setText(data["nama"])
            self.npm_input.setText(data["npm"])

    def add_mahasiswa(self):
        nama = self.nama_input.text()
        npm = self.npm_input.text()
        if not nama or not npm:
            QMessageBox.warning(self, "Peringatan", "Nama dan NPM tidak boleh kosong.")
            return

        if add_mahasiswa_db(nama, npm):
            QMessageBox.information(self, "Sukses", "Mahasiswa ditambahkan.")
            self.load_data()
        else:
            QMessageBox.warning(self, "Gagal", "NPM sudah ada atau input tidak valid.")

    def update_mahasiswa(self):
        if not self.id_label.text():
            QMessageBox.warning(self, "Error", "Pilih mahasiswa terlebih dahulu.")
            return
        mahasiswa_id = int(self.id_label.text())
        nama = self.nama_input.text()
        npm = self.npm_input.text()

        if update_mahasiswa_db(mahasiswa_id, nama, npm):
            QMessageBox.information(self, "Sukses", "Data mahasiswa diperbarui.")
            self.load_data()
        else:
            QMessageBox.warning(self, "Gagal", "Gagal memperbarui data.")

    def delete_mahasiswa(self):
        if not self.id_label.text():
            QMessageBox.warning(self, "Error", "Pilih mahasiswa terlebih dahulu.")
            return
        mahasiswa_id = int(self.id_label.text())
        delete_mahasiswa_db(mahasiswa_id)
        QMessageBox.information(self, "Sukses", "Mahasiswa dihapus.")
        self.nama_input.clear()
        self.npm_input.clear()
        self.id_label.clear()
        self.load_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MahasiswaApp()
    window.show()
    sys.exit(app.exec_())
