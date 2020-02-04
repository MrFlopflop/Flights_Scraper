# Flights_Scraper
Web scraper that checks flights

1. Make a dictionaty above 'cheapest =...' (line 5)  like so:
myDict = {
    'to': 'Destination',
    'type': 'type', ('retour' or 'enkele'(aka return or single))
    'url1': 'Part_of_url_before_the_first_date',
    'middleBit': 'Part_of_url_between_the_dates', (for return trips, otherwise None)
    'url2': 'Part_of_url_after_dates',
    'price': Price threshhold,
    'toDates': List of dates ('dd-mm-yyyy') you want to depart on,
    'fromDates': List of dates ('dd-mm-yyyy') you want to come back on
}
2. Make a Flight() object above 'driver.quit()' with your dict and the variable cheapest. 
Example: flight = Flight(myDict, cheapest)
3. Run scraper() for your Flight() object right below step 2.
Example: flight.scraper()
