from dotenv import load_dotenv
load_dotenv()


testConfig = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './myTesTdatabase.sqlite3'
    }
}
