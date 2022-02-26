from requests_html import HTMLSession
import json
import time
from colorama import Fore, Back, Style

import vote as param  # Contains vote code an later on the words to post!


# Subroutine to prepare JSON-Data
def buildJSONPayload(words, len=25):
    votePayload = ""  # Predefine wordlist for vote
    voteCnt = 1

    # Run through all words and attach it together
    #  Additionally the length is checked an a warning is printed out! (but can posted anyway!)
    for word in words:
        if votePayload == "":
            votePayload += word
        else:
            votePayload += " " + word
        print("Added #" + voteCnt.__str__() +
              ": \"" + word + "\" added to wordlist")
        voteCnt += 1
        if word.__len__() > len:
            print(Fore.YELLOW + "Note" + Fore.RESET + ": \"" + Fore.RED + word + Fore.RESET +
                  "\" is longer than allowed, but posted anyway!")

    return votePayload


# --------------------------- Main-Sequence ---------------------------
blockLF = "\n"  # Separator between functional blocks

# Define necessary URLs
print("Preparing URLs:")
urls = {
    "voteKey": "https://api.mentimeter.com/vote-ids/" + param.idCode + "/series",  # Fetch voteKey
    "voteBase": "https://www.menti.com"  # Attach voteKey
}
print(urls)
print(Fore.GREEN + "--> Ok <--" + Fore.RESET + blockLF)


print("Instanciating HTMLSession:")
s = HTMLSession()  # Instanciate html-session for requests
print(Fore.GREEN + "--> Ok <--" + Fore.RESET + blockLF)

# Fetch votekey
print("Fetching voteKey from \"" + urls["voteKey"] + "\":")
r = s.get(urls["voteKey"])
r.html.render(sleep=0, keep_page=True)
voteKey = json.loads(r.content)["vote_key"]
voteID = json.loads(r.content)["questions"][0]["id"]
print("Extracted VoteKey: " + voteKey +
      " --> Questionpage: " + urls["voteBase"] + "/" + voteKey)
print("Extracted VoteID: " + voteID + " --> POST-Request address:" +
      urls["voteBase"] + "/core/votes" + voteID)
print(Fore.GREEN + "--> Ok <--" + Fore.RESET + blockLF)

# Surf question-page and prepare POST
print("Grabbing necessary cookies and preparing POST-request to menti:")
r = s.get(urls["voteBase"] + "/" + voteKey)  # Grab question-page cookies
# Grab identifier cookies
r = s.post(urls["voteBase"] + "/core/identifiers")
# Add identifier to header
s.headers.update({"X-Identifier": r.cookies["identifier1"]})
print("Fetched Cookies: " + s.cookies.__str__() + "\n")
print("Added identifier to header: " + s.headers.__str__())
print(Fore.GREEN + "--> Ok <--" + Fore.RESET + blockLF)

# Prepare JSON and POST-request to menti
print("Preparing JSON-Data:")
jsonPayload = {
    "question_type": "wordcloud",
    "vote": buildJSONPayload(param.words)
}
jsonPayload = json.dumps(jsonPayload)
jsonPayload = json.loads(jsonPayload)
print(Fore.GREEN + "--> Ok <--" + Fore.RESET + blockLF)

# Wait given wait-time
wait = param.wait_seconds
print("Awaiting time (" + wait.__str__() + " seconds) from conf-file:")
while wait > 0:
    print(wait.__str__() + " seconds left")
    time.sleep(1)
    wait -= 1
print(Fore.GREEN + "--> Wait finished <--" + Fore.RESET + blockLF)

# Send POST-Request to server and check status
print("Sending POST-Request to server:")
r = s.post(urls["voteBase"] + "/core/votes/" + voteID, json=jsonPayload)

if r.status_code == 200:
    print(Fore.GREEN + "--> Request successful <--" + Fore.RESET + blockLF)
else:
    print(Fore.RED + "Request failed" + Fore.RESET + blockLF)

print("Finished - Closing app" + blockLF)
