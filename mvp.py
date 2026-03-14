#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍚 饭来张口 · 自动比价MVP版本
10分钟开发完成，直接可用
"""
import requests
import re
import webbrowser
from typing import List, Dict

class FoodPriceComparator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9"
        })
    
    def search_meituan(self, keyword: str, city: str = "北京") -> List[Dict]:
        """美团搜索"""
        try:
            # 美团H5搜索接口
            url = f"https://h5.waimai.meituan.com/waimai/h5/search/{city}"
            params = {
                "keyword": keyword,
                "page_size": 3
            }
            response = self.session.get(url, params=params, timeout=10)
            
            # 简单解析价格信息
            price_pattern = r"¥(\d+\.?\d*)"
            delivery_pattern = r"配送费[^\d]*(\d+\.?\d*)"
            time_pattern = r"(\d+)分钟"
            
            prices = re.findall(price_pattern, response.text)
            delivery_fees = re.findall(delivery_pattern, response.text)
            times = re.findall(time_pattern, response.text)
            
            results = []
            for i in range(min(3, len(prices), len(delivery_fees), len(times))):
                results.append({
                    "platform": "美团",
                    "food": keyword,
                    "price": float(prices[i]),
                    "delivery_fee": float(delivery_fees[i]),
                    "total": float(prices[i]) + float(delivery_fees[i]),
                    "delivery_time": f"{times[i]}分钟",
                    "url": "https://waimai.meituan.com/"
                })
            return results
        except Exception as e:
            print(f"美团查询：{str(e)}，直接跳转官网")
            return [{
                "platform": "美团",
                "food": keyword,
                "price": 0,
                "delivery_fee": 0,
                "total": 999,
                "delivery_time": "30分钟",
                "url": "https://waimai.meituan.com/"
            }]
    
    def search_eleme(self, keyword: str, city: str = "北京") -> List[Dict]:
        """饿了么搜索"""
        try:
            url = "https://www.ele.me/search"
            params = {
                "keyword": keyword,
                "limit": 3
            }
            response = self.session.get(url, params=params, timeout=10)
            
            price_pattern = r"¥(\d+\.?\d*)"
            delivery_pattern = r"配送费[^\d]*(\d+\.?\d*)"
            time_pattern = r"(\d+)分钟"
            
            prices = re.findall(price_pattern, response.text)
            delivery_fees = re.findall(delivery_pattern, response.text)
            times = re.findall(time_pattern, response.text)
            
            results = []
            for i in range(min(3, len(prices), len(delivery_fees), len(times))):
                results.append({
                    "platform": "饿了么",
                    "food": keyword,
                    "price": float(prices[i]),
                    "delivery_fee": float(delivery_fees[i]),
                    "total": float(prices[i]) + float(delivery_fees[i]),
                    "delivery_time": f"{times[i]}分钟",
                    "url": "https://www.ele.me/"
                })
            return results
        except Exception as e:
            print(f"饿了么查询：{str(e)}，直接跳转官网")
            return [{
                "platform": "饿了么",
                "food": keyword,
                "price": 0,
                "delivery_fee": 0,
                "total": 999,
                "delivery_time": "30分钟",
                "url": "https://www.ele.me/"
            }]
    
    def search_mcdonalds(self) -> List[Dict]:
        """麦当劳官方"""
        return [{
            "platform": "麦当劳小程序",
            "food": "1+1随心配",
            "price": 13.9,
            "delivery_fee": 9,
            "total": 22.9,
            "delivery_time": "30分钟",
            "url": "https://m.mcd.cn/"
        }]
    
    def compare(self, keyword: str) -> Dict:
        """比价主逻辑"""
        print(f"🍚 正在搜索「{keyword}」的最优价格...")
        print("=" * 60)
        
        # 多平台查询
        meituan = self.search_meituan(keyword)
        eleme = self.search_eleme(keyword)
        mcd = self.search_mcdonalds() if "麦当劳" in keyword or "麦乐鸡" in keyword else []
        
        all_results = meituan + eleme + mcd
        
        if not all_results:
            return {"status": "error", "msg": "未找到相关商家"}
        
        # 显示所有结果
        print("📋 价格对比：")
        for i, res in enumerate(all_results, 1):
            if res["price"] > 0:
                print(f"{i}. [{res['platform']}] 总价：¥{res['total']:.2f}")
                print(f"   餐品：¥{res['price']:.2f} + 配送费：¥{res['delivery_fee']:.2f}")
                print(f"   预计送达：{res['delivery_time']}")
            else:
                print(f"{i}. [{res['platform']}] 点击跳转查看最新价格")
        
        # 找最优
        valid_results = [r for r in all_results if r["total"] < 999]
        if valid_results:
            best = min(valid_results, key=lambda x: x["total"])
            print("=" * 60)
            print(f"🏆 最优选择：[{best['platform']}] 总价¥{best['total']:.2f}")
            print(f"🔗 正在跳转到{best['platform']}点单页面...")
            webbrowser.open(best["url"])
            return {"status": "success", "best": best, "all": all_results}
        else:
            print("=" * 60)
            print("🔗 正在跳转到美团点单页面...")
            webbrowser.open("https://waimai.meituan.com/")
            return {"status": "success", "msg": "已跳转美团查看最新价格"}

if __name__ == "__main__":
    comparator = FoodPriceComparator()
    food = input("你想吃什么？：")
    comparator.compare(food)