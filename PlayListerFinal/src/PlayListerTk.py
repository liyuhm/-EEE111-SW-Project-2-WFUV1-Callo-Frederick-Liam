from PlayListDb import PlayListDb
from PlayListGuiTk import PlayListGuiTk

def main():
    db = PlayListDb(init=False, dbName='PlayListDb.csv')
    app = PlayListDbGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()