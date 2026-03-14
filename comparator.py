#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍚 饭来张口 · 比价神器
今天就能用！自动比美团和饿了么哪个便宜
"""
import requests
import json
from typing import List, Dict

class PriceComparator:
    """比价引擎"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        }
    
    def search_meituan(self, keyword: str, address: str = "北京市朝阳区") -> List[Dict]:
        """搜索美团商家价格"""
        try:
            # 美团搜索接口（模拟移动端请求）
            url = "https://wmapi.meituan.com/api/v7/poi/search"
            params = {
                "keyword": keyword,
                "city_name": "北京",
                "address": address,
                "page_size": 5
            }
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            data = response.json()
            
            results = []
            if data.get("code") == 0:
                for poi in data.get("data", {}).get("pois", []):
                    results.append({
                        "platform": "美团",
                        "store_name": poi.get("name"),
                        "min_price": poi.get("min_price_tip", "0"),
                        "delivery_fee": poi.get("delivery_fee", "0"),
                        "delivery_time": poi.get("delivery_time", "30分钟"),
                        "score": poi.get("avg_score", "0")
                    })
            return results
        except Exception as e:
            print(f"美团查询失败：{e}")
            return []
    
    def search_eleme(self, keyword: str, address: str = "北京市朝阳区") -> List[Dict]:
        """搜索饿了么商家价格"""
        try:
            # 饿了么搜索接口
            url = "https://www.ele.me/restapi/shopping/v3/restaurants"
            params = {
                "keyword": keyword,
                "latitude": "39.9042",
                "longitude": "116.4074",
                "limit": 5
            }
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            data = response.json()
            
            results = []
            for item in data.get("items", []):
                restaurant = item.get("restaurant", {})
                results.append({
                    "platform": "饿了么",
                    "store_name": restaurant.get("name"),
                    "min_price": f"¥{restaurant.get('float_delivery_fee', 0)}起送",
                    "delivery_fee": f"¥{restaurant.get('float_delivery_fee', 0)}",
                    "delivery_time": f"{restaurant.get('order_lead_time', 30)}分钟",
                    "score": restaurant.get("rating", "0")
                })
            return results
        except Exception as e:
            print(f"饿了么查询失败：{e}")
            return []
    
    def compare(self, keyword: str, address: str = "北京市朝阳区") -> Dict:
        """比价并返回最优结果"""
        print(f"🔍 正在搜索「{keyword}」的价格...")
        print("=" * 70)
        
        meituan_results = self.search_meituan(keyword, address)
        eleme_results = self.search_eleme(keyword, address)
        
        all_results = meituan_results + eleme_results
        
        if not all_results:
            return {"status": "error", "msg": "没有找到相关商家"}
        
        # 显示所有结果
        print(f"📋 找到{len(all_results)}个商家：")
        for i, result in enumerate(all_results, 1):
            print(f"{i}. [{result['platform']}] {result['store_name']}")
            print(f"   评分：{result['score']} | 配送费：{result['delivery_fee']} | 预计送达：{result['delivery_time']}")
        
        # 找最便宜的（简单按配送费+起送价估算）
        def get_total_price(result):
            try:
                delivery = float(result['delivery_fee'].replace("¥", ""))
                min_order = float(result['min_price'].replace("¥", "").replace("起送", ""))
                return delivery + min_order
            except:
                return 999
        
        best = min(all_results, key=get_total_price)
        print("=" * 70)
        print(f"🏆 最优选择：[{best['platform']}] {best['store_name']}")
        print(f"   综合成本最低，推荐在{best['platform']}下单！")
        
        return {
            "status": "success",
            "best": best,
            "all": all_results
        }

if __name__ == "__main__":
    comparator = PriceComparator()
    food = input("你想吃什么？：")
    address = input("你的地址是？（默认北京朝阳区）：") or "北京市朝阳区"
    comparator.compare(food, address)