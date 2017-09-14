"""
module to storing all the routes
"""

from controllers import *

routes = [
    (
        r"/login",
        login.LoginHandler
    ),
    (
        r"/logout",
        logout.LogoutHandler
    ),
    (
        r"/",
        index.IndexHandler
    ),
    (
        r"/getchurn",
        churn_predict.ChurnPredictHandler
    ),
    (
        r"/company/(\w+)",
        company.CompanyHandler
    ),
    (
        r"/newCompany",
        addCompany.AddCompanyHandler
    )
]
