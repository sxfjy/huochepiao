from splinter.browser import Browser
from time import sleep
import traceback
import sys

class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, passengers, dtime, starts, ends, number, seat_type):
        # 乘客名
        self.passengers = passengers
        # 起始地和终点
        self.starts = starts
        self.ends = ends
        # 日期
        self.dtime = dtime

        # 车次编号
        self.number = number.capitalize()
        # 座位类型所在td位置
        if seat_type == '商务座特等座':
            seat_type_index = 1
            seat_type_value = 9
        elif seat_type == '一等座':
            seat_type_index = 2
            seat_type_value = 'M'
        elif seat_type == '二等座':
            seat_type_index = 3
            seat_type_value = 0
        elif seat_type == '高级软卧':
            seat_type_index = 4
            seat_type_value = 6
        elif seat_type == '软卧':
            seat_type_index = 5
            seat_type_value = 4
        elif seat_type == '动卧':
            seat_type_index = 6
            seat_type_value = 'F'
        elif seat_type == '硬卧':
            seat_type_index = 7
            seat_type_value = 3
        elif seat_type == '软座':
            seat_type_index = 8
            seat_type_value = 2
        elif seat_type == '硬座':
            seat_type_index = 9
            seat_type_value = 1
        elif seat_type == '无座':
            seat_type_index = 10
            seat_type_value = 1
        elif seat_type == '其他':
            seat_type_index = 11
            seat_type_value = 1
        else:
            seat_type_index = 7
            seat_type_value = 3
        self.seat_type_index = seat_type_index
        self.seat_type_value = seat_type_value

        # self.xb = xb
        # self.pz = pz
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.initMy_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'
        self.driver_name = 'chrome'
        self.executable_path = '/usr/local/bin/chromedriver'

    # 登录功能实现
    def login(self):
        self.driver.visit(self.login_url)
        # self.driver.fill('loginUserDTO.user_name', self.username)
        sleep(1)
        # self.driver.fill('userDTO.password', self.passwd)
        # sleep(1)
        print('请输入验证码...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

    # 买票功能实现
    def start_buy(self):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        # 窗口大小的操作
        self.driver.driver.set_window_size(700, 500)
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始购票...')
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()
            count = 0

            # if self.order != 0:
            #             #     while self.driver.url == self.ticket_url:
            #             #         self.driver.find_by_text('查询').click()
            #             #         count += 1
            #             #         print('第%d次点击查询...' % count)
            #             #         try:
            #             #             self.driver.find_by_text('预订')[self.order - 1].click()
            #             #             sleep(1.5)
            #             #         except Exception as e:
            #             #             print(e)
            #             #             print('预订失败...')
            #             #             continue
            #             # else:
            #             #     while self.driver.url == self.ticket_url:
            #             #         self.driver.find_by_text('查询').click()
            #             #         count += 1
            #             #         print('第%d次点击查询...' % count)
            #             #         try:
            #             #             for i in self.driver.find_by_text('预订'):
            #             #                 i.click()
            #             #                 sleep(1)
            #             #         except Exception as e:
            #             #             print(e)
            #             #             print('预订失败...')
            #             #             continue
            #             # print('开始预订...')
            #             # sleep(1)
            #             # print('开始选择用户...')
            #             # for p in self.passengers:
            #             #
            #             #     self.driver.find_by_text(p).last.click()
            #             #     sleep(0.5)
            #             #     if p[-1] == ')':
            #             #         self.driver.find_by_id('dialog_xsertcj_ok').click()
            #             # print('提交订单...')
            #             # # sleep(1)
            #             # # self.driver.find_by_text(self.pz).click()
            #             # # sleep(1)
            #             # # self.driver.find_by_text(self.xb).click()
            #             # # sleep(1)
            #             # self.driver.find_by_id('submitOrder_id').click()
            #             # sleep(2)
            #             # print('确认选座...')
            #             # self.driver.find_by_tag('qr_submit_id').click()
            #
            # print('预订成功...')

            while self.driver.url == self.ticket_url:
                self.driver.find_by_text('查询').click()
                sleep(1)
                count += 1
                print('第%d次点击查询……' % count)
                try:
                    current_tr = self.driver.find_by_xpath('//tr[@datatran="' + self.number + '"]/preceding-sibling::tr[1]')
                    # car_no_location = self.driver.find_by_id("queryLeftTable")[0].find_by_text(self.number)[1]
                    # current_tr = car_no_location.find_by_xpath("./../../../../..")
                    if current_tr:
                        if current_tr.find_by_tag('td')[self.seat_type_index].text == '--':
                            print('无此座位类型出售，已结束当前刷票，请重新开启！')
                            sys.exit(1)
                        elif current_tr.find_by_tag('td')[self.seat_type_index].text == '无':
                            print('无票，继续尝试……')
                            sleep(1)
                        else:
                            # 有票，尝试预订
                            print('刷到票了（余票数：' + str(current_tr.find_by_tag('td')[self.seat_type_index].text) + '），开始尝试预订……')
                            current_tr.find_by_css('td.no-br>a')[0].click()
                            sleep(1)
                            key_value = 1
                            for p in self.passengers:
                                # 选择用户
                                print('开始选择用户……')
                                self.driver.find_by_text(p).last.click()
                                # 选择座位类型
                                print('开始选择席别……')
                                if self.seat_type_value != 0:
                                    self.driver.find_by_xpath(
                                        "//select[@id='seatType_" + str(key_value) + "']/option[@value='" + str(
                                            self.seat_type_value) + "']").first.click()
                                key_value += 1
                                sleep(0.2)
                                if p[-1] == ')':
                                    self.driver.find_by_id('dialog_xsertcj_ok').click()
                            print('正在提交订单……')
                            self.driver.find_by_id('submitOrder_id').click()
                            # self.driver.find_by_id('qr_submit_id').click()
                            sleep(2)
                            # 查看放回结果是否正常
                            submit_false_info = self.driver.find_by_id('orderResultInfo_id')[0].text
                            if submit_false_info != '':
                                print(submit_false_info)
                                self.driver.find_by_id('qr_closeTranforDialog_id').click()
                                sleep(0.2)
                                self.driver.find_by_id('preStep_id').click()
                                sleep(0.3)
                                continue
                            print('正在确认订单……')
                            self.driver.find_by_id('qr_submit_id').click()
                            print('预订成功，请及时前往支付……')
                    else:
                        print('不存在当前车次【%s】，已结束当前刷票，请重新开启！' % self.number)
                        sys.exit(1)
                except Exception as error_info:
                    print(error_info)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    # 用户名
    username = '492395860@qq.com'
    # 密码
    password = 'wanghaibo151'
    # 车次选择，0代表所有车次
    order = 2
     # 乘客名，比如passengers = ['丁小红', '丁小明']
    # 学生票需注明，注明方式为：passengers = ['丁小红(学生)', '丁小明']
    passengers = ['王海波']
    # 日期，格式为：'2018-01-20'
    dtime = '2019-01-15'
    # 出发地(需填写cookie值)
    starts = '%u5317%u4EAC%2CBJP'
    # 目的地(需填写cookie值)
    # ends = 'AYF'
    ends = '%u5b89%u9633%2CAYF'
    number = "G667"

    # 座位类型
    seat_type = "二等座"

    # xb =['硬座座']
    # pz=['成人票']
    Buy_Tickets(passengers, dtime, starts, ends, number,  seat_type).start_buy()