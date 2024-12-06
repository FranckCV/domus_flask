import pymysql

def obtener_conexion():
    return pymysql.connect(
                            host = 'localhost' ,
                            # port = 3306,
                            port = 3307,
                            user = 'root' ,
                            password = '' ,
                            db = 'bd_domus'
                            )




# def obtener_conexion():
#     return pymysql.connect(
#                             host = 'DomusMarket.mysql.pythonanywhere-services.com',
#                             user = 'DomusMarket',
#                             password = 'SOMOSDOMUS2024',
#                             db = 'DomusMarket$bd_domus'
#                             )

