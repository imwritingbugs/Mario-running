#游戏入口
import pygame
from source import tool ,setup
from source.states import main_manu,load_screen, level ,shop
from source import constants as c
from source.components import loginWindow as lw

import pygame as pg

if __name__=='__main__':
    loginwindow = lw.LoginWindow()
    print('start here')
    game = tool.Control()
    state_dict = {c.MAIN_MENU: main_manu.Menu(),
                  c.LOAD_SCREEN: load_screen.LoadScreen(),
                  c.LEVEL: level.Level(),
                  c.SHOP: shop.Shop(),
                  c.GAME_OVER: load_screen.GameOver(),
                  c.WANNA_EXIT: load_screen.ifExit(),
                  c.TIME_OUT: load_screen.TimeOut(),
                  c.WIN: load_screen.Win()}
    game.setup_states(state_dict, c.MAIN_MENU) #不停把statedict丢进来 game类的state_dict就包含以上7个状态，每一次都要查找标题，然后把相应的函数放进来
    #比如这个初始状态 下标就等于c.MAIN_MENU，因此game.state=main_manu.Menu()
    #下一次如果状态变为 c.SHOP，那么game.state=shop.Shop() 就是这么简单的逻辑
    game.main()
    pg.quit()

