# Benchmark Tracker

一个可直接部署到 Netlify 的静态站点骨架。

## 目录

- `index.html`：固定首页，始终展示最新报告
- `archive/YYYY-MM-DD.html`：每日历史快照
- `archive/index.html`：历史归档入口
- `data/latest.json`：最新机器可读数据
- `data/history.json`：历史索引
- `data/daily-schema.example.json`：每日 JSON 建议结构
- `scripts/publish_daily.py`：把当天 HTML/JSON 发布到固定目录的辅助脚本
- `netlify.toml`：Netlify 静态站点配置，最新页禁用缓存

## 首次部署到 Netlify

1. 解压本目录。
2. 登录 Netlify。
3. 选择 **Add new site → Deploy manually**。
4. 将整个 `benchmark-tracker-site` 文件夹拖入 Netlify Drop。
5. 部署完成后会得到固定网址，例如 `https://xxx.netlify.app/`。
6. 把该网址发给同事即可共同查看。

## 推荐的真正自动更新架构

最稳妥的是：

`每日数据生成 → 写入 GitHub 仓库 → Netlify 自动部署`

Netlify 连接 GitHub 后，每次仓库里的 `index.html / data/latest.json / archive/...` 更新，网站都会自动发布，无需手工拖文件。

要让 ChatGPT 每日任务自动完成“写入 GitHub”，还需要在 ChatGPT 侧连接一个具有仓库写权限的 GitHub 工具/连接器。当前会话环境没有可用的 GitHub/Netlify 写入连接，因此本包先提供可部署站点和标准发布结构。

## 每日文件更新规则

每天 10:00 的报告完成后，应：

- 覆盖 `index.html`
- 覆盖 `data/latest.json`
- 新增 `archive/YYYY-MM-DD.html`
- 更新 `data/history.json`

可使用：

```bash
python scripts/publish_daily.py todays-report.html todays-data.json
```

然后提交/推送到 GitHub，Netlify 会自动部署。
