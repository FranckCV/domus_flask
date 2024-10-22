import pymysql

def obtener_conexion():
    return pymysql.connect(
                            host = 'localhost' ,
                            # port = 3306,
<<<<<<< HEAD
                            port = 3307,
=======
                            port = 3306,
>>>>>>> 5e03a827cda9e0f6b42eef89331ee51912c6c545
                            user = 'root' ,
                            password = '' ,
                            db = 'bd_domus'
                            )