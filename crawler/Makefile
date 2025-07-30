FOLDER_DESTINATION = alfa/ bravo/ charlie/ delta/ echo/ foxtrot/ golf/ hotel/ india/ juliet/ kilo/ lima/ mike/ november/ oscar/ papa/ quebec/ romeo/ sierra/ tango/ uniform/ victor/ whiskey/ xray/ yankee/ zulu/
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
	cd alfa && python3 crawler.py https://google.com/ & \
    cd bravo && python3 crawler.py https://youtube.com & \
    cd charlie && python3 crawler.py https://facebook.com & \
    cd delta && python3 crawler.py https://instagram.com & \
    cd echo && python3 crawler.py https://chatgpt.com & \
    cd foxtrot && python3 crawler.py https://x.com & \
    cd golf && python3 crawler.py https://whatsapp.com & \
    cd hotel && python3 crawler.py https://reddit.com & \
    cd india && python3 crawler.py https://wikipedia.org & \
    cd juliet && python3 crawler.py https://yahoo.co.jp & \
    cd kilo && python3 crawler.py https://yahoo.com & \
    cd lima && python3 crawler.py https://amazon.com & \
    cd mike && python3 crawler.py https://linkedin.com & \
    cd november && python3 crawler.py https://netflix.com & \
    cd oscar && python3 crawler.py https://live.com & \
    cd papa && python3 crawler.py https://bing.com & \
    cd quebec && python3 crawler.py https://office.com & \
    cd romeo && python3 crawler.py https://pinterest.com & \
    cd sierra && python3 crawler.py https://microsoft.com & \
    cd tango && python3 crawler.py https://weather.com & \
    cd uniform && python3 crawler.py https://fandom.com & \
    cd victor && python3 crawler.py https://duckduckgo.com & \
    cd whiskey && python3 crawler.py https://nytimes.com & \
    cd xray && python3 crawler.py https://ebay.com & \
    cd yankee && python3 crawler.py https://openai.com & \
    cd zulu && python3 crawler.py https://news.ycombinator.com/ & \
    wait
