# App Review Extraction to CSV

This repository provides simple Python scripts to gather and process public reviews of apps from both the Apple App Store and Google Play Store, exporting the data to flat CSV files.

---

## Apple App Store Example

Fetch the latest 500 reviews for a given app and save them as a CSV. The API is paginated, with up to 10 pages of results:

```python
no_of_pages = 10
country = "hk"
review_id = 1234567890
all_reviews = get_and_collect_reviews(review_id, no_of_pages)
save_reviews(all_reviews, define_csv_file_name())
```

### Apple App Store Review API

App Store reviews are publicly accessible through an RSS endpoint:

```
https://itunes.apple.com/{country}/rss/customerreviews/id={appid}/page={pageno}/sortby=mostrecent/json
```

- `country`: The App Store country code (e.g., gb).
- `page_no`: Page number for paginated results.
- `app_id`: The app's numeric ID from its App Store URL.

The included Python script retrieves these reviews using the `requests` library, flattens the nested JSON structure, and saves them as a CSV.

See [example_apple_reviews.json](example_apple_reviews.json) for an example API response format.

---

## Google Play Store Example

### Using `google-play-scraper`

Adjust the values of `country_names`, `languages`, and `package` in the script as needed.

---

### Google Play Store Review API

Currently, the processing script expects the review API response to be saved as JSON before further processing. However, you can process the response directly if loaded as a variable (e.g. `reviews_j`):

```python
# Flatten reviews and save to CSV
all_review_data = process_json(reviews_j)
save_reviews(all_review_data, define_csv_file_name())

# Optionally work with plain Python dictionaries/lists
for review in all_review_data:
    print(review["review_id"], review["star_rating"])
```

To access Google Play reviews via the Play Console API, you'll need a service account private key (OAuth2 credentials provided by your app admin). Example usage in Python:

```python
from google.oauth2 import service_account
from apiclient.discovery import build

# TODO: Read credentials from a JSON file and assign as a dictionary to 'credentials_dict'

try:
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
except Exception as e:
    print(e)
    return

try:
    service = build('androidpublisher', 'v3', credentials=credentials)
    response = service.reviews().list(packageName='uk.organisation.appname.production').execute()
except Exception as e:
    print(e)
    return

if 'reviews' not in response or not response['reviews']:
    print('No reviews available')
else:
    print('Reviews detected.')
    # Save or process the response, e.g., with json.dumps(response)
    ...
```

For API response details, consult the [Google Review API documentation](https://developers.google.com/android-publisher/api-ref/rest/v3/reviews).
