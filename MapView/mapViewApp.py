from kivy.app import App
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarker

from datasource import Datasource
from lineMapLayer import LineMapLayer


class MapViewApp(App):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.car_marker = None
        self.map_view = None
        self.map_layer = None
        self.pothole_marker = None
        self.pit = None
        self.bump_marker = None
        self.datasource = None

    def on_start(self) -> None:
        self.datasource = Datasource(1)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args) -> None:
        points = self.datasource.get_new_points()
        if len(points) == 0:
            return
        for point in points:
            print(point)
            self.map_layer.add_point(point)
        self.update_car_marker(points[-1])

    def update_car_marker(self, point) -> None:
        pit = point[2]
        if pit == "small pits":
            self.create_pit(point, "images/pothole.png")
        elif pit == "large pits":
            self.create_pit(point, "images/bump.png")
        elif pit == "normal":
            self.move_car(point)
        else:
            print(f"unknown pit value", {pit})

    def create_pit(self, point, pit_img) -> None:
        self.pit = MapMarker(
            lat=point[0],
            lon=point[1],
            source=pit_img,
        )
        self.map_view.add_marker(self.pit)
        self.move_car(point)

    def move_car(self, point) -> None:
        self.map_view.remove_marker(self.car_marker)
        self.car_marker.lat = point[0]
        self.car_marker.lon = point[1]
        self.map_view.add_marker(self.car_marker)

    def set_pothole_marker(self, point) -> None:
        if self.pothole_marker:
            self.map_view.remove_marker(self.pothole_marker)
        self.pothole_marker = MapMarker(
            lat=point[0],
            lon=point[1],
            source="images/pothole.png",
        )
        self.map_view.add_marker(self.pothole_marker)

    def set_bump_marker(self, point) -> None:
        if self.bump_marker:
            self.map_view.remove_marker(self.bump_marker)
        self.bump_marker = MapMarker(
            lat=point[0],
            lon=point[1],
            source="images/bump.png",
        )
        self.map_view.add_marker(self.bump_marker)

    def build(self) -> MapView:
        self.map_layer = LineMapLayer()
        self.map_view = MapView(
            zoom=14,
            lat=50.4501,
            lon=30.5234,
        )
        self.map_view.add_layer(self.map_layer, mode="scatter")
        self.car_marker = MapMarker(
            lat=50.45034509664691,
            lon=30.5246114730835,
            source="images/car.png",
        )
        self.map_view.add_marker(self.car_marker)
        return self.map_view
