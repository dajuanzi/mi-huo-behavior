import random
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


@app.post("/generate_confusion/")
async def generate_confusion(theme: str = ""):
    client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

    messages = [
        {
            "role": "user",
            "content": f"""生成一个迷惑行为。通常用来形容那些看起来匪夷所思、不合常理或者让人难以理解的行为或言论。它包含了一种调侃和娱乐的成分，常常被用来形容让人摸不着头脑的场景或人类奇怪的举动。
例如：
早晨用咖啡洗脸，宣称这是抗疲劳护肤新方式。
在老板总结时，突然站起来背诵圆周率。
边开会边用望远镜看同事。

不要重复指令，不要解释，用中文回答，省略思考。

生成一个迷惑行为。"""
            f"随机编号: {random.randint(1, 100000)}",
        }
    ]

    completion = client.chat.completions.create(
        model="google/gemma-2-9b-it",
        messages=messages,
        temperature=1.5,
        max_tokens=100,
        top_p=0.7,
        stop=["/n"],
    )

    print(completion.choices[0].message)
    result = completion.choices[0].message.content

    if result:
        return {"confusion": result}
    else:
        raise HTTPException(status_code=500, detail="Invalid response from model")
