ERR_UPDATE = 'В проект были внесены средства, не подлежит удалению!'
ERR_FULL_AMOUNT = 'Нельзя установить требуемую сумму меньше уже вложенной'
ERR_CLOSE_PROJECT = 'Закрытый проект нельзя редактировать!'
ERR_NOT_FOUND_PROJECT = 'Проект не найден!'
ERR_NAME_DUPLICATE = 'Проект с таким именем уже существует!'

SERVICE_SHEETS = 'sheets'
SHEETS_VERSION = 'v4'
SERVICE_DRIVER = 'driver'
DRIVER_VERSION = 'v3'
SPREADSHEETS_BODY_SHEETS = [
    {'properties': {
        'sheetType': 'GRID',
        'sheetId': 0,
        'title': 'Лист1',
        'gridProperties': {
            'rowCount': 100,
            'columnCount': 11
        }
    }
    }]
