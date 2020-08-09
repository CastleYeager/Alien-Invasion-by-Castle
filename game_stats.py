"""
游戏状态模块，保存游戏状态的信息
"""
import pygame
from ship import Ship
from pygame.sprite import Group


class GameStats():
    # 初始化游戏状态，设置玩家开局将有多少架飞船可以使用
    def __init__(self, settings):
        self.settings = settings
        # 游戏最高分
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        # 游戏刚开始时，处于非活跃状态
        self.game_active = False
        # 游戏初始化时，分数为0
        self.score = 0
        # 游戏初始化时，等级为1
        self.level = 1


# 计分板类
class ScoreBoard():
    def __init__(self, screen, settings, stats):
        # 初始化信息
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.stats = stats
        # 分数图形的参数
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 获取分数图形
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        # 将分数近似转换为10的倍数
        round_score = round(self.stats.score, -1)
        # 将数字分数转换成字符串分数，按照三位一逗号的形式
        str_score = '{:,}'.format(round_score)
        # 将字符串转换成 Surface对象
        self.score_image = self.font.render(str_score, True, self.text_color, self.settings.background_color)
        # 获取分数图形的坐标位置
        self.score_rect = self.score_image.get_rect()
        # 将分数图形绘制到屏幕右上角
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_scoreboard(self):
        # 绘制当前分数
        self.screen.blit(self.score_image, self.score_rect)
        # 绘制最高分
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # 绘制等级
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制玩家剩余飞船
        self.ships.draw(self.screen)

    def prep_high_score(self):
        # 将最高分转换成10的倍数
        high_score = int(round(self.stats.high_score, -1))
        # 将最高分数字转换成字符串
        str_high_score = '{:,}'.format(high_score)
        # 将最高分字符串转换成 Surface对象
        self.high_score_image = self.font.render(str_high_score, True, self.text_color, self.settings.background_color)
        # 获取最高分图形的坐标
        self.high_score_rect = self.high_score_image.get_rect()
        # 将最高分图形绘制到屏幕顶部中间
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        str_level = 'Lv.' + str(self.stats.level)
        self.level_image = self.font.render(str_level, True, self.text_color, self.settings.background_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom

    def prep_ships(self):
        # 保存飞船的编组
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.screen, self.settings)
            ship.rect.left = 10 + ship_number * ship.rect.width
            ship.rect.bottom = ship.rect.height
            self.ships.add(ship)
