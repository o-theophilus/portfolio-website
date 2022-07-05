from application import create_app
from deta import App
import requests

app = App(create_app())

if __name__ == "__main__":
    app.run()


@app.lib.cron()
def cron(event):
    resp = requests.get('https://meji.deta.dev/cron')
    return resp.json()
