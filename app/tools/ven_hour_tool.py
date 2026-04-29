from datetime import datetime, timedelta, timezone
from langchain_core.tools import tool

@tool
def get_current_time_ven() -> dict:
    """ 
    Obtiene la fecha y hora actual de Venezuela (UTC-4).
    Retorna un diccionario con el objeto datetime y el texto formateado con la fecha/hora.
    """
    try:
        # Obtener hora UTC actual
        utc_now = datetime.now(timezone.utc)
        
        # Definir el offset de Venezuela (UTC-4)
        venezuela_offset = timedelta(hours=-4)
        venezuela_tz = timezone(venezuela_offset)
        
        # Convertir a hora de Venezuela
        now = utc_now.astimezone(venezuela_tz)
        
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        nombre_dia = dias[now.weekday()]
        fecha_texto = f"{nombre_dia}, {now.day} de {meses[now.month-1]} del {now.year}"
        hora_texto = now.strftime('%I:%M:%S %p')
        
        return {
            "datetime": now,
            "info_hoy": f"Fecha local (Venezuela): {fecha_texto}\nHora: {hora_texto}\nZona: UTC-4"
        }
        
    except Exception as e:
        return {
            "error": f'Error: No se pudo obtener la hora. Detalles: {str(e)}'
        }