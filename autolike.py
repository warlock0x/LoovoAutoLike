import urllib2
import cookielib
import getpass
import json

# Read username and password
inputUsername = raw_input("Username/email:")
inputPassword = getpass.getpass()
inputUsername = urllib2.quote(inputUsername.encode("utf8"))

# Let's retrieve the cookies
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
r = opener.open("http://www.lovoo.com/")

# Making login
r = opener.open("http://www.lovoo.com/login_check", "_username=" + inputUsername + "&_password=" + inputPassword + "&_remember_me=false")

r = opener.open("http://www.lovoo.com/welcome/login")

# Loop to like matches
while 1 == 1:
    # Take the main match in the page
    try:
        r = opener.open("https://www.lovoo.com/api_web.php/matches?preview=1")
        jsonMatch = json.loads(r.read())
        # Get the match id
        matchID = jsonMatch['response']['result'][0]['id']
        matchName = jsonMatch['response']['result'][0]['name']
        matchAge = jsonMatch['response']['result'][0]['age']
        matchGender = "male"
        if jsonMatch['response']['result'][0]['gender'] == 2:
            matchGender = "female"
        matchLocation = jsonMatch['response']['result'][0]['location']
        # Like the match
        try:
            req = urllib2.Request("http://www.lovoo.com/api_web.php/matches/" + matchID, "{\"userId\":\"" + matchID + "\",\"vote\":1}")
            req.add_header("DNT", "1")
            req.add_header("Content-Type", "application/json;charset=utf-8")
            req.add_header("KISSAPI_NOTIHASH", "no")
            req.add_header("Referer", "https://www.lovoo.com/")
            req.add_header("Connection", "keep-alive")
            req.add_header("Pragma", "no-cache")
            req.add_header("Cache-Control", "no-cache")
            r = opener.open(req)

        except urllib2.HTTPError, e:
            if e.code == 500:
                print "Maybe you finished the daily number of matches. Try again tomorrow."
                print "Code: " + str(e.code) + " - Message: " + e.message
                break

        print "You just liked " + matchName + ", a beautiful " + matchGender + " of age " + str(matchAge) + " from " + matchLocation

    except urllib2.HTTPError, e:
        if e.code == 403:
            print "Something went wrong, maybe wrong credentials? Check and try again."
        elif e.code == 404:
            print "Maybe they moved the login page, try to check this url if it's valid: " + e.url
        elif e.code == 302:
            print "It seems that there is a redirect but probably i am so dumb that i didn't handle it."
        else:
            print "The procedure encountered an unknown error."
        print "Message: " + e.message
        break