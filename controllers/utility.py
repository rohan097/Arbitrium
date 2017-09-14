from controllers.modules import *

def tokenizeCokkie(_id):

    """
    function to tokenize cokkie and return it

    @params
    id : mongo user id
    """

    now = datetime.now()
    time = now.strftime("%d-%m-%Y %I:%M %p")

    token = jwt.encode({"id" : str(_id), "time" : time}, secret, algorithm = 'HS256')

    return token

def untokenizeCokkie(token):

    """
    function to untokenize cokkie and return payload from it

    @params
    token : tokenized_cokkie
    """

    payload = jwt.decode(token, verify = False)

    return ObjectId(payload["id"])

def load_csv(fname):

    """
    funtion to load csv file
    """

    df = pd.read_csv(fname)
    return df

def find_KPI(df):

    """
    function to get KPI
    """

    df['year_avg'] = (df['Jan'] + df['Feb']  + df['Mar'] + df['Apr'] + df['May'] + df['Jun'] + df['Jul'] + df['Aug']  + df['Sep']+  df['Oct'] + df['Nov'] + df['Dec'])/12
    df['unique_client'] = df['Customer'] +' ' +  df['Country']
    drop_cols = ['Customer','Country','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for col_ in drop_cols:
        df = df.drop(col_, 1 )
    all_cc = df.unique_client
    all_cc = set(all_cc)
    year_min = np.min(df['Year'])
    year_max = np.max(df['Year'])
    score = []
    for cc in all_cc  :

        dfc = df.loc[df.unique_client == cc ]
        for year in range(year_min, year_max+1):
            dd  = {}
            dd['Client'] = cc
            dd['Client'] = cc
            dfcy1 = dfc.loc[dfc['Year'] == year]

            dd['Year'] = year

            for idx, row in dfcy1.iterrows():
                dd[row['KPI'] ] = row['year_avg']
            score.append(dd)

    final_dicts = []
    for dicti in score:
        dicti['Country'] = (dicti['Client'].split())[-1]
        required_terms_for_kpi_positive = ['Inventory Location Accuracy','On Time Delivery',  'On Time Shipping','Shipping Accuracy']
        required_terms_for_kpi_negative = ['Lost Time Injury Frequency Rate']

        for term_ in required_terms_for_kpi_positive:
            if term_ not in dicti:
                dicti[term_] = 99

        for term_ in required_terms_for_kpi_negative:
            if term_ not in dicti:
                dicti[term_] = 0.01


        dicti['dhl_performance'] = 0.2*dicti['Inventory Location Accuracy'] + 0.2*dicti['On Time Delivery'] +  0.2*dicti['On Time Shipping'] + 0.2*dicti['Shipping Accuracy']+ 0.2*(100-dicti['Lost Time Injury Frequency Rate'])
        dicti['dhl_performance_normed '] = ((0.2*dicti['Inventory Location Accuracy'] + 0.2*dicti['On Time Delivery'] +  0.2*dicti['On Time Shipping'] + 0.2*dicti['Shipping Accuracy']+ 0.2*(100-dicti['Lost Time Injury Frequency Rate']))-96)/3.87

        final_dicts.append(dicti)

    ans_json = { }
    for sc in  final_dicts:
        if 'dhl_performance' in sc:
            if sc['Client'] not in ans_json  :
                ans_json[sc['Client']] =  sc['dhl_performance']
                ans_json[sc['Client'] + "_norm"] =  100*((sc['dhl_performance']-96)/3.87)



    modular_json = {}
    for i in ans_json:
        cname = i.split()[:-1]
        cname =  ' '.join(cname)
        country = i.split()[-1]
        if cname not  in modular_json:
                modular_json[cname] = {}

        if 'norm' in country:
            modular_json[cname][country.split('_')[0]] = ans_json[i]

    for cname in modular_json:
        ss  = 0.001
        cnt = 0
        for cc in modular_json[cname]:
            ss = ss + modular_json[cname][cc]
            cnt = cnt +1
        cnt = max(cnt,1)
        modular_json[cname]['avg'] =  ss/cnt

    return modular_json


def renderKPI(fname):

    """
    main KPI render funtion
    """

    df = load_csv(fname)
    js = find_KPI(df)
    return js

def strip_whitespace(df):

    """
    funtion to strip whitespaces
    """

    for i in df.columns:
        for j in range(len(df[i])):
            try:
                df[i][j] = df[i][j].strip()
            except AttributeError:
                pass
    df.replace(['-'], 0, inplace=True)
    return df


def map_columns(df):

    """
    function to map columns
    """

    df['Status'].replace(
        to_replace={'1. Gain': 1, '2. Opportunity': 0.7, '3. Potential Opps': 0.5, '4. Early Lead': 0, '5. Lost': 0,
                    '7. Cancelled': 0}, inplace=True)
    df['Opp Type'].replace(to_replace={'1. New': 'New', '2. Renewal': 'Renewal'}, inplace=True)
    df['BCA_Status'].replace(
        to_replace={'Approved': 1, 'Transactional': 0.7, 'Awaiting Approval': 0.5, 'Not started': 0, 0: 0.5},
        inplace=True)
    df['Contract Term'].replace(
        to_replace={'< 1 Year': 1, '2-3 Years': 2.5, '3-5 Years': 4, '1-2 Years': 1.5, '7+ Years': 7}, inplace=True)
    df = df.fillna(0)
    df['Milestone'].replace(
        to_replace={'Closed - Lost': -1,
                    'Verbal Customer Commitment Received': 0.7,
                    'Qualified and signed off by Sponsor': 0.8,
                    'Potential Opportunity': 0.3,
                    'Contract Signed': 1,
                    'Closed - Canceled': -1,
                    'Customer commitment– Move to gain': 1,
                    'Early Lead': 0,
                    'Proposal and solution fit presented': 0.5,
                    'Proposal (incl. COO & COS) signed off': 0.6,
                    'Shortlisted': 0.5,
                    'Data quality assessment conducted': 0.3}, inplace=True)
    return df


def date_time(df):

    df['Created'] = pd.to_datetime(df['Created'], format="%d/%m/%Y")
    df['Date Exp Gain'] = pd.to_datetime(df['Date Exp Gain'], format="%d/%m/%Y")
    for i in range(len(df['Go Live Date'])):
        try:
            df['Go Live Date'][i] = pd.to_datetime(df['Go Live Date'][i], format="%d/%m/%Y")
        except ValueError:
            pass
    for i in range(len(df['Cust Dec Date'])):
        try:
            df['Cust Dec Date'][i] = pd.to_datetime(df['Cust Dec Date'][i], format="%d/%m/%Y")
        except ValueError:
            pass

    diff1 = []
    for i, j in zip(df['Go Live Date'], df['Date Exp Gain']):
        try:
            diff1.append(abs((i - j).days))
        except TypeError:
            diff1.append(0)
    # Find difference between Created and Customer Dec Date
    diff2 = []
    for i, j in zip(df['Cust Dec Date'], df['Created']):
        try:
            diff2.append(abs((i - j).days))
        except TypeError:
            diff2.append(0)

    df['Live-Exp'] = pd.Series(np.array(diff1), index=df.index)
    df['Created-Dec'] = pd.Series(np.array(diff2), index=df.index)
    return df


def remove_cols(df):

    df = df.drop(['Opp No', 'Opp Type', 'Region', 'Country', 'BU', 'Sector', 'Customer', 'Product',
                  'Cust Dec Date', 'Go Live Date', 'Created', 'Date Exp Gain'], axis=1)
    return df


def arrange(df):

    df = df[['Customer Group', 'Status', 'Payment Terms', 'Contract Term', 'Milestone', 'BCA_Status',
            'Ann Rev', 'Ann GP', 'Live-Exp', 'Created-Dec', 'Prob to win %']]
    return df


def rename_cols(df):

    for i in df.columns:
        if 'Rev' in i:
            df = df.rename(columns={i: 'Ann Rev'})
        elif 'GP' in i:
            df = df.rename(columns={i: 'Ann GP'})
    for i in df.columns:
        df = df.rename(columns={i: i.strip()})
    return df

def create_json(df):

    json_file = dict({})
    headers = df.columns
    for i in df['Customer Group'].unique():
        values = []
        for j in df[df['Customer Group'] == i].values:
            temp_dict = dict({})
            for k in range(len(headers) - 1):
                temp_dict[headers[k+1]] = j[k+1]
            values.append(temp_dict)
        json_file[i.replace(" ", "_").lower()] = values

    return json_file

def clean_data(fname):

    df = load_csv(fname)
    df = map_columns(df)
    df = date_time(df)
    df = remove_cols(df)
    df = rename_cols(df)
    df = arrange(df)
    df = strip_whitespace(df)
    df = create_json(df)
    return df


def renderTrain(fname):

    df = clean_data(fname)
    return df


if __name__ == '__main__':
    main()
