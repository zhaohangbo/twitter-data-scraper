# Twitter Data Srapeer


# 步骤一：授权

## 创建Twitter Application，并获取秘钥

Sign up for developer credentials and create a Twitter app here:

	https://apps.twitter.com/

Twitter will provide you `consumer_key` and `consumer_secret`

To authorize your application, run:

	python twitter-authorize.py


## 把 Tokens 添加到 config.py 文件
Then add your consumer and access tokens to `config.py`

```
consumer_key = 'coTnUn4Fqhx66640TFvn'
consumer_secret = '76zIesJIh0fwc666WDIlM8PseCp3iKixiNSUCq8efP'
access_key = '88727857996663lKnfj1GlPv5Uw8ztLJruAllyL2i'
access_secret = 'RK9ll8Jl6666FCEtfrdTN7GDbEcdlQYqbILndd'
```

# 步骤二：爬数据

## Case 1: Scrape Twitter Data

```
python scrape_twitter_data.py --twitter_name "President Trump"
```

## Case 2: Search Twitter Data
```
python search_twitter_data.py --search_words "President Trump"
```
