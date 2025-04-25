from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout


import json

'''
note = {
    "Ласкаво просимо!" : {
        "текст" : "Це найкращий додаток для заміток у світі!",
        "теги" : ["добро", "інструкція"]
    }
}


with open("notes_data.json", "w", encoding="utf-8") as file:
   json.dump(note, file, ensure_ascii=False)

'''



app = QApplication([])


'''Інтерфейс програми'''
# параметри вікна програми
notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)


# віджети вікна програми
list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')


button_note_create = QPushButton('Створити замітку') # з'являється вікно з полем "Введіть ім'я замітки"
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')


field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')


# розташування віджетів по лейаутах
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)


col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)


col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)


col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

###############
def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки")
    if ok and note_name:
        list_notes.addItem(note_name)
        notes[note_name] = {"текст": "","теги": []}
        list_tags.clear()
        list_tags.addItems(notes[note_name]["теги"])

        print("after add note", notes)

def save_note():
    if list_notes.selectedItems():
        text = field_text.toPlainText()
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = text
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print("замітка не обрана")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        print("deleted note:", key)
        del notes[key]
            #
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
            #
        with open("notes_data.json", "w", encoding="utf-8") as file: #В ОКРЕМИЙ МЕТОД 
            json.dump(notes, file, ensure_ascii=False)

        list_notes.addItems(notes)
        print("notes after deleting", notes)
    else:
        print("не обрана замітка")

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text().strip()
        if tag and tag not in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=False)
        else:
            print("вже існує")
    else:
        print("Не обрана замітка")
 
def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=False)
    else:
        print("Не обрана замітка або тег")



# запуск програми
notes_win.show()


with open("notes_data.json", "r", encoding="utf-8") as file:
    notes = json.load(file)
    print(f"notes onload {notes}")


list_notes.addItems(notes)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
app.exec_()