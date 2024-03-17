import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url: str) -> None:
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]) -> bool:
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """

        endpoint = f"{self.api_base_url}/processed_agent_data/"

        try:
            res = requests.post(
                endpoint,
                data=json.dumps(
                    processed_agent_data_batch,
                    default=pydantic_core.to_jsonable_python,
                ),
            )

            if res.status_code in (200, 201):
                return True
            else:
                logging.info(
                    f"{res.status_code} STATUS CODE. Failure while saving "
                    f"processed data."
                )

                return False

        except requests.exceptions.RequestException as error:
            logging.info(f"Failed to connect to the Store API: {error}")

            return False
