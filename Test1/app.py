#http://www.tornadoweb.org/en/stable/guide/security.html

import tornado.ioloop
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello! Please sign in below.")

class LoginHandler(BaseHandler):
    def get(self):
        #The Login Page
        self.write('<html><body><form action="/login" method="post">'
                   'Username: <input type="text" name="name">'
                   'Password: <input type="password" name="pass">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

        #If Password is wrong. 
        # if self.current_user is None: 
        # 	self.write("Wrong Username/ Password! Please try again.")

    def post(self):
        getusername = tornado.escape.xhtml_escape(self.get_argument("name"))
        getpassword = tornado.escape.xhtml_escape(self.get_argument("pass"))
        if "demo" == getusername and "demo" == getpassword:
            self.set_secure_cookie("user", self.get_argument("name"))
            self.set_secure_cookie("incorrect", "0")
            self.redirect("/")
        else:
            incorrect = self.get_secure_cookie("incorrect") or 0
            increased = str(int(incorrect)+1)
            self.set_secure_cookie("incorrect", increased)
            self.write("""<center>
                            Something Wrong With Your Data (%s)<br />
                            <a href="/">Go Home</a>
                          </center>""" % increased)
        


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()