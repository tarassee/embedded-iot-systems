from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    _position: int
    _accelerometer: list[Accelerometer]
    _gps: list[Gps]

    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename

    def read(self) -> AggregatedData:
        if self._position == len(self._accelerometer):
            self._position = 0

        data = AggregatedData(
            config.USER_ID,
            self._accelerometer[self._position],
            self._gps[self._position],
            datetime.now(),
        )
        self._position += 1
        return data

    def startReading(self, *args, **kwargs):
        self._position = 0
        self._accelerometer = []
        self._gps = []
        with open(self.accelerometer_filename, "r") as accelerometer_file:
            with open(self.gps_filename, "r") as gps_file:
                accelerometer_data_reader = reader(accelerometer_file)
                gps_data_reader = reader(gps_file)
                next(accelerometer_data_reader)
                next(gps_data_reader)

                def make_gps_smoother(gps_generator):
                    longitude1, latitude1 = map(float, next(gps_generator))
                    yield longitude1, latitude1
                    smooth_step = 8
                    for p2 in gps_generator:
                        longitude2, latitude2 = map(float, p2)
                        for i in range(1, smooth_step):
                            yield (
                                longitude1 + (longitude2 - longitude1) * i / smooth_step,
                                latitude1 + (latitude2 - latitude1) * i / smooth_step,
                            )
                        longitude1 = longitude2
                        latitude1 = latitude2

                for accelerometer_row, gps_row in zip(
                        accelerometer_data_reader, make_gps_smoother(gps_data_reader)
                ):
                    if len(accelerometer_row) == 0 or len(gps_row) == 0:
                        continue
                    self._accelerometer.append(
                        Accelerometer(*map(int, accelerometer_row))
                    )
                    self._gps.append(
                        Gps(*map(float, gps_row))
                    )

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
