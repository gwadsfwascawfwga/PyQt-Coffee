import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from UI.main import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_AddEditCoffeeForm

class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()

        # Добавляем кнопки "Добавить" и "Редактировать"
        self.addButton = QPushButton("Добавить")
        self.editButton = QPushButton("Редактировать")

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.editButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[0]))

        headers = ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(rows):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))

        conn.close()

    def add_coffee(self):
        self.form = AddEditCoffeeForm()
        self.form.show()
        self.form.saveButton.clicked.connect(lambda: self.save_coffee(None))
        self.form.cancelButton.clicked.connect(self.form.close)

    def edit_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            return

        self.form = AddEditCoffeeForm()
        self.form.show()
        self.form.saveButton.clicked.connect(lambda: self.save_coffee(selected_row))
        self.form.cancelButton.clicked.connect(self.form.close)

        # Заполняем форму данными из выбранной строки
        self.form.nameEdit.setText(self.tableWidget.item(selected_row, 1).text())
        self.form.roastEdit.setText(self.tableWidget.item(selected_row, 2).text())
        self.form.typeEdit.setText(self.tableWidget.item(selected_row, 3).text())
        self.form.tasteEdit.setText(self.tableWidget.item(selected_row, 4).text())
        self.form.priceEdit.setText(self.tableWidget.item(selected_row, 5).text())
        self.form.volumeEdit.setText(self.tableWidget.item(selected_row, 6).text())

    def save_coffee(self, row=None):
        name = self.form.nameEdit.text()
        roast = self.form.roastEdit.text()
        coffee_type = self.form.typeEdit.text()
        taste = self.form.tasteEdit.text()
        price = self.form.priceEdit.text()
        volume = self.form.volumeEdit.text()

        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()

        if row is None:
            cursor.execute("INSERT INTO coffee (name, roast, type, taste, price, volume) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, roast, coffee_type, taste, price, volume))
        else:
            cursor.execute("UPDATE coffee SET name=?, roast=?, type=?, taste=?, price=?, volume=? WHERE id=?",
                           (name, roast, coffee_type, taste, price, volume, self.tableWidget.item(row, 0).text()))

        conn.commit()
        conn.close()
        self.load_data()
        self.form.close()

class AddEditCoffeeForm(QWidget, Ui_AddEditCoffeeForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
