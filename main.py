# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import smtplib
import datetime as dt
import random
import pandas
import sys
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

# get today's date
now = dt.datetime.now()
today_month = now.month
today_day = now.day
today = (today_month, today_day)


# read birthdays from csv file using Pandas
try:
    data_frame = pandas.read_csv("birthdays.csv")
except FileNotFoundError:
    print("File not found.")
    sys.exit(1)
else:
    birthdays_dict = {(row.month, row.day): row for (index, row) in data_frame.iterrows()}
    print(birthdays_dict)

# match today's date with any birthdays in birthdays_dict
if today in birthdays_dict:
    birthday_person = birthdays_dict[today]
    person_name = birthday_person["name"]
    person_email = birthday_person["email"]

    letter_num = random.randint(1, 3)
    try:
        with open(f"letter_templates/letter_{letter_num}.txt", "r") as data:
            letter = data.read()
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)

    # replace [NAME] with name; using .replace() must be saved to a new variable
    updated_letter = letter.replace("[NAME]", person_name)

    # send email
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=f"{person_email}",
                msg=f"Subject: Happy Birthday!\n\n{updated_letter}"
            )
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    else:
        print("No birthday's match today's date.")
