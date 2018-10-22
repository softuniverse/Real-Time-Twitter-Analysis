import tweepy
from textblob import TextBlob
import time
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import json
import re


#overriding methods from the twitter api for analysis of real time text

class MyStreamListener(tweepy.StreamListener):

    def on_data(self, data):
    	json_data=json.loads(data)
    	text_data=json_data["text"]
    	#clean the text from url
    	text_data=re.sub(r"https\S+", "", text_data)
    	#text_data=text_data.decode("utf-8")

    	print(text_data)
    	print(json_data["lang"])
    	print(json_data['user']['time_zone'])
		# declaring all the global variables required for graph and pie charts

    	global positive
    	global negative
    	global net
    	global init_time
    	global pos_count
    	global neg_count
    	global neutral_count

    	senti=0
    	t=int(time.time()-init_time)
    	analysis=TextBlob(text_data)
		# translate the tweet if the tweet is not in english 
    	if(json_data["lang"] != 'en'):
    		try :
    			analysis.translate(to='en')
    		except :
    			pass

    	#print(analysis.sentiment)
    	for line in analysis.sentences :
    		senti=senti+line.sentiment.polarity
    		if line.sentiment.polarity >=0 :
    			positive=positive+line.sentiment.polarity
    			if line.sentiment.polarity==0:
    				neutral_count=neutral_count+1
    			else :
    				pos_count=pos_count+1
    			
    		else :
    			negative=negative+line.sentiment.polarity
    			neg_count=neg_count+1
    			
    	net=net+senti
    	print(senti)
    	print("positive :"+str(positive))
    	print("negative :"+str(negative))
    	print("net :"+str(net))

    	

    	# finally priniting the graph
    	
    	plt.subplot(1,2,1)
    	plt.title('time v/s sentiment graph')
    	plt.grid(color='c')
    	
    	plt.axis([0,300,-40,40])
    	plt.xlabel("time(seconds)")
    	plt.ylabel("sentiment")
    	plt.plot([t],[positive],'go',[t] ,[negative],'ro',[t],[net],'bo',label='linear')

    	
    	#piechart
    	
    	
    	plt.subplot(1,2,2).cla()
    	#plt.gcf().clear()
    	plt.title('pie chart')
    	labels='positive','negative','neutral'
    	sizes=[(pos_count/(pos_count+neg_count+neutral_count))*100,(neg_count/(pos_count+neg_count+neutral_count))*100,(neutral_count/(pos_count+neg_count+neutral_count))*100]
    	plt.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    	plt.axis('equal')
    	
    	
    	

    	
		###################################################################
    	plt.show()
    	plt.pause(0.0001)
    	print("")

    	
    	
 

    def on_error(self,status):
		# print out any error ie. time out, credentials mismatch , system - server time mismatch
    	print (status)



    	


#test 1 : 401 authorization error rectified by changing the time line 
#if the system time has error by more than 15 minutes with respect to official time we get 401 error


if __name__ == '__main__':

	# Enter your twitter application credentials here

	consumer_key= '*********************************'
	consumer_secret= '******************************'

	access_token='************************************************'
	access_token_secret='*****************************************'

	#variables for analysis
	positive=0
	negative=0
	net=0
	pos_count=0 
	neg_count=0
	neutral_count=0

	init_time=time.time()
	plt.ion()

	#authenticate

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	myStream.filter(track=[input("input keyword that you want to search : ")])



