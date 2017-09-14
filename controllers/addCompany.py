from controllers.modules import *
from controllers.utility import *

class AddCompanyHandler(RequestHandler):

    """
    class resposible to add new company to database
    route : /newCompany
    """

    def upload(self, fle):
        extn = os.path.splitext(fle['filename'])[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(cname, 'wb')
        print(fle['body'])
        fh.write(fle['body'])
        fh.close()
        return cname

    @coroutine
    @removeslash
    def post(self):

        token = self.get_secure_cookie('token')
        if token:
            _id = untokenizeCokkie(token)
            isValidtkn = yield db.tokens.find_one({"token" : token, "_uid" : _id})
            if isValidtkn:

                com_key = self.get_argument("com_key")
                com_name = self.get_argument("com_name")
                com_symbol = self.get_argument("com_symbol")

                kpi_file = self.request.files["kpi"][0]
                train_file = self.request.files["train"][0]
                cname = self.upload(kpi_file)
                kpi = renderKPI(cname)
                os.remove(cname)
                cname = self.upload(train_file)
                train = renderTrain(cname)
                os.remove(cname)

                temp = yield db.company.insert({
                    "key" : com_key,
                    "name" : com_name,
                    "symbol" : com_symbol,
                    "kpi" : kpi
                })

                temp = yield db.train.insert(train)

                self.redirect("/company/ford")
            else:
                self.redirect("/login?invalid_token=true")
        else:
            self.redirect("/login?loggedin=false")
