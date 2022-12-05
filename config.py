import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

#print(TOKEN, ADMIN_ID)