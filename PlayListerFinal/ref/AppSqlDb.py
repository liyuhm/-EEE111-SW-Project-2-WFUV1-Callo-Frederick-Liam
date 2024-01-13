from EmpDbSqlite import EmpDbSqlite
from EmpGui import EmpGui

def main():
    db = EmpDbSqlite('EmpDbSql.db')
    app = EmpGui(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()