from __future__ import annotations
from typing import TYPE_CHECKING
from tcod.console import Console
from tcod.map import compute_fov
from render_functions import render_bar, render_names_at_mouse_location
from input_handlers import MainGameEventHandler
from message_log import MessageLog
import exceptions
import variables as var
if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler

class Engine:
    game_map: GameMap
    
    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.player = player
        self.mouse_location = (0, 0)
        
    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.
     
    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=var.fov_radius,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

            
    def render(self, console: Console) -> None:
        
        self.game_map.render(console)
        self.message_log.render(console=console, x=var.screen_width-60, y=var.screen_height-5, width=60, height=4)
        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=var.bar_width,
        )
        console.print(var.bar_width + 1, var.screen_height-5, "E: use item in inventory.")
        console.print(var.bar_width + 1, var.screen_height-4, "Q: drop item from inventory.")
        console.print(var.bar_width + 1, var.screen_height-3, "F: pick up item.")
        render_names_at_mouse_location(console, *self.mouse_location, self, self.game_map)
        
        