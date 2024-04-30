
import datetime

class View:
    
    def cls(self) -> None:
        print("\033c")

    def output(self, *text) -> None:
        res = ''
        for s in text:
            res += str(s)
        print(res)

    def clsout(self, *text) -> None:
        self.cls()
        self.output(*text)
        
    def out_wait(self, is_cls: bool, *obj, text: str) -> None:
        if is_cls:
            self.cls()
        self.output(*obj)
        if text != '\n' and text != '':
            text += ', '
        self.output(text, 'нажмите Enter для продолжения.')
        self.input()

    
    def input(self, text: str = '') -> str:
        try:
            return input(text)

        except KeyboardInterrupt:
            return None
        except EOFError:
            return None
        except ValueError:
            return None


    def input_data(self, str_date = '', str_time = '', default = datetime.datetime.today()) -> datetime.datetime:
        try:
            sdate = input(str_date)
            stime = input(str_time)
        
            if len(sdate) == 0:
                sdate = f'{default.day:02d}.{default.month:02d}.{default.year}'
            if len(stime) == 0:
                stime = f'{default.hour:02d}:{default.minute:02d}'
            return datetime.datetime.strptime(f'{sdate} {stime}', '%d.%m.%Y %H:%M')
        
        except KeyboardInterrupt:
            return None
        except EOFError:
            return None
        except ValueError:
            return None


