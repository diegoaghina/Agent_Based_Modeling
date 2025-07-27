import asyncio
from chat_agent import ChatAgent
from config_keys import MAX_MESSAGES
from config_keys import password
from spade.message import Message

async def main():
    trump = ChatAgent("fakebot.@xmpp.jp", password)
    trump.partner_jid = "receive.-_-@xmpp.jp"
    trump.kickoff = True  # This tells it to start the chat

    joebiden = ChatAgent("receive.-_-@xmpp.jp", password)
    joebiden.partner_jid = "fakebot.@xmpp.jp"

    await trump.start()
    await joebiden.start()

    # Wait briefly for both agents to be fully ready
    await asyncio.sleep(2)

    # Kick off debate
    kickoff = Message(to=joebiden.jid)
    kickoff.set_metadata("performative", "inform")
    kickoff.body = "Let's talk about inflation. What are you doing to fix it?"
    await trump.behaviours[0].send(kickoff)
    print(f"[{trump.name}] Sent kickoff message.")

    # Allow time for chatting
    await asyncio.sleep(20)

    await trump.stop()
    await joebiden.stop()

if __name__ == "__main__":
    asyncio.run(main())