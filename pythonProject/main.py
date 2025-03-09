from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import csv

initialPage = urlopen("https://www.identifyyourbreyer.com/identify/traditional.htm").read()
pattern = r'^[^\/\\]*\.htm$'
soup = BeautifulSoup(initialPage, 'html.parser')
links = []
for link in soup.find_all('a', href=re.compile(pattern)):
    links.append(link.get('href'))

with open('table_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    header_written = False  # Flag to check if the header has been written
    for link in links:
        page = urlopen('https://www.identifyyourbreyer.com/identify/' + link).read()
        soup = BeautifulSoup(page, 'html.parser')

        # Extract text after the dash in the title
        title_tag = soup.find('title')
        if title_tag:
            model_name = title_tag.get_text(strip=True).split('-')[-1].strip()
        else:
            model_name = None

        table = soup.find('table', attrs={'border': '1', 'cellpadding': '4', 'cellspacing': '0'})
        # Extract data from the table
        if table:
            rows = table.find_all('tr')
            if rows:
                # Get the first row (header row)
                header_row = rows[0].find_all(['td', 'th'])
                header_data = [model_name]  # Add model name at the start
                header_data += [cell.get_text(strip=True) for cell in header_row[4:]]  # Ignore first four columns
                if not header_written:
                    # Write the header row only once
                    writer.writerow(header_data)
                    header_written = True

                # Write the rest of the rows (excluding the first row)
                for row in rows[1:]:
                    cells = row.find_all(['td', 'th'])
                    cells = cells[4:]  # Ignore first four columns
                    row_data = [model_name] + [cell.get_text(strip=True) for cell in
                                               cells]  # Add model name at the start
                    writer.writerow(row_data)
