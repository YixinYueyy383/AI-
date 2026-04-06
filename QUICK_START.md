# AI Editorial Layout Agent - 快速开始

## 5分钟上手

### 1. 安装 (1分钟)

```bash
cd /mnt/okcomputer/output/editorial_agent
pip install -r requirements.txt
```

### 2. 启动 (1分钟)

```bash
streamlit run app.py
```

### 3. 使用 (3分钟)

1. 打开浏览器访问 `http://localhost:8501`
2. 粘贴微信公众号文章链接
3. 点击"生成图文卡片"
4. 预览并下载PPTX文件

## 核心功能

| 功能 | 说明 |
|------|------|
| 文章抓取 | 自动获取微信公众号内容 |
| 语义拆解 | 智能分割为内容块 |
| 智能配图 | 原文/Instagram/网络搜索 |
| 多样排版 | 10+ 种布局自动轮换 |
| PPTX导出 | 可编辑的PowerPoint文件 |

## 布局类型

1. **大图+底部文字** - 产品展示
2. **左图+右文** - 对比说明
3. **上文+下图** - 配方展示
4. **居中标题** - 章节标题
5. **双图拼贴** - 多角度展示
6. **半图半文** - 视觉冲击
7. **纯文字** - 引用总结
8. **文字叠加** - 海报风格
9. **三图网格** - 步骤展示
10. **全出血图** - 封面结尾

## 视觉风格

| 风格 | 背景色 | 特点 |
|------|--------|------|
| Editorial | #FAFAFA | 杂志编辑风格 |
| Minimal | #FFFFFF | 极简现代 |
| Warm | #FDF8F3 | 温馨舒适 |
| Dark | #1A1A1A | 高端大气 |
| Pastel | #F5F0F5 | 柔和清新 |

## 文件说明

```
editorial_agent/
├── app.py              # 主程序
├── requirements.txt    # 依赖列表
├── start.sh           # 启动脚本
├── test_system.py     # 测试脚本
├── modules/           # 核心模块
│   ├── article_fetcher.py
│   ├── image_matcher.py
│   ├── layout_generator.py
│   └── pptx_exporter.py
├── tools/             # 工具模块
│   └── image_search.py
├── assets/            # 静态资源
│   ├── system_architecture.png
│   └── layout_types.png
└── docs/              # 文档
    ├── README.md
    ├── DEMO.md
    ├── USER_GUIDE.md
    └── PROJECT_SUMMARY.md
```

## 常用命令

```bash
# 启动应用
streamlit run app.py

# 运行测试
python test_system.py

# 安装依赖
pip install -r requirements.txt
```

## 配置选项

### 卡片数量
- 范围：5-18张
- 默认：13张

### 图片尺寸
- 1080×1350 (4:5) - Instagram
- 1080×1080 (1:1) - 方形
- 1080×1920 (9:16) - Stories

### 自定义参数
```
font_family=宋体
background_color=#FFFFFF
text_color=#333333
line_spacing=1.8
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 文章抓取失败 | 检查链接和网络 |
| 图片无法显示 | 点击"替换图片" |
| PPTX打不开 | 使用PowerPoint 2016+ |

## 技术支持

- 查看 `USER_GUIDE.md` 获取详细说明
- 运行 `test_system.py` 检查系统状态
- 查看 `DEMO.md` 了解功能演示

## 许可证

MIT License

---

**开始使用：** `streamlit run app.py`
