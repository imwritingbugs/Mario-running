import pygame as pg
from .. import setup, tool
from .. import constants as c
from ..components import info
from ..components import mydatabase as db
from ..components import dataBaseGlobalData as GD
'''
#商店的内容
#除了在components.info中的背景设置(包括金币，游戏各类数据)，还需要表层的商品设计(读取图片+标题)
'''
class Shop(tool.State):
    def __init__(self):
        tool.State.__init__(self) #完成父类的初始化
        self.canUse=0
        self.lastKeyEvent=pg.key.get_pressed()
    def startup(self,current_time, persist):
        self.next = c.SHOP #shop商店界面的下一级默认还是shop
        self.persist = persist
        self.game_info = persist
        self.overhead_info = info.Info(self.game_info, c.SHOP,self.persist) #制作顶部信息 以及所有文字显示区域的信息
        self.setup_cursor()#设置游标
        self.setup_background()
        self.setup_goods()
        db.updateShopInfo(GD.userid)


    def setup_goods(self):
        #货架实际453*279
        #货架盈余总宽度453-408=47
        #货架盈余总高度
        #s商品y1 y2 货架底部y=100+279=379  下瓶底留6空 下瓶y=379-6-128=145 上瓶y=55=379/2-6-128
        # 商品x1 x2 空间三等分 空56 x1=56 x2=453-105-56=292
        #更改，瓶子大小变为原来的3/4，放在一排
        image = tool.get_image(setup.GFX['shop_items'], 0, 0, 42, 51,colorkey=(0,0,0),
                                scale= c.SIZE_MULTIPLIER*0.7) #实际一件商品84*102
        rect = image.get_rect()
        rect.x, rect.y = (170+9+30, 100+35)
        self.image_dict['shop_item1'] = (image, rect)

        image = tool.get_image(setup.GFX['shop_items'], 42, 0, 42, 51,colorkey=(0,0,0),
                                scale= c.SIZE_MULTIPLIER*0.7) #实际一件商品84*102
        rect = image.get_rect()
        rect.x, rect.y = (170+60+42+30, 100+35)
        self.image_dict['shop_item2'] = (image, rect)

        image = tool.get_image(setup.GFX['shop_items'], 84, 0, 42, 51,colorkey=(0,0,0),
                                scale= c.SIZE_MULTIPLIER*0.7) #实际一件商品84*102
        rect = image.get_rect()
        rect.x, rect.y = (170+111+84+30, 100+35)
        self.image_dict['shop_item3'] = (image, rect)

        image = tool.get_image(setup.GFX['shop_items'], 126, 0, 42, 50,colorkey=(0,0,0),
                                scale= c.SIZE_MULTIPLIER*0.7) #实际一件商品84*102
        rect = image.get_rect()
        rect.x, rect.y = (170+162+126+30, 100+35)
        self.image_dict['shop_item4'] = (image, rect)

        image = tool.get_image(setup.GFX['mario_bros'], 178, 32, 12, 16,c.BLACK,
                                scale= c.SIZE_MULTIPLIER*1.5) #实际一件商品84*102
        rect = image.get_rect()
        rect.x, rect.y = (170+9+40, 100+35+140)
        self.image_dict[c.PLAYER_MARIO] = (image, rect)

        image = tool.get_image(setup.GFX['mario_bros'], 178, 128, 12, 16,c.BLACK,
                                scale= c.SIZE_MULTIPLIER*1.5) #实际一件商品84*102
        rect = image.get_rect()
        rect.x, rect.y = (170+9+115, 100+35+140)
        self.image_dict[c.PLAYER_LUIGI] = (image, rect)



    def setup_background(self):
        if self.persist[c.LEVEL_NUM]==1:
            self.background = setup.GFX['level_1']
        elif self.persist[c.LEVEL_NUM]==2:
            self.background = setup.GFX['level_2']
        elif self.persist[c.LEVEL_NUM]==3:
            self.background = setup.GFX['level_3']
        elif self.persist[c.LEVEL_NUM]==4:
            self.background = setup.GFX['level_4']
        self.background_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                    (int(self.background_rect.width*c.BACKGROUND_MULTIPLER),
                                    int(self.background_rect.height*c.BACKGROUND_MULTIPLER)))
        #设置了背景（第一关的蓝天白云，如果后期切换关卡，应该切换到相应的关卡）
        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)
        self.image_dict = {}
        image = tool.get_image(setup.GFX['shop_shelf2'], 0, 0, 151, 93,colorkey=(255,0,255),
                            scale= c.SIZE_MULTIPLIER*c.SIZE_MULTIPLIER_SHELF)#实际453*279
        rect = image.get_rect()
        rect.x, rect.y = (173, 100)#货架下边沿379 留有221
        self.image_dict['shop_shelf2'] = (image, rect)



    def setup_cursor(self):
        self.cursor = pg.sprite.Sprite()
        self.cursor.image = tool.get_image(setup.GFX[c.ITEM_SHEET], 24, 160, 8, 8, c.BLACK, 3)
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = (170, 110) #初始指向Life
        self.cursor.rect = rect
        self.cursor.state = c.LIFE

    def update(self, surface, keys, current_time):

        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        temp=pg.key.get_pressed()
        if self.lastKeyEvent!=temp:
            self.lastKeyEvent=temp
            self.canUse=1
        if self.canUse:
            self.update_cursor(keys)
        self.overhead_info = info.Info(self.game_info, c.SHOP,self.persist)
        self.overhead_info.update(self.game_info)

        surface.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.image_dict['shop_shelf2'][0],
                     self.image_dict['shop_shelf2'][1])
        surface.blit(self.image_dict['shop_item1'][0],
                     self.image_dict['shop_item1'][1])
        surface.blit(self.image_dict['shop_item2'][0],
                     self.image_dict['shop_item2'][1])
        surface.blit(self.image_dict['shop_item3'][0],
                     self.image_dict['shop_item3'][1])
        surface.blit(self.image_dict['shop_item4'][0],
                     self.image_dict['shop_item4'][1])
        surface.blit(self.image_dict[c.PLAYER_MARIO][0],
                     self.image_dict[c.PLAYER_MARIO][1])
        surface.blit(self.image_dict[c.PLAYER_LUIGI][0],
                     self.image_dict[c.PLAYER_LUIGI][1])
        surface.blit(self.cursor.image, self.cursor.rect)
        #self.overhead_info.draw(surface)
        self.overhead_info.draw(surface)
    '''
    注意啦！这里由于之需要检测键盘按下来的一次动作，当键盘动作与之前没有改变的时候，cursor的值是不需要切换的，因此需要设置一个记录ifUsed,记录当前的键盘信息已经被使用过了，
    每一次按键状态变更的时候ifUsed置1，每一次进入update首先观察指标是否为1，若不为1，需要
    '''
    def update_cursor(self, keys):

        if self.cursor.state == c.LIFE:
            self.cursor.rect.x=170
            self.cursor.rect.y=100
            #self.cursor.state=()
            if keys[pg.K_UP]:
                self.cursor.state = c.UNLOCK
                self.cursor.rect.x = 80
                self.cursor.rect.y = 405
                self.canUse=0
            elif keys[pg.K_DOWN]:
                self.cursor.state = c.PLAYER_MARIO
                self.cursor.rect.x = 235
                self.cursor.rect.y = 315
                self.canUse=0
            elif keys[pg.K_LEFT]:
                self.cursor.state = c.WEAPON
                self.cursor.rect.x = 452
                self.cursor.rect.y = 215
                self.canUse=0
            elif keys[pg.K_RIGHT]:
                self.cursor.state = c.FASTER
                self.cursor.rect.x = 262
                self.cursor.rect.y = 215
                self.canUse=0
            elif keys[pg.K_b]:
                print("buylife")
                if db.buyThings(c.LIFEPRICE, c.LIFEID):
                    self.game_info[c.COIN_TOTAL] -= c.LIFEPRICE
                print(GD.shopinfo)
                self.canUse = 0

        elif self.cursor.state == c.FASTER:
            self.cursor.rect.x = 262
            self.cursor.rect.y = 215
            if keys[pg.K_UP]:
                self.cursor.state = c.UNLOCK
                self.cursor.rect.x = 80
                self.cursor.rect.y = 405
                self.canUse=0
            elif keys[pg.K_DOWN]:
                self.canUse=0
                self.cursor.state = c.PLAYER_MARIO
                self.cursor.rect.x = 235
                self.cursor.rect.y = 315
            elif keys[pg.K_LEFT]:
                self.canUse=0
                self.cursor.state = c.LIFE
                self.cursor.rect.x = 170
                self.cursor.rect.y = 100
            elif keys[pg.K_RIGHT]:
                self.canUse=0
                self.cursor.state = c.POWERUP
                self.cursor.rect.x = 355
                self.cursor.rect.y = 110
            elif keys[pg.K_b]:
                print("buyspeed")
                if db.buyThings(c.SPEEDPRICE, c.SPEEDID):
                    self.game_info[c.COIN_TOTAL] -= c.SPEEDPRICE
                print(GD.shopinfo)
                self.canUse = 0

        elif self.cursor.state == c.POWERUP:
            self.cursor.rect.x = 355
            self.cursor.rect.y = 110
            if keys[pg.K_UP]:
                self.canUse=0
                self.cursor.state = c.UNLOCK
                self.cursor.rect.x = 80
                self.cursor.rect.y = 405
            elif keys[pg.K_DOWN]:
                self.canUse=0
                self.cursor.state = c.PLAYER_MARIO
                self.cursor.rect.x = 235
                self.cursor.rect.y = 315
            elif keys[pg.K_LEFT]:
                self.canUse=0
                self.cursor.state = c.FASTER
                self.cursor.rect.x = 262
                self.cursor.rect.y = 215
            elif keys[pg.K_RIGHT]:
                self.canUse=0
                self.cursor.state = c.WEAPON
                self.cursor.rect.x = 452
                self.cursor.rect.y = 215
            elif keys[pg.K_b]:
                print("buyjump")
                if db.buyThings(c.JUMPPRICE, c.JUMPID):
                    self.game_info[c.COIN_TOTAL] -= c.JUMPPRICE
                print(GD.shopinfo)
                self.canUse = 0

        elif self.cursor.state == c.WEAPON:
            self.cursor.rect.x = 452
            self.cursor.rect.y = 215
            if keys[pg.K_UP]:
                self.canUse=0
                keys[pg.K_UP]=0
                self.cursor.state = c.UNLOCK
                self.cursor.rect.x = 80
                self.cursor.rect.y = 405
            elif keys[pg.K_DOWN]:
                self.canUse=0
                self.cursor.state = c.PLAYER_MARIO
                self.cursor.rect.x = 235
                self.cursor.rect.y = 315
            elif keys[pg.K_LEFT]:
                self.canUse=0
                self.cursor.state=c.POWERUP
                self.cursor.rect.x=355
                self.cursor.rect.y=110
            elif keys[pg.K_RIGHT]:
                self.canUse=0
                self.cursor.state=c.LIFE
                self.cursor.rect.x=170
                self.cursor.rect.y=100
            elif keys[pg.K_b]:
                print("buyweapom")
                if db.buyThings(c.WEAPONPRICE, c.WEAPONID):
                    self.game_info[c.COIN_TOTAL] -= c.WEAPONPRICE
                print(GD.shopinfo)
                self.canUse = 0

        elif self.cursor.state == c.PLAYER_MARIO:
            self.cursor.rect.x = 240
            self.cursor.rect.y = 315
            if keys[pg.K_DOWN]:
                self.canUse=0
                self.cursor.state = c.UNLOCK
                self.cursor.rect.x = 80
                self.cursor.rect.y = 405
            elif keys[pg.K_UP]:
                self.canUse=0
                self.cursor.state=c.LIFE
                self.cursor.rect.x=170
                self.cursor.rect.y=100
            elif keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
                self.canUse=0
                self.cursor.state = c.PLAYER_LUIGI
                self.persist[c.PLAYER_NAME]=c.PLAYER_LUIGI
                self.player_index = 1
                self.game_info[c.PLAYER_NAME] = c.PLAYER_LUIGI
                self.cursor.rect.x = 289
                self.cursor.rect.y = 315
            elif keys[pg.K_b]:
                print("buymario")
                db.buyThings(0, 0)
                self.canUse = 0

        elif self.cursor.state == c.PLAYER_LUIGI:
            self.cursor.rect.x = 289
            self.cursor.rect.y = 315
            if keys[pg.K_DOWN]:
                self.canUse=0
                self.cursor.state = c.UNLOCK
                self.cursor.rect.x = 80
                self.cursor.rect.y = 405
            elif keys[pg.K_UP]:
                self.canUse=0
                self.cursor.state=c.LIFE
                self.cursor.rect.x=170
                self.cursor.rect.y=100
            elif keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
                self.canUse=0
                self.cursor.state = c.PLAYER_MARIO
                self.persist[c.PLAYER_NAME]=c.PLAYER_MARIO
                self.player_index = 0
                self.game_info[c.PLAYER_NAME] = c.PLAYER_MARIO
                self.cursor.rect.x = 235
                self.cursor.rect.y = 315
            elif keys[pg.K_b]:
                print("buyluigi")
                #如果已经购买，数据为1，此时无法再次购买。如果未购买，数据为0，即可购买
                if db.buyThings(c.SKINPRICE * ((1- GD.shopinfo[c.SKINID])), c.SKINID):
                    self.game_info[c.COIN_TOTAL] -= c.SKINPRICE
                print(GD.shopinfo)
                self.canUse = 0
            elif keys[pg.K_RETURN]:
                self.canUse = 0
                self.next = c.MAIN_MENU
                self.persist[c.STARTUP] = 0
                self.done = True

        elif self.cursor.state == c.UNLOCK:
            self.cursor.rect.x = 80
            self.cursor.rect.y = 405
            if keys[pg.K_UP]:
                self.canUse=0
                self.cursor.state = c.PLAYER_MARIO
                self.cursor.rect.x = 235
                self.cursor.rect.y = 315
            elif keys[pg.K_DOWN]:
                self.canUse=0
                self.cursor.state=c.LIFE
                self.cursor.rect.x=170
                self.cursor.rect.y=100
            elif keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
                self.canUse=0
                self.cursor.state = c.MAIN_MENU
                self.cursor.rect.x = 525
                self.cursor.rect.y =405
            elif keys[pg.K_b]:
                self.canUse=0
                self.maxlevel = GD.shopinfo[c.LEVELID]
                self.nowlevel = self.persist[c.LEVEL_NUM]
                if self.nowlevel <= self.maxlevel:
                    db.buyThings(0, 0)
                else :
                    if db.buyThings(c.LEVELPRICE * ((self.nowlevel - self.maxlevel)), c.LEVELID):
                        self.game_info[c.COIN_TOTAL] -= c.LEVELPRICE*((self.nowlevel - self.maxlevel))
                    print(GD.shopinfo)
                    self.canUse = 0
            elif keys[pg.K_RETURN]:
                self.canUse=0
                if self.persist[c.MAX_LEVEL]==4:
                    self.persist[c.MAX_LEVEL]=4
                else:
                    self.persist[c.MAX_LEVEL] += 1
                    #self.persist[c.COIN_TOTAL]-=(self.persist[c.MAX_LEVEL]*50)
                if  self.persist[c.LEVEL_NUM]==4:
                    self.persist[c.LEVEL_NUM]=1
                else:
                    self.persist[c.LEVEL_NUM] += 1
                    #self.persist[c.COIN_TOTAL]-=(self.persist[c.MAX_LEVEL]*50)
                #self.persist[c.LEVEL_NUM]=self.persist[c.MAX_LEVEL]

        elif self.cursor.state == c.MAIN_MENU:
            self.cursor.rect.x = 525
            self.cursor.rect.y =405
            if keys[pg.K_UP]:
                self.canUse=0
                self.cursor.state = c.PLAYER_MARIO
                self.cursor.rect.x = 235
                self.cursor.rect.y = 315
            elif keys[pg.K_DOWN]:
                self.canUse=0
                self.cursor.state=c.LIFE
                self.cursor.rect.x=170
                self.cursor.rect.y=100
            elif keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
                self.canUse=0
                self.cursor.state = c.UNLOCK
                self.cursor.rect.x = 80
                self.cursor.rect.y = 399
            elif keys[pg.K_RETURN]:
                self.canUse=0
                #此处需要连接数据库判断金币是否足够
                #设计买官的价格（比如关卡数*50）
                self.next=c.MAIN_MENU
                self.persist[c.STARTUP]=0
                self.done = True
                #self.game_info[c.PLAYER
                # _NAME] = c.PLAYER_MARIO
        #         self.player_index = 0
        #         self.game_info[c.PLAYER_NAME] = c.PLAYER_MARIO
        # if keys[pg.K_RETURN]:
        #     self.reset_game_info()
        #     self.done = True


