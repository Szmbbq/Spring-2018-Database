from datetime import datetime
from dateutil.relativedelta import relativedelta

today = datetime.today().strftime('%Y-%m-%d %H:%M')
one_mon_ago = datetime.now() - relativedelta(days=30)
one_mon_ago = one_mon_ago.strftime('%Y-%m-%d')

    
def upcomingAgentFlights(agent_id):
    query = 'SELECT P.customer_email,F.* FROM purchases P LEFT JOIN ticket T ON T.ticket_id = P.ticket_id LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num) WHERE P.booking_agent_id = %s AND F.departure_time >= %s'
    return query,(agent_id,today)

def commissionQuery(agent_id):
    query = "SELECT 0.1*SUM(F.price) AS commission\
                FROM purchases P LEFT JOIN booking_agent B ON P.customer_email = B.email\
				LEFT JOIN ticket T ON T.ticket_id = P.ticket_id\
                LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num)\
                WHERE P.booking_agent_id = %s AND (P.purchase_date BETWEEN %s AND %s)"
    return query,(agent_id,one_mon_ago,today)

def numTickQuery(agent_id):
    query = 'SELECT COUNT(T.ticket_id) AS num_ticket\
                FROM purchases P LEFT JOIN booking_agent B ON P.customer_email = B.email\
                LEFT JOIN ticket T ON T.ticket_id = P.ticket_id\
                LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num)\
                WHERE P.booking_agent_id=%s AND (P.purchase_date BETWEEN %s AND %s)'
    return query,(agent_id,one_mon_ago,today)


def avgComm(agent_id):
    query = 'SELECT 0.1*AVG(F.price) AS avg_comm\
            FROM purchases P LEFT JOIN booking_agent B ON P.customer_email = B.email\
                LEFT JOIN ticket T ON T.ticket_id = P.ticket_id\
                LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num)\
                WHERE P.booking_agent_id=%s AND (P.purchase_date BETWEEN %s AND %s)'
    return query,(agent_id,one_mon_ago,today)       

def custTicket(agent_id):
    six_mon_ago = datetime.now() - relativedelta(months=6)
    six_mon_ago = six_mon_ago.strftime('%Y-%m-%d')
    query = 'SELECT C.email,C.name,COUNT(T.ticket_id) AS num_ticket\
            FROM purchases P LEFT JOIN ticket T ON T.ticket_id = P.ticket_id\
                				LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num)\
                        LEFT JOIN customer C ON C.email = P.customer_email\
                        WHERE P.booking_agent_id = %s AND (P.purchase_date BETWEEN %s AND %s)\
                        GROUP BY C.email\
                        ORDER BY num_ticket DESC\
                        LIMIT 5'
    return query,(agent_id,six_mon_ago,today)

def custComm(agent_id):
    one_yr_ago = datetime.now() - relativedelta(years=1)
    one_yr_ago = one_yr_ago.strftime('%Y-%m-%d')
    query = 'SELECT C.email,C.name,0.1*SUM(F.price) AS commission\
            FROM purchases P LEFT JOIN ticket T ON T.ticket_id = P.ticket_id\
                				LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num)\
                        LEFT JOIN customer C ON C.email = P.customer_email\
                        WHERE P.booking_agent_id = %s AND (P.purchase_date BETWEEN %s AND %s)\
                        GROUP BY C.email\
                        ORDER BY commission DESC\
                        LIMIT 5'
    return query,(agent_id,one_yr_ago,today)            

def viewFlights():
    query = 'SELECT P.customer_email,F.* FROM purchases P LEFT JOIN ticket T ON T.ticket_id = P.ticket_id LEFT JOIN flight F ON (F.airline_name,F.flight_num) = (T.airline_name,T.flight_num) WHERE P.booking_agent_id = %s AND (F.departure_time BETWEEN %s AND %s)'
    return query