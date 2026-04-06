"""
系统测试脚本
测试 AI Editorial Layout Agent 的各个模块
"""
import os
import sys
import tempfile

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.article_fetcher import WeChatArticleFetcher, ArticleParser
from modules.layout_generator import LayoutGenerator, LayoutType, StyleManager
from modules.image_matcher import ImageMatcher, ImageSource
from modules.pptx_exporter import PPTXExporter


def test_layout_generator():
    """测试布局生成器"""
    print("=" * 50)
    print("测试布局生成器")
    print("=" * 50)
    
    # 创建布局生成器
    generator = LayoutGenerator((1080, 1350))
    
    # 生成13张卡片的布局序列
    layouts = generator.generate_layout_sequence(13)
    
    print(f"生成了 {len(layouts)} 个布局")
    
    for i, layout in enumerate(layouts):
        print(f"\n卡片 {i+1}:")
        print(f"  类型: {layout.layout_type.value}")
        print(f"  图片数: {layout.image_count}")
        print(f"  文字位置: {layout.text_position}")
        print(f"  标题字号: {layout.font_size_title}pt")
        print(f"  正文字号: {layout.font_size_body}pt")
    
    print("\n✅ 布局生成器测试通过")
    return True


def test_article_parser():
    """测试文章解析器"""
    print("\n" + "=" * 50)
    print("测试文章解析器")
    print("=" * 50)
    
    # 模拟文章数据
    article_data = {
        'success': True,
        'title': '测试文章标题',
        'author': '测试作者',
        'content_text': '''
这是文章的第一段内容，介绍了一些基本概念。

第一节标题

这是第一节的内容，详细说明了某个主题。这里有很多文字，需要被正确分割。

第二节标题

第二节的内容更加详细，包含了更多的信息。我们需要测试解析器是否能正确处理这些内容。

第三节标题

这是最后一节的内容，总结了全文的主要观点。
        ''',
        'sections': [
            {'level': 1, 'text': '第一节标题', 'tag': 'h2'},
            {'level': 1, 'text': '第二节标题', 'tag': 'h2'},
            {'level': 1, 'text': '第三节标题', 'tag': 'h2'},
        ],
        'original_images': []
    }
    
    # 创建解析器
    parser = ArticleParser(article_data)
    
    # 解析为内容块
    blocks = parser.parse_to_blocks(target_card_count=5)
    
    print(f"解析出 {len(blocks)} 个内容块")
    
    for i, block in enumerate(blocks):
        print(f"\n块 {i+1}:")
        print(f"  标题: {block.get('title', 'N/A')}")
        print(f"  类型: {block.get('type', 'N/A')}")
        print(f"  字数: {block.get('word_count', 0)}")
        print(f"  摘要: {block.get('summary', 'N/A')[:50]}...")
    
    print("\n✅ 文章解析器测试通过")
    return True


def test_style_manager():
    """测试风格管理器"""
    print("\n" + "=" * 50)
    print("测试风格管理器")
    print("=" * 50)
    
    # 获取所有主题
    themes = ['editorial', 'minimal', 'warm', 'dark', 'pastel']
    
    for theme_name in themes:
        theme = StyleManager.get_theme(theme_name)
        print(f"\n主题: {theme_name}")
        print(f"  背景色: {theme['background_color']}")
        print(f"  文字色: {theme['text_color']}")
        print(f"  强调色: {theme['accent_color']}")
        print(f"  字体: {theme['font_family']}")
    
    print("\n✅ 风格管理器测试通过")
    return True


def test_pptx_exporter():
    """测试PPTX导出器"""
    print("\n" + "=" * 50)
    print("测试PPTX导出器")
    print("=" * 50)
    
    try:
        # 创建导出器
        exporter = PPTXExporter((1080, 1350))
        
        # 创建测试卡片
        from modules.layout_generator import LayoutConfig, LayoutType
        
        test_cards = [
            {
                'index': 0,
                'title': '测试标题 1',
                'content': '这是第一张测试卡片的内容。',
                'type': 'intro',
                'layout': LayoutGenerator.LAYOUT_PRESETS[LayoutType.CENTER_TITLE_MINIMAL],
                'images': [],
                'summary': '测试摘要'
            },
            {
                'index': 1,
                'title': '测试标题 2',
                'content': '这是第二张测试卡片的内容，包含更多信息。',
                'type': 'content',
                'layout': LayoutGenerator.LAYOUT_PRESETS[LayoutType.TEXT_ONLY_MINIMAL],
                'images': [],
                'summary': '测试摘要2'
            }
        ]
        
        # 导出PPTX
        output_path = os.path.join(tempfile.gettempdir(), 'test_output.pptx')
        exporter.export_cards(test_cards, output_path, theme='editorial')
        
        # 检查文件是否存在
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"PPTX文件已生成: {output_path}")
            print(f"文件大小: {file_size} 字节")
            print("\n✅ PPTX导出器测试通过")
            return True
        else:
            print("❌ PPTX文件未生成")
            return False
    
    except Exception as e:
        print(f"❌ PPTX导出器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_matcher():
    """测试图片匹配器"""
    print("\n" + "=" * 50)
    print("测试图片匹配器")
    print("=" * 50)
    
    # 创建图片匹配器
    cache_dir = os.path.join(tempfile.gettempdir(), 'test_image_cache')
    matcher = ImageMatcher(cache_dir)
    
    # 设置原文图片
    original_images = [
        {
            'url': 'https://example.com/image1.jpg',
            'caption': '烘焙面包图片',
            'width': 1080,
            'height': 1350
        },
        {
            'url': 'https://example.com/image2.jpg',
            'caption': '蛋糕甜点图片',
            'width': 1080,
            'height': 1350
        }
    ]
    
    matcher.set_original_images(original_images)
    
    # 测试内容块
    block = {
        'title': '面包制作',
        'summary': '介绍如何制作美味的面包',
        'content': '面包制作需要面粉、酵母、水和盐。'
    }
    
    # 查找图片
    images = matcher.find_images_for_block(block, count=2)
    
    print(f"找到 {len(images)} 张图片")
    
    for i, img in enumerate(images):
        print(f"\n图片 {i+1}:")
        print(f"  URL: {img.url}")
        print(f"  来源: {img.source_type}")
        print(f"  说明: {img.caption}")
    
    print("\n✅ 图片匹配器测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("AI Editorial Layout Agent 系统测试")
    print("=" * 50)
    
    tests = [
        ("布局生成器", test_layout_generator),
        ("文章解析器", test_article_parser),
        ("风格管理器", test_style_manager),
        ("图片匹配器", test_image_matcher),
        ("PPTX导出器", test_pptx_exporter),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name}测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 打印测试结果汇总
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️ {total - passed} 项测试未通过")


if __name__ == "__main__":
    run_all_tests()
