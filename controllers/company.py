from controllers.modules import *
from controllers.utility import *

class CompanyHandler(RequestHandler):

    """
    class resposible to render the dashbaord
    route : /company/company_name
    """

    @coroutine
    @removeslash
    def get(self, com_name):

        token = self.get_secure_cookie('token')
        if token:
            _id = untokenizeCokkie(token)
            isValidtkn = yield db.tokens.find_one({"token" : token, "_uid" : _id})
            if isValidtkn:

                com_data = yield db.company.find_one({"key" : com_name})
                cursor = db.company.find()
                companies = []
                while (yield cursor.fetch_next):
                    doc = cursor.next_object()
                    companies.append([doc["key"], doc["name"]])

                # change this line to the live_stock_data api ip
                stk = requests.post("http://localhost:8080/getdata/" + com_name + "?timestamp=5year")
                stk = json.dumps(stk.json()["data"])

                kpi = com_data["kpi"]
                cagr = com_data["cagr"]

                twitter = int((requests.get("http://104.236.108.87:5000/").json()[com_name])*100)

                avg = cagr["1010"]
                del(cagr["1010"])

                temp = []
                for i in cagr:
                    temp.append([int(i), cagr[i]])
                cagr = temp

                data = {
                        "companies" : companies,
                        "kpi" : kpi,
                        "cagr" : cagr,
                        "stk" : stk,
                        "name" : com_data["name"],
                        "id" : com_name,
                        "show" : 2,
                        "twitter" : twitter,
                        "comb" : int(twitter + avg),
                        "val" : 50
                        }

                self.render("index.html", data = data)
            else:
                self.redirect("/login?invalid_token=true")
        else:
            self.redirect("/login?loggedin=false")
