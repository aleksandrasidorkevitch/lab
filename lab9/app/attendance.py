# app/attendance.py
"""Модуль учёта посещаемости студентов.

Реализует задачу 25: подсчёт процента посещаемости и формирование
списка студентов, чья посещаемость строго ниже заданного порога.
"""

from __future__ import annotations


class AttendanceError(ValueError):
    """Базовое исключение домена «посещаемость».

    Отделяет ошибки бизнес-логики от общих ValueError, чтобы вызывающий
    код мог ловить их отдельно (например, при валидации пользовательского ввода).
    """


class AttendanceTracker:
    """Трекер посещаемости группы студентов.

    Параметры
    ----------
    total_classes : int
        Общее количество занятий в отчётном периоде.
        Допускается значение 0 (начало семестра, занятия ещё не проводились).

    Исключения
    ----------
    AttendanceError
        Если `total_classes` отрицательный.
    """

    def __init__(self, total_classes: int) -> None:
        if not isinstance(total_classes, int):
            raise AttendanceError(
                f"Количество занятий должно быть целым числом. Получено: {total_classes!r}"
            )
        if total_classes < 0:
            raise AttendanceError(
                f"Общее количество занятий не может быть отрицательным. Получено: {total_classes}"
            )
        self._total_classes: int = total_classes
        # Хранилище: {имя_студента: количество_посещённых_занятий}
        self._records: dict[str, int] = {}

    @property
    def total_classes(self) -> int:
        return self._total_classes

    def record_attendance(self, student_name: str, attended_classes: int) -> None:
        """Записывает количество посещённых занятий для студента.

        Параметры
        ----------
        student_name : str
            Имя студента (непустая строка).
        attended_classes : int
            Количество посещённых занятий. Должно быть в диапазоне
            [0, total_classes].

        Исключения
        ----------
        AttendanceError
            Некорректное имя, отрицательное число посещений или
            посещений больше, чем всего занятий.
        """
        if not isinstance(student_name, str) or not student_name.strip():
            raise AttendanceError("Имя студента должно быть непустой строкой")

        if not isinstance(attended_classes, int):
            raise AttendanceError(
                f"Количество посещений должно быть целым числом. "
                f"Студент '{student_name}', получено: {attended_classes!r}"
            )
        if attended_classes < 0:
            raise AttendanceError(
                f"Количество посещённых занятий не может быть отрицательным "
                f"для студента '{student_name}'. Получено: {attended_classes}"
            )
        if attended_classes > self._total_classes:
            raise AttendanceError(
                f"Студент '{student_name}' не мог посетить {attended_classes} занятий, "
                f"если всего их было {self._total_classes}"
            )

        self._records[student_name] = attended_classes

    def get_attendance_percent(self, student_name: str) -> float:
        """Возвращает процент посещаемости конкретного студента.

        Исключения
        ----------
        AttendanceError
            Если студент не зарегистрирован или занятий не было (0).
        """
        if student_name not in self._records:
            raise AttendanceError(
                f"Студент '{student_name}' не найден в журнале посещаемости"
            )
        if self._total_classes == 0:
            raise AttendanceError(
                f"Невозможно рассчитать процент посещаемости для '{student_name}': "
                f"занятий в отчётном периоде не было"
            )
        return (self._records[student_name] / self._total_classes) * 100.0

    def get_students_below_threshold(self, threshold_percent: float) -> list[str]:
        """Возвращает список студентов с посещаемостью строго ниже порога.

        Параметры
        ----------
        threshold_percent : float
            Порог в диапазоне [0, 100]. Студент попадает в результат,
            если его процент строго меньше порога.

        Возвращает
        ----------
        list[str]
            Список имён студентов. Если занятий не было (total_classes == 0),
            возвращается пустой список — это осознанное решение: при отсутствии
            занятий порог нарушить невозможно, поэтому «должников» нет.

        Исключения
        ----------
        AttendanceError
            Если порог вне диапазона [0, 100].
        """
        if not isinstance(threshold_percent, (int, float)):
            raise AttendanceError(
                f"Порог должен быть числом. Получено: {threshold_percent!r}"
            )
        if not (0 <= threshold_percent <= 100):
            raise AttendanceError(
                f"Порог посещаемости должен быть в диапазоне от 0 до 100. "
                f"Получено: {threshold_percent}"
            )

        # Ключевой краевой случай: занятий не было → никто не может быть ниже порога.
        # Это предотвращает ZeroDivisionError и делает API устойчивым.
        if self._total_classes == 0:
            return []

        below: list[str] = []
        for name, attended in self._records.items():
            percent = (attended / self._total_classes) * 100.0
            if percent < threshold_percent:
                below.append(name)
        return below

    def summary(self) -> dict[str, float]:
        """Возвращает словарь {имя: процент_посещаемости}.

        Для total_classes == 0 возвращает пустой словарь.
        """
        if self._total_classes == 0:
            return {}
        return {
            name: (attended / self._total_classes) * 100.0
            for name, attended in self._records.items()
        }


# ---------- Демо-запуск ----------
if __name__ == "__main__":
    tracker = AttendanceTracker(total_classes=10)
    tracker.record_attendance("Анна", 8)    # 80%
    tracker.record_attendance("Борис", 5)   # 50%
    tracker.record_attendance("Виктор", 7)  # 70%
    tracker.record_attendance("Глеб", 10)   # 100%

    print("Сводка по группе:")
    for name, percent in tracker.summary().items():
        print(f"  {name:>8}: {percent:5.1f}%")

    threshold = 75.0
    below = tracker.get_students_below_threshold(threshold)
    print(f"\nСтуденты ниже порога {threshold}%: {below or 'нет'}")

    # Краевой случай: начало семестра
    empty_tracker = AttendanceTracker(total_classes=0)
    empty_tracker.record_attendance("Дарья", 0)
    print(f"\nПри 0 занятий список отстающих: {empty_tracker.get_students_below_threshold(75)}")

