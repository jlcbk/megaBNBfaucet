import subprocess
import json

def claim_megabnb(address):
    # 调用Node.js脚本并传递参数
    result = subprocess.run(
        ['node', '-e', 
         f"const {{ claimAirdrop }} = require('./@getMegaBNB.js'); \
          claimAirdrop('{address}').then(console.log);"],
        capture_output=True,
        text=True
    )
    
    # 解析返回结果
    try:
        return json.loads(result.stdout)
    except:
        return {"success": False, "message": "调用失败"}

# 使用示例
if __name__ == "__main__":
    result = claim_megabnb("0xYourAddressHere")
    print(result)