import requests
from bs4 import BeautifulSoup
import pandas as pd

class DataDownloader:

    def Test():
        print("Sử dụng class thành công")

    def Cao_du_lieu(url):
        response = requests.get(url)

        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        job_listings = soup.find_all(class_='job card')
        titles = []
        links = []
        names = []
        salarys = []
        locations = []

        for job_listing in job_listings:

            job_title = job_listing.find('a').text
            job_link = job_listing.find('a')['href']
            company_name = job_listing.find(class_ = 'company').text
            salary = job_listing.find(class_ = 'salary').text
            location = job_listing.find(class_ = 'location').text

            titles.append(job_title)
            links.append(job_link)
            names.append(company_name)
            salarys.append(salary)
            locations.append(location)

            print(f'Job title: {job_title}')
            print(f'Job link: {job_link}')
            print(f'Company name: {company_name}')
            print(f'Salary: {salary}')
            print(f'Location: {location}')
            print('\n')

        dic = {'title': titles, 'link': links, 'name': names, 'salary': salarys, 'location': locations}
        df = pd.DataFrame(dic)
        print(df.head(10))
