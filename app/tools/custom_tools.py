from datetime import datetime
from zoneinfo import ZoneInfo
from langchain_core.tools import tool


@tool
def get_current_datetime(timezone: str = 'America/Caracas') -> str:
    """ 
    Obtiene la fecha y hora actual en el timezone especificado.
    Usala cuando necesites saber la fecha o hora actual.
    
    Args:
        timezone: Zona horaria en formato IANA (ej: 'America/Caracas')
    Returns:
        String con fecha y hora formateada, incluyendo el día de la semana.
    """
    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        nombre_dia = dias[now.weekday()]
        return f"Fecha local ({timezone}): {nombre_dia}, {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        return f'Error: No se pudo obtener la zona horaria "{timezone}". INSTRUCCIÓN PARA EL AGENTE: Utiliza obligatoriamente la herramienta "duckduckgo_search" para buscar "timezonemap venezuela" (o el país correspondiente) y obtener la hora actualizada de internet.'