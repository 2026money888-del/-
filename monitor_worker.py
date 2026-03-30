import os      # <--- 必须加上这一行！
import time
import requests
from tronpy import Tron

# 第 6 行修正：加上引号，并确保导入了 os
TOKEN = os.environ.get("BOT_TOKEN") 
API_URL = f"https://api.telegram.org{TOKEN}/sendMessage"

client = Tron() # 默认连接主网
tasks = {} # 格式: { "地址": {"last_tx": "ID", "chats": [id1, id2]} }

def check_and_notify():
    for addr, info in tasks.items():
        try:
            # 获取该地址最新一笔交易记录
            # 注意：实际生产建议使用 TronGrid API 获取更详细的转账/授权数据
            txs = client.get_address_transactions(addr, limit=1)
            if txs:
                current_tx = txs[0]['txID'] # 获取最新交易ID
                
                if info['last_tx'] is None:
                    tasks[addr]['last_tx'] = current_tx
                elif info['last_tx'] != current_tx:
                    # 发现新动向！发送提醒
                    for cid in info['chats']:
                        msg = f"⚠️ <b>监控地址动向提醒！</b>\n\n地址: <code>{addr}</code>\n交易ID: <code>{current_tx}</code>\n<a href='https://tronscan.org{current_tx}'>点击查看详情</a>"
                        requests.post(API_URL, json={"chat_id": cid, "text": msg, "parse_mode": "HTML"})
                    tasks[addr]['last_tx'] = current_tx
        except Exception as e:
            print(f"监控 {addr} 出错: {e}")

# 这里可以手动添加你想监控的测试地址
tasks["TSsyPmSkDBAbWrAcprseoEMDUyu7777777"] = {"last_tx": None, "chats": [你的ChatID]}

print("📡 副服务器监控程序已启动...")
while True:
    check_and_notify()
    time.sleep(10) # 每10秒轮询一次
