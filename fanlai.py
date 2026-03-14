#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍚 饭来张口 · 超轻量版
今天就能用的点单神器！
"""
import webbrowser
import time

def show_coupons():
    """显示今天可用的优惠券"""
    coupons = [
        {"platform": "支付宝", "desc": "满20减5元", "get": "支付宝搜「麦当劳」"},
        {"platform": "美团", "desc": "新用户满20减15元", "get": "美团外卖首页弹窗"},
        {"platform": "饿了么", "desc": "会员5元无门槛红包", "get": "饿了么会员中心"},
        {"platform": "麦当劳小程序", "desc": "1+1随心配13.9元", "get": "小程序首页直接点"},
        {"platform": "周一会员日", "desc": "0元香芋派", "get": "每周一自动到账"}
    ]
    
    print("🎁 今日可用优惠券：")
    for i, coupon in enumerate(coupons, 1):
        print(f"{i}. [{coupon['platform']}] {coupon['desc']} → {coupon['get']}")
    print("=" * 60)

def recommend_meals(budget: int = 20):
    """推荐套餐"""
    meals = [
        {"name": "丐版套餐", "price": 13.9, "desc": "1+1随心配：双层吉士堡 + 可乐", "platform": "麦当劳小程序", "url": "https://m.mcd.cn/"},
        {"name": "性价比套餐", "price": 19.9, "desc": "工作日午餐：汉堡 + 小薯条 + 小可乐", "platform": "麦当劳小程序", "url": "https://m.mcd.cn/"},
        {"name": "豪华套餐", "price": 29, "desc": "板烧鸡腿堡套餐：板烧 + 中薯 + 中可乐", "platform": "美团/饿了么", "url": "https://waimai.meituan.com/"},
        {"name": "全家桶", "price": 89, "desc": "5块炸鸡 + 3对鸡翅 + 2份薯条 + 3杯可乐", "platform": "美团/饿了么", "url": "https://waimai.meituan.com/"},
        {"name": "减脂套餐", "price": 25, "desc": "板烧鸡腿堡 + 蔬菜杯 + 零度可乐", "platform": "麦当劳小程序", "url": "https://m.mcd.cn/"}
    ]
    
    # 按预算筛选
    suitable = [m for m in meals if m["price"] <= budget]
    print(f"🍱 为你推荐¥{budget}以内的套餐：")
    for i, meal in enumerate(suitable, 1):
        print(f"{i}. {meal['name']} ¥{meal['price']}")
        print(f"   包含：{meal['desc']}")
        print(f"   平台：{meal['platform']}")
    
    print("=" * 60)
    return suitable

def main():
    print("🍚 欢迎使用「饭来张口」点单神器！")
    print("=" * 60)
    
    # 显示优惠券
    show_coupons()
    
    # 输入预算
    while True:
        try:
            budget = int(input("请输入你的预算（元）："))
            if budget <= 0:
                print("预算得大于0哦~")
                continue
            break
        except ValueError:
            print("请输入数字哦~")
    
    # 推荐套餐
    meals = recommend_meals(budget)
    
    # 选择套餐
    while True:
        try:
            choice = int(input("请选择你想吃的套餐（输入序号）：")) - 1
            if 0 <= choice < len(meals):
                selected = meals[choice]
                break
            print(f"请输入1到{len(meals)}之间的数字哦~")
        except ValueError:
            print("请输入数字哦~")
    
    # 跳转到点单页面
    print(f"✅ 你选择了：{selected['name']} ¥{selected['price']}")
    print("🔗 正在跳转到点单页面...")
    time.sleep(1)
    webbrowser.open(selected["url"])
    
    print("\n🎉 操作完成！领完券直接下单就行啦~")
    print("有啥想吃的随时喊我，我帮你找最划算的！😜")

if __name__ == "__main__":
    main()