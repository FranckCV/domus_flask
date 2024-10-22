import pymysql

def obtener_conexion():
    return pymysql.connect(
                            host = 'localhost' ,
<<<<<<< HEAD
                            # port = 3306,
                            port = 3307,
=======
                            port = 3306,
                            # port = 3307,
>>>>>>> d0bf1fb2e0d16ecea198fb3ac70917b64d5813a6
                            user = 'root' ,
                            password = '' ,
                            db = 'bd_domus'
                            )