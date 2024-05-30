import aiohttp
import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta, timezone
from fw import get_secret, get_config

# Load secrets and config once
secret = get_secret()
config = get_config()

headers = {
    "Accept": "application/json",
    "authorization": f"Bearer {secret.clash_royale_token}"
}

intents = discord.Intents.default()
intents.message_content = True

class MyClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.send_removal_list_task = None

    async def on_ready(self):
        print("Bot is ready.")
        channel = self.get_channel(secret.channel_id)
        if channel:
            await channel.send("Sentinel is online...")
            print("Sent 'Sentinel is online...' message to the channel.")
            await self.send_removal_list()  # Manually trigger the removal list for testing
        else:
            print("Channel not found.")

    async def setup_hook(self):
        self.send_removal_list_task = self.loop.create_task(self.start_send_removal_list())

    async def start_send_removal_list(self):
        await self.wait_until_ready()
        self.send_removal_list.start()

    @tasks.loop(hours=168)  # Run once a week
    async def send_removal_list(self):
        try:
            print("Fetching clan data...")
            clan_data = await self.fetch_clan_data()
            if clan_data:
                print("Clan data fetched successfully.")
                members_to_remove = self.filter_members(clan_data)
                print(f"Filtered members: {members_to_remove}")
                removal_list = self.format_removal_list(members_to_remove)
                print(f"Formatted removal list: {removal_list}")

                channel = self.get_channel(secret.channel_id)
                if channel:
                    await channel.send(removal_list)
                    print("Sent removal list to the channel.")
                else:
                    print("Channel not found when sending removal list.")
            else:
                print("No clan data found.")
        except Exception as e:
            print(f"An error occurred while sending the removal list: {e}")

    async def fetch_clan_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(secret.clash_royale_api_base + f'/clans/%23{config.clanID}', headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to fetch clan data. Status code: {response.status}")
                    return None

    def filter_members(self, clan_data):
        member_list = clan_data['memberList']
        now = datetime.now(timezone.utc)
        days_threshold = now - timedelta(days=config.days_threshold)
        members_to_remove = [
            member for member in member_list 
            if member['donations'] == config.donation_threshold
            and member['clanChestPoints'] == config.clanChestPoints_threshold
            and datetime.strptime(member['lastSeen'], '%Y%m%dT%H%M%S.%fZ').replace(tzinfo=timezone.utc) < days_threshold
        ]
        return sorted(members_to_remove, key=lambda x: datetime.strptime(x['lastSeen'], '%Y%m%dT%H%M%S.%fZ').replace(tzinfo=timezone.utc))

    def format_removal_list(self, members):
        if not members:
            return "No members to be removed."
        thresholds_info = f"Thresholds: Last Seen <= {config.days_threshold} days ago, Donations = 0, Clan Chest Points = 0\n"
        members_info = "Members to be removed:\n" + "\n".join(
            [f"{member['name']} (Last Seen: {datetime.strptime(member['lastSeen'], '%Y%m%dT%H%M%S.%fZ').replace(tzinfo=timezone.utc).strftime('%m-%d-%Y')})"
             for member in members])
        return thresholds_info + members_info

client = MyClient(command_prefix="!", intents=intents)
client.run(secret.discord_token)
