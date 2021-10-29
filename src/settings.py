import os
import dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_file = os.path.join(BASE_DIR, "../.env")


if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
    KAFKA_SERVICE_URI = os.environ.get('KAFKA_SERVICE_URI')
    KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
    POSTGRESQL_URI = os.environ.get('POSTGRESQL_URI')
