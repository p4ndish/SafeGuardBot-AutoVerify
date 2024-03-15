import asyncio
import json
import os
import re 
from time import sleep
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, InviteHashExpiredError
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberUnoccupiedError
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import StartBotRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon import functions, types
from verifier import Verifier
load_dotenv()
apiId = os.environ.get("apiId")
apiHash = os.environ.get("apiHash")



class TelegramBot:
    def __init__(self, session_name, api_id, api_hash):
        self.client = TelegramClient(session_name, api_id, api_hash)
        
        self.success_list = []

    def failed_groups(self, group_name):
        with open("failed_groups.txt", "+a") as f: 

            f.write(f"{group_name}\n")
            f.close() 

    async def join_private_group(self, invite_link, group_name):
        try:
            # Join the channel using the invite link
            await self.client(ImportChatInviteRequest(invite_link))
            print(f"[+] Joined the channel using invite link: {invite_link}")
            self.success_list.append(group_name)
        except (UserAlreadyParticipantError,InviteHashExpiredError) as e:
            print(f"[-] {e} ")
            self.failed_groups(group_name)

    async def check_for_unread_msg(self, group_name):
        user_id_or_username = 'http://t.me/SafeguardRobot'
        unread_messages = []
        dialogs = await self.client.get_dialogs(limit=4) 
        for dialog in dialogs: 
            if dialog.is_user and dialog.entity.bot: 
                if dialog.unread_count > 0:
                    msg = dialog.message.message
                    await dialog.message.mark_read() 
                    if "Verified, you" in msg :
                        # print("in")
                        regex = re.findall(r"https://t.me/.*", msg)
                        link = regex[0].split("https://t.me/+")
                        await self.join_private_group(link[-1], group_name)
                        # return link
                        # print(regex)
                        
                        return True 
                    else:
                        print("[-] Verification failed, retry later for: ",group_name )
                        self.failed_groups(group_name)
                    
                # print(dialog.unread_count)
                # print(dialog.message.message)
                break 
        return unread_messages

    async def join_safeguard_bot(self, bot_link, param, group_name):
        a = await self.client.send_message("http://t.me/SafeguardRobot", f"/{param}")
        print("[+] Message sent")

        # run verify process 
        async def main():
            f = open("sessions.json")
            localstorage_data = json.load(f)
            # print(localstorage_data)
            c = Verifier(localstorage_data)
            value = await c.browse()
            print("final result: ", value)

            if value == True: 
                print("[+] Now Joining group...")
                await self.check_for_unread_msg(group_name)
            else:
                print(f"[x] Failed for {group_name}... \n\t[-] Adding it to failed channels" )
                self.failed_groups(group_name)

        await main()


        
        # info = await self.client.get_entity(bot_link)
        # messages = await self.client.get_messages(info, limit=1)

        # print(messages[0].reply_markup.rows[0].buttons[0].url)

    async def join_given_channel(self, channel_username):
        try:
            result = await self.client(JoinChannelRequest(channel=channel_username))
            print(f"[+] Joined the channel: {channel_username}")
            channel_entity = await self.client.get_entity(channel_username)
            messages = await self.client.get_messages(channel_entity, limit=10)
            for message in messages:
                if message.reply_markup:
                    #for debuging 
                    # print("->", message.reply_markup.rows[0].buttons[0].url)
                    return message.reply_markup.rows[0].buttons[0].url.split("?")[-1]
        except Exception as e:
            print(f"[-] Error joining the channel: {e}")

    async def main(self):
        me = await self.client.get_me()
        # await self.check_for_unread_msg()
        bot_link = "http://t.me/SafeguardRobot"
        
        channel_username = ["chainpulseapp","MumuTheBullPortal","gorillainacoupe_eth", ]
        for channel in channel_username:
            param = await self.join_given_channel(channel)
            # param = f"/{param}"
            # print(param)
            print("[+] Working On: ", channel)
            await self.join_safeguard_bot(bot_link, param, channel)
        
        print("Successfully joined the channels:")
        for c in self.success_list:
            print(c) 

if __name__ == "__main__":
    bot = TelegramBot('projectUpwork', apiId, apiHash)
    with bot.client:
        bot.client.loop.run_until_complete(bot.main())