# LLM Mini Projects (大模型应用实战开源合集)

本项目包含三个独立的、基于大语言模型（如智谱 GLM-4 / DeepSeek 等）落地的提效应用，涵盖从自然语言转 SQL 到全能 Agent 智能体的全栈 AI 实践。

## 📦 项目列表

### 1. NL2SQL 智能查询引擎 (`/nl2sql`)
* **核心功能**：通过自然语言输入，自动生成符合 MySQL 方言的最佳实践 SQL 语句。
* **技术亮点**：Context Engineering (上下文工程)、防 SQL 注入兜底逻辑。

### 2. 多模态内容翻译与润色平台 (`/translator`)
* **核心功能**：支持风格迁移（如：商务/小红书/学术）的文本处理引擎，并在管线中集成了文生图能力。
* **技术亮点**：Pipeline 管线编排、LLM 自动提取 Image Prompt、Text-to-Image API 集成。

### 3. 带记忆系统的全能 Agent 智能体 (`/chatbot`)
* **核心功能**：高自由度角色扮演 Chatbot，支持长文本记忆，并能自主调用外部 API 获取实时数据（如查天气）。
* **技术亮点**：Memory System (滑动窗口截断机制)、Function Calling / Skill (工具调用与本地调度)。

## 🚀 如何运行

1. 进入对应的项目文件夹（如：`cd nl2sql`）
2. 将 `.env` 文件中的 `API_KEY` 替换为您自己的智谱大模型 API Key（或其他兼容 OpenAI SDK 的模型 Key）。
3. 安装依赖并运行：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python [对应的脚本名.py]
```

## 📄 License
MIT License
