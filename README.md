# App Review Code to CSV

Simple code to allow the gathering and processing of public reviews of apps on the Apple App Store and Google Play Store APIs.

### Example Use for App Store 
The following code will go get the last 500 reviews and process the JSON response into a flat CSV file. Results from the api are paginated up to a maximum of 10 pages
```
    no_of_pages = 10
    country = "hk"
    review_id = 1234567890
    all_reviews = get_and_collect_reviews(review_id, no_of_pages) 
    save_reviews(all_reviews, define_csv_file_name() )
```

## The Apple App Store Review API
Reviews on published apps in the Apple App store are openly available. A limited number of reviews can be accessed via a rss call to: 

https://itunes.apple.com/{country}/rss/customerreviews/id={appid}/page={pageno}/sortby=mostrecent/json

- country is the App Store country where you sell it, e.g. gb
- page_no is the page of the data to return - data is from paginated
- app_id is the number following "id" in the App Store URL

The example Python code calls the API the requests library. The resulting nested JSON is flattened and saves as a CSV file.

An example of format returned by the API is give in the [example_apple_reviews.json](https://github.com/datasciencecampus/app_review/blob/master/get_review_data/example_apple_reviews.json) file

### Example Use for Play Store
The processing code currently assumes the response has been saved as a JSON file and then loaded before further processing. The review data could be processed directly from the response above. Assuming the JSON has been loaded to a variable ```reviews_j```:

```
# Process the reviews toa flast file
all_review_data = process_json(review_j)

# You can save the reviews to CSV file directly
save_reviews(all_review_data, define_csv_file_name())

# Or convert to a Pandas dataframe abnd manipluate as required
all_reviews = pd.DataFrame(all_review_data)
```



## The Google Play Store Review API
The Google Play reviews are accessed via the Play Console using a private key using oauth2. This should be generated by the app administrator on the Google Play Console. Accessing the Google Play API within Python can be acheived using

```
    from google.oauth2 import service_account
    from apiclient.discovery import build
    
    # TODO: read in the credentials from a JSON file, converyt to dict and assign to 'credentials_dict'
    
    try:
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    except Exception as e:
         print(e) 
         return   
    # Get list of reviews using googleapiclient.discovery
    try:      
        service = googleapiclient.discovery.build('androidpublisher', 'v3', credentials=credentials)
        response = service.reviews().list(packageName='uk.organisation.appname.production').execute()
    except Exception as e:
         print(e) 
         return
  
    if not 'reviews' in response or len(response['reviews']) == 0:
        print('No reviews available')
    else:
        print('Reviews detected.')
        # Save or process the response, e.g. save the json.dumps(response) to a JSON file
        ...

```
For the format and details of the returned data please see the [Google Review API Documnetation](https://developers.google.com/android-publisher/api-ref/rest/v3/reviews)
