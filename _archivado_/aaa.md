N	PANTALLA	API	METODO	REQUEST	RESPONSE	HECHO
-	GENERAL	agregar_prod_lista_deseos	POST	"{
    "usuario_id" : "" ,
    "producto_id" : ""
}"	"{
    "code": 1 ,
	"data": {},
	"message": "Producto agregado exitosamente"
}"	o
		agregar_prod_carrito	POST	"{
    "usuario_id" : "" ,
    "producto_id" : ""
}"	"{
    "code": 1 ,
	"data": {},
	"message": "Producto agregado exitosamente"
}"	o
		quitar_prod_lista_deseos	POST	"{
    "usuario_id" : "" ,
    "producto_id" : ""
}"	"{
    "code": 1 ,
        "data": {},
        "message": "Producto quitado exitosamente"
}"	o
		quitar_prod_carrito	POST	"{
    "usuario_id" : "" ,
    "producto_id" : ""
}"	"{
    "code": 1 ,
	"data": {},
	"message": "Producto quitado exitosamente"
}"	o
1	Homepage	listar_novedades_recientes	GET	"{
    "usuario_id" : "" 
}"	"{
    "code": 1 ,
        "data": {
        "lista" : [
            {
                "id" : "",
                "ruta" : ""
            }
        ]
    },
        "message": "Listado de novedades recientes"
}"	O
		listar_productos_recientes	GET	"{
    "usuario_id" : "" 
}"	"{
    "code": 1 ,
        "data": {
        "lista" : [
            {
                "id" : "",
                "nombre" : "",
                "favorito" : "",
                "precio" : "" ,
                "ruta" : "" 
            }
        ]
    },
        "message": "Listado de productos recientes"
}"	O
		listar_productos_populares	GET	"{
    "usuario_id" : "" 
}"	"{
    "code": 1 ,
        "data": {
        "lista" : [
            {
                "id" : "",
                "nombre" : "",
                "favorito" : "",
                "precio" : "" ,
                "ruta" : "" 
            }
        ]
    },
        "message": "Listado de productos populares"
}"	O
		listar_marcas	GET	{}	"{
    "code": 1 ,
        "data": {
        "lista" : [
            {
                "id" : "",
                "nombre" : "",
                "ruta" : "" 
            }
        ]
    },
    "message": "Listado de marcas"
}"	O
7	Busqueda / catalogo	listar_productos_busqueda	GET	"{
	"busqueda" : "" ,
	"orden" : "" ,
	"categorias" : [] ,
	"subcategorias" : [] ,
	"precio_max" : "" ,
	"precio_min" : "" 
}"	""{
    ""code"": 1 ,
        ""data"": {
        ""lista"" : [
            {
                ""id"" : """",
                ""nombre"" : """",
                ""favorito"" : """",
                ""precio"" : """" ,
                ""ruta"" : """" 
            }
        ]
    },
        ""message"": ""Listado de busqueda de productos""
}""	O
8	Detalles del producto	consultar_producto	GET	"{
    "producto_id" : "" ,
    "usuario_id"
}"	"{
    "code": 1 ,
    "data": {
        "producto_id" : "",
        "nombre" : "",
        "categoria" : "",
        "subcategoria" : "",
        "precio" : "",
        "descripcion" : "" ,
        "favorito" : "" ,
        "rutas" : [
            ""
        ]
    },
    "message": "Producto encontrado"
}"	o
11	Login	consultar_usuario	GET	"{
    "correo" : "" 
}"	"{
  "code": 1,
  "data": {
    "usuario_id": "",
    "nombres": "",
    "apellidos": "",
    "correo": "",
    "nro_celular": "",
    "direccion": ""
  },
  "message": "Consulta de perfil de usuario"
}"	o
		procesar_login	POST	"{
    "correo" : "" ,
    "contrasenia" : ""
}"	"{
  "code": 1,
  "data": {
    "usuario_id": ""
  },
  "message": "Login exitoso"
}"	o
12	Sign up	procesar_sign_up	POST	"{
    "nombres" : "" ,
    "apellidos" : "" ,
    "dni" : "" ,
    "nro_celular" : "" ,
    "correo" : "" ,
    "contrasenia" : "" 
}"	"{
    "code": 1 ,
        "data": {
        "usuario_id" : ""
    },
        "message": "Usuario registrado correctamente"
}"	O
13	Carrito	consultar_carrito	GET	"{
    "usuario_id" : "" 
}"	"{
    "code": 1 ,
    "data": {
    },
    "message": "Informacion de carrito"
}"	o
		listar_productos_carrito	GET	"{
    "usuario_id" : "" 
}"	"{
    "code": 1 ,
    "data": {
         "lista" : [],
    },
    "message": "Lista de productos del carrito"
}"	o
		modificar_producto_carrito	POST	"{
    "usuario_id" : "" ,
    "producto_id":"",
    "cantidad":""
}"	"{
    "code": 1 ,
    "data": { "producto_id": "", "cantidad":""},
    "message": "Cantidad modificada correctamente"
}"	o
		eliminar_producto_carrito	POST	"{
    "usuario_id" : "" ,
    "producto_id":""
}"	"{
    "code": 1 ,
    "data": { "producto_id": ""},
    "message": "Producto eliminado correctamente"
}"	o
		agregar_producto_carrito	POST	"{
    "usuario_id" : "" ,
    "producto_id":"",
    "cantidad"
}"	"{
    "code": 1 ,
    "data": {},
    "message": "Producto agregado correctamente"
}"	o
15	Resumen del pedido	consultar_pedido	GET	"{
    "usuario_id" : "" ,
    "pedido_id" : ""
}"	"{
    "code": 1 ,
    "data": {
    },
    "message": "Informacion de pedido"
}"	o
16	Mi perfil	consultar_usuario	GET	"{
    "usuario_id" : "" 
}"	"{
  "code": 1,
  "data": {
    "usuario_id": "",
    ...
  },
  "message": "Usuario encontrado"
}"	o
		cambiar_contrasenia	POST	"{
  "usuario_id": "",
  "contrasenia_actual": "",
  "contrasenia_nueva": "",
  "conf_contrasenia_nueva": ""
}"	"{
  "code": 1,
  "data": {},
  "message": "Contraseña actualizada correctamente"
}"	o
		listar_deseos	GET	"{
    "usuario_id" : "" 
}"	"{
  "code": 1,
  "data": {
    "lista": []
  },
  "message": "Listado de productos en deseos"
}"	o
		editar_perfil	POST	"{
    "usuario_id" : "" ,
    "nombres" : "" ,
    "apellidos" : "" ,
    "dni" : "" ,
    "nro_celular" : "" ,
    "correo" : "" ,
}"	"{
  "code": 1,
  "data": {},
  "message": "Perfil modificado exitosamente"
}"	o
18	Mis pedidos	listar_pedidos	GET	"{
    "usuario_id" : "" 
}"	"{
  "code": 1,
  "data": {
    "lista": [
      {
        "pedido_id": "",
        "fecha": "",
        "estado": "",
        "total": 0,
        "productos": [
          {
            "producto_id": "",
            "nombre": "",
            "precio": 0,
            "cantidad": 0
          }
        ]
      }
    ]
  },
  "message": "Listado de pedidos del usuario"
}
"	o
19	Mis direcciones	listar_direcciones	GET	"{
    "usuario_id" : "" 
}"	"{
  "code": 1,
  "data": {
    "lista": []
  },
  "message": "Listado de direcciones del usuario"
}
"	o
		agregar_direccion	POST	"{
  "usuario_id": "",
  "alias": "Casa / Oficina / Otro",
  "direccion": "",
  "distrito": "",
  "ciudad": ""
}"	"{
  "code": 1,
  "data": {
    "direccion_id": "3"
  },
  "message": "Dirección agregada correctamente"
}
"	o