import carla
import time

client = carla.Client('localhost', 2000)
world = client.get_world()

# Spawn and despawn pedestrian multiple pedestrians one by one at the same location
def main():
    try:
        settings = world.get_settings()
        settings.synchronous_mode = True  # Enables synchronous mode
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        blueprint_library = world.get_blueprint_library()
        pedestrian_bp = blueprint_library.filter('walker.pedestrian.*')


        # get spectators location and set the spawn point in front of it to see the pedestrian
        spectator = world.get_spectator()
        spec_transform = spectator.get_transform()

        spawn_point = spec_transform
        spawn_point.location += spec_transform.get_forward_vector() * 5  # 5 meters in front
        print(f'Spawn point for pedestrians: {spawn_point.location}')

        # Change the range in the for loop to try different pedestrians
        for i in range(59, 65):
            pedestrian_bps = blueprint_library.filter('walker.pedestrian.00' + str(i).zfill(2))
            if len(pedestrian_bps) > 0:
                pedestrian_bp = pedestrian_bps[0]
                pedestrian = world.try_spawn_actor(pedestrian_bp, spawn_point)
                for j in range(100):
                    world.tick()
                print(f'Spawned pedestrian {pedestrian.type_id}')

                pedestrian.destroy()
                for k in range(20):
                    world.tick()
            else:
                print(f'Failed to spawn pedestrian')

    finally:
        settings.synchronous_mode = False
        world.apply_settings(settings)
        pedestrian.destroy()
        print('All done!')


if __name__ == '__main__':
    main()