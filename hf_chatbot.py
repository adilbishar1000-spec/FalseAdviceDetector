import os
# Fix for Vercel's read-only file system
os.environ['HOME'] = '/tmp'
os.environ['USERPROFILE'] = '/tmp'

import g4f
from g4f.client import Client

def hf_explain(text):
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful medical myth analyzer. Keep answers to 2 concise sentences explaining why the advice is dangerous or misleading."},
                {"role": "user", "content": f"Health advice: {text}"}
            ]
        )
        reply = response.choices[0].message.content
        return reply.strip() or "No explanation returned."
    except Exception as e:
        return f"⚠️ Free AI unavailable currently: {str(e)}"