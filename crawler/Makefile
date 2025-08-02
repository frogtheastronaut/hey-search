FOLDER_DESTINATION = bot_1/ bot_2/ bot_3/ bot_4/ bot_5/ bot_6/ bot_7/ bot_8/ bot_9/ bot_10/ bot_11/ bot_12/ bot_13/ bot_14/ bot_15/ bot_16/ bot_17/ bot_18/ bot_19/ bot_20/ bot_21/ bot_22/ bot_23/ bot_24/ bot_25/ bot_26/ bot_27/ bot_28/ bot_29/ bot_30/ bot_31/ bot_32/ bot_33/ bot_34/ bot_35/ bot_36/ bot_37/ bot_38/ bot_39/ bot_40/ bot_41/ bot_42/ bot_43/ bot_44/ bot_45/ bot_46/ bot_47/ bot_48/ bot_49/ bot_50/
init:
	for folder in $(FOLDER_DESTINATION); do \
		mkdir -p $$folder; \
	done

copy:
	for folder in $(FOLDER_DESTINATION); do \
	    cp -r src/* $$folder; \
	done

clean:
	# remove all crawlres.json from each folder
	for folder in $(FOLDER_DESTINATION); do \
	    rm -f $$folder/crawlres.json; \
	done

run-all:
	# run crawler.py
	cd bot_1 && python3 crawler.py https://google.com & \
    cd bot_2 && python3 crawler.py https://youtube.com & \
    cd bot_3 && python3 crawler.py https://facebook.com & \
    cd bot_4 && python3 crawler.py https://twitter.com & \
    cd bot_5 && python3 crawler.py https://instagram.com & \
    cd bot_6 && python3 crawler.py https://amazon.com & \
    cd bot_7 && python3 crawler.py https://wikipedia.org & \
    cd bot_8 && python3 crawler.py https://reddit.com & \
    cd bot_9 && python3 crawler.py https://yahoo.com & \
    cd bot_10 && python3 crawler.py https://whatsapp.com & \
    cd bot_11 && python3 crawler.py https://netflix.com & \
    cd bot_12 && python3 crawler.py https://tiktok.com & \
    cd bot_13 && python3 crawler.py https://linkedin.com & \
    cd bot_14 && python3 crawler.py https://discord.com & \
    cd bot_15 && python3 crawler.py https://twitch.tv & \
    cd bot_16 && python3 crawler.py https://ebay.com & \
    cd bot_17 && python3 crawler.py https://telegram.org & \
    cd bot_18 && python3 crawler.py https://github.com & \
    cd bot_19 && python3 crawler.py https://snapchat.com & \
    cd bot_20 && python3 crawler.py https://pinterest.com & \
    cd bot_21 && python3 crawler.py https://msn.com & \
    cd bot_22 && python3 crawler.py https://bing.com & \
    cd bot_23 && python3 crawler.py https://stackoverflow.com & \
    cd bot_24 && python3 crawler.py https://microsoft.com & \
    cd bot_25 && python3 crawler.py https://duckduckgo.com & \
    cd bot_26 && python3 crawler.py https://nytimes.com & \
    cd bot_27 && python3 crawler.py https://cnn.com & \
    cd bot_28 && python3 crawler.py https://news.ycombinator.com & \
    cd bot_29 && python3 crawler.py https://apple.com & \
    cd bot_30 && python3 crawler.py https://medium.com & \
    cd bot_31 && python3 crawler.py https://quora.com & \
    cd bot_32 && python3 crawler.py https://spotify.com & \
    cd bot_33 && python3 crawler.py https://wordpress.com & \
    cd bot_34 && python3 crawler.py https://tumblr.com & \
    cd bot_35 && python3 crawler.py https://zoom.us & \
    cd bot_36 && python3 crawler.py https://paypal.com & \
    cd bot_37 && python3 crawler.py https://dropbox.com & \
    cd bot_38 && python3 crawler.py https://salesforce.com & \
    cd bot_39 && python3 crawler.py https://imdb.com & \
    cd bot_40 && python3 crawler.py https://weather.com & \
    cd bot_41 && python3 crawler.py https://espn.com & \
    cd bot_42 && python3 crawler.py https://bbc.com & \
    cd bot_43 && python3 crawler.py https://guardian.com & \
    cd bot_44 && python3 crawler.py https://washingtonpost.com & \
    cd bot_45 && python3 crawler.py https://reuters.com & \
    cd bot_46 && python3 crawler.py https://forbes.com & \
    cd bot_47 && python3 crawler.py https://bloomberg.com & \
    cd bot_48 && python3 crawler.py https://slack.com & \
    cd bot_49 && python3 crawler.py https://etsy.com & \
    cd bot_50 && python3 crawler.py https://airbnb.com & \
    wait
