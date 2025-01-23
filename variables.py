import sdl2

# Initialize SDL2 to get screen resolution
sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

display_index = 0  # Use primary display
display_mode = sdl2.SDL_DisplayMode()
sdl2.SDL_GetCurrentDisplayMode(display_index, display_mode)

# Get screen dimensions in pixels
screen_width = display_mode.w
screen_height = display_mode.h

# Avoid too large sizes, and ensure a reasonable console size
tile_size = 10  # Adjust if necessary
screen_width = max(80, screen_width // tile_size)  
screen_height = max(50, screen_height // tile_size)

# Game map dimensions
map_width = screen_width
map_height = screen_height

room_max_size = 20
room_min_size = 8
max_rooms = 30
max_monsters_per_room = 2
max_items_per_room = 2

fov_radius = 16
bar_width = 20

sdl2.SDL_Quit()
