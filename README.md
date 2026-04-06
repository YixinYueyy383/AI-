# AI Editorial Layout Agent

AI Editorial Layout Agent 是一个将微信公众号长文章自动拆解并重新排版为视觉化图文卡片的智能系统。系统能够将文章内容转化为适合社交媒体发布的图文轮播内容，并最终输出为可编辑的 PPTX 文件。

## 功能特性

### 核心功能
- **文章抓取与解析**：自动抓取微信公众号文章内容，提取标题、小标题、正文和图片
- **语义拆解**：根据语义将文章拆解为多个独立的信息块，保持叙事节奏与情绪停顿
- **智能配图**：优先使用原文图片，支持从 Instagram 或互联网搜索匹配图片
- **多样化排版**：10+ 种排版布局自动轮换，避免视觉疲劳
- **PPTX 导出**：生成可编辑的 PowerPoint 文件，所有元素独立分层

### 排版布局类型
1. **大图配底部文字** - 图片占70%，文字占30%
2. **左图右文** - 左右各50%分割
3. **上文下图** - 文字在上，图片在下
4. **居中标题留白** - 极简风格，文字居中
5. **双图拼贴** - 两张图片并排
6. **半图半文字** - 无内边距分割
7. **纯文字极简** - 仅文字内容
8. **图片上叠加文字** - 文字叠加在图片上
9. **三图网格** - 三张图片网格排列
10. **全出血图片** - 图片铺满整张卡片

### 视觉风格主题
- **Editorial 编辑风格** - 杂志编辑风格，优雅经典
- **Minimal 极简风格** - 简洁干净，现代感强
- **Warm 温暖风格** - 暖色调，温馨舒适
- **Dark 深色风格** - 深色背景，高端大气
- **Pastel 柔和风格** - 柔和色彩，清新淡雅

## 安装与使用

### 环境要求
- Python 3.8+
- pip 包管理器

### 安装步骤

1. 克隆或下载项目
```bash
cd editorial_agent
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用程序
```bash
streamlit run app.py
```

### 使用流程

1. **输入文章链接**
   - 在侧边栏粘贴微信公众号文章完整链接
   - 例如：`https://mp.weixin.qq.com/s/xxxxx`

2. **配置选项**
   - **卡片数量**：5-18张，默认13张
   - **图片尺寸**：支持多种预设尺寸
     - 1080×1350 (4:5 Instagram)
     - 1080×1080 (1:1 方形)
     - 1080×1920 (9:16 故事)
   - **视觉风格**：选择预设主题
   - **Instagram 来源**（可选）：提供Instagram账号链接
   - **额外需求**：自定义字体、颜色等参数

3. **生成卡片**
   - 点击"生成图文卡片"按钮
   - 等待系统处理（包括文章抓取、内容解析、图片匹配）

4. **预览与调整**
   - 左右滑动浏览每张卡片
   - 点击"替换当前图片"可更换图片素材
   - 查看布局类型和文字内容

5. **导出文件**
   - 点击"生成 PPTX 文件"
   - 下载生成的 PowerPoint 文件

## 项目结构

```
editorial_agent/
├── app.py                      # 主应用程序（Streamlit界面）
├── requirements.txt            # 依赖包列表
├── README.md                   # 项目说明文档
├── modules/                    # 核心模块
│   ├── __init__.py
│   ├── article_fetcher.py      # 文章抓取与解析模块
│   ├── image_matcher.py        # 图片匹配与获取模块
│   ├── layout_generator.py     # 排版生成模块
│   └── pptx_exporter.py        # PPTX导出模块
├── tools/                      # 工具模块
│   ├── __init__.py
│   └── web_search.py           # 网络搜索工具
└── assets/                     # 静态资源
```

## 模块说明

### Article Fetcher（文章抓取器）
- 抓取微信公众号文章内容
- 提取标题、作者、发布时间、正文和图片
- 解析文章结构，识别小标题

### Article Parser（文章解析器）
- 将文章拆解为内容块
- 保持语义完整性和叙事节奏
- 支持按段落或小标题分割
- 自动调整块数量以匹配目标卡片数

### Image Matcher（图片匹配器）
- 优先使用原文图片
- 支持 Instagram 图片来源
- 互联网图片搜索作为补充
- 图片下载和缓存管理

### Layout Generator（布局生成器）
- 10+ 种预设布局
- 自动轮换布局类型
- 根据内容自动调整字体大小
- 支持自定义风格偏好

### PPTX Exporter（PPTX导出器）
- 生成可编辑的 PowerPoint 文件
- 所有文字和图片为独立元素
- 支持分页结构和独立图层
- 多种尺寸和主题支持

## 配置说明

### 卡片尺寸
系统支持以下预设尺寸：
- `1080×1350` - 4:5比例，适合Instagram帖子
- `1080×1080` - 1:1比例，方形图片
- `1080×1920` - 9:16比例，适合Instagram Stories
- `1200×1500` - 4:5大尺寸
- `1200×1200` - 1:1大尺寸

### 视觉参数
可通过额外需求输入框自定义：
- `font_family` - 字体家族
- `background_color` - 背景颜色（十六进制）
- `text_color` - 文字颜色（十六进制）
- `line_spacing` - 行距倍数
- `text_align` - 文字对齐方式
- `padding_scale` - 内边距缩放比例

## 技术实现

### 文章抓取
- 使用 `requests` 发送HTTP请求
- 使用 `BeautifulSoup` 解析HTML
- 支持多种选择器匹配微信页面结构

### 内容解析
- 基于语义的内容分割
- 智能段落合并与拆分
- 保持内容完整性和可读性

### 图片处理
- 多来源图片获取策略
- 图片相关性评分算法
- 本地缓存机制

### 排版生成
- 基于规则的布局选择
- 响应式字体大小调整
- 视觉节奏控制

### PPTX生成
- 使用 `python-pptx` 库
- EMU单位精确控制
- 支持透明度和渐变效果

## 注意事项

1. **微信公众号限制**
   - 部分文章可能需要登录才能访问
   - 频繁抓取可能触发反爬虫机制

2. **图片版权**
   - 原文图片版权归原作者所有
   - 网络搜索图片需注意使用授权
   - 建议替换为自有版权图片

3. **Instagram 抓取**
   - Instagram 有严格的反爬虫机制
   - 建议使用官方 API 或第三方服务

4. **性能优化**
   - 大图处理可能需要较长时间
   - 建议分批处理大量卡片

## 扩展开发

### 添加新布局
在 `layout_generator.py` 中添加新的 `LayoutType` 和对应的 `LayoutConfig`：

```python
class LayoutType(Enum):
    # 现有布局...
    NEW_LAYOUT = "new_layout"

LAYOUT_PRESETS = {
    # 现有配置...
    LayoutType.NEW_LAYOUT: LayoutConfig(
        layout_type=LayoutType.NEW_LAYOUT,
        image_count=1,
        text_position='bottom',
        image_position='full',
        # ...其他配置
    )
}
```

### 添加新主题
在 `StyleManager` 中添加新主题：

```python
THEMES = {
    # 现有主题...
    'custom': {
        'background_color': '#FFFFFF',
        'text_color': '#000000',
        'accent_color': '#FF0000',
        'font_family': 'Arial, sans-serif',
        'line_spacing': 1.6
    }
}
```

### 集成图片搜索API
在 `web_search.py` 中实现实际的图片搜索：

```python
def search_images(query: str, count: int = 5) -> List[Dict]:
    # 调用实际的图片搜索API
    # 例如 Google Custom Search、Bing Image Search 等
    pass
```

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
