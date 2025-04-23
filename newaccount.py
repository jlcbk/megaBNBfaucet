import sqlite3
import subprocess
import json
from eth_account import Account
import secrets

def generate_evm_address():
    priv = secrets.token_hex(32)
    acct = Account.from_key(priv)
    return acct.address, priv

def save_to_db(address, private_key):
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO wallets (address, private_key) VALUES (?, ?)", 
                 (address, private_key))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def claim_airdrop(address):
    try:
        result = subprocess.run(
            ['node', '-e', 
             f"const {{ claimAirdrop }} = require('/Users/fomostorm/Documents/megaBNBfaucet/@getMegaBNB.js'); \n              claimAirdrop('{address}').then(console.log);"],
            capture_output=True,
            text=True,
            check=True  # 添加check参数捕获子进程错误
        )
        print("Node输出:", result.stderr)  # 打印错误输出
    
        try:
            # 处理JavaScript模块可能返回的不同格式
            if isinstance(result.stdout, str):
                return json.loads(result.stdout)
            else:
                return result.stdout
        except Exception as e:
            print(f"JSON解析错误: {e}")
            return {"success": False, "message": "调用失败"}
    except subprocess.CalledProcessError as e:
        return {"success": False, "message": f"Node进程错误: {e.stderr}"}

def main():
    while True:  # 添加无限循环
        address, private_key = generate_evm_address()
        if save_to_db(address, private_key):
            print(f"新地址生成成功: {address}")
            result = claim_airdrop(address)
            print(result['message'])
            
            if result['success']:
                conn = sqlite3.connect('wallets.db')
                c = conn.cursor()
                c.execute("UPDATE wallets SET claimed = 1 WHERE address = ?", (address,))
                conn.commit()
                conn.close()
        else:
            print("地址已存在，跳过处理")
        
        # 等待1秒
        time.sleep(1)

if __name__ == "__main__":
    import time  # 添加time模块
    main()