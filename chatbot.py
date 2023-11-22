import openai
from openai import OpenAI
import os
import time
import json

def show_json(obj):
    print(json.loads(obj.model_dump_json()))

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
assistant = os.getenv('ASSISTANT_KEY')
client = OpenAI()
sheila = client.beta.assistants.retrieve(
    assistant_id=assistant
)
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_answer(question):
    thread = client.beta.threads.create(
    )
    create_message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role= "user",
        content= f"{question} You can answer this question based off of the PDF file you have access to. NOTHING ELSE"
    )
    message = client.beta.threads.messages.retrieve(
        thread_id =thread.id,
        message_id = create_message.id
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=sheila.id,
        model="gpt-4-1106-preview",
        instructions="please be very respectful",
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}]
    )

    run = wait_on_run(run, thread) 
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    assistant_message = next((msg for msg in messages.data if msg.role == 'assistant'), None)
    
    if assistant_message:
        answer = assistant_message.content[0].text.value
        return answer
    else:
        return "no message found"
        

    
    
    
    


