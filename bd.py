import pymysql

def obtener_conexion():
    return pymysql.connect(
                            host = 'localhost' ,
<<<<<<< HEAD
                            # port = 3306,
                            port = 3306,
=======
                            port = 3306,
                            # port = 3307,
>>>>>>> 22f207293be09f9f84b625805215c958ce86ccb7
                            user = 'root' ,
                            password = '' ,
                            db = 'bd_domus'
                            )