import pygame
import socket
import threading
import pickle

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Pong")
clock = pygame.time.Clock()

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 5
    
    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"  # Change to server IP for network play
        self.port = 5555
        self.player_num = None
        self.game_data = None
        self.connect()
    
    def connect(self):
        try:
            self.client.connect((self.server, self.port))
            initial_data = pickle.loads(self.client.recv(2048))
            if 'error' in initial_data:
                print(initial_data['error'])
                return False
            self.player_num = initial_data['player_num']
            self.game_data = initial_data['game_data']
            print(f"Connected as Player {self.player_num+1}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(f"Network error: {e}")
            return None

def draw_waiting_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 50)
    text = font.render("Waiting for second player...", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()

def main():
    n = Network()
    if n.player_num is None:
        pygame.quit()
        return
    
    # Create paddle based on player number
    if n.player_num == 0:
        paddle = Paddle(20, HEIGHT//2 - PADDLE_HEIGHT//2)  # Left paddle
    else:
        paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)  # Right paddle

    run = True
    
    def receive_data():
        nonlocal n
        while run:
            try:
                data = n.send({'paddle_y': paddle.rect.y})
                if data:
                    n.game_data = data
            except:
                break
    
    # Start network thread
    thread = threading.Thread(target=receive_data)
    thread.start()
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Handle controls
        keys = pygame.key.get_pressed()
        if n.player_num == 0:
            if keys[pygame.K_w]:
                paddle.move(up=True)
            if keys[pygame.K_s]:
                paddle.move(up=False)
        else:
            if keys[pygame.K_UP]:
                paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                paddle.move(up=False)
        
        # Draw game state
        if not n.game_data['game_started']:
            draw_waiting_screen()
            continue
            
        screen.fill(BLACK)
        
        # Draw paddles
        paddle.draw()
        opponent_paddle = Paddle(
            20 if n.player_num == 1 else WIDTH - 20 - PADDLE_WIDTH,
            n.game_data['paddle1_y'] if n.player_num == 1 else n.game_data['paddle2_y']
        )
        opponent_paddle.draw()
        
        # Draw ball
        ball_rect = pygame.Rect(n.game_data['ball_x'] - 7, n.game_data['ball_y'] - 7, 15, 15)
        pygame.draw.rect(screen, WHITE, ball_rect)
        
        # Draw scores
        font = pygame.font.SysFont(None, 74)
        score_text = font.render(f"{n.game_data['score1']} - {n.game_data['score2']}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
        
        pygame.display.update()
    
    pygame.quit()
    thread.join()

if __name__ == "__main__":
    main()