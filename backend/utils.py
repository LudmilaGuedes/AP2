from datetime import datetime

def validar_dia_util(data, feriados):
    """
    Verifica se uma data é dia útil (não é final de semana nem feriado).

    Args:
        data (datetime.date): Data a ser validada.
        feriados (list): Lista de datas de feriados.

    Returns:
        bool: True se for dia útil, False caso contrário.
    """
    return data.weekday() < 5 and data not in feriados
