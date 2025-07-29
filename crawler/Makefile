FOLDER_DESTINATION = alfa/ bravo/ charlie/ delta/ echo/ foxtrot/ golf/ hotel/ india/ juliet/ kilo/ lima/ mike/ november/ oscar/ papa/ quebec/ romeo/ sierra/ tango/ uniform/ victor/ whiskey/ xray/ yankee/ zulu/

URLS = https://google.com/ \
       https://www.wikipedia.org/ \
       https://www.github.com/ \
       https://www.bbc.com/news \
       https://www.stackoverflow.com/ \
       https://www.reddit.com/ \
       https://www.youtube.com/ \
       https://www.amazon.com/ \
       https://www.netflix.com/ \
       https://www.twitter.com/ \
       https://www.instagram.com/ \
       https://www.linkedin.com/ \
       https://www.microsoft.com/ \
       https://www.apple.com/ \
       https://www.facebook.com/ \
       https://www.cnn.com/ \
       https://www.nytimes.com/ \
       https://www.adobe.com/ \
       https://www.spotify.com/ \
       https://www.twitch.tv/ \
       https://www.dropbox.com/ \
       https://www.slack.com/ \
       https://www.zoom.us/ \
       https://www.tesla.com/

1:
	cd alfa && python3 crawler.py https://google.com/

2:
	cd bravo && python3 crawler.py https://www.wikipedia.org/

3:
	cd charlie && python3 crawler.py https://www.github.com/

4:
	cd delta && python3 crawler.py https://www.bbc.com/news

5:
	cd echo && python3 crawler.py https://www.stackoverflow.com/

6:
	cd foxtrot && python3 crawler.py https://www.reddit.com/

7:
	cd golf && python3 crawler.py https://www.youtube.com/

8:
	cd hotel && python3 crawler.py https://www.amazon.com/

9:
	cd india && python3 crawler.py https://www.netflix.com/

10:
	cd juliet && python3 crawler.py https://www.twitter.com/

11:
	cd kilo && python3 crawler.py https://www.instagram.com/

12:
	cd lima && python3 crawler.py https://www.linkedin.com/

13:
	cd mike && python3 crawler.py https://www.microsoft.com/

14:
	cd november && python3 crawler.py https://www.apple.com/

15:
	cd oscar && python3 crawler.py https://www.facebook.com/

16:
	cd papa && python3 crawler.py https://www.cnn.com/

17:
	cd quebec && python3 crawler.py https://www.nytimes.com/

18:
	cd romeo && python3 crawler.py https://www.adobe.com/

19:
	cd sierra && python3 crawler.py https://www.spotify.com/

20:
	cd tango && python3 crawler.py https://www.twitch.tv/

21:
	cd uniform && python3 crawler.py https://www.dropbox.com/

22:
	cd victor && python3 crawler.py https://www.slack.com/

23:
	cd whiskey && python3 crawler.py https://www.zoom.us/

24:
	cd xray && python3 crawler.py https://www.tesla.com/

25:
	cd yankee && python3 crawler.py https://www.reddit.com/r/programming/

26:
	cd zulu && python3 crawler.py https://news.ycombinator.com/

copy:
	for folder in $(FOLDER_DESTINATION); do \
        cp -r src/* $$folder; \
    done
clean:
	# remove all crawlres.json from each folder
	for folder in $(FOLDER_DESTINATION); do \
		rm -f $$folder/crawlres.json; \
	done
