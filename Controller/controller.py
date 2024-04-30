from View.menu import *
from View.ansi import *
from View.view import *
from Model.menu import *
from Model.note import *
from Model.noteitem import *
from Model.DateRW import *


class Controller:
    menu: Menu
    note: Note
    file: FileCSV = None
    view: View = None

    def __init__(self) -> None:
        self.menu = Menu("Записная книжка. v 1.0", [
                        MenuItem(mCmd.CREATE_REC, "Новая запись"),
                        MenuItem(mCmd.VIEW_REC, "Просмотр записей",
                                Menu("Просмотр записей", [
                                    MenuItem(mCmd.VIEW_LAST, "Посмотреть последнюю"),
                                    MenuItem(mCmd.VIEW_FROM_INDEX, "Выбрать запись"),
                                    MenuItem(mCmd.VIEW_FROM_DATE, "Просмотр по дате"),
                                    MenuItem(mCmd.VIEW_ALL, "Просмотр всех записей")
                                ])),
                        MenuItem(mCmd.EDIT_REC, "Редактировать запись"),
                        MenuItem(mCmd.DELETE_REC, "Удаление записей",
                                Menu("Удаление записей", [
                                    MenuItem(mCmd.DELETE_LAST, "Удалить последнюю"),
                                    MenuItem(mCmd.DELETE_FROM_INDEX, "Выбрать запись"),
                                    MenuItem(mCmd.DELETE_FROM_DATE, "Удалить по дате")
                                ]))
                        ])
        
        self.view = View()
        self.file = FileCSV('note.csv')
        self.note = self.file.load()


    def run(self):
        while True:
            n = self.menu.run()
            if n == 0:
                break
            self.proceed_cmd(n)

    #
    # Обработчик главного меню
    #
    def proceed_cmd(self, cmd: int):
        if cmd == mCmd.CREATE_REC:
            self.create_record()                # добавить новую запись

        elif cmd == mCmd.VIEW_LAST:
            self.view_last()                    # посмотреть последнюю запись

        elif cmd == mCmd.VIEW_FROM_INDEX:
            self.view_one()                     # посмотреть выбранную запись

        elif cmd == mCmd.VIEW_FROM_DATE:
            self.view_date()                    # просмотр по временному промежутку

        elif cmd == mCmd.VIEW_ALL:              # просмотр всех записей
            self.view_all()

        elif cmd == mCmd.EDIT_REC:              # изменения записи
            self.edit_rec()

        elif cmd == mCmd.DELETE_LAST:           # удаление последней записи
            self.delete_last()

        elif cmd == mCmd.DELETE_FROM_INDEX:
            self.delete_one()                   # удаление выбранной записи

        elif cmd == mCmd.DELETE_FROM_DATE:
            self.delete_date()                  # удаление за временной промежуток

    ############################################
    #
    # Методы для работы с записями
    #
    ############################################
    
    def create_record(self):                        # добавление новой записи
        self.view.cls()
        rec = self.__new_rec(self.note.id)
        if rec is not None:
            self.note.add(rec)
            self.view.out_wait(True, rec, text='\nЗапись добавлена')

    def view_one(self):                             # просмотр одной записи
        idx = self.__short_select('просмотра')
        if idx > 0:
            self.view.out_wait(True, self.note.get(idx-1), text='\n')

    def view_all(self):                             # просмотр всех записей
        self.view.out_wait(True, self.note, text='\n')

    def view_last(self):                            # посмотреть последнюю запись
        self.view.cls()
        idx = self.note.size()
        if idx > 0:
            self.view.out_wait(False, self.note.get(idx-1), text='\n')

    def view_date(self):                            # посмотреть по временному промежутку
        indt, outdt = self.__date_select('просмотра')
        if indt is not None and outdt is not None:
            n = Note()
            for elem in self.note:
                dt = elem.getData()['date']
                if dt >= indt and dt <= outdt:
                    n.add(elem)
            self.view.out_wait(True, n, text='\n')

    def edit_rec(self):                             # изменение записи
        idx = self.__short_select('изменения')
        if idx > 0:
            rec = self.note.get(idx-1)
            self.view.clsout(rec, '\n')
            nrec = self.__new_rec(rec.id)
            if nrec is not None:
                self.note.add(nrec)
                self.view.out_wait(True, nrec, text = '\nЗапись изменена')

    def delete_last(self):                          # удаление последней записи
        self.view.cls()
        self.__delrec(self.note.size())
        
    def delete_one(self):                           # удаление выбранной записи
        self.view.cls()
        self.__delrec(self.__short_select('удаления'))

    def delete_date(self):                          # удаление за временной промежуток
        indt, outdt = self.__date_select('удаления')
        if indt is not None and outdt is not None:
            idx = 0
            while idx < self.note.size():
                dt = self.note.get(idx).getData()['date']
                if dt >= indt and dt <= outdt:
                    self.note.delete(idx)
                else:
                    idx += 1
            self.view.out_wait(True, self.note, text = '\nУдаление произведено')


    #
    # возвращает введенную с консолит новую запись или None (например юзер нажал Ctrl+C)
    #
    def __new_rec(self, id: int) -> NoteItem:         
        title = self.view.input('Введите заголовок: ')
        body = self.view.input('Введите заметку: ')
        if title is not None and body is not None:
            return NoteItem(id, title, body)
        return None

    #
    # удаляет запись по индексу
    #
    def __delrec(self, index):
        if index > 0:
            if self.note.delete(index-1):
                s = '\nЗапись удалена'
            else:
                s = '\nНе удалось удалить запись'
            self.view.out_wait(False, '', text = s)

    #
    # Выбор записи из краткого списка (заголовки)
    #
    def __short_select(self, text: str) -> int:
        m = Menu(f'Выберите запись для {text}', [])
        idx = 1
        for n in self.note:
            rec = n.getData()
            s = f"{rec['title']}"
            m.append(MenuItem(idx, s))
            idx += 1
        return m.run()

    #
    # Выбор временного промежутка
    #
    def __date_select(self, text: str):
        self.view.clsout(f'Введите диапазон даты для {text}\n')
        indt = self.view.input_data('Введите начальную дату (dd.mm.yyyy) Enter для 01.01.2000: ', 
                                    'Введите начальное время (hh:mm), Enter для 00:00: ', 
                                    datetime.datetime(2000,1,1, 0, 0, 0))
        outdt= self.view.input_data('Введите конечную дату (dd.mm.yyyy) Enter для текущей даты: ', 
                                    'Введите конечное время (hh:mm), Enter для текущего времени: ', 
                                    datetime.datetime.today())
        if indt is None or outdt is None:
            self.view.out_wait(False,'', text='\nВведено некорректное значение')
        return indt, outdt
    

