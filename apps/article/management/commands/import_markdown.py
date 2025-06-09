from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from article.models import ArticlePost, ArticleTag, Category
import os
import re
import shutil
from datetime import datetime
from django.core.files import File
from urllib.parse import quote, urljoin

category_icon = os.path.join(settings.BASE_DIR, 'static', 'images', 'category.jpg').replace('\\', '/')


class Command(BaseCommand):
    help = '检查并导入markdown文件到文章系统'

    def parse_yaml_metadata(self, content):
        # 查找开头和结尾的 ---
        yaml_pattern = r'^---\s*$([\s\S]+?)^---\s*$'
        match = re.search(yaml_pattern, content, re.MULTILINE)
        
        if not match:
            return None, content
            
        # 提取YAML内容
        yaml_content = match.group(1)
        
        # 解析YAML内容
        metadata = {}
        current_key = None
        current_list = []
        
        for line in yaml_content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # 检查是否是新的键值对
            if ':' in line and not line.startswith('-'):
                if current_key and current_list:
                    metadata[current_key] = current_list
                    current_list = []
                
                key, value = [x.strip() for x in line.split(':', 1)]
                if value:
                    metadata[key] = value
                else:
                    current_key = key
                    current_list = []
            # 检查是否是列表项
            elif line.startswith('-'):
                value = line[1:].strip()
                current_list.append(value)
        
        # 处理最后一个列表（如果有）
        if current_key and current_list:
            metadata[current_key] = current_list
        
        # 移除元数据部分，只保留正文
        remaining_content = content[match.end():].strip()
        
        return metadata, remaining_content

    def handle(self, *args, **options):

        dirs = [item for item in os.listdir(settings.LOCAL_MARKDOWN_PATH) if os.path.isdir(os.path.join(settings.LOCAL_MARKDOWN_PATH, item)) and item !='public' ]
        if not dirs:
            self.stdout.write(self.style.SUCCESS('没有找到需要导入的文章专题信息'))
            return

        # 处理图片信息
        image_dir = os.path.join(settings.BASE_DIR, 'media', 'article_images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # 拷贝图片目录
        source_dir = os.path.join(settings.LOCAL_MARKDOWN_PATH, 'public')
        target_dir = os.path.join(settings.BASE_DIR, 'media', 'article_images')
        if os.listdir(source_dir):
            # 执行复制
            copy_directory_contents(source_dir, target_dir)
            self.stdout.write(self.style.SUCCESS('图片目录导入成功'))
        
        for dir in dirs:
            # 创建专题信息
            category_query = Category.objects.filter(name=dir)
            if not category_query.exists():
                Category.objects.create(name=dir)
            
            md_files = [f for f in os.listdir(os.path.join(settings.LOCAL_MARKDOWN_PATH, dir)) if f.endswith('.md')]
            if not md_files:
                self.stdout.write(self.style.SUCCESS('没有找到需要导入的markdown文件'))
                return

            for md_file in md_files:
                file_path = os.path.join(settings.LOCAL_MARKDOWN_PATH, dir, md_file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 解析YAML元数据
                    metadata, content = self.parse_yaml_metadata(content)
                    if not metadata:
                        self.stdout.write(self.style.WARNING(f'文件 {md_file} 没有元数据，跳过'))
                        continue

                    # 获取标题和创建时间
                    title = metadata.get('title')
                    create_time_str = metadata.get('createTime')
                    tags = metadata.get('tags', [])

                    if not title:
                        self.stdout.write(self.style.WARNING(f'文件 {md_file} 没有标题，使用文件名作为标题'))
                        title = os.path.splitext(md_file)[0]
                    # 判断标题是否存在
                    if ArticlePost.objects.filter(title=title).exists():
                        self.stdout.write(self.style.WARNING(f'文章 {title} 已存在，跳过'))
                        continue

                    # 解析创建时间
                    if create_time_str:
                        try:
                            created = datetime.strptime(create_time_str, '%Y/%m/%d %H:%M:%S')
                        except ValueError:
                            created = timezone.now()
                    else:
                        created = timezone.now()

                    # 处理图片
                    img_pattern = r'!\[([^\]]*)\]\(([^\)]*)\)'

                    def process_image(match):
                        alt_text = match.group(1)
                        img_url = match.group(2)
                        # 处理图片编程django能够访问的路径信息
                        if not img_url.startswith(('http://', 'https://' )):
                            _img_url = "/".join(segment.strip("/") for segment in [settings.SERVER_ADDR, settings.MEDIA_URL, 'article_images', img_url])
                            return f'![{alt_text}]({_img_url})'
                        return match.group(0)

                    processed_content = re.sub(img_pattern, process_image, content)

                    category = Category.objects.get_or_create(name=dir)[0]  # 使用当前目录名作为分类名
                    
                    # 创建文章时指定分类
                    article = ArticlePost.objects.create(
                        author_id=1,  # 设置默认作者ID
                        title=title,
                        body=processed_content,
                        created=created,
                        updated=created,
                        category=category  # 添加分类关联
                    )

                    # 处理标签
                    for tag_name in tags:
                        tag, created = ArticleTag.objects.get_or_create(name=tag_name)
                        article.tag.add(tag)

                    self.stdout.write(self.style.SUCCESS(f'成功导入文章: {title}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'解析文件 {md_file} 元数据失败: {str(e)}'))
                    continue
        
                
            
            




        

        # for md_file in md_files:
        #     file_path = os.path.join(markdown_dir, md_file)

        #     try:
        #         with open(file_path, 'r', encoding='utf-8') as f:
        #             content = f.read()

        #         # 解析YAML元数据
        #         metadata, content = self.parse_yaml_metadata(content)
                
        #         if not metadata:
        #             self.stdout.write(self.style.WARNING(f'文件 {md_file} 没有元数据，跳过'))
        #             continue

        #         # 获取标题和创建时间
        #         title = metadata.get('title')
        #         create_time_str = metadata.get('createTime')
        #         tags = metadata.get('tags', [])

        #         if not title:
        #             self.stdout.write(self.style.WARNING(f'文件 {md_file} 没有标题，使用文件名作为标题'))
        #             title = os.path.splitext(md_file)[0]

        #         # 解析创建时间
        #         if create_time_str:
        #             try:
        #                 created = datetime.strptime(create_time_str, '%Y/%m/%d %H:%M:%S')
        #             except ValueError:
        #                 created = timezone.now()
        #         else:
        #             created = timezone.now()

        #         # 处理图片
        #         img_pattern = r'!\[([^\]]*)\]\(([^\)]*)\)'

        #         def process_image(match):
        #             alt_text = match.group(1)
        #             img_url = match.group(2)

        #             if not img_url.startswith(('http://', 'https://', '/')):
        #                 img_name = os.path.basename(img_url)
        #                 relative_path = f'article_images/{created.strftime("%Y%m%d")}/{img_name}'
        #                 absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                        
        #                 os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
                        
        #                 img_source = os.path.join(os.path.dirname(file_path), img_url)
        #                 if os.path.exists(img_source):
        #                     shutil.copy2(img_source, absolute_path)
        #                     return f'![{alt_text}]({settings.MEDIA_URL}{relative_path})'
        #                 else:
        #                     self.stdout.write(self.style.WARNING(f'图片不存在: {img_source}'))
        #                     return match.group(0)
                    
        #             return match.group(0)

        #         processed_content = re.sub(img_pattern, process_image, content)

        #         # 创建文章
        #         article = ArticlePost.objects.create(
        #             author_id=1,  # 设置默认作者ID
        #             title=title,
        #             body=processed_content,
        #             created=created,
        #             updated=created
        #         )

        #         # 处理标签
        #         for tag_name in tags:
        #             tag, created = ArticleTag.objects.get_or_create(name=tag_name)
        #             article.tag.add(tag)

        #         self.stdout.write(self.style.SUCCESS(f'成功导入文章: {title}'))

        #     except Exception as e:
        #         self.stdout.write(self.style.ERROR(f'导入文章失败: {str(e)}'))


def copy_directory_contents(source_dir, target_dir):
    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # 遍历源目录中的所有内容
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)
        
        # 如果是目录，则递归复制
        if os.path.isdir(source_path):
            # 判断目录是否已存在
            if os.path.exists(target_path):
                # 递归复制
                copy_directory_contents(source_path, target_path)
                continue
            shutil.copytree(source_path, target_path)
        # 如果是文件，则直接复制
        else:
            if os.path.exists(target_path):
                continue
            shutil.copy2(source_path, target_path)