from ad_controle_financeiro_bot.telegramBot import TelegramBot
from ad_controle_financeiro_bot.driveBot import DriveBot

#bot = TelegramBot()
#bot.start()

driveBot = DriveBot()
print(driveBot.get_data())