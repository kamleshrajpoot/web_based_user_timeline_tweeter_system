import tweepy
import datetime
import xlsxwriter
import sys
from django.shortcuts import render
from django.shortcuts import redirect




def home(request):
	if request.method == 'POST' and 'btnform1' in request.POST:
		fromdate = request.POST['fromdate']
		todate = request.POST['todate']
		username=request.POST['user_id']
		consumerKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
		consumerSecret = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
		accessToken = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		accessTokenSecret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

		auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
		auth.set_access_token(accessToken, accessTokenSecret)

		api = tweepy.API(auth)
		a=fromdate[0:4]
		a=int(a)
		b=fromdate[5:7]
		b=int(b)
		c=fromdate[9:11]
		c=int(c)
		d=todate[0:4]
		d=int(d)
		e=todate[5:7]
		e=int(e)
		f=todate[9:11]
		f=int(f)

		startDate = datetime.datetime(a,b,c,0,0,0)
		endDate =  datetime.datetime(d,e,f,0,0,0)
		tweets = []
		tmpTweets = api.user_timeline(username)
		for tweet in tmpTweets:
			if tweet.created_at < endDate and tweet.created_at > startDate:
				tweets.append(tweet)

		while (tmpTweets[-1].created_at > startDate):
			tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id)
		for tweet in tmpTweets:
			if tweet.created_at < endDate and tweet.created_at > startDate:
				tweets.append(tweet)

		workbook = xlsxwriter.Workbook("/home/kamleshsisodiya/Desktop/"+username + ".xlsx")
		worksheet = workbook.add_worksheet()
		row = 0

		for tweet in tweets:
			worksheet.write_string(row, 0, str(tweet.id))
			worksheet.write_string(row, 1, str(tweet.created_at))
			worksheet.write(row, 2, tweet.text)
			worksheet.write_string(row, 3, str(tweet.in_reply_to_status_id))
			row += 1

		workbook.close()
		print("Excel file ready")
		message="Excel file ready"
		return render(request,'search.html',{'fromdate':message})
	elif request.method=='POST' and 'btnform2' in request.POST:
		keywordsearch=request.POST['user_id']
		
		consumerKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
		consumerSecret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		accessToken = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		accessTokenSecret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
		auth.set_access_token(accessToken, accessTokenSecret)
		api = tweepy.API(auth)
		screen_name=keywordsearch

    #initialize a list to hold all the tweepy Tweets
		alltweets = []  

    #make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
		alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		while len(new_tweets) > 0:

        #all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
			alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1


		workbook = xlsxwriter.Workbook("/home/kamleshsisodiya/Desktop/"+screen_name+"1@"+ ".xlsx")
		worksheet = workbook.add_worksheet()
		row = 0
		for tweet in alltweets:
			worksheet.write_string(row, 0, str(tweet.id))
			worksheet.write_string(row, 1, str(tweet.created_at))
			worksheet.write(row, 2, tweet.text)
			worksheet.write_string(row, 3, str(tweet.in_reply_to_status_id))
			row += 1

		workbook.close()
		print("Excel file ready")
		keywordsearch1="Excel file ready"
		return render(request,'search.html',{'keywordsearch':keywordsearch1})
	else:
		return render(request,'search.html')
