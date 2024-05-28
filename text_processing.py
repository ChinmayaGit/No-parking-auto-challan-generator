# text_processing.py

import re

# Function to clean the recognized text and keep only alphanumeric characters
def clean_text(text):
    # Remove special characters
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)

    # Remove 'IND' if present
    cleaned_text = cleaned_text.replace('IND', '')

    # Check if the last four characters are numeric, keep the entire string
    if cleaned_text[-4:].isdigit() and len(cleaned_text) <= 10:
        return cleaned_text
    else:
        return ''


# Function to check if the recognized text contains the specified format
def contains_license_plate_format(text):
    num_alpha = sum(c.isalpha() for c in text)
    num_digit = sum(c.isdigit() for c in text)
    num_dash_dot = text.count('-') + text.count('.')

    return (
        10 <= len(text) <= 14 and
        text[0:2] in ('MH','PB','GJ','RJ','AN','AP','AR','AS','BH','BR','CH','CG','DD','GL','GA','GJ','HR','HP','JK','JH','KA','KL','LA','LD','MP','MN','ML','MZ','NL','OD','PY','SK','TN','TS','TR','UP','UK','WB') and
        num_alpha >= 4 and
        num_digit >= 6 and
        num_alpha + num_digit + num_dash_dot == len(text)
    )
