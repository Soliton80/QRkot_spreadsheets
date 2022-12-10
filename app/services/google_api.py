import copy
from datetime import datetime

from aiogoogle import Aiogoogle
from aiogoogle.excs import ValidationError
from app.core.config import settings
from typing import Dict


TITLE = 'Отчет на {}'
ROW = 100
COLUMN = 11

SPREADSHEET_BODY = dict(
    properties=dict(
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW,
            columnCount=COLUMN,
        )
    ))]
)
HEADER = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

SPREADSHEET_CREATE_ERROR = (
    'Количество передаваемых данных не помещается в таблице. '
    'Вы передаете {in_row} строк {in_column} столбцов. '
    'Размер таблицы: {100} строк {11} столбцов.'
)


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    now_date_time: datetime,
    spreadsheet_body: Dict = None,
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = (
        copy.deepcopy(SPREADSHEET_BODY) if spreadsheet_body
        is None else spreadsheet_body)
    spreadsheet_body['properties']['title'] = TITLE.format(str(now_date_time))
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle,
        now_date_time: datetime,
) -> None:
    service = await wrapper_services.discover(
        'sheets',
        'v4'
    )
    projects_fields = sorted((
        (
            project.name,
            project.close_date - project.create_date,
            project.description
        ) for project in projects
    ), key=lambda x: x[1])
    header = copy.deepcopy(HEADER)
    header[0][1] = str(now_date_time)
    table_values = [
        *header,
        *[list(map(str, field)) for field in projects_fields],
    ]
    in_row, in_column = len(table_values), max(len(i) for i in header)
    if in_row > 100 or in_column > 11:
        raise ValidationError(
            SPREADSHEET_CREATE_ERROR.format(
                in_row=in_row, in_column=in_column,
                row=ROW, column=COLUMN),
        )

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{ROW}C{COLUMN}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
