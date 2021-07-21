from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time 

#Opens Instagram and logins in
def StartInstagram(browser):
    browser.get('https://www.instagram.com/accounts/login/')
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.NAME,'username')))
    iGUser = browser.find_element(By.NAME,'username')
    iGUser.send_keys(open('LoginInfo.txt').readlines()[0][0:-1])
    iGPassword = browser.find_element(By.NAME,'password')
    iGPassword.send_keys(open('LoginInfo.txt').readlines()[1])
    iGPassword.submit()
    return browser
#End of def


#Asks a question
def PrintOptions(Q, list):
    print(Q)

    for i in range(len(list)):
        print(str(i) + ': ' + list[i])
    hold = input()
    print()
    print('▪¤《◇》¤▪')
    print()
    return hold
#end of def


#Determine what you want to do
def WelcomeScreen(browser):
    print('Welcome to the Instagram Follow & Unfollow Program (IF&UP)')
    input()
    followOrUnfollow = PrintOptions('Today do you want to (enter number)', ['Play the Game','Mass Unfollow'])
    if followOrUnfollow == '0':
        Follow(browser,0,0,0,0,0,0,0)
    elif followOrUnfollow == '1':
        Unfollow(browser,0,0,0,0)
    else:
        print("Error 101")
        input()
        WelcomeScreen()
    #End of if
#End of def

def GetFollowing(browser):
    listOfFollowing = []
    browser.get('https://www.instagram.com/'+open('LoginInfo.txt').readlines()[0][0:-1])
    time.sleep(0.250)
    iGClick = browser.find_element(By.XPATH,'/html/body/span/section/main/div/header/section/ul/li[3]/a')
    iGClick.click()
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.TAG_NAME,'li')))
    iGFollowing = browser.find_elements(By.TAG_NAME,'li')
    scroll = browser.find_elements(By.TAG_NAME,'li')[1]
    for i in range(20):
        scroll.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.500)
    print(len(iGFollowing))
    for i in range(len(iGFollowing)):
        iGFollowingName = browser.find_elements(By.XPATH,'/html/body/div[3]/div/div/div[2]/ul[1]/div/li['+str(i)+'/div/div[2]/div[1]')
        iGFollowingButton = browser.find_elements(By.XPATH,'/html/body/div[3]/div/div/div[2]/ul[1]/div/li['+str(i)+']/div/div[3]')
        print(iGFollowingName)
        print(iGFollowingButton)
        listOfFollowing.append([iGFollowingName, iGFollowingButton])
    return listOfFollowing
#end of def


def GetFollowers(browser):
    listOfFollowers = []
    browser.get('https://www.instagram.com/'+open('LoginInfo.txt').readlines()[0][0:-1])
    time.sleep(0.250)
    iGClick = browser.find_element(By.XPATH,'/html/body/span/section/main/div/header/section/ul/li[2]/a')
    iGClick.click()
    scroll = browser.find_element(By.XPATH,'/html/body')
    iGFollowers = browser.find_elements(By.CLASS_NAME,'uu6c_')
    for i in range(20):
        scroll.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.500)
    print(len(iGFollowers))
    for i in range(len(iGFollowers)):
        iGFollowersName = browser.find_elements(By.CSS_SELECTOR('//html/body/div[3]/div/div/div[2]/ul[1]/div/li['+str(i)+']/div/div[2]/div[1]/div[1]'))
        iGFollowersButton = browser.find_elements(By.CSS_SELECTOR('/html/body/div[3]/div/div/div[2]/ul[1]/div/li['+str(i)+']/div/div[2]')) 
        listOfFollowers[i] = [iGFollowersName, iGFollowersButton]
    return listOfFollowers
    
    
#End of def

def UseWhitelist(people):
    for i in range(len(open('whitelist.txt').readlines())):
        for j in range(len(people), 1, -1):
            if people[j][1] == open('whitelist.txt').readlines()[I][0:-1]:
                people.splice(j,1)
                break
            #end of if
        #end of for
    return people
#end of def


def PeopleSort(browser, people):
    hold = []
    followers = GetFollowers(browser)
    for i in range(len(followers)):
        for j in range(len(people), 1, -1):
            if people[j][1] == followers[i][1]:
                hold.splice(len(hold)+1,0, people[j])
                people.splice(j,1)
            #end of if
        #end of for
    hold = hold + people
    return hold
#end of def


def Unfollow(browser,skip,followingYou,whitelistActive, unfollowAmount):
    if skip != 1:
        followingYou = int(PrintOptions('Unfollow people following you first?', ['No','Yes']))
        whitelistActive = int(PrintOptions('Do you want to use Whitelisting?',['No','Yes']))
        unfollowAmount = int(PrintOptions('Amount of people you want to unfollow',['Everyone','Or just enter amount']))
    #End of If

    peopleImFollowing = GetFollowing(browser)
    
    if whitelistActive == 1:
        peopleImFollowing = UseWhitelist(peopleImFollowing)
    if followingYou == 1:
        peopleImFollowing = PeopleSort(browser, peopleImFollowing)

    if unfollowAmount == 0:
        unfollowAmount = len(peopleImFollowing)
    if unfollowAmount > len(peopleImFollowing):
        unfollowAmount = len(peopleImFollowing)

    #Click following
    for i in range(len(unfollowAmount)):
        peopleImFollowing[i][2].click()    


def Follow(browser, skip, careRatio, ratioWait, ratioType, ratioNumber, trackPeople, whereFollow):
    if skip != 1:
        careRatio = PrintOptions('Do you care about your ratio?', ['No','Yes'])
        if careRatio == 1:
            ratioWait = PrintOptions('How long do you want to wait if your ratio is set(In minutes)', ['No'])
            ratioWait = ratioWait * 60000
            ratioType = PrintOptions('What type do you want?', ['Followers - X','X Following','% of Followers'])
            print(ratioText[ratioType])
            ratioNumber = input()
        else:
            ratioType = 0
            ratioWait = 0
            ratioNumber = 0
        trackPeople = PrintOptions('Do you want to track who you follow?', ['No','Yes'])
        whereFollow = PrintOptions('Where to follow?', ['Hashtag','Profile Followers','Location','Random'])

        #this needs to be changed tofastest
        followWait = 3000
        #this needs to be changed to fastest

        #navigate browser to that spot
        #Check location file with place
        browser.get('https://www.instagram.com/'+open('LoginInfo.txt').readlines()[0][0:-1])
        time.sleep(0.250)
        #grab list of names
        #Checks ratio to make sure you can still add people
        #checks to see if tracking is on
        #checks g
        #Adds person
        #ticks = 0
        #sleep followWait
        #if ratio is bad at tick and wait X
        #if ticks == X limit 
        # unfollow(1,1,1,5)
        #if out of people to follow
        #loop ++
        #if loop < 5
        #Follow(1, careRatio, ratioWait, ratioType, ratioNumber, trackPeople, whereFollow)
        #Follow(1, careRatio, ratioWait, ratioType, ratioNumber, trackPeople, 3)


website = webdriver.Chrome()
website = StartInstagram(website)
website = WelcomeScreen(website)

'''
Whitelist.txt
-contains all the people you don't want to unfollow
-[name 1, name 2, ... name 10, name 11, THIS IS A PLACE HOLDER]
-must manually add to it

LoginInfo.txt
-contains your username then password for Instagram
-[username, password]
-must manually add to it

PeoplePreviouslyAdded.txt
-contains a list of people the program has previously added
-[name 1, name 2, name 3, name 4, name 5 ... name 9999, name 10000]
-program adds to it with each follow click

WhereToFollow.txt
-contains a list of places to follow
#TODO make it also see what follow type that is
-[place 1, place 2, place 3, place 4, place 5]
-must manually add to it



'''
