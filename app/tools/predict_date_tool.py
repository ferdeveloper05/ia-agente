from dateutil.relativedelta import relativedelta
from langchain_core.tools import tool
from tools.ven_hour_tool import get_current_time_ven

@tool
def calculate_future_date_ven(years: int = 0, months: int = 0, weeks: int = 0, days: int = 0) -> str:
    """
    Usa la fecha de current_time_data y predice una fecha calculando la diferencia en años, meses, semanas y días que especifiques.
    
    Por ejemplo, si el usuario pregunta qué día será el próximo mes, asigna months=1.
    Si pregunta qué día fue hace 2 años y 5 días, asigna years=-2, days=-5.
    
    Args:
        years (int): Cantidad de años a sumar (positivo) o restar (negativo).
        months (int): Cantidad de meses a sumar (positivo) o restar (negativo).
        weeks (int): Cantidad de semanas a sumar (positivo) o restar (negativo).
        days (int): Cantidad de días a sumar (positivo) o restar (negativo).
        
    Returns:
        str: Un mensaje formateado con la fecha calculada y el día de la semana.
    """
    try:
        current_time_data = get_current_time_ven.invoke({})
        
        if "error" in current_time_data:
            return current_time_data["error"]
        
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        meses_nombres = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
                         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            
        try:
            years = int(float(years))
            months = int(float(months))
            weeks = int(float(weeks))
            days = int(float(days))
        except (ValueError, TypeError):
            return "Error: Los valores numéricos proporcionados no son válidos."
        
        # Calcular la nueva fecha usando relativedelta
        delta = relativedelta(years=years, months=months, weeks=weeks, days=days)
        target_date = current_time_data["datetime"] + delta
        
        nombre_dia = dias_semana[target_date.weekday()]
        fecha_texto = f"{target_date.day} de {meses_nombres[target_date.month-1]} del {target_date.year}"
        
        if target_date.date() > current_time_data["datetime"].date():
            estado = "futuro"
        elif target_date.date() < current_time_data["datetime"].date():
            estado = "pasado"
        else:
            estado = "presente (hoy)"
            
        return f"La fecha en el {estado} calculada es: {fecha_texto}, {nombre_dia}"
        
    except Exception as e:
        return f'Error al calcular la fecha: {str(e)}.'
