import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        # Implement it
        endpoint_url = f"{self.api_base_url}/processed_agent_data/"
        try:
            response = requests.post(
                endpoint_url,
                data=json.dumps(
                    processed_agent_data_batch, default=pydantic_core.to_jsonable_python
                ),
            )
            if response.status_code in (200, 201):
                # logging.info("Processed road data saved successfully.")
                return True
            else:
                logging.info(
                    f"Failed to save processed road data. Status code: {response.status_code}"
                )
                return False
        except requests.exceptions.RequestException as e:
            logging.info(f"Failed to connect to the Store API: {e}")
            return False
