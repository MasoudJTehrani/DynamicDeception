import carla

def set_weather(world):
    weather = carla.WeatherParameters(
        sun_altitude_angle=120.0,
        sun_azimuth_angle=30.0)
    world.set_weather(weather)
    
client = carla.Client('localhost', 2000)
world = client.get_world()
set_weather(world)
