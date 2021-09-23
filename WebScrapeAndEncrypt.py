import requests
from bs4 import BeautifulSoup
import csv
import os
from cryptography.fernet import Fernet

# Get webpage and parse contents.
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
job_elements = results.find_all("div", class_="card-content")

# Write to csv file.
os.mkdir('output')
output_csv_file_name = 'output/all_saved_jobs.csv'
csv_header = ['job_title', 'company', 'location']
with open(output_csv_file_name, 'w', encoding='UTF8', newline='') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow(csv_header)

	for job_element in job_elements:
		title_element = job_element.find("h2", class_="title")
		company_element = job_element.find("h3", class_="company")
		location_element = job_element.find("p", class_="location")
		new_row_data = [title_element.text.strip(), company_element.text.strip(), location_element.text.strip()]
		writer.writerow(new_row_data)

# Generate fernet key required for encryption.
key = Fernet.generate_key()
with open('output/keyfile.key', 'wb') as keyfile:
	keyfile.write(key)
	
with open('output/keyfile.key', 'rb') as keyfile:
	key = keyfile.read()
	
fernet = Fernet(key)

# Encrypt csv file contents.
encrypted_csv_file_name = 'output/encrypted_all_saved_jobs.csv'
with open(output_csv_file_name, 'rb') as file:
	original = file.read()
	
encrypted = fernet.encrypt(original)

with open(encrypted_csv_file_name, 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
	
# Unencrypt csv file contents.
unencrypted_csv_file_name = 'output/unencrypted_all_saved_jobs.csv'
with open(encrypted_csv_file_name, 'rb') as encrypted_file:
	encrypted = encrypted_file.read()
	
decrypted = fernet.decrypt(encrypted)

with open(unencrypted_csv_file_name, 'wb') as decrypted_file:
	decrypted_file.write(decrypted)
