
import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 設定視窗大小和格子大小
GRID_SIZE = 20
GRID_WIDTH = 480
GRID_HEIGHT = 480
GRID_ROWS = GRID_WIDTH // GRID_SIZE
GRID_COLS = GRID_HEIGHT // GRID_SIZE

# 設定顏色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 定義方向常數
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 顯示分數和遊戲畫面更新
def display_score(surface, current_score, high_score):
    # 在畫面上顯示分數和最高分
    font = pygame.font.Font("pixel_font.ttf", 16)
    score_text = font.render(f"Score: {current_score}  High Score: {high_score}", True, WHITE)
    surface.blit(score_text, (10, 10))

# 主遊戲函數
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
    pygame.display.set_caption("貪吃蛇遊戲")

    snake = Snake()  # 初始化貪吃蛇
    food = Food()    # 初始化食物
    current_score = 0
    high_score = 0

    running = True
    while running:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 按鍵事件處理，控制貪吃蛇移動方向
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        # 移動貪吃蛇，並檢查遊戲狀態
        if not snake.move():
            # 若遊戲結束，重設遊戲狀態並更新最高分
            if current_score > high_score:
                high_score = current_score
            current_score = 0
            food.randomize_position()
            snake.reset()

        # 檢查是否吃到食物
        if snake.get_head_position() == food.position:
            # 吃到食物後，貪吃蛇長度增加，重設食物位置，更新分數
            snake.length += 1
            food.randomize_position()
            current_score += 1
            if current_score > high_score:
                high_score = current_score

        # 清除畫面
        screen.fill((0, 0, 0))

        # 繪製貪吃蛇、食物和分數
        snake.draw(screen)
        food.draw(screen)
        display_score(screen, current_score, high_score)

        # 更新畫面
        pygame.display.update()

        # 控制遊戲速度
        clock.tick(10)

# 定義貪吃蛇類別
class Snake:
    def __init__(self):
        # 初始化貪吃蛇的屬性
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]  # 起始位置在視窗中央
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])        # 隨機選擇起始移動方向
        self.color = GREEN

    def get_head_position(self):
        # 取得貪吃蛇頭部位置
        return self.positions[0]

    def turn(self, point):
        # 改變貪吃蛇移動方向，但不允許直接掉頭
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        # 移動貪吃蛇，並檢查是否碰撞到自身或邊界
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % GRID_WIDTH), (cur[1] + (y * GRID_SIZE)) % GRID_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False  # 碰撞到自身，遊戲結束
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        # 重設貪吃蛇的屬性，用於遊戲重新開始
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]  # 重置到初始位置
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])        # 隨機選擇新的起始移動方向

    def draw(self, surface):
        # 繪製貪吃蛇的每一節身體
        for p in self.positions:
            r = pygame.Rect(p, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

# 定義食物類別
class Food:
    def __init__(self):
        # 初始化食物的屬性
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        # 隨機設定食物的位置
        self.position = (random.randint(0, GRID_ROWS - 1) * GRID_SIZE, random.randint(0, GRID_COLS - 1) * GRID_SIZE)

    def draw(self, surface):
        # 繪製食物
        r = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# 執行主程式 Designed by Allen Tsai
if __name__ == "__main__":
    main()