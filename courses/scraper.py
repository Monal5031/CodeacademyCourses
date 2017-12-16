from bs4 import BeautifulSoup
import re
import urllib.request, urllib.parse, urllib.error

regex_course = r'([a-zA-z]+)</h5>'
regex_percent = r'style=\"width:([0-9]+)%\"></div>'
general_url = 'https://www.codeacademy.com/{username}'


def fetch_data(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    url_handle = urllib.request.urlopen(req)
    # Data we read is not unicode so we need to decode
    data = url_handle.read().decode()
    return data


def parse_data(data):
    html_data = BeautifulSoup(data, 'html.parser')

    # Course names are present in the h5 tag
    # will need some updates here to filter based on class
    completed_courses = html_data('h5')

    # Course percentages are present in a div
    # with a class = 'progress_bar_complete'
    course_percentage = html_data.find_all('div', class_='progress__bar__complete')

    # List of all the courses with tuples of course_name and its percent completed
    courses = []

    for course, percent in zip(completed_courses, course_percentage):
        # Splitting with space gives 3 strings, 3rd one contains
        # course name, retrieved the course_name using the regex
        # defined above
        course_name = str(course).split()[2]
        course_name = re.findall(regex_course, course_name)[0]

        # Splitting with space gives 3 strings, 3rd one contains
        # percent_value, retrieved the percent_value using
        # the regex defined above
        percent_value = str(percent).split()[2]
        percent_value = re.findall(regex_percent, percent_value)[0]

        # append course_name and percent_value as tuple
        courses.append((course_name, percent_value))
    print(courses)
    return courses


class Scrape:

    def __init__(self, username=''):
        if username is '':
            raise AttributeError('Username cannot be empty')
        elif type(username) is not str:
            raise AssertionError('Need only string username')
        self.username = username
        self.url = general_url.format(username=username)
        self.data = fetch_data(self.url)
        self.courses = parse_data(self.data)

    def __str__(self):
        return self.url


