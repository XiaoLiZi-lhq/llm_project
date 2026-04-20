# 智能翻译与润色助手

不仅仅是翻译，更能让您的表达更加地道、专业。输入一段文本，AI 自动提炼、翻译并根据您设定的场景（如商务邮件、学术论文、小红书文案等）对文本进行语气润色和修改建议。

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
   python translator.py
   ```

## 体验建议
您可以随便丢给它一段大白话，然后要求它润色成“严肃的法律声明”或者“轻松幽默的朋友圈文案”，看看它的变脸速度。
