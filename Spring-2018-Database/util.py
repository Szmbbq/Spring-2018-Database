# def flightSearchValidation(request):
#     return (request.form['departure_city'] or request.form['departure_airport']) and\
#         (request.form['destination_city'] or request.form['destination_airport']) and\
#         (request.form['date'])

def flightSearchValidation(request):
    return request.form['departure_airport'] and request.form['arrival_airport'] and\
        request.form['departure_date']

# def flightSearchQuery(form):
#     query = 'SELECT * FROM flight WHERE date = %s' % form['date']
#     for key, value in form.items():
#         if value and key != 'date':
#             query += ' and ' + key + ' = %s'
#             query = query % value
#     return query

def flightSearchQuery(request):
    return 'SELECT * FROM flight WHERE departure_time LIKE %s and departure_airport = %s and arrival_airport = %s',\
    (request.form['departure_date'] + '%', request.form['departure_airport'], request.form['arrival_airport'])




def showFlightsOfAirlineCo(cursor, airline_name, in_n_days = None, start_time = None, end_time = None):
    if in_n_days:
        query = 'SELECT * FROM flight WHERE departure_time >= NOW() and departure_time < NOW() + INTERVAL %s DAY and airline_name = %s'
        cursor.execute(query, (in_n_days, airline_name))
    elif start_time and end_time:
        query = 'SELECT * FROM flight WHERE departure_time >= %s and departure_time < %s and airline_name = %s'
        cursor.execute(query, (start_time, end_time, airline_name))
    data = cursor.fetchall()
    return data


def showAirplanesOfAirlineCo(cursor, airline_name):
    query = 'SELECT * FROM airplane WHERE airline_name = %s'
    cursor.execute(query, airline_name)
    data = cursor.fetchall()
    return data


def queryForTopDestinations(interval):
    if interval == 'MONTH':
        query = ('SELECT airport_city, COUNT(*) AS ticket_sold '
                 'FROM (SELECT airport_city, arrival_airport '
                       'FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, airport '
                       'WHERE airline_name = %s AND departure_time >= NOW() - INTERVAL 3 MONTH AND arrival_airport = airport_name) AS T '
                 'GROUP BY airport_city '
                 'ORDER BY ticket_sold DESC '
                 'LIMIT 3')
    else:
        query = ('SELECT airport_city, COUNT(*) AS ticket_sold '
                 'FROM (SELECT airport_city, arrival_airport '
                       'FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, airport '
                       'WHERE airline_name = %s AND departure_time >= NOW() - INTERVAL 1 YEAR AND arrival_airport = airport_name) AS T '
                 'GROUP BY airport_city '
                 'ORDER BY ticket_sold DESC '
                 'LIMIT 3')
    return query

    