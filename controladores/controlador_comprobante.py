import bd
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import os
from datetime import datetime
from decimal import Decimal
from pymysql.cursors import DictCursor

# CONSTANTE PARA RUTA BASE DE COMPROBANTES (relativa al proyecto)
RUTA_BASE_COMPROBANTES = "comprobantes"


def truncar_texto(texto, max_length=50):
    """Trunca el texto si supera el máximo de caracteres"""
    if len(texto) > max_length:
        return texto[:max_length-3] + "..."
    return texto


def obtener_siguiente_numero_comprobante(tipo_comprobante):
    """Obtiene y actualiza el siguiente número de comprobante"""
    conexion = bd.obtener_conexion()
    
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql_get = """
                SELECT serie, ultimo_numero 
                FROM secuencia_comprobante 
                WHERE tipo = %s 
                LIMIT 1
            """
            cursor.execute(sql_get, (tipo_comprobante,))
            result = cursor.fetchone()
            
            if not result:
                raise Exception(f"No se encontró serie para {tipo_comprobante}")
            
            serie = result['serie']
            nuevo_numero = result['ultimo_numero'] + 1
            
            sql_update = """
                UPDATE secuencia_comprobante 
                SET ultimo_numero = %s 
                WHERE tipo = %s AND serie = %s
            """
            cursor.execute(sql_update, (nuevo_numero, tipo_comprobante, serie))
            conexion.commit()
            
            return f"{serie}-{str(nuevo_numero).zfill(8)}"
    
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()


def insertar_comprobante(pedidoid, tipo_comprobante, doc_identidad_cliente, 
                         nombre_cliente, subtotal, igv, total, nombre_archivo,
                         numero_comprobante, razon_social=None, ruc=None, direccion_cliente=None):
    """Inserta un nuevo comprobante en la base de datos - Solo guarda el nombre del archivo"""
    
    conexion = bd.obtener_conexion()
    
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
                INSERT INTO comprobante 
                (pedidoid, tipo_comprobante, numero_comprobante, doc_identidad_cliente, 
                 nombre_cliente, razon_social, ruc, direccion_cliente, 
                 subtotal, igv, total, ruta_archivo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(sql, (
                pedidoid, tipo_comprobante, numero_comprobante, doc_identidad_cliente,
                nombre_cliente, razon_social, ruc, direccion_cliente,
                subtotal, igv, total, nombre_archivo
            ))
            conexion.commit()
            
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()
    
    return numero_comprobante


def obtener_comprobante_por_pedido(pedidoid):
    """Obtiene el comprobante asociado a un pedido"""
    conexion = bd.obtener_conexion()
    
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
                SELECT * FROM comprobante WHERE pedidoid = %s
            """
            cursor.execute(sql, (pedidoid,))
            return cursor.fetchone()
    
    finally:
        conexion.close()


def obtener_ruta_completa_comprobante(pedidoid, nombre_archivo):
    """Construye la ruta ABSOLUTA del comprobante usando el directorio base del proyecto"""
    # Obtener directorio base del proyecto (donde está este archivo)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, RUTA_BASE_COMPROBANTES, str(pedidoid), nombre_archivo)


def generar_pdf_comprobante(pedidoid, tipo_comprobante, datos_cliente, datos_productos, datos_empresa):
    """
    Genera un PDF de comprobante (boleta o factura) con diseño mejorado
    
    Args:
        pedidoid: ID del pedido
        tipo_comprobante: 'boleta' o 'factura'
        datos_cliente: dict con datos del cliente
        datos_productos: lista de productos
        datos_empresa: dict con datos de la empresa
    
    Returns:
        nombre del archivo generado (sin la ruta completa)
    """
    
    # Obtener directorio base del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Obtener número de comprobante
    numero_comprobante = obtener_siguiente_numero_comprobante(tipo_comprobante)
    
    # Crear estructura de carpetas (ruta absoluta)
    base_path = os.path.join(base_dir, RUTA_BASE_COMPROBANTES, str(pedidoid))
    os.makedirs(base_path, exist_ok=True)
    
    # Nombre del archivo
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tipo_comprobante}_{pedidoid}_{fecha_str}.pdf"
    filepath = os.path.join(base_path, filename)
    
    # Crear documento PDF
    doc = SimpleDocTemplate(filepath, pagesize=A4, 
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=1.5*cm, bottomMargin=1.5*cm)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # ==================== ESTILOS OPTIMIZADOS ====================
    
    style_empresa = ParagraphStyle(
        'Empresa',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=3,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=28
    )
    
    style_contacto_small = ParagraphStyle(
        'ContactoSmall',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#7F8C8D'),
        alignment=TA_LEFT,
        spaceAfter=2,
        leading=10
    )
    
    style_tipo_comprobante = ParagraphStyle(
        'TipoComprobante',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    style_numero = ParagraphStyle(
        'Numero',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        alignment=TA_CENTER,
        spaceAfter=15,
        fontName='Helvetica-Bold'
    )
    
    style_section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    # ==================== ENCABEZADO CON LOGO (RUTA ABSOLUTA) ====================
    
    # Ruta absoluta del logo
    logo_path = os.path.join(base_dir, 'static', 'img', 'ic_logo_invert.png')
    
    if os.path.exists(logo_path):
        # Logo sin fondo, tal cual es la imagen
        logo = Image(logo_path, width=2.8*cm, height=2.8*cm)
        
        # Información de la empresa en formato compacto
        empresa_info = [
            [Paragraph("<b>DomusMarket</b>", style_empresa)],
            [Paragraph(
                f"<b>RUC:</b> {datos_empresa.get('ruc', '20123456789')} | "
                f"<b>Tel:</b> {datos_empresa.get('telefono', '(01) 234-5678')}",
                style_contacto_small
            )],
            [Paragraph(
                datos_empresa.get('correo', 'contacto@domusmarket.com'),
                style_contacto_small
            )],
            [Paragraph(
                truncar_texto(datos_empresa.get('direccion', 'Av. Principal 123, Lima, Perú'), 65),
                style_contacto_small
            )]
        ]
        
        empresa_table = Table(empresa_info, colWidths=[12*cm])
        empresa_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        
        header_data = [[logo, empresa_table]]
        
        header_table = Table(header_data, colWidths=[3.5*cm, 12.5*cm])
        header_table.setStyle(TableStyle([
            # SIN FONDO - Logo tal cual es
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ]))
        
        elements.append(header_table)
    else:
        # Si no hay logo, solo mostrar datos de empresa
        elements.append(Paragraph("<b>DomusMarket</b>", style_empresa))
        contacto_text = (
            f"<b>RUC:</b> {datos_empresa.get('ruc', '20123456789')} | "
            f"<b>Tel:</b> {datos_empresa.get('telefono', '(01) 234-5678')}"
        )
        elements.append(Paragraph(contacto_text, style_contacto_small))
        elements.append(Paragraph(datos_empresa.get('correo', 'contacto@domusmarket.com'), style_contacto_small))
        elements.append(Paragraph(
            truncar_texto(datos_empresa.get('direccion', 'Av. Principal 123, Lima, Perú'), 80),
            style_contacto_small
        ))
    
    elements.append(Spacer(1, 1*cm))  # Espacio generoso después del header
    
    # ==================== TIPO Y NÚMERO DE COMPROBANTE ====================
    
    tipo_texto = "BOLETA DE VENTA" if tipo_comprobante == 'boleta' else "FACTURA ELECTRÓNICA"
    
    comprobante_data = [
        [Paragraph(f"<b>{tipo_texto}</b>", style_tipo_comprobante)],
        [Paragraph(f"<b>{numero_comprobante}</b>", style_numero)]
    ]
    
    comprobante_table = Table(comprobante_data, colWidths=[15*cm])
    comprobante_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#2C3E50')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(comprobante_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # ==================== DATOS DEL CLIENTE ====================
    
    elements.append(Paragraph("<b>DATOS DEL CLIENTE</b>", style_section_header))
    elements.append(Spacer(1, 0.2*cm))
    
    cliente_info = [
        ['Cliente:', truncar_texto(datos_cliente.get('nombre_completo', ''), 40)],
        ['Doc:', f"{datos_cliente.get('tipo_doc', 'DNI')}: {datos_cliente.get('doc_identidad', '')}"],
    ]
    
    if tipo_comprobante == 'factura':
        cliente_info.extend([
            ['RUC:', datos_cliente.get('ruc', 'N/A')],
            ['Dirección:', truncar_texto(datos_cliente.get('direccion', 'N/A'), 50)]
        ])
    
    cliente_info.append(['Fecha:', datetime.now().strftime("%d/%m/%Y %H:%M")])
    
    cliente_table = Table(cliente_info, colWidths=[3*cm, 12*cm])
    cliente_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8F9FA')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(cliente_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # ==================== DETALLE DE PRODUCTOS ====================
    
    elements.append(Paragraph("<b>DETALLE DE PRODUCTOS</b>", style_section_header))
    elements.append(Spacer(1, 0.2*cm))
    
    productos_data = [['Cant.', 'Descripción', 'P. Unit.', 'Total']]
    
    for prod in datos_productos:
        nombre_producto = truncar_texto(prod['nombre'], 50)
        
        productos_data.append([
            str(prod['cantidad']),
            nombre_producto,
            f"S/ {float(prod['precio_unitario']):.2f}",
            f"S/ {float(prod['total']):.2f}"
        ])
    
    productos_table = Table(productos_data, colWidths=[2*cm, 8.5*cm, 2.5*cm, 2*cm])
    productos_table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Filas de datos
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 1), (-1, -1), 8),
        ('RIGHTPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(productos_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # ==================== TOTALES ====================
    
    subtotal = sum(float(p['total']) for p in datos_productos)
    igv = subtotal * 0.18
    total = subtotal + igv
    
    totales_data = [
        ['Subtotal:', f"S/ {subtotal:.2f}"],
        ['IGV (18%):', f"S/ {igv:.2f}"],
        ['TOTAL:', f"S/ {total:.2f}"]
    ]
    
    totales_table = Table(totales_data, colWidths=[11*cm, 4*cm])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 1), 10),
        ('FONTSIZE', (0, 2), (-1, 2), 12),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#2C3E50')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F8F9FA')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(totales_table)
    elements.append(Spacer(1, 1*cm))
    
    # ==================== PIE DE PÁGINA ====================
    
    footer_text = """
    <para align=center>
    <font size=7 color="#95A5A6">
    Gracias por su compra en DomusMarket | Este documento tiene validez tributaria
    </font>
    </para>
    """
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Construir PDF
    doc.build(elements)
    
    # Guardar en base de datos
    insertar_comprobante(
        pedidoid=pedidoid,
        tipo_comprobante=tipo_comprobante,
        doc_identidad_cliente=datos_cliente.get('doc_identidad', ''),
        nombre_cliente=datos_cliente.get('nombre_completo', ''),
        subtotal=subtotal,
        igv=igv,
        total=total,
        nombre_archivo=filename,
        numero_comprobante=numero_comprobante,
        razon_social=datos_cliente.get('razon_social') if tipo_comprobante == 'factura' else None,
        ruc=datos_cliente.get('ruc') if tipo_comprobante == 'factura' else None,
        direccion_cliente=datos_cliente.get('direccion') if tipo_comprobante == 'factura' else None
    )
    
    return filename