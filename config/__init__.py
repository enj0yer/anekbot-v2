from os import path

if path.exists("hidden.py"):
    pass
else:
    with open('hidden.py', 'w', encoding='utf-8') as file:
        file.write('PATH = "%sqlite database path%"\nTOKEN = "%bot token%"')