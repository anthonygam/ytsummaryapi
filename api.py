import asyncio
from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from concurrent.futures import ThreadPoolExecutor
from google import genai
from os import getenv

app = FastAPI()
formatter = TextFormatter()
executor = ThreadPoolExecutor()
ytt_api = YouTubeTranscriptApi()
gemini_api = genai.Client(api_key = getenv('GEMINI_API_KEY'))


def prompt(transcript: str) -> str:
    return \
        "Please write a brief summary of the following YouTube" + \
        "video transcript:\n" + transcript


async def fetch_transcript(video_id: str) -> str:
    try:
        loop = asyncio.get_running_loop()
        transcript = await loop.run_in_executor(
            executor, lambda: ytt_api.fetch(video_id)
        )
        return formatter.format_transcript(transcript)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f'Transcript error: {str(e)}'
        )


async def summarise_transcript(transcript: str) -> str:
    result = await gemini_api.aio.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt(transcript)
    )
    return result.text


@app.get('/')
async def root():
    return {
        'message': 'Hello World'
    }


@app.get('/transcript/{video_id}')
async def summarise(video_id: str):
    transcript = await fetch_transcript(video_id)
    summary = await summarise_transcript(transcript)
    return summary


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
