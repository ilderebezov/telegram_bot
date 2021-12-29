import logging
from aiohttp import web
from pyngrok import ngrok
import requests
from src.service import routes
from src.ngrok import authtoken
from src.api.status.data import TOKEN


def main():
    """Инициализация приложения."""
    ngrok.set_auth_token(authtoken)
    http_tunnel = ngrok.connect(8080)
    ssh_tunnel = ngrok.connect(8080, "tcp")
    link_to_tunnel = ngrok.connect(8080, bind_tls=True).data['public_url']
    link_to_tunnel += str('/')
    del_url = 'https://api.telegram.org/bot'
    del_url += TOKEN
    del_url +='/deleteWebhook'
    set_url = 'https://api.telegram.org/bot'
    set_url += TOKEN
    set_url +='/setWebhook?url='
    set_url += link_to_tunnel
    requests.get(del_url)
    requests.get(set_url)
    app = web.Application()
    logging.basicConfig(filename='log_file',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logging.info("Running Urban Planning")
    logging.getLogger('urbanGUI')
    routes.setup_routes(app)
    web.run_app(app, host='0.0.0.0', port=8080)
    ngrok.disconnect(http_tunnel.public_url)


if __name__ == '__main__':
    main()
