import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import requests
import os
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
async def generate_confusion(theme: str):
    client = InferenceClient(
        api_key=HUGGINGFACE_API_KEY
    )

    messages = [
        {
        "role": "user",
        "content": f"生成一个迷惑行为。迷惑行为的定义是普通行为 + 反向逻辑 + 奇怪目的。- 普通行为：一个日常生活中常见的行为，比如吃饭、睡觉、工作、学习、运动、娱乐等。 - 反向逻辑：与普通行为的预期不符或相反。例如：\n早晨用咖啡洗脸，宣称这是抗疲劳护肤新方式。\n在老板总结时，突然站起来背诵圆周率。\n边开会边用望远镜看同事。\n\n不要重复指令，不要解释，用中文回答，省略思考。\n以主题'{theme}'生成一个迷惑行为。迷惑行为："
                    f"随机编号: {random.randint(1, 100000)}"
    }
    ]

    completion = client.chat.completions.create(
    model="google/gemma-2-9b-it", 
	messages=messages, 
	temperature=1.2,
	max_tokens=100,
	top_p=0.8,
    stop=["/n"]
)

    print(completion.choices[0].message)
    result = completion.choices[0].message.content
   
    if result:
        return {"confusion": result}
    else:
        raise HTTPException(status_code=500, detail="Invalid response from model")
    
