ANSI_BLACK              = "\033[30m"
ANSI_RED                = "\033[31m"
ANSI_GREEN              = "\033[32m"
ANSI_YELLOW             = "\033[33m"
ANSI_BLUE               = "\033[34m"
ANSI_PURPLE             = "\033[35m"
ANSI_CYAN               = "\033[36m"
ANSI_WHITE              = "\033[37m"
ANSI_BLACK_BACKGROUND   = "\033[40m"
ANSI_RED_BACKGROUND     = "\033[41m"
ANSI_GREEN_BACKGROUND   = "\033[42m"
ANSI_YELLOW_BACKGROUND  = "\033[43m"
ANSI_BLUE_BACKGROUND    = "\033[44m"
ANSI_PURPLE_BACKGROUND  = "\033[45m"
ANSI_CYAN_BACKGROUND    = "\033[46m"
ANSI_WHITE_BACKGROUND   = "\033[47m"    


def cls():
    print("\033c")

def color(col: str):
    print(col)
        
