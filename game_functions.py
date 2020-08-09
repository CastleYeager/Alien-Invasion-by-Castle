"""
专门用于存放主模块中复杂的代码，将其封装成一个个函数来使用
"""
import pygame
# 事件循环中有退出游戏的功能，因此需要导入sys模块
import sys
# 导入子弹模块中的子弹类
from bullet import Bullet
# 从 alien 模块中导入 Alien 类
from alien import Alien
# 导入时间包中的 sleep 模块，用于在飞船被击中后暂停一瞬间
from time import sleep


# 封装事件循环中，所有 按下 键盘按键的事件
def check_keydown_events(event, ship, screen, settings, bullets):
    # 当玩家在键盘上按下的是 右方向键时，飞船开始向右移动
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # 当玩家在键盘上按下的是 左方向键时，飞船开始向左移动
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 当玩家在键盘上按下的是 空格键时，会生成一枚子弹
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, settings, screen, ship)
    # 当玩家在键盘上按下 Q 键时，退出游戏
    elif event.key == pygame.K_q:
        sys.exit()


# 封装事件循环中，所有 按下 键盘按键的事件
def check_keyup_events(event, ship):
    # 当玩家在键盘上松开的是 右方向键时，飞船停止向右移动
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # 当玩家在键盘上松开的是 左方向键时，飞船停止向左移动
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ship, screen, settings, bullets, play_button, game_stats, aliens, scoreboard):
    """
    事件检测循环，持续检测来自鼠标、键盘的请求，并作出相应的相应
    """
    # 循环监视事件的发生
    for event in pygame.event.get():
        # 当玩家点击关闭按钮时，退出游戏
        if event.type == pygame.QUIT:
            sys.exit()

        # 当玩家 按下键盘 发出事件时
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, screen, settings, bullets)

        # 当玩家 松开键盘 发出事件时
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        # 当玩家 点击鼠标 发出事件时
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 获取玩家鼠标点击的位置
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(mouse_x, mouse_y, play_button, game_stats, aliens, bullets, settings, screen, ship,
                              scoreboard)


# 玩家点击Play按钮后开始新游戏
def check_play_button(mouse_x, mouse_y, play_button, game_stats, aliens, bullets, settings, screen, ship, scoreboard):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 当玩家在游戏处于非活跃状态下点击Play按钮时
    if button_clicked and not game_stats.game_active:
        # 游戏难度初始化（重置）
        settings.initialize_dynamic_settings()
        # 游戏活跃时隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏设置
        game_stats.reset_stats()
        # 绘制重置后的游戏分数、最高分、等级
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()
        # 将游戏切换回活跃状态
        game_stats.game_active = True
        # 清空子弹和外星人
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并让飞船居中
        create_fleet(settings, screen, aliens, ship)
        ship.center_ship()


def update_screen(screen, setting, ship, bullets, aliens, game_stats, button, scoreboard):
    # 为纯黑的游戏屏幕填充上不一样的颜色
    screen.fill(setting.background_color)

    # 在背景之上绘制我们的飞船，注意这里的逻辑，必须是飞船在背景之后绘制，确保飞船在背景的上层
    ship.blitme()

    # 在屏幕和飞船之上，绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 在屏幕上绘制外星人
    aliens.draw(screen)

    # 绘制计分板
    scoreboard.show_scoreboard()

    # 如果游戏处于非活跃状态，那么就绘制按钮
    if not game_stats.game_active:
        button.draw_button()

    # 刷新屏幕，使得元素能够不断刷新位置
    pygame.display.flip()


def update_bullet(bullets, settings, aliens, screen, ship, scoreboard, stats):
    # 更新子弹队列中的所有子弹位置
    bullets.update(settings)

    # 如果子弹超出了屏幕范围，那么就删除这枚子弹
    for bullet in bullets.copy():  # 注意这里我们判断的是副本中的子弹，但是删除的是本体的子弹
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # 检测子弹和外星人之间的碰撞，并且在外星人被打完时创建一组新的外星人
    check_bullet_alien_collide(bullets, aliens, settings, screen, ship, scoreboard, stats)


def check_bullet_alien_collide(bullets, aliens, settings, screen, ship, scoreboard, stats):
    # 检测子弹队列中的每颗子弹是否击中外星人队列中的外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 每击落一只外星人，就加上相应的分数
    if collisions:
        # collisions是一个字典，其中每一个键值对分别是 子弹：子弹击中的外星人列表
        # 我们需要遍历每一个值，来判断击中了多少只外星人
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            # 重新绘制新的分数的图形
            scoreboard.prep_score()
        # 判断当前分数是否超过最高分
        check_high_score(stats, scoreboard)

    # 当外星人全都被打完时，删除现有子弹，并重新创建一群外星人
    if len(aliens) == 0:
        bullets.empty()
        # 玩家等级 +1
        stats.level += 1
        # 绘制等级图形
        scoreboard.prep_level()
        # 新一批外星人的速度提高
        settings.increase_speed()
        create_fleet(settings, screen, aliens, ship)


# 判断当前分数是否大于最高分的方法
def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


# 发射子弹的方法
def fire_bullet(bullets, settings, screen, ship):
    # 发射前检查当前子弹数是否超过最大限制的数量
    if len(bullets) < settings.max_bullets:
        # 只有当前子弹数小于限制数时，才会发射新子弹出来
        new_bullet = Bullet(screen, ship, settings)
        bullets.add(new_bullet)


# 创建一群外星人的方法
def create_fleet(settings, screen, aliens, ship):
    # 创建一只外星人，我们要通过这只外星人的数据来作一些处理
    alien = Alien(screen, settings)
    # 获取一行上外星人的数量
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    # 获取屏幕上总共需要多少行外星人
    number_rows = get_number_aliens_y(settings, alien.rect.height, ship.rect.height)
    for number_row in range(number_rows):
        # 创造一行外星人
        for alien_number in range(number_aliens_x):
            create_alien(screen, settings, aliens, alien_number, number_row)


# 求出一行上可以容纳多少只外星人
def get_number_aliens_x(settings, alien_width):
    # 首先要知道一行可以容纳多少只外星人
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


# 求出在屏幕上可以容纳多少行外星人
def get_number_aliens_y(settings, alien_height, ship_height):
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y


# 生成外星群中的每一个外星人
def create_alien(screen, settings, aliens, alien_number, number_row):
    alien = Alien(screen, settings)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x += alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * number_row
    aliens.add(alien)


# 更新外星人位置的方法
def update_aliens(aliens, settings, ship, game_stats, bullets, screen, scoreboard):
    # 外星人对屏幕边界的碰撞检测
    check_fleet_edges(aliens, settings)
    aliens.update()
    # 检测飞船和外星人之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # 飞船和外星人碰撞后的业务
        ship_hit(game_stats, aliens, bullets, settings, screen, ship, scoreboard)
    # 检测外星人和屏幕底端的碰撞
    check_alien_bottom(game_stats, aliens, bullets, settings, screen, ship, scoreboard)


# 检测外星人和屏幕底端的碰撞
def check_alien_bottom(game_stats, aliens, bullets, settings, screen, ship, scoreboard):
    screen_height = settings.screen_height
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_height:
            ship_hit(game_stats, aliens, bullets, settings, screen, ship, scoreboard)


# 飞船被撞到后的业务
def ship_hit(game_stats, aliens, bullets, settings, screen, ship, scoreboard):
    if game_stats.ship_left > 0:
        # 玩家可用的飞船数 -1
        game_stats.ship_left -= 1
        # 重新绘制玩家剩余飞船
        scoreboard.prep_ships()
        # 删除全部外星人 和 全部子弹
        aliens.empty()
        bullets.empty()
        # 重新生成一群外星人
        create_fleet(settings, screen, aliens, ship)
        # 将飞船重置到屏幕中间底部位置
        ship.center_ship()
        # 停止游戏 0.5秒，让玩家能意识到飞船被撞到了
        sleep(0.5)
    # 当玩家剩余飞船小于0时
    else:
        # 显示玩家的光标
        pygame.mouse.set_visible(True)
        # 将游戏设置为非活跃
        game_stats.game_active = False


# 判断外星人群是否碰到边界，如果碰到了，则改变移动方向
def check_fleet_edges(aliens, settings):
    for alien in aliens:
        if alien.check_edges():
            change_direction(aliens, settings)
            # 只要有一个外星人到达边界，就不用再判断后续的外星人了
            break


# 当外星人群触碰到边界时，向下移动外星人群并改变移动方向的方法
def change_direction(aliens, settings):
    for alien in aliens.sprites():
        alien.rect.y += settings.alien_drop_speed
    settings.fleet_direction *= -1
