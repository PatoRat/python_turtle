Set WshShell = CreateObject("WScript.Shell")
' El comando incluye la ruta del Python y la del script, ambas entre comillas
comando = """C:\Users\usuario\AppData\Local\Programs\Python\Python312\python.exe"" ""d:\Documents\My Stuff\python_turtle\pvp.py"""
' El 0 al final oculta la ventana por completo
WshShell.Run comando, 0, False
Set WshShell = Nothing