"""
Jun 2023

Using scraper instead of Google Play Console API
https://github.com/JoMingyu/google-play-scraper

"""
from google_play_scraper import Sort, reviews_all
import csv
import pycountry
#country_names = [country.alpha_2 for country in pycountry.countries]
#languages = [language.alpha_3 for language in pycountry.languages]
country_names = ['hk','tw','us','cn']
languages = ['en','zh']
# Define the CSV file path
csv_file = 'output.csv'

# Open the CSV file in write mode
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row to the CSV file
    writer.writerow(['Review ID', 'User Name', 'User Image', 'Content', 'Rating', 'ThumbsUp', 'Reviewed App Version', 'Review Time', 'Reply', 'Reply Time', 'App Version', 'Language', 'Country'])

    # Iterate over the countries and languages
    for country in country_names:
        for language in languages:
            result = reviews_all(
                'package',
                lang=language,
                country=country
            )

            # Write each review to the CSV file
            for review in result:
                writer.writerow([review['reviewId'], review['userName'], review['userImage'], review['content'], review['score'], review['thumbsUpCount'], review['reviewCreatedVersion'], review['at'], review['replyContent'], review['repliedAt'], review['appVersion'], language, country])

print(f"Data successfully written to {csv_file}")