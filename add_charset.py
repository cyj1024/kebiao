import os
import chardet

# 项目文件夹路径
project_folder = '.'

# 遍历项目文件夹下的所有文件
for root, dirs, files in os.walk(project_folder):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            # 检测文件编码
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']

            # 读取文件内容
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
            except UnicodeDecodeError:
                # 若检测编码仍无法读取，尝试使用 UTF-8 并替换无法解码的字符
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()

            # 检查是否已经有字符编码声明
            if '<meta charset="utf-8">' not in content:
                # 在<head>标签内添加字符编码声明
                if '<head>' in content:
                    index = content.index('<head>') + len('<head>')
                    new_content = content[:index] + '\n    <meta charset="utf-8">' + content[index:]
                else:
                    # 如果没有<head>标签，则在文件开头添加
                    new_content = '<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="utf-8">\n</head>\n' + content
                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)