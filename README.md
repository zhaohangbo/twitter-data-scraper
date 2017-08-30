# Twitter Data Srapeer

## Usage

You will need to authenticate with Twitter to use these scripts. To do
so, sign up for developer credentials and create a Twitter app here:

	https://apps.twitter.com/

You can create access credentials directly through Twitter's web
interface, authorized under the username you used to create the app.

If you want your application to act on behalf of other users (for example,
to post on behalf of several usernames), you'll need to authorize each
separately. To be guided through this process, run:

	python twitter-authorize.py
	
## Add Tokens to Config
Then add your consumer and access tokens to 
```
config.py
```

## Case 1: Scrape Twitter Data

```
python scrape_twitter_data.py --twitter_name "President Trump"
```

## Case 2: Search Twitter Data
```
python search_twitter_data.py --search_words "President Trump"
```
