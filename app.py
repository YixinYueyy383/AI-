"""
AI Editorial Layout Agent - 主应用程序
微信公众号文章转视觉化图文卡片系统
"""
import os
import json
import streamlit as st
from typing import List, Dict, Optional, Tuple
import tempfile
import base64
from pathlib import Path

from modules.article_fetcher import WeChatArticleFetcher, ArticleParser
from modules.image_matcher import ImageMatcher
from modules.layout_generator import LayoutGenerator, StyleManager
from modules.pptx_exporter import PPTXExporter, CardDataBuilder


# 页面配置
st.set_page_config(
    page_title="AI Editorial Layout Agent",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .card-preview {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    .stSlider > div > div > div {
        background-color: #4A90E2;
    }
    .sidebar-section {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


class EditorialLayoutAgent:
    """AI Editorial Layout Agent 主类"""
    
    def __init__(self):
        self.article_fetcher = WeChatArticleFetcher()
        self.image_matcher = None
        self.layout_generator = None
        self.pptx_exporter = None
        self.card_data_builder = None
        
        # 会话状态
        if 'article_data' not in st.session_state:
            st.session_state.article_data = None
        if 'content_blocks' not in st.session_state:
            st.session_state.content_blocks = []
        if 'cards' not in st.session_state:
            st.session_state.cards = []
        if 'current_preview_index' not in st.session_state:
            st.session_state.current_preview_index = 0
    
    def run(self):
        """运行应用程序"""
        # 主标题
        st.markdown('<p class="main-header">🎨 AI Editorial Layout Agent</p>', 
                   unsafe_allow_html=True)
        st.markdown('<p class="sub-header">将微信公众号文章自动转化为视觉化图文卡片</p>', 
                   unsafe_allow_html=True)
        
        # 侧边栏配置
        with st.sidebar:
            st.header("⚙️ 配置选项")
            
            # 文章URL输入
            st.subheader("1. 文章链接")
            article_url = st.text_input(
                "微信公众号文章链接",
                placeholder="https://mp.weixin.qq.com/s/...",
                help="粘贴微信公众号文章的完整链接"
            )
            
            # 卡片数量设置
            st.subheader("2. 卡片数量")
            card_count = st.slider(
                "生成卡片数量",
                min_value=5,
                max_value=18,
                value=13,
                help="选择要生成的卡片数量"
            )
            
            # 图片尺寸设置
            st.subheader("3. 图片尺寸")
            size_options = {
                "1080 × 1350 (4:5 Instagram)": (1080, 1350),
                "1080 × 1080 (1:1 方形)": (1080, 1080),
                "1080 × 1920 (9:16 故事)": (1080, 1920),
                "1200 × 1500 (4:5 大尺寸)": (1200, 1500),
                "1200 × 1200 (1:1 大尺寸)": (1200, 1200),
            }
            selected_size = st.selectbox(
                "选择卡片尺寸",
                options=list(size_options.keys()),
                index=0
            )
            card_size = size_options[selected_size]
            
            # 视觉风格设置
            st.subheader("4. 视觉风格")
            theme_options = {
                "Editorial 编辑风格": "editorial",
                "Minimal 极简风格": "minimal",
                "Warm 温暖风格": "warm",
                "Dark 深色风格": "dark",
                "Pastel 柔和风格": "pastel"
            }
            selected_theme = st.selectbox(
                "选择主题风格",
                options=list(theme_options.keys()),
                index=0
            )
            theme = theme_options[selected_theme]
            
            # Instagram 链接（可选）
            st.subheader("5. Instagram 图片来源（可选）")
            instagram_url = st.text_input(
                "Instagram 账号链接",
                placeholder="https://www.instagram.com/...",
                help="提供Instagram账号作为图片来源"
            )
            
            # 额外需求
            st.subheader("6. 额外需求")
            extra_requirements = st.text_area(
                "自定义设置",
                placeholder="例如：字体=宋体，背景色=#FFFFFF，行距=1.8...",
                help="输入自定义的视觉参数"
            )
            
            # 生成按钮
            st.markdown("---")
            generate_btn = st.button(
                "🚀 生成图文卡片",
                type="primary",
                use_container_width=True
            )
        
        # 主内容区域
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📄 文章预览")
            
            if article_url and generate_btn:
                with st.spinner("正在抓取文章..."):
                    self._process_article(article_url, card_count, card_size, theme)
            
            # 显示文章信息
            if st.session_state.article_data:
                self._display_article_info(st.session_state.article_data)
        
        with col2:
            st.subheader("📊 生成状态")
            self._display_generation_status()
        
        # 卡片预览区域
        if st.session_state.cards:
            st.markdown("---")
            st.subheader("🎴 卡片预览")
            self._display_card_previews()
            
            # 下载按钮
            st.markdown("---")
            self._display_download_button()
    
    def _process_article(self, url: str, card_count: int, 
                         card_size: Tuple[int, int], theme: str):
        """处理文章并生成卡片"""
        try:
            # 1. 抓取文章
            article_data = self.article_fetcher.fetch_article(url)
            st.session_state.article_data = article_data
            
            if not article_data.get('success', False):
                st.error(f"抓取文章失败: {article_data.get('error', '未知错误')}")
                return
            
            # 2. 解析为内容块
            parser = ArticleParser(article_data)
            content_blocks = parser.parse_to_blocks(card_count)
            st.session_state.content_blocks = content_blocks
            
            # 3. 初始化图片匹配器
            self.image_matcher = ImageMatcher(
                cache_dir=os.path.join(tempfile.gettempdir(), 'image_cache')
            )
            self.image_matcher.set_original_images(
                article_data.get('original_images', [])
            )
            
            # 4. 初始化布局生成器
            self.layout_generator = LayoutGenerator(card_size)
            
            # 5. 构建卡片数据
            self.card_data_builder = CardDataBuilder(
                self.layout_generator,
                self.image_matcher
            )
            cards = self.card_data_builder.build_cards(content_blocks)
            st.session_state.cards = cards
            
            st.success(f"成功生成 {len(cards)} 张卡片！")
            
        except Exception as e:
            st.error(f"处理文章时出错: {str(e)}")
    
    def _display_article_info(self, article_data: Dict):
        """显示文章信息"""
        with st.expander("文章详情", expanded=True):
            st.markdown(f"**标题:** {article_data.get('title', 'N/A')}")
            st.markdown(f"**作者:** {article_data.get('author', 'N/A')}")
            st.markdown(f"**发布时间:** {article_data.get('publish_time', 'N/A')}")
            
            # 显示原文图片
            original_images = article_data.get('original_images', [])
            if original_images:
                st.markdown(f"**原文图片:** {len(original_images)} 张")
                cols = st.columns(min(4, len(original_images)))
                for i, img in enumerate(original_images[:4]):
                    with cols[i % 4]:
                        st.caption(f"图片 {i+1}")
    
    def _display_generation_status(self):
        """显示生成状态"""
        status_container = st.container()
        
        with status_container:
            # 文章抓取状态
            if st.session_state.article_data:
                st.success("✅ 文章抓取完成")
            else:
                st.info("⏳ 等待文章链接")
            
            # 内容解析状态
            if st.session_state.content_blocks:
                st.success(f"✅ 内容解析完成 ({len(st.session_state.content_blocks)} 个信息块)")
            
            # 卡片生成状态
            if st.session_state.cards:
                st.success(f"✅ 卡片生成完成 ({len(st.session_state.cards)} 张)")
    
    def _display_card_previews(self):
        """显示卡片预览"""
        cards = st.session_state.cards
        
        if not cards:
            return
        
        # 导航控制
        nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
        
        with nav_col1:
            if st.button("◀ 上一张", disabled=st.session_state.current_preview_index <= 0):
                st.session_state.current_preview_index = max(
                    0, st.session_state.current_preview_index - 1
                )
                st.rerun()
        
        with nav_col2:
            st.markdown(
                f"<p style='text-align: center;'>"
                f"卡片 {st.session_state.current_preview_index + 1} / {len(cards)}"
                f"</p>",
                unsafe_allow_html=True
            )
        
        with nav_col3:
            if st.button("下一张 ▶", 
                        disabled=st.session_state.current_preview_index >= len(cards) - 1):
                st.session_state.current_preview_index = min(
                    len(cards) - 1, st.session_state.current_preview_index + 1
                )
                st.rerun()
        
        # 显示当前卡片
        current_card = cards[st.session_state.current_preview_index]
        self._render_card_preview(current_card)
        
        # 缩略图导航
        st.markdown("---")
        st.caption("快速导航")
        thumb_cols = st.columns(min(8, len(cards)))
        for i, card in enumerate(cards[:8]):
            with thumb_cols[i]:
                is_current = i == st.session_state.current_preview_index
                btn_type = "primary" if is_current else "secondary"
                if st.button(f"{i+1}", key=f"thumb_{i}", type=btn_type):
                    st.session_state.current_preview_index = i
                    st.rerun()
    
    def _render_card_preview(self, card: Dict):
        """渲染卡片预览"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 卡片视觉预览（简化版）
            st.markdown("#### 布局预览")
            
            layout = card.get('layout')
            layout_name = layout.layout_type.value if layout else "未知"
            
            st.info(f"布局类型: {layout_name}")
            
            # 显示布局示意图
            self._render_layout_diagram(layout)
            
            # 图片信息
            images = card.get('images', [])
            if images:
                st.markdown("**图片素材:**")
                for i, img in enumerate(images):
                    source_type = img.get('source_type', 'unknown')
                    source_icon = {
                        'original': '📄',
                        'instagram': '📷',
                        'web_search': '🌐'
                    }.get(source_type, '📎')
                    st.caption(f"{source_icon} 图片 {i+1}: {source_type}")
        
        with col2:
            # 文字内容
            st.markdown("#### 文字内容")
            
            title = card.get('title', '')
            if title:
                st.markdown(f"**标题:** {title}")
            
            content = card.get('content', '')
            if content:
                with st.expander("查看正文", expanded=True):
                    st.write(content[:500] + "..." if len(content) > 500 else content)
            
            # 图片替换功能
            st.markdown("---")
            if st.button("🔄 替换当前图片", key=f"replace_img_{card['index']}"):
                self._replace_card_image(card)
    
    def _render_layout_diagram(self, layout):
        """渲染布局示意图"""
        if not layout:
            return
        
        # 使用ASCII艺术或简单图形表示布局
        layout_diagrams = {
            'full_image_bottom_text': """
            ┌─────────────────┐
            │                 │
            │     图片        │
            │    (70%)        │
            │                 │
            ├─────────────────┤
            │    文字         │
            │    (30%)        │
            └─────────────────┘
            """,
            'left_image_right_text': """
            ┌────────┬────────┐
            │        │        │
            │  图片  │  文字  │
            │  (50%) │  (50%) │
            │        │        │
            └────────┴────────┘
            """,
            'top_text_bottom_image': """
            ┌─────────────────┐
            │    文字         │
            │    (30%)        │
            ├─────────────────┤
            │                 │
            │     图片        │
            │    (70%)        │
            └─────────────────┘
            """,
            'center_title_minimal': """
            ┌─────────────────┐
            │                 │
            │                 │
            │    标题文字     │
            │     居中        │
            │                 │
            │                 │
            └─────────────────┘
            """,
            'two_image_collage': """
            ┌────────┬────────┐
            │ 图片1  │ 图片2  │
            │ (50%)  │ (50%)  │
            ├────────┴────────┤
            │     文字        │
            └─────────────────┘
            """,
        }
        
        diagram = layout_diagrams.get(
            layout.layout_type.value, 
            "布局示意图不可用"
        )
        st.code(diagram, language=None)
    
    def _replace_card_image(self, card: Dict):
        """替换卡片图片"""
        # 重新搜索图片
        block = {
            'title': card.get('title', ''),
            'summary': card.get('summary', '')
        }
        
        new_images = self.image_matcher.find_images_for_block(
            block, 
            card['layout'].image_count
        )
        
        # 下载新图片
        downloaded_images = []
        for img in new_images:
            local_path = self.image_matcher.download_image(img)
            if local_path:
                downloaded_images.append({
                    'url': img.url,
                    'local_path': local_path,
                    'source_type': img.source_type,
                    'source_url': img.source_url
                })
        
        # 更新卡片
        card['images'] = downloaded_images
        st.success("图片已替换！")
        st.rerun()
    
    def _display_download_button(self):
        """显示下载按钮"""
        st.subheader("📥 导出文件")
        
        if not st.session_state.cards:
            return
        
        # 生成PPTX
        if st.button("📊 生成 PPTX 文件", type="primary", use_container_width=True):
            with st.spinner("正在生成PPTX文件..."):
                try:
                    # 创建临时文件
                    temp_dir = tempfile.gettempdir()
                    output_path = os.path.join(
                        temp_dir, 
                        f"editorial_cards_{int(os.times().system)}.pptx"
                    )
                    
                    # 获取卡片尺寸
                    card_size = (1080, 1350)  # 默认值
                    if st.session_state.cards:
                        first_layout = st.session_state.cards[0].get('layout')
                        if first_layout:
                            # 从layout_generator获取尺寸
                            pass
                    
                    # 导出PPTX
                    exporter = PPTXExporter(card_size)
                    exporter.export_cards(
                        st.session_state.cards,
                        output_path,
                        theme='editorial'
                    )
                    
                    # 提供下载
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ 下载 PPTX 文件",
                            data=f.read(),
                            file_name="editorial_cards.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True
                        )
                    
                    st.success("PPTX文件已生成！")
                    
                except Exception as e:
                    st.error(f"生成PPTX文件失败: {str(e)}")


def main():
    """主函数"""
    agent = EditorialLayoutAgent()
    agent.run()


if __name__ == "__main__":
    main()
