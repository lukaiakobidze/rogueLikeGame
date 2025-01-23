import copy
import tcod
from engine import Engine
import entity_factories
from proc_gen import generate_dungeon
import color
import traceback
import variables as var

def main() -> None:
    # screen_width = 192
    # screen_height = 108
    # #TO DO --------------------------------------------
    # map_width = 192
    # map_height = 75
    
    # room_max_size = 16
    # room_min_size = 6
    # max_rooms = 20
    # max_monsters_per_room = 2
    # max_items_per_room = 1
    
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    
    player = copy.deepcopy(entity_factories.player)
    
    engine = Engine(player=player)
    engine.game_map = generate_dungeon(var.map_width, var.map_height, var.room_max_size, var.room_min_size, var.max_rooms, var.max_monsters_per_room, var.max_items_per_room, engine=engine)
    engine.update_fov()
    
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )
    with tcod.context.new_terminal(
        var.screen_width,
        var.screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        
        root_console = tcod.Console(var.screen_width, var.screen_height, order="F")
        
        while True:
            
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            
            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:  # Handle exceptions in game.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(), color.error)
                
                
if __name__ == "__main__":
    main()