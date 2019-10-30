# python3
from sanic import Sanic, response
from sanic.response import html
import sanic_cookiesession
from wechat.wx_thread import WxThead
from wechat.wx_status import WxStatus

app = Sanic(__name__)
# app.static("/", "./page")
app.config['SESSION_COOKIE_SECRET_KEY'] = 'rookie'
sanic_cookiesession.setup(app)
wx_status = WxStatus()


@app.route("/")
async def index(request):
    return html(open('./page/index.html').read())


@app.route("/favicon.ico")
async def ico(request):
    return html(open('./page/favicon.ico').read())


@app.route("/jquery.min.js")
async def jquery(request):
    return html(open('./page/jquery.min.js').read())


@app.route("/login")
async def start_wecaht(request):
    wxthread = WxThead(wx_status)
    wxthread.setDaemon(True)
    wxthread.start()
    return response.text("susscess")


@app.route("/check_status")
def get_qrcode(request):
    return response.json({"status": wx_status.get().value[0], "info": wx_status.userInfo})


app.run(host="127.0.0.1", port=8888)
