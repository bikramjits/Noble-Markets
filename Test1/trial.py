import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
from tornado.options import define, options
from models import Balance, Base, User 
from sqlalchemy import create_engine, update

#SQLAlchemy Stuff: 
engine = create_engine('sqlite:///sqlalchemy_user.db')

Base.metadata.bind = engine 

from sqlalchemy.orm import sessionmaker 

DBSession = sessionmaker()
DBSession.bind = engine 

session = DBSession()

def data_verify(usern, passw):
    input_user = session.query(User).filter(User.username == usern).first()
    if (input_user is None): 
        return False
    if (input_user.password != passw): 
        return False
    return True

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
        
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')

class LoginHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write("Type in your credentials below to get started!")
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 20:
            self.write('<center>blocked</center>')
            return
        self.render('login.html')

    @tornado.gen.coroutine
    def post(self):
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 20:
            self.write('<center>blocked</center>')
            return
        
        getusername = tornado.escape.xhtml_escape(self.get_argument("username"))
        getpassword = tornado.escape.xhtml_escape(self.get_argument("password"))
        if data_verify(getusername, getpassword):
            input_user = session.query(Balance).filter(User.username == getusername).first()
            self.set_secure_cookie("user", self.get_argument("username"))
            self.set_secure_cookie("incorrect", "0")
            self.redirect(self.reverse_url("main"))
        else:
            incorrect = self.get_secure_cookie("incorrect") or 0
            increased = str(int(incorrect)+1)
            self.set_secure_cookie("incorrect", increased)
            self.write("""<center>
                            Something Wrong With Your Data (%s)<br />
                            <a href="/">Go Home</a>
                          </center>""" % increased)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", self.reverse_url("main")))

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "login_url": "/login",
            'template_path': os.path.join(base_dir, "templates"),
            'static_path': os.path.join(base_dir, "static"),
            'debug':True,
            "xsrf_cookies": True,
        }

        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/", MainHandler, name="main"),
            tornado.web.url(r'/login', LoginHandler, name="login"),
            tornado.web.url(r'/logout', LogoutHandler, name="logout"),
            tornado.web.url(r'/trade', TradeHandler, name="trade"),
        ], **settings)


class TradeHandler(BaseHandler):
   
   def post(self): 
    curr_user = session.query(Balance).filter(Balance.username == "Jack").first()
    trade_amount = float(tornado.escape.xhtml_escape(self.get_argument("amount")))
    to = (tornado.escape.xhtml_escape(self.get_argument("to")))
    to_user = session.query(Balance).filter(Balance.username == to).first()
    print(trade_amount)
    trade_balance = float(curr_user.trading_balance) + float(curr_user.checking_balance)
    print(trade_balance)
    allowed = trade_balance > 1.2 * trade_amount
    if to_user is None: 
        incorrect = self.get_secure_cookie("incorrect") or 0
        increased = str(int(incorrect)+1)
        self.set_secure_cookie("incorrect", increased)
        self.write("""<center>
                        Receiver not in Database. (%s)<br />
                        <a href="/">Go Home</a>
                       </center>""" % increased)

    elif allowed: 
        if float(curr_user.trading_balance) >= trade_amount:  
            curr_user.trading_balance = str(float(curr_user.trading_balance) - trade_amount)
        else: 
            curr_user.trading_balance = '0'
            curr_user.checking_balance = str(float(curr_user.checking_balance) + float(curr_user.trading_balance) - trade_amount)
        to_user.trading_balance = str(float(to_user.trading_balance) + trade_amount)
        session.commit()
        incorrect = self.get_secure_cookie("incorrect") or 0
        increased = str(int(incorrect)+1)
        self.set_secure_cookie("incorrect", increased)
        self.write("""<center>
                        Your transaction was processed! (%s)<br />
                        <a href="/">Go Home</a>
                       </center>""" % increased)

    else:
        need_more = 1.2 * trade_amount - trade_balance 
        incorrect = self.get_secure_cookie("incorrect") or 0
        increased = str(int(incorrect)+1)
        self.set_secure_cookie("incorrect", increased)
        self.write("""<center>
                        You need $$$ to complete this transaction (%s)<br />
                        <a href="/">Go Home</a>
                       </center>""" % increased)


def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()