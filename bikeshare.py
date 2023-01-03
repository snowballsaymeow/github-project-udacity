import time
import pandas as pd
import numpy as np
 
CITY_DATA = { 'chicago': 'datasets/chicago.csv',
              'new york city': 'datasets/new_york_city.csv',
              'washington': 'datasets/washington.csv' }
MONTH_DATA = {'all': 0, 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
DAY_DATA = {'monday': 0, 'tuesday': 1, 'wednesday': 2,'thursday': 3,  'friday': 4, 'saturday': 5, 'sunday': 6, 'all': 7}
 
 
def check_data_entry(prompt, valid_entries): 
    """
    Asks user to type some input and verify if the entry typed is valid.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()
 
        while user_input not in valid_entries : 
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()
 
        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input
 
    except:
        print('Seems like there is an issue with your input')
 
 
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
 
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, CITY_DATA.keys())
 
    # get user input for month (all, january, february, ... , june)
    prompt_month =  "Which month? All, January, February, March, April, May, or June? "
    month = check_data_entry(prompt_month, MONTH_DATA.keys())
 
    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt_day = "Which day? All, Monday, Tuesday, ..., Sunday? "
    day = check_data_entry(prompt_day, DAY_DATA.keys())
 
    print('-'*40)
    return city, month, day
 
 
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
 
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
 
    # create columns: month (int) and day (int)
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
 
    # filter by month and day
    if month != 'all':
        df = df[df['month']==MONTH_DATA[month]]
 
    if day != 'all':
        df = df[df['day']==DAY_DATA[day]]
    return df
 
 
def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
 
    Args:
        (DataFrame) df - The data frame you want to work with.
    Returns:
        None
    """
 
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    int2month = {key: value for value, key in MONTH_DATA.items()}
    int2day = {key: value for value, key in DAY_DATA.items()}
 
    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f"The most common month: {int2month[popular_month].title()}")
 
 
    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print(f"The most common day of week: {int2day[popular_day].title()}")
 
 
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"The most common start hour: {popular_hour}")
 
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
 
def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
 
    Args:
        (DataFrame) df - The data frame you want to work with.
    Returns:
        None
    """
 
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
 
    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print(f"Most commly used start station: {most_start_station}")
 
 
    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print(f"Most commly used end station: {most_end_station}")
 
    # display most frequent combination of start station and end station trip
    df['Station Trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    most_station_trip = df['Station Trip'].mode()[0]
    print(f"Most frequent combination of start station and end station strip: {most_station_trip}")
 
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
 
def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
 
    Args:
        (DataFrame) df - The data frame you want to work with.
    Returns:
        None
    """
 
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
 
    # display total travel time
    print(f"Totol travel time: {df['Trip Duration'].sum()} s")
 
 
    # display mean travel time
    print(f"Mean travel time: {df['Trip Duration'].mean()} s")
 
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
 
def user_stats(df):
    """
    Displays statistics on bikeshare users.
 
    Args:
        (DataFrame) df - The data frame you want to work with.
    Returns:
        None
    """
 
    print('\nCalculating User Stats...\n')
    start_time = time.time()
 
    # Display counts of user types
    print(f"Counts of user types:\n{df['User Type'].value_counts()} ")
 
 
    # Display counts of gender
    try:
        print(f"Counts of user types:\n{df['Gender'].value_counts()} ")
    except:
        print("There is no 'Gender' column in this file.")
 
 
    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"The earliest year of birth: {earliest}\nThe most recent year of birth: {recent}\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")
 
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
 
def display_data(df):
    """
    Displays 5 rows of data from the csv file for the selected city.
 
    Args:
        (DataFrame) df - The data frame you want to work with.
    Returns:
        None
    """
    promt_view_data = "Would you like to view 5 rows of individual trip data? Enter yes or no: "
    is_view_data = check_data_entry(promt_view_data, ["yes", "no"])
    index = 0
    while is_view_data == 'yes':
        print(df.iloc[index:index+5])
        index += 5
        if index > len(df):
            promt_review_data = "Have seen all the data, do you want to see it again? Enter yes or no: "
            is_review_data = check_data_entry(promt_review_data, ["yes", "no"])
            if is_review_data == 'yes':
                index = 0
            else:
                break
        is_view_data = check_data_entry(promt_view_data, ["yes", "no"])
    print('-'*40)
 
 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
 
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
 
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
 
 
if __name__ == "__main__":
	main()