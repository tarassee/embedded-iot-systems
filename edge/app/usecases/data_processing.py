from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData


def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    z_acceleration = agent_data.accelerometer.z

    if 14000 > z_acceleration < 18000:
        road_state = "normal"
    elif 12000 > z_acceleration < 14000 or 18000 > z_acceleration < 20000:
        road_state = "small pits"
    else:
        road_state = "large pits"
    return ProcessedAgentData(road_state=road_state, agent_data=agent_data)
