import carla

def set_weather(world):
    """
    Set a specific weather condition in the CARLA world.
    Args:
        world (carla.World): The CARLA world instance where the weather will be set.
    """
    weather = carla.WeatherParameters(
        sun_altitude_angle=120.0,
        sun_azimuth_angle=30.0)
    world.set_weather(weather)