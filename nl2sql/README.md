# 自然语言转 MySQL 查询工具

这是一个可以通过命令行交互的轻量级 Python 脚本。它调用大语言模型（如智谱 GLM），将用户的自然语言描述准确地转换为高效、规范的 MySQL 查询语句。

## 快速开始

1. **配置 API Key**
   请在当前目录下的 `.env` 文件中填入您的智谱 API Key。
   打开 `.env` 文件，将 `API_KEY="your_api_key_here"` 替换为您的真实 Key。

2. **安装依赖**
   建议使用虚拟环境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python nl2sql.py
   ```

## 使用示例
在终端中输入：`查询所有年龄大于 18 岁并且在过去 30 天内有过购买记录的用户的姓名和邮箱。`
程序将输出对应的 MySQL 语句。
