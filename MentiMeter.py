from colorama.ansi import Fore
from requests_html import HTMLSession
import json
from Common import *

__strOk__ = "--> OK <--"


class MentiMeter():
    urls = {
        "voteKey": "https://api.mentimeter.com/vote-ids/<<ReplaceID>>/series",
        "voteBase": "https://www.menti.com"  # Attach voteKey
    }

    def __init__(self):
        printBlock("Instanciating HTMLSession():")
        self.s = HTMLSession()
        printSuccess(__strOk__)
        return

    def FetchPOSTRequestData(self, id):
        voteKeyURL = self.urls["voteKey"].replace("<<ReplaceID>>", id)
        printBlock("Fetching voteKey from \"" + voteKeyURL + "\":")
        r = self.s.get(voteKeyURL)
        del voteKeyURL

        # r.html.render(sleep=0, keep_page=True)
        self.voteKey = json.loads(r.content)["vote_key"]
        self.voteID = json.loads(r.content)["questions"][0]["id"]
        printBlock("Extracted VoteKey: " + Fore.YELLOW + self.voteKey + Fore.RESET +
                   " --> Questionpage: " + self.urls["voteBase"] + "/" + self.voteKey)
        printBlock("Extracted VoteID: " + Fore.YELLOW + self.voteID + Fore.RESET + " --> POST-Request address:" +
                   self.urls["voteBase"] + "/core/votes" + self.voteID)
        printSuccess(__strOk__)

        # Surf question-page and prepare POST
        printBlock(
            "Grabbing necessary cookies and preparing POST-request to menti:")
        # Grab question-page cookies
        r = self.s.get(self.urls["voteBase"] + "/" + self.voteKey)
        # Grab identifier cookies
        r = self.s.post(self.urls["voteBase"] + "/core/identifiers")
        # Add identifier to header
        self.s.headers.update({"X-Identifier": r.cookies["identifier1"]})
        printBlock("Fetched Cookies: " +
                   Fore.YELLOW + self.s.cookies.__str__() + Fore.RESET)
        printBlock("Added identifier to header: " +
                   Fore.YELLOW + self.s.headers.__str__() + Fore.RESET)
        printSuccess("POST-request informations fetched", blockSpacer="")
        printSuccess(__strOk__)
        return

    def PreparePOSTRequestWordlist(self, wordlist):
        # Prepare JSON and POST-request to menti
        printBlock("Preparing JSON-Data:")
        jsonPayload = {
            "question_type": "wordcloud",
            "vote": self.buildJSONPayload(wordlist)
        }
        printSuccess(__strOk__)
        return jsonPayload

    def buildJSONPayload(self, words, warnLen=25):
        votePayload = ""  # Predefine wordlist for vote
        voteCnt = 1

        # Run through all words and attach it together
        #  Additionally the length is checked an a warning is printed out! (but can posted anyway!)
        for word in words:
            if votePayload == "":
                votePayload += word
            else:
                votePayload += " " + word
            printBlock("Added #" + voteCnt.__str__() +
                       ": \"" + word + "\" to JSON-payload")
            voteCnt += 1
            if word.__len__() > warnLen:
                print(Fore.YELLOW + "Note" + Fore.RESET + ": \"" + Fore.RED + word + Fore.RESET +
                      "\" is longer than allowed, but posted anyway!")

        return votePayload

    def SendPOSTRequest(self, wordlist):
        print("Sending POST-Request to server:")
        payload = self.PreparePOSTRequestWordlist(wordlist)
        r = self.s.post(self.urls["voteBase"] +
                        "/core/votes/" + self.voteID, json=payload
                        )

        if r.status_code == 200:
            printSuccess("--> Request successful <--")
        else:
            printFail("Request failed")

        printBlock("Finished job. Now I'm tired and going home to sleep...")
        return
