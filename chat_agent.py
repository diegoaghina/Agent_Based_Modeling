from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from config_keys import MAX_MESSAGES, OPENAI_API_KEY, PROFILE_PROMPTS
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


class ChatAgent(Agent):
    class ChatBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.counter = 0

        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                print(f"[{self.agent.name}] Received: {msg.body}")
                self.counter += 1

                if self.counter < MAX_MESSAGES:
                    # Get OpenAI response
                    openai_reply = await self.query_openai(msg.body)

                    # Send to other agent
                    reply = Message(to=self.agent.partner_jid)
                    reply.body = openai_reply
                    await self.send(reply)
                    print(f"[{self.agent.name}] Sent: {openai_reply}")
                else:
                    print(f"[{self.agent.name}] Done chatting.")
                    await self.agent.stop()
            else:
                await asyncio.sleep(1)

        async def query_openai(self, user_input):
            profile_prompt = PROFILE_PROMPTS.get(str(self.agent.name), "You are a helpful assistant.")
            try:
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": profile_prompt},
                        {"role": "user", "content": user_input}
                    ]
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"[OpenAI Error]: {e}"   

    async def setup(self):
        print(f"{self.name} is starting.")
        self.add_behaviour(self.ChatBehaviour())
