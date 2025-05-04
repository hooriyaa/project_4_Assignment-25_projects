import socket
import threading
import pickle
import random
import time

class GameServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 5555))
        self.server.listen(2)
        self.players = []
        self.game_data = {
            'paddle1_y': 250,
            'paddle2_y': 250,
            'ball_x': 400,
            'ball_y': 300,
            'ball_dx': 3,  # Slower initial speed
            'ball_dy': 3,
            'score1': 0,
            'score2': 0,
            'game_started': False
        }
        print("Server started on port 5555. Waiting for players...")

    def handle_client(self, conn, player):
        try:
            conn.send(pickle.dumps({'player_num': player, 'game_data': self.game_data}))
            print(f"Player {player+1} connected")
            
            while True:
                try:
                    data = pickle.loads(conn.recv(2048))
                    if not data:
                        break
                    
                    # Update paddle position
                    if player == 0:
                        self.game_data['paddle1_y'] = data['paddle_y']
                    else:
                        self.game_data['paddle2_y'] = data['paddle_y']
                    
                    # Only start game when both players connected
                    if len(self.players) == 2 and not self.game_data['game_started']:
                        self.game_data['game_started'] = True
                        print("Both players connected! Game starting...")
                    
                    # Only update ball if game has started
                    if self.game_data['game_started'] and player == 0:  # Player 1 controls ball
                        self.update_ball()
                    
                    conn.send(pickle.dumps(self.game_data))
                    time.sleep(0.016)  # ~60FPS sync
                    
                except Exception as e:
                    print(f"Error: {e}")
                    break
                    
        except Exception as e:
            print(f"Player {player+1} error: {e}")
        finally:
            print(f"Player {player+1} disconnected")
            if player < len(self.players):
                self.players.pop(player)
            conn.close()

    def update_ball(self):
        # Update ball position
        self.game_data['ball_x'] += self.game_data['ball_dx']
        self.game_data['ball_y'] += self.game_data['ball_dy']
        
        # Wall collision
        if self.game_data['ball_y'] <= 0 or self.game_data['ball_y'] >= 580:
            self.game_data['ball_dy'] *= -1
        
        # Paddle collision
        paddle1_rect = pygame.Rect(20, self.game_data['paddle1_y'], 15, 100)
        paddle2_rect = pygame.Rect(765, self.game_data['paddle2_y'], 15, 100)
        ball_rect = pygame.Rect(self.game_data['ball_x']-7, self.game_data['ball_y']-7, 15, 15)
        
        if ball_rect.colliderect(paddle1_rect) or ball_rect.colliderect(paddle2_rect):
            self.game_data['ball_dx'] *= -1
            # Slight random angle change
            self.game_data['ball_dy'] += random.uniform(-1, 1)
        
        # Scoring
        if self.game_data['ball_x'] <= 0:
            self.game_data['score2'] += 1
            self.reset_ball()
        elif self.game_data['ball_x'] >= 800:
            self.game_data['score1'] += 1
            self.reset_ball()

    def reset_ball(self):
        self.game_data['ball_x'] = 400
        self.game_data['ball_y'] = 300
        self.game_data['ball_dx'] = 3 * random.choice((1, -1))
        self.game_data['ball_dy'] = 3 * random.choice((1, -1))
        time.sleep(1)  # Pause before next round

    def run(self):
        while True:
            conn, addr = self.server.accept()
            player_num = len(self.players)
            if player_num < 2:
                self.players.append(conn)
                thread = threading.Thread(target=self.handle_client, args=(conn, player_num))
                thread.start()
            else:
                conn.send(pickle.dumps({'error': 'Game is full'}))
                conn.close()

if __name__ == "__main__":
    import pygame  # For Rect collision
    pygame.init()
    server = GameServer()
    server.run()