# -*- encoding=utf8 -*-
import re
import random

from airtest.core.api import *

auto_setup(__file__)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

def main():
    # 启动淘宝
    start_taobao()
    # 进去签到页
    enter_check_in_page()
    # 做任务赚元宝
    do_tasks()
    # 签到
    check_in()
    # 点击领取
    click_to_reap()
    # 验证
    verify()
    
def start_taobao():
    app = "com.taobao.taobao"
    stop_app(app)
    start_app(app)
    sleep(10)
    while poco(name="关闭按钮").exists():
        poco(name="关闭按钮").click()
    
def enter_check_in_page():
    poco(name="签到").click()
    sleep(10)
    while poco(text="关闭").exists():
        poco(text="关闭").click()
        
def check_in():
    if poco(text="立即签到").exists():
        poco(text="立即签到").click()
        
def do_tasks():
    poco(text="赚元宝").click()
    sleep(5)
    
    # 逛精选好货赚元宝
    browse_carefully_selected_good_pattern = r"逛精选好货赚元宝\((\d+)/(\d+)\)"
    while True:
        finished_total = poco(textMatches=browse_carefully_selected_good_pattern).get_text()
        match_groups = re.match(browse_carefully_selected_good_pattern, finished_total).groups()
        finished, total = int(match_groups[0]), int(match_groups[1])
        if finished == total:
            break
        poco(text='去逛逛')[0].click()
        total_time = 30
        max_sleep_time = 5
        while True:
            poco(text="红包签到浏览下单页").swipe("up")
            sleep_time = random.random() * max_sleep_time
            total_time -= sleep_time
            if total_time >= 0:
                sleep(sleep_time)
            else:
                break
        while poco(text="关闭").exists():
            poco(text="关闭").click()
        keyevent("KEYCODE_BACK")
        poco(text="赚元宝").click()
        
    # 逛0.99元专区赚元宝
    browse_carefully_selected_good_pattern = r"逛0.99元专区赚元宝\((\d+)/(\d+)\)"
    while True:
        finished_total = poco(textMatches=browse_carefully_selected_good_pattern).get_text()
        match_groups = re.match(browse_carefully_selected_good_pattern, finished_total).groups()
        finish, total = int(match_groups[0]), int(match_groups[1])
        if finish == total:
            break
        poco(text='去逛逛')[0].click()
        total_time = 10
        max_sleep_time = 5
        while True:
            poco(text="淘工厂特卖店").swipe("up")
            sleep_time = random.random() * max_sleep_time
            total_time -= sleep_time
            if total_time >= 0:
                sleep(sleep_time)
            else:
                break
        while poco(text="关闭").exists():
            poco(text="关闭").click()
        keyevent("KEYCODE_BACK")
        poco(text="赚元宝").click()
    
    poco(text="关闭").click()
    
def check_in():
    if poco(text="立即签到").exists():
        poco(text="立即签到").click()
    sleep(5)
    while poco(text="关闭").exists():
        poco(text="关闭").click()
        
def click_to_reap():
    sleep_time = [10, 30, 60, 150, 300, 600]
    n_click = 5
    for i in range(n_click):
        if poco(text="点击领取").exists():
            poco(text="点击领取").click()
        else:
            sleep(sleep_time[i])
            
def verify():
    assert_equal(poco(text="立即签到").exists(), False, "签到检查")
    poco(text="赚元宝").click()
    assert_equal(poco(text='去逛逛').exists(), False, "逛精选好物赚元宝、逛0.99元赚元宝检查")
    
main()