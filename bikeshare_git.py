import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    cities= {"chicago":1, "new york city":2,"washington":3}
    
    while True:
        try:
            city_input = input('Would you like to see data for Chicago, New York City or Washington?\n')
            city= city_input.lower()
            if city in cities:
                print("Looks like you would like to see data of {} city". format(city_input)) 
                break
            else:
                raise error
        except:
            print('Opps, we do not have data of this city, please choose a valid city')
    
    
    # get user input for month (all, january, february, ... , june)
    month_filter= ["january", "february","march","april","may","june"]   
    while True:
        try:
            entered_filter_raw= input("Would you like to filter the data by month, day, both(month and day) or not at all? Enter \"none\" for no time filter\n")
            entered_filter= entered_filter_raw.lower()
            if entered_filter == 'both':
                month_input_raw=input('Please choose a month,and please keep in mind we have only first 6 months data\n')    
                month_input= month_input_raw.lower()
                if month_input in month_filter:
                    month = month_filter.index(month_input)+1
                    day=int(input('Please choose a day from 1 to 31 of selected month\n'))
                    if month_input== 'february' and day>28:
                        print('Opps, {} have only 28 days' . format(month_input))
                        raise error
                    elif month_input== 'april' or month_input=='june' and day>30:
                        print('Opps, {} have only 30 days' . format(month_input))
                        raise error    
                    elif day > 0 and day <= 31:
                        print("You have selected month and day")
                        break
                    else:
                        raise error
                else:
                    raise error
                    
            elif entered_filter == 'month':
                month_input_raw=input('Please choose a month, type month name in lower case like january, please keep in mind we have only first 6 months data\n')    
                month_input= month_input_raw.lower()
                if month_input in month_filter:
                    month = month_filter.index(month_input)+1 
                    day= 0
                    break
                else:
                    raise error
    # get user input for day (1 to 31)
            elif entered_filter == 'day':
                day=int(input('Please choose a day from 1 to 31 of selected month\n'))
                if day > 0 and day <= 31:
                    month= 0
                    break
                else:
                    raise error
            elif entered_filter =='none':
                day= 0
                month= 0
                break
            else:
                 raise error
                
        except:
            print("Please enter valid filter conditions as explained in question.")
    

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
    
    filename = (CITY_DATA[city])

    # load data file into a dataframe
    main_data = pd.read_csv(filename)
    
    main_data['month_data']=main_data['Start Time'].str[5:7] #learned from reference_2
    main_data['day_data']=main_data['Start Time'].str[8:10] #learned from reference_2

    # filtering by month
    if month <=7 and month >0 and day>0:
        pd.options.mode.chained_assignment = None  # taken from reference_1
        new_month= '0{}'. format(month)
        if day<10:
            new_day= '0{}'. format(day)
        else:
            new_day= '{}'. format(day)
        df_initial=main_data[main_data['month_data']== new_month]
        df=df_initial[df_initial['day_data']== new_day]
    elif month <=7 and month >0 and day== 0:
        pd.options.mode.chained_assignment = None  # taken from reference_1
        new_month= '0{}'. format(month)
        df=main_data[main_data['month_data']== new_month]
    #filtering by day
    elif month== 0 and day> 0:
        pd.options.mode.chained_assignment = None  # taken from reference_1
        if day<10:
            new_day= '0{}'. format(day)
        else:
            new_day= '{}'. format(day)

        df=main_data[main_data['day_data']== new_day]
    else:
        df= main_data

        
    """Adding new columns to washington.csv for gender and birth year which is not available in document."""
    if city=='washington':
        df['Gender']= 'No data available'
        df['Birth Year']= 'No data available'
 
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time']) #taken from udacity practice questions

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour #taken from udacity practice solution_1

    # find the most popular hour
    popular_hour = df['hour'].mode()[0] #taken from udacity practice solution_1

    print('Most Popular Start Hour:', popular_hour) #taken from udacity practice solution_1
    
    # display the most common month
    popular_month = df['month_data'].mode()[0]
    print('\nMost Popular Month In Selection: {}\n'. format (popular_month))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station: {}'. format(popular_station))

    # display most commonly used end station
    popular_station_end = df['End Station'].mode()[0]
    print('\nMost Popular End Station: {}' . format(popular_station_end))

    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_total = df['Trip Duration'].sum()/3600
    print('\nTotal Trip Duration: {} hours'. format(travel_total))

    # display mean travel time
    travel_mean = df['Trip Duration'].mean()/60
    print('\nAverage Trip Duration: {} minutes'. format(travel_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts() # taken from Udacity practice solution_2

    print('\nUser types:\n')
    print(user_types)

    # Display counts of gender

    gender = df['Gender'].value_counts() 
    print('\nGender Distribution:\n')
    print(gender)
    # Display earliest, most recent, and most common year of birth
    birth_year_max = df['Birth Year'].min()
    birth_year_min = df['Birth Year'].max()
    birth_year_common = df['Birth Year'].mode()[0] 

    print('\nThe oldest user\'s birth date: {}'. format(birth_year_max))
    print('\nThe youngest user\'s birth date: {}'. format(birth_year_min))
    print('\nCommon birth year among users: {}'. format(birth_year_common))
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    
    
    """Asking user if they want to see raw data""" 
    show_data=input("\nWould you like to see the first five rows of raw data? Enter yes or no.\n")
    if show_data=='yes':
        print(df.head())
        i=5        
        while True:
            show_data_remaining= input('\nWould you like to see more five rows? Enter yes or no.\n')
            if show_data_remaining=='yes':
                i+= 5
                print(df.head(i))        
            else:
                print('Raw Data Will Not Be Shown Anymore')
                break
    else:
        print('Raw Data Will Not Be Shown')
        
    
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
