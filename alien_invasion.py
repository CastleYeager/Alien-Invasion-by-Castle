
# 从pygame的精灵模块中导入管理精灵编组的类
from pygame.sprite import Group
# 导入设置类，存放着我们要用到的所有设置参数
from settings import Settings
# 从ship模块中导入飞船类，用以创建飞船
from ship import Ship
# 从 game_functions 模块中导入所有函数，以供使用
from game_functions import *
# 从 游戏状态模块中导入 GameStats 类
from game_stats import GameStats
# 从 按钮模块 中导入 Button 类
from button import Button
# 从 计分板模块 中导入 ScoreBoard 类
from game_stats import ScoreBoard


# 游戏的主逻辑都在 run_game()函数中运行
def run_game():
    # 初始化 pygame。使其可以绘制屏幕   初始化pg返回一个元组，元组第一个元素是导入成功的包的数量，第二个元素是失败的数量
    import_pygame_info = pygame.init()
    print('pygame包导入成功和失败的数量分别为： ', import_pygame_info)

    # 查看 display 模块是否导入成功
    is_display_import = pygame.display.get_init()
    print('pygame.display 模块是否导入成功： ', bool(is_display_import))

    # 初始化设置类，得到所有我们要用到的设置参数值
    my_settings = Settings()

    # 获取当前屏幕的全屏参数
    print('全屏宽度为： ', pygame.display.Info().current_w)
    print('全屏高度为： ', pygame.display.Info().current_h)

    # 绘制游戏窗口 my_screen，所有的游戏元素都在这个窗口里运动交互
    my_screen = pygame.display.set_mode(size=(my_settings.screen_width, my_settings.screen_height))

    # 修改游戏窗口的标题，这里当然是‘外星人入侵’
    pygame.display.set_caption(my_settings.screen_title)

    # 初始化游戏状态
    my_gamestats = GameStats(my_settings)

    # 初始化计分板
    my_scoreboard = ScoreBoard(my_screen, my_settings, my_gamestats)

    # 初始化飞船对象，创建一架飞船
    my_ship = Ship(my_screen, my_settings)

    # 初始化一个子弹队列，用于存放所有生成的子弹精灵
    bullets = Group()

    # 初始化一个外星人队列，用于存放所有外星人
    aliens = Group()

    # 向外星人队列中添加一行外星人
    create_fleet(my_settings, my_screen, aliens, my_ship)

    # 创建一个 启动游戏 的按钮
    play_button = Button(my_settings, my_screen, 'Play')

    # 游戏主循环，使得循环中的代码可以不断循环执行
    while True:
        # 事件检测，现在我们已经将事件循环的代码封装到函数中了，直接运行即可
        check_events(my_ship, my_screen, my_settings, bullets, play_button, my_gamestats, aliens, my_scoreboard)

        # 绘制游戏画面，包括屏幕背景、飞船，并将内容显示到游戏屏幕上
        update_screen(my_screen, my_settings, my_ship, bullets, aliens, my_gamestats, play_button, my_scoreboard)

        # 当游戏处于活跃状态时，才渲染屏幕元素
        if my_gamestats.game_active:

            # 每次执行完事件检测循环后，都更新飞船的位置
            my_ship.update()

            # 每次执行完事件检测循环后，都更新子弹的位置、并删除出界的子弹，检测子弹和外星人之间的碰撞
            update_bullet(bullets, my_settings, aliens, my_screen, my_ship, my_scoreboard, my_gamestats)

            # 每次执行完事件检测后，都更新外星人的位置，检测外星人和飞船之间的碰撞
            update_aliens(aliens, my_settings, my_ship, my_gamestats, bullets, my_screen, my_scoreboard)


# 运行游戏主逻辑
run_game()
