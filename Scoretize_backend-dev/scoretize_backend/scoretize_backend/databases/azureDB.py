from dotenv import load_dotenv
import os
load_dotenv()

azureConfig = {
    'default': {
        'ENGINE': 'mssql',
        'HOST': os.environ['HOST'],
        'USER': os.environ['USER_NAME'],
        'PASSWORD': os.environ['PASSWORD'],
        'NAME': os.environ['DB_NAME'],
        'OPTIONS': {
            'driver': os.environ['DRIVER'],
        },
    }
}
