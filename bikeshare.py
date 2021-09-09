# Student details - Programming for Data Science Aug 2021
# Analysis of Bikeshare data for Chicago, Washington and New York City, based off 2017 data (Jan-June)
# This is an interactive python program which runs via a console and asks the user for input to determine filters
# There are 3 csv files for each city (chicago.csv, new_york_city.csv, washington.csv)
# The csv files need to be saved to the same location as this Python script

import time
import pandas as pd
import numpy as np

# Dictionary of file names for each city
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def bike_graphic():
    """
    bike logo in asci
    """
    print('-' * 80)
    print("--       __@                 __@                          __~@'               --")
    print("--    _`\<,_              _`\<,_                       _`\<,_'                --")
    print("--  (*)/ (*)            (*)/ (*)                     (*)/ (*)'                --")
    print('-' * 80)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington), using a while loop to handle invalid inputs
    print('We have data from 2017 available for three cities: Chicago, New York City and Washington')
    while True:
        try:
            city = input('Enter the city name you are interested in: ')
            city = city.lower()
        except ValueError:
            print('Not a valid choice.')
            # lets try again... Return to the start of the loop
            continue

        # lets check to see if they entered a valid city
        if city in ('chicago', 'new york city', 'washington'):
            # we have a valid city, exit loop.
            break
        else:
            print('Sorry, not one of the cities we have data for.')
            continue

    # Get user input for month (all, january, february, ... , june)
    print('\nWe have data for the first 6 months of the year - January, February, March, April, May & June')
    while True:
        try:
            month = input("Specify a month or enter 'All' to see data for January to June: ")
            month = month.lower()
        except ValueError:
            print('Not a valid choice.')
            continue

        # checking to see if they entered a valid month
        if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            break
        else:
            print('Sorry, this is not one of the months have data for.')
            # we have a valid month, exit loop.
            continue

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("\nEnter a day to filter the data by day, or 'All' to see data for the whole week: ")
            day = day.lower()
        except ValueError:
            print('Not a valid choice.')
            # better try again... Return to the start of the loop
            continue

        # Check to see if a valid day was entered
        if day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            break
        else:
            print("Sorry, not a valid day.")
            continue

    print('Retrieving data for', city.title(), '+', month.title(), '+', day.title())
    print('-' * 80)
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

    # convert the Start Time and End time columns to datetime values for later calculations
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time and store in new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if it has been set
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the Most Frequent Times of Travel....\n')
    start_time = time.time()

    # Display the most common month, first determine if dataframe only contains data for one month
    df['month'] = pd.to_datetime(df['month'], format='%m').dt.month_name()  # determine the full month name
    common_month = df['month'].mode().to_string(index=False)
    unique_month_count = df['month'].nunique()  # to see if there is more than 1 month in the df

    if unique_month_count != 1:
        print('The most common month was: ', common_month)

    else:
        print('Printing data for',
              common_month)  # here the user selected one month to view data, which is by default the common_month

    # Display the most common day of week
    common_day = df['day_of_week'].mode().to_string(index=False)
    unique_day_count = df['day_of_week'].nunique()  # to see if there is more than 1 day in the df

    if unique_day_count != 1:
        print('The most popular day was: ', common_day)
    else:
        print('Calculating data for', common_day + 's in',
              common_month)  # in this case the user selected one day to view data, it is by default the common_day

    # Display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode().to_string(index=False)
    popular_trips = df['Hour'].value_counts().max()
    print('The most popular hour for cycling was:', (common_hour + ':00,'), '   number of trips: ', popular_trips)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station and count
    common_start = df['Start Station'].mode().to_string(index=False)
    common_start_value = df['Start Station'].value_counts().max()
    print('The most commonly used starting station was: ', common_start, '      Count:', common_start_value)

    # Display most commonly used end station and count
    common_end = df['End Station'].mode().to_string(index=False)
    common_end_value = df['End Station'].value_counts().max()
    print('The most common end station was: ', common_end, '        Count:', common_end_value)

    # Display most frequent combination of start station and end station trip using a new column in the df
    df['journey_details'] = 'Start ' + df['Start Station'] + ' to end ' + df['End Station']
    common_trip = df['journey_details'].mode().values  # using values function here so full trip details display
    print('The most frequent combination of start station and end station trip was: ', common_trip)

    # Display the least popular start station and count
    least_start = df['Start Station'].value_counts().idxmin()
    least_start_value = df['Start Station'].value_counts().min()
    print('The least popular starting station was: ', least_start, '      Count:', least_start_value)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    df['total_travel_time'] = df['End Time'] - df['Start Time']
    total_time_for_everyone = df['total_travel_time'].sum()
    print('The total travel time for all the trips was: ', total_time_for_everyone)

    # Display mean travel time
    mean_travel_time = df['total_travel_time'].mean()
    print('The average trip duration was: ', mean_travel_time)

    # Display the shortest trip duration
    min_travel_time = df['total_travel_time'].min()
    print('The shortest trip time was: ', min_travel_time)

    # Display the longest trip duration
    max_travel_time = df['total_travel_time'].max()
    print('The longest trip time was: ', max_travel_time)

    # Display how many trips were taken
    total_trips = len(df.index)
    print('The total number of trips for this time period was: ', total_trips)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types, all of the dataframes should have this value
    print('\n')
    print(df['User Type'].value_counts().to_frame())

    # Display counts of gender only for chicago and new york city
    if 'Gender' in df.columns:
        print('\n')
        print(df['Gender'].value_counts().to_frame())
    else:
        print('\nNo gender data for this city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df['Birth Year'] = df['Birth Year'].astype('Int64')
        earliest_year = df['Birth Year'].min()
        print('\n\nThe earliest recorded birth year was: ', earliest_year)

        max_year = df['Birth Year'].max()
        print('\n\nThe most recent birth year was: ', max_year)

        common_birthyear = df['Birth Year'].mode().to_string(index=False)
        print('\n\nThe most common birth year was: ', common_birthyear)

        # lets calculate and display the most popular ages using bikeshare
        df['Age'] = 2017 - df['Birth Year']  # calculating age at 2017 data source
        df['Age'] = df['Age'].astype('Int64')  # turn age into an integer column to make it display nicer
        print('\n\nHere are the most popular ages for the people using Bikeshare during this time period: ')
        print(df['Age'].value_counts().head(15).to_frame())

        # lets display the least popular ages that went on bikeshare trips
        print('\nThese ages took the least amount of trips:')
        print(df['Age'].value_counts().tail().to_frame())

        # lets work out the average age
        average_age = df['Age'].mean()
        print('\n\nThe average age was: ', int(average_age))

        # lets work out the median age
        median_age = df['Age'].median()
        print('\n\nThe median age was: ', int(median_age))

    else:
        print('\nNo Birth Year data for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def raw_data(df):
    """Displays raw data to the user, 5 rows at at time from the df."""

    print('Raw data is available for the above statistics')
    # Iterate through the raw data using a while loop to handle invalid inputs
    start_loc = 0
    while True:
        try:
            view_data = input('Would you like to view 5 rows of raw data? Enter yes or no: ')
            view_data = view_data.lower()
        except ValueError:
            print('Not a valid choice.')
            # try again... Return to the start of the loop
            continue

        # lets print 5 lines of the dataframe
        if view_data == 'yes':
            print('Here are 5 rows of data:')
            print(df.columns)
            print((df.iloc[start_loc:start_loc + 5]).values)
            # use the values function to show all of the data, just printing the dataframe will not display all data
            # print((df.iloc[start_loc:start_loc + 5]).to_dict('index')) - other option that doesn't display as neatly
            start_loc += 5

            continue
        else:
            break


def main():
    while True:
        bike_graphic()
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart the program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
