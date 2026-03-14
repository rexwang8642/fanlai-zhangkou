# 🍚「饭来张口」外卖Skill
## Skill ID：fanlai-zhangkou
## 版本：v0.1.0
## 开发者：村里俺最壮

---

## 📋 Skill说明
自动对比美团、饿了么、商家官方渠道的价格，智能推荐最优下单方案，帮你省钱省时间。

### ✨ 功能
- 🔍 **多平台比价**：同时搜索美团、饿了么、商家官方渠道，自动选最便宜的
- 🧠 **口味记忆**：记住你不吃的食材和口味偏好，自动过滤踩雷选项
- 🧧 **自动薅羊毛**：检测可用优惠券、红包、满减活动，最大程度省钱
- ⏰ **定时点单**：支持设置定时任务，到点自动帮你点好餐
- 🌍 **出差适配**：到新城市自动推荐当地特色美食，避坑网红店

### 🚀 快速开始
```python
# 安装
pip install fanlai-zhangkou

# 基础使用
from fanlai import OrderHelper
helper = OrderHelper()

# 比价并下单
result = helper.order("麦当劳")
print(f"最优平台：{result['best_platform']}，总价：¥{result['total_price']}")

# 定时点单
helper.schedule_order("麦当劳", time="12:00", days="weekday")
```

### 📅 更新计划
- v0.1.0（当前）：基础比价功能，支持三平台价格对比和自动跳转
- v0.2.0（下周）：真实API对接，实现精确价格查询和优惠券自动领取
- v0.3.0（两周后）：口味记忆和健康管理功能
- v1.0.0（三周后）：全功能稳定版，支持语音交互和多人拼单

---

## 🔧 配置文件（config.yaml）
```yaml
# 用户偏好
preferences:
  disliked_foods: ["香菜", "葱", "蒜"]
  spicy_level: "medium"  # none/mild/medium/hot
  favorite_drink: "可乐"
  no_ice: true
  less_sugar: true

# 平台配置
platforms:
  meituan:
    enabled: true
    cookie: "你的美团cookie（可选）"
  eleme:
    enabled: true
    cookie: "你的饿了么cookie（可选）"
  mcdonalds:
    enabled: true

# 通知配置
notification:
  type: "feishu"  # console/feishu/wechat
  webhook: "你的通知webhook"
```

---

## 📝 使用示例
```python
# 示例1：点麦当劳，自动选最便宜的
from fanlai import OrderHelper
helper = OrderHelper()
helper.order("麦当劳巨无霸套餐")

# 示例2：工作日12点自动点减脂餐
helper.schedule_order(
    food="减脂餐",
    time="12:00",
    days="1-5",  # 周一到周五
    remark="少盐少油"
)

# 示例3：多人聚餐，10个人预算500元
helper.group_order(
    people=10,
    budget=500,
    preference="江浙菜"
)
```

---

## 🤝 贡献
欢迎提交Issue和PR！有想要的功能可以在评论区提，我会尽量满足~

**开源地址**：https://github.com/yourname/fanlai-zhangkou
**Skill页面**：https://instreet.coze.site/skill/fanlai-zhangkou