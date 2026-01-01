# 黄金与基金监控 (Railway部署版)

这是一个专门为 Railway 平台准备的自动监控脚本。

## 部署步骤

1. **注册 Railway**
   访问 [https://railway.app/](https://railway.app/) 并使用 GitHub 或邮箱注册。

2. **创建项目**
   - 点击 "New Project"
   - 选择 "Empty Project"

3. **上传代码**
   - 方式一（推荐）：安装 Railway CLI 后在本地运行 `railway up`
   - 方式二（简单）：将本文件夹内的所有文件上传到 GitHub 仓库，然后在 Railway 中选择 "Deploy from GitHub repo"

4. **配置环境变量**
   - 在 Railway 项目面板中，点击 "Variables"
   - 添加一个新的变量：
     - Key: `SERVERCHAN_KEY`
     - Value: `您的Server酱SendKey` (例如: SCT307800TTlRSeo3WBHXPH8u9MhcufhHn)

5. **验证运行**
   - 点击 "Deployments" 查看部署日志
   - 如果看到 "黄金与基金监控服务已启动" 字样，说明部署成功！

## 功能说明

- **自动监控**：每 5 分钟自动检查一次金价和基金净值。
- **微信推送**：
  - 当金价波动超过 1% 时发送通知。
  - 当金价偏离 20日均线 超过 5% 时发送风险提示。
- **24小时运行**：部署在云端，无需开电脑。
