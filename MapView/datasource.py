import asyncio
import json

import websockets
from kivy import Logger

from config import STORE_HOST, STORE_PORT
from data import ProcessedAgentData


class Datasource:
    def __init__(self, user_identifier: int):
        self.idx = 0
        self.user_identifier = user_identifier
        self.conn_status = None
        self._new_data_points = []
        asyncio.ensure_future(self.establish_server_connection())

    def get_new_points(self):
        data_points = self._new_data_points
        self._new_data_points = []
        return data_points

    async def establish_server_connection(self):
        uri = f"ws://{STORE_HOST}:{STORE_PORT}/ws/{self.user_identifier}"
        while True:
            async with websockets.connect(uri) as websocket:
                self.conn_status = "Connected"
                try:
                    await self.data_reception_loop(websocket)
                except websockets.ConnectionClosedOK:
                    self.conn_status = "Disconnected"

    async def data_reception_loop(self, websocket):
        while True:
            data = await websocket.recv()
            parsed_data = json.loads(data)
            self.process_received_data(parsed_data)

    def process_received_data(self, data):
        Logger.debug(f"Received data: {json.loads(data)}")
        processed_agent_data_list = self.process_agent_data(json.loads(data))
        self._new_data_points.extend(self.extract_point_info(processed_agent_data_list))

    @staticmethod
    def process_agent_data(data):
        return sorted(
            [
                ProcessedAgentData(**processed_data_json)
                for processed_data_json in data
            ],
            key=lambda v: v.timestamp
        )

    @staticmethod
    def extract_point_info(processed_agent_data_list):
        return [
            (
                processed_agent_data.longitude,
                processed_agent_data.latitude,
                processed_agent_data.road_state,
            )
            for processed_agent_data in processed_agent_data_list
        ]
