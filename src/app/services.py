import asyncio
from openai import AsyncOpenAI

from src.app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
assistant_id = settings.ASSISTANT_ID


async def create_new_thread(message_text):
    new_thread = await client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": message_text
            },
        ]
    )
    return new_thread.id


async def create_new_message(thread_id, message_text):
    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_text
    )


async def create_new_run(thread_id):
    return await client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )


async def get_response(thread_id, run):

    while run.status != 'completed':
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        await asyncio.sleep(5)

    messages = await client.beta.threads.messages.list(thread_id, limit=1)
    return messages.data[0].content[0].text.value

    # async with client.beta.threads.runs.stream(
    #   thread_id=thread_id,
    #   assistant_id=assistant_id,
    #   event_handler=EventHandler(),
    # ) as stream:
    #     stream.until_done()
    #     print(stream)
    #