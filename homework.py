from dataclasses import asdict, dataclass
from typing import ClassVar, List, Union


@dataclass
class InfoMessage:
    """Класс информационного сообщения о тренировке.

    Параметры:
     ----------
     training_type : str
         Тип тренировки
     duration : float
         Длительность тренировки в часах
     distance : float
         Преодоленная дистанция
     speed : float
         Средняя скорость спортсмена в км/ч
     calories : float
         Потраченные спортсменом калории
    """

    TRAINING_DATA_MSG: ClassVar[str] = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч;'
        ' Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вернуть строку сообщения."""

        return self.TRAINING_DATA_MSG.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        """
        Параметры:
        ----------
        action : int
            Число совершённых шагов или гребков
        duration : float
            Длительность тренировки в часах
        weight : float
            Вес спортсмена в кг.
        """

        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError('Метод не определён.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        dist: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(
            type(self).__name__, self.duration, dist, speed, calories
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        speed: float = super().get_mean_speed()
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MULTIPLIER_1: float = 0.035
    CALORIES_MULTIPLIER_2: float = 0.029
    KMH_TO_MS: float = 0.278
    CM_IN_M: int = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        """
        Параметры:
        ----------
        action : int
            Число совершённых шагов или гребков
        duration : float
            Длительность тренировки в часах
        weight : float
            Вес спортсмена в кг.
        height : float
            Рост спортсмена в см.
        """

        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        speed_ms: float = super().get_mean_speed() * self.KMH_TO_MS
        height_m: float = self.height / self.CM_IN_M
        return (
            (
                self.CALORIES_MULTIPLIER_1 * self.weight
                + (speed_ms ** 2 / height_m)
                * self.CALORIES_MULTIPLIER_2
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        """
        Параметры:
        ----------
        action : int
            Число совершённых шагов или гребков
        duration : float
            Длительность тренировки в часах
        weight : float
            Вес спортсмена в кг.
        length_pool : float
            Длина бассейна в метрах
        count_pool : int
            Количество пересечения бассейна
        """

        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        speed: float = self.get_mean_speed()
        return (
            (speed + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_MEAN_SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type not in training_types:
        raise KeyError('Такая тренировка не определена.')
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, List[Union[int, float]]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
