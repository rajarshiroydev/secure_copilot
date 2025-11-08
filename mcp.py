import asyncio
import os
from dotenv import load_dotenv

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

load_dotenv()

composio = Composio(
    api_key=os.getenv("COMPOSIO_API_KEY"), provider=OpenAIAgentsProvider()
)

externalUserId = "roystark.dev@gmail.com"

# Delete the old connection first (optional but recommended)
# composio.connected_accounts.delete(connected_account_id="ca_G_BWH0nP_uyO")

# Create new connection with updated scopes
connection_request = composio.connected_accounts.link(
    user_id=externalUserId,
    auth_config_id="ac_sPfAAtVlsPfI",  # This should now have the send scope
)

redirect_url = connection_request.redirect_url
print(f"Please authorize the app by visiting this URL: {redirect_url}")

# Wait for the connection to be established
connected_account = connection_request.wait_for_connection()
print(
    f"Connection established successfully! Connected account id: {connected_account.id}"
)

# Get Gmail tools
tools = composio.tools.get(user_id=externalUserId, tools=["GMAIL_SEND_EMAIL"])

agent = Agent(
    name="Email Manager",
    model="litellm/gemini/gemini-2.5-flash",
    instructions="""You are a helpful assistant for gmail related tasks. 
    When sending emails, use roystark.dev@gmail.com as the sender email address.""",
    tools=tools,
)


async def main():
    result = await Runner.run(
        starting_agent=agent,
        input="Send an email to roystark.dev@gmail.com with the subject 'Hello from composio 👋🏻' and the body 'Congratulations on sending your first email using AI Agents and Composio!'",
    )
    print(result.final_output)


asyncio.run(main())
