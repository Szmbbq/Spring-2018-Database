from datetime import datetime
from dateutil.relativedelta import relativedelta




today = datetime.today().strftime('%Y-%m-%d %H:%M')
one_yr_ago = datetime.now() - relativedelta(years=1)
one_yr_ago = one_yr_ago.strftime('%Y-%m-%d')

def flightsQuery():
    query = 'SELECT F.* FROM purchases P LEFT JOIN ticket T ON T.ticket_id = P.ticket_id LEFT JOIN flight F ON (F.airline_name, F.flight_num) =(T.airline_name, T.flight_num) WHERE P.customer_email = %s AND( F.departure_time BETWEEN %s AND %s )'
    return query

def upcomingFlightsQuerry(ID):
    query = 'SELECT F.* FROM purchases P LEFT JOIN ticket T ON T.ticket_id = P.ticket_id LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num) WHERE P.customer_email = %s AND F.departure_time >= %s'
    return query,(ID,today)

def defaultSpendingQuerry(ID):
    query = 'SELECT SUM(F.price) AS spending FROM purchases P LEFT JOIN ticket T ON T.ticket_id = P.ticket_id LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num) WHERE P.customer_email = %s AND (P.purchase_date BETWEEN %s AND %s)'
    return query,(ID,one_yr_ago,today)

def spendingQuerry():
    query = 'SELECT SUM(F.price) AS spending FROM purchases P LEFT JOIN ticket T ON T.ticket_id = P.ticket_id LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num) WHERE P.customer_email = %s AND (P.purchase_date BETWEEN %s AND %s)'
    return query

