from colorama import Fore, Back, Style
import time

__blockSpacer = "\n"


def printBlock(str):
    print(str)


def printSuccess(str, blockSpacer=__blockSpacer):
    print(Fore.GREEN + str + Fore.RESET + blockSpacer)


def printWarning(str):
    print(Fore.YELLOW + str + Fore.RESET)


def printFail(str, blockSpacer=__blockSpacer):
    print(Fore.RED + str + Fore.RESET + blockSpacer)


def Wait(time_seconds):
    # Wait given wait-time
    wait = time_seconds
    printBlock("Awaiting time (" + wait.__str__() + " seconds) from conf-file:")
    while wait > 0:
        print(wait.__str__() + " seconds left")
        time.sleep(1)
        wait -= 1
    printSuccess("--> Wait finished <--")
