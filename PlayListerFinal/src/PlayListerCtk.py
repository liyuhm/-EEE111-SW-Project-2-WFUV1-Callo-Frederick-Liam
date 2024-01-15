from PlayListDb import PlayListDb
from PlayListDbSqlite import PlaylistDbSqlite
from PlayListGuiCtk import PlayListGuiCtk

def main():
    db = PlaylistDbSqlite()
    app = PlayListGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()
