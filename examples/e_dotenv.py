import os
import dotenv

dotenv.load_dotenv()
env = os.getenv("EXAMPLE")
host = os.getenv("HOST")
auth = os.getenv("AUTH")
id = os.getenv("ID")

print(env)
# example
print(__name__)
# examples.e_dotenv
# note: import 方式不改变这个值。

