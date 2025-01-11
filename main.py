import copy
import tcod
from engine import Engine
from input_handlers import EventHandler
import entity_factories
from proc_gen import generate_dungeon



def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45
    
    room_max_size = 12
    room_min_size = 4
    max_rooms = 30
    max_monsters_per_room = 2
    
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()
    
    player = copy.deepcopy(entity_factories.player)
    #npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    #entities = {player, npc}

    game_map = generate_dungeon(map_width, map_height, room_max_size, room_min_size, max_rooms, max_monsters_per_room, player)
    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        
        root_console = tcod.Console(screen_width, screen_height, order="F")
        
        while True:
            
            engine.render(console=root_console,context=context)

            events = tcod.event.wait()
            
            engine.handle_events(events)
                
                
if __name__ == "__main__":
    main()