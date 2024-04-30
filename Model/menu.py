import enum

class mCmd(enum.Enum):
    CREATE_REC = 1
    VIEW_REC = 2
    VIEW_LAST = 20              # просмотр последней записи
    VIEW_FROM_INDEX = 21        # выбор записи из списка
    VIEW_FROM_DATE = 22         # просмотр записей за определенную дату
    VIEW_ALL = 23               # просмотр всех записей
    EDIT_REC = 3
    DELETE_REC = 4
    DELETE_LAST = 40            # удаление последней записи
    DELETE_FROM_INDEX = 41      # выбор конкретной записи из списка
    DELETE_FROM_DATE = 42       # удаление всех записей за определенную дату

    