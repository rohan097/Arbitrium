from controllers.modules import *

# This calculates the probability win rate for a particular company.
class ChurnPredictHandler(RequestHandler):

    def preprocess(self):

        user_data = []
        if self.oppType == 1:
            user_data.append(1)
            user_data.append(0)

        else:
            user_data.append(0)
            user_data.append(1)

        if self.status == 1:
            user_data.append(1)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)

        elif self.status == 2:
            user_data.append(0)
            user_data.append(1)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)

        elif self.status == 3:
            user_data.append(0)
            user_data.append(0)
            user_data.append(1)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)

        elif self.status == 4:
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(1)
            user_data.append(0)
            user_data.append(0)

        elif self.status == 5:
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(1)
            user_data.append(0)

        else:
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(0)
            user_data.append(1)

        user_data.append(self.payment_terms)
        user_data.append(self.contract_terms)
        user_data.append(self.milestone)

        return user_data

    def post(self):

        self.company = self.get_argument("id")
        self.status = self.get_argument("stat")
        self.milestone = float(self.get_argument("mlstn"))
        self.oppType = int(self.get_argument("opptp"))
        self.payment_terms = int(self.get_argument("pmtterm"))
        self.contract_terms = int(self.get_argument("ctterm"))

        mp = {
            "ford" : "ford",
            "proctor_and_gamble" : "pg",
            "unilever" : "ul",
            "pepsico" : "pep",
            "hewlett_packard" : "hp"
        }

        user_data = {"company" : mp[self.company], "data" : self.preprocess()}
        print (user_data)

        df = pd.read_csv("Clean2.csv", header=None, skiprows=1)
        companies = df[0].unique()
        data = {}
        predictors = {}

        if not(isfile('./controllers/classifiers.sav')):
            for i in range(len(companies)):
                data = df[df[0] == companies[i]]
                data_labels = data.iloc[ : , -1].as_matrix()
                data_train = data.iloc[ : , 1 : -1].as_matrix()
                data_train_data, data_test_data, data_train_labels, data_test_labels = train_test_split(data_train, data_labels)
                predictors[companies[i]] = RandomForestClassifier(n_estimators=200, n_jobs=4)
                predictors[companies[i]].fit(data_train_data, data_train_labels)
            pickle.dump(predictors, open('./controllers/classifiers.sav', 'wb'))
        else:
            predictors=pickle.load(open('./controllers/classifiers.sav', 'rb'))

        probability = predictors[user_data['company']].predict(user_data['data'])
        self.write({"percentage" : int(probability[0])})
