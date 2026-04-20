import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

if not API_KEY or "your_api_key_here" in API_KEY:
    print("错误: 未配置 API_KEY。请在 .env 文件中配置您的 API_KEY。")
    sys.exit(1)

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def generate_image(prompt_text: str) -> str:
    """调用智谱的 CogView 模型生成图片"""
    try:
        response = client.images.generate(
            model="cogview-3-plus", # 智谱最新的文生图模型
            prompt=prompt_text,
            size="1024x1024"
        )
        # 获取生成的图片URL
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return f"❌ 图片生成失败: {str(e)}"

def translate_and_polish(text: str, style: str) -> dict:
    prompt = f"""你是一个精通多国语言的资深翻译专家和文学编辑。
请将以下文本翻译并润色（如果已经是中文，则直接进行结构和语言的润色优化）。

【目标风格/场景】
{style}

【要求输出格式】
严格按照以下三部分输出，不要添加其他寒暄废话，各部分之间用三个短横线 --- 分隔：

（在此处输出你优化后的文本）
---
（在此处简要解释你做了哪些词汇、句式或语气的调整）
---
（在此处提取一段极其简短的英文画面描述词，用于稍后调用AI生成符合这段文字意境的配图，不超过30个英文单词）
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content.strip()
        parts = content.split("---")
        
        if len(parts) >= 3:
            polished_text = parts[0].strip()
            explanation = parts[1].strip()
            image_prompt = parts[2].strip()
        else:
            # 如果模型没有严格按照格式输出的容错处理
            polished_text = content
            explanation = "模型未按格式返回说明。"
            image_prompt = "A beautiful and aesthetic scene related to the text."
            
        return {
            "text": polished_text,
            "explanation": explanation,
            "image_prompt": image_prompt
        }
    except Exception as e:
        return {"error": f"❌ 发生错误: {str(e)}"}

def main():
    print("="*50)
    print("🌍 智能翻译与润色助手已启动！")
    print("不仅仅是翻译，更能让您的表达更加地道、专业。")
    print("="*50)
    
    while True:
        try:
            print("\n" + "-"*30)
            text = input("✍️  请输入需要翻译或润色的文本 (输入 'q' 退出): \n").strip()
            if text.lower() in ['q', 'quit', 'exit']:
                print("再见！👋")
                break
            if not text:
                continue
                
            print("\n可选风格示例：商务正式、学术论文、日常闲聊、小红书种草风、委婉拒信等")
            style = input("🎯 请输入目标风格 (默认: 商务正式): ").strip()
            if not style:
                style = "商务正式"
                
            print("\n⏳ [阶段1] 正在思考并润色文本中...")
            result = translate_and_polish(text, style)
            
            if "error" in result:
                print(result["error"])
                continue
                
            print("\n" + "="*40)
            print("🌟 润色结果：\n" + result["text"])
            print("\n📝 改进说明：\n" + result["explanation"])
            
            print("\n⏳ [阶段2] 正在根据润色结果自动调用大模型生成配图...")
            # 拿到生成的英文提示词，传给图片生成API
            image_prompt = result["image_prompt"]
            image_url = generate_image(image_prompt)
            
            print("\n🎨 为这段文本生成的【社交媒体配图】链接如下：")
            print(f"👉 {image_url}")
            print("="*40)
            
        except KeyboardInterrupt:
            print("\n再见！👋")
            break
        except Exception as e:
            print(f"\n❌ 程序发生异常: {str(e)}")

if __name__ == "__main__":
    main()
