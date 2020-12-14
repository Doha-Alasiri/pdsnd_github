import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            'Would you like to see data for Chicago, New York City, or Washington? \n').lower()
        if city == 'chicago':
            print('\nlooks like you want to see data for Chicago!\n')
            break

        elif city == 'new york city':
            print('\nlooks like you want to see data for New York City!\n')
            break

        elif city == 'washington':
            print('\nlooks like you want to see data for Washington!\n')
            break

        else:
            print('Something went wrong! Make sure to enter a valid city.\n')
            continue

    # get user input for month and day of week

    while True:
        filter_by = input(
            "Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter.\n").lower()
        if filter_by == 'month':
            print('We\'re filtering by month..\n')
            month = input(
                'Which month - January, February, March, April, May, or June?\n').lower()
            day = None
            while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                print('Invalid month!')
                month = input(
                'Which month - January, February, March, April, May, or June?\n').lower()
            break

        elif filter_by == 'day':
            print('We\'re filtering by day..\n')
            day = input(
                'Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
            month = None
            while day not in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
                print('Invalid day!')
                day = input(
                'Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
            break

        elif filter_by == 'both':
            print('We\'re filtering by both month and day!\n')
            month = input(
                'Which month - January, February, March, April, May, or June?\n').lower()
            while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                print('Invalid month!')
                month = input(
                'Which month - January, February, March, April, May, or June?\n').lower()
            day = input(
                'Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
            while day not in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
                print('Invalid day!')
                day = input(
                'Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
            break

        elif filter_by == 'none':
            month = None
            day = None
            print('No time filter was applied!')
            break

        else:
            print(
                'Something went wrong! Make sure to enter one of the options (month - day - none).\n')
            continue


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all' and month != None:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all' and day != None:
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print("Most common month: ", common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("Most common day is: ", common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most common hour is: ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station is: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print('Most Common End Station is: ', common_end_station)

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + " to " + df['End Station']
    frq_comb_start_end = df['Start and End Station'].value_counts().idxmax()
    print('Most Frequent Combination of Start Station and End Station: ', frq_comb_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time = ', total_travel_time, 'seconds.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time = ', mean_travel_time, 'seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('Counts of User Type:\n', count_user_types)

    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        print('\n\nCounts of Gender:\n', count_gender)
    except:
        print('\n\nInformation about gender are not available in this city')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min().astype(int)
        print('\n\nEarliest Birth Year is:', earliest_birth_year)
        recent_birth_year = df['Birth Year'].max().astype(int)
        print('Most Recent Birth Year is:', recent_birth_year)
        common_birth_year = df['Birth Year'].value_counts().idxmax().astype(int)
        print('Most Common Birth Year is:', common_birth_year)
    except:
        print('\nBirth Year Information are not available in this city\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():


    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask to show row data
        raw_data = input('\nDo you want to see the raw data? Enter "yes" or "no".\n')
        while raw_data.lower() == 'yes':
            data_iterator = pd.read_csv(CITY_DATA[city], chunksize = 5)
            print(next(data_iterator))
            raw_data = input('\nDo you want to see more of the data? Enter "yes" or "no".\n')



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
