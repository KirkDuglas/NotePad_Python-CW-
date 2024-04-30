from __future__ import annotations
from View.ansi import *


class MenuItem:
    def __init__(self, id: int, text: str, submenu = None):
        self._id = id
        self._text = text
        self._submenu = submenu    

    @property
    def id(self):
        return self._id

    @property
    def submenu(self):
        return self._submenu
    

    def __repr__(self) -> str:
        s = self._text.ljust(30)
        if (self._submenu is not None):
            s += '-->'
        else:
            s += '   '
            
        return s

    
class Menu:
    head: list[MenuItem]
    active = None
    prev = None
    text: str

    def __init__(self, text: str, lst: list[MenuItem] = []):
        self.text = text
        self.head = lst
        self.active = self
        self.prev = None
        
    def append(self, item: MenuItem):
        self.active.head.append(item)
        
    def show(self):
        idx = 1
        cls()
        if self.active.text is not None:
            print(ANSI_BLUE_BACKGROUND, self.active.text, ANSI_BLACK_BACKGROUND, "\n")
        for n in self.active.head:
            print(f'{idx}. {n}')
            idx += 1
        if self.active.prev is None:
            print("0. Выход")
        else:
            print("0. Назад")
            
    def select(self, index: int) -> int:
        if index < len(self.active.head):
            sm = self.active.head[index]
            if sm.submenu is not None:
                sm.submenu.prev = self.active
                self.active = sm.submenu
            else:
                return sm.id
        return None

    def back(self):
        if self.active.prev is not None:
            self.active = self.active.prev
     

    def run(self) -> int:
        while True:
            self.show()
            try:
                print(">", end = "")
                key = int(input())
                if key == 0:
                    if self.active.prev is None:
                        return 0
                    self.back()
                else:
                    key -= 1
                    if self.select(key) is not None:
                        return self.active.head[key].id
            except KeyboardInterrupt:
                continue
            except EOFError:
                continue
            except ValueError:
                continue
            

