const axios = require('axios');

async function claimAirdrop(address) {
  try {
    const response = await axios.post('https://mbscan.io/airdrop', {
      address: address.trim()
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return JSON.stringify({ 
      success: true, 
      message: `地址 ${address} 领取成功`,
      data: response.data  // 添加返回数据
    });

    if (response.status === 200) {
      return { success: true, message: `地址 ${address} 领取成功` };
    }
  } catch (error) {
    if (error.response && error.response.status === 403) {
      return { success: false, message: `地址 ${address} 不符合要求` };
    } else {
      return { success: false, message: `地址 ${address} 请求失败: ${error.message}` };
    }
  }
}

// 导出函数供外部调用
module.exports = { claimAirdrop };