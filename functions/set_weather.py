import carla

def set_weather(world, sun_altitude_angle, sun_azimuth_angle):
    """
    Set a specific weather condition in the CARLA world.
    Args:
        world (carla.World): The CARLA world instance where the weather will be set.
        sun_altitude_angle (float): The altitude angle of the sun.
        sun_azimuth_angle (float): The azimuth angle of the sun.
    """
    weather = carla.WeatherParameters(
        sun_altitude_angle= sun_altitude_angle,
        sun_azimuth_angle= sun_azimuth_angle)
    world.set_weather(weather)