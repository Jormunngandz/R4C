import io
from io import BytesIO
from typing import List,  Tuple
import xlsxwriter
from django.http import FileResponse
from django.utils import timezone
from django.views import View
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet
from .models import Robot


class GetLastWeekRobotsStatistic(View):

    @classmethod
    def get(cls, request) -> FileResponse:
        """На основе полученной из модели данных формируем Excel-файл
        с постраничной разбивкой для каждой модели роботов."""
        last_week_robots_info: List[Tuple] = Robot.get_last_week_robots_statistic()
        # Создаем Excel-книгу, информацию о каждой модели записываем на отдельный лист книги
        buffer: BytesIO = io.BytesIO()
        workbook: Workbook = xlsxwriter.Workbook(buffer)
        if last_week_robots_info:

            for model_stat in last_week_robots_info:
                worksheet: Worksheet = workbook.add_worksheet(f'Model {model_stat[0][0]}')
                worksheet.write_row("A1", ["Модель", "Версия", 'Количество за неделю'])
                for i, version in enumerate(model_stat):
                    worksheet.write_row(f"A{i + 2}", version)

                worksheet.autofit()
        else:
            worksheet: Worksheet = workbook.add_worksheet()
            worksheet.write("A1", "За последние 7 дней роботов не был")
            worksheet.autofit()
        workbook.close()
        buffer.seek(0)

        return FileResponse(buffer,
                            as_attachment=True,
                            filename=f'report{timezone.now().date()}.xlsx',
                            status=200)
