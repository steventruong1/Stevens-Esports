
import pygsheets
import time

def returnCellValue(x,y): # row number then column number. takes cell x,y and returns the value
    return(wks.cell((x,y)).value)

def returnRow(x): # returns a list of cell values. Takex x which is row number. 
    return(wks.get_row(x))

def findSheetIndex(name): # Given a string, will return the index of the sheet number if found. Otherwise create the sheet
    try:
        return(sh.worksheet('title',name).index)
        print(name + " found")
    except:
        createNewSheet(name)

def createNewSheet(name): #Given a string, will attempt to add a new sheet and returns the index of said sheet
    try:
        sh.add_worksheet(name)
        print(name + " added")
        return(findSheetIndex(name))
    except:
        print(name + " already added")
        return(findSheetIndex(name))

#def emptyRow(var): #checks cells until it finds an empty one
    # while(placeholder != returnCellValue(var,1)) :
           #var+=1
    # return var

def dictHelper(name): #given a key, returns specific value in the dictionary. if not found, add it and with a value of 0
    if name in hdict:
        temp = hdict.get(name)
        return temp
    else:
        hdict.update({name + "EmptyRow": 1})
        hdict.update({name: createNewSheet(name)})
        return hdict.get(name)
    
def dictHelper1(name): #given a key, returns specific value in the dictionary and upadtes it by 1. speicifc for pasting code
    temp = hdict.get(name + "EmptyRow")
    hdict.update({name + "EmptyRow": temp + 1})
    return temp

def charstoString(array,time1,temp, colorList) :
    print(b[temp]) # debug prints out name of user
    time.sleep(time1) #we are limited by google api call limits, so we have to sleep here. may need to be adjusted depending on responses. 5 seconds works for 92 responses, 7ish games.
    gameLength = len(array) # takes the length of all games selected to turn into a string later on
    new = ""
    counter = 0
    global wks
    #while counter <= gameLength - 1: #way for us to split the array. takes csgo, valorant and turns it into csgo which will check the sheet if we have page for it, create it if we don't and copy user data to it. repeat for valorant,etc
        #new = ""
       # for x in array[counter:gameLength]: # char by char for comma, breaks when found. otherwise add char to string
            #if x == ',' :
             #    counter += 1 
             #    break
           # else:
           #     counter += 1 
               # new += x
        #counter +=1 #skips the space after the comma
    for i in (''.join(array)).split(', '):     
        wks =sh[dictHelper(i)] #look up index of game sheet in dictionary and returns said index. if not found, will add to dictionary and update index
        wks.update_row(dictHelper1(i),b,0) #copy the data into the next empty row       
        if "Red" in colorList and "substitute" not in colorList and "Gray" not in colorList: #red only, and not a sub
            c1 = wks.cell('L' + str(hdict.get(i + "EmptyRow") - 1))
            c1.color = (1.0,0.0,0.3, .9)
        elif "Gray" in colorList and "substitute" not in colorList and "Red" not in colorList: #gray only and not a sub
            c1 = wks.cell('L' + str(hdict.get(i + "EmptyRow") - 1))
            c1.color = (0.7,0.6,0.7,.9)
        elif "Red" in colorList and "Gray" not in colorList and "substitute" in colorList: #red sub only
            c1 = wks.cell('L' + str(hdict.get(i + "EmptyRow") - 1))
            c1.color = (1.0,0.0,0.7,.9)
        elif "Gray" in colorList and "Red" not in colorList and "substitute" in colorList: #gray sub only
            c1 = wks.cell('L' + str(hdict.get(i + "EmptyRow") - 1))
            c1.color = (0.3,0.3,0.3,.9)
        elif "Gray" in colorList and "Red" in colorList: #play/sub gray or red
            c1 = wks.cell('L' + str(hdict.get(i + "EmptyRow") - 1))
            c1.color = (0.3,1.0,1.0,.9)
        elif "coach" in colorList:
            c1 = wks.cell('L' + str(hdict.get(i + "EmptyRow") - 1))
            c1.color = (1,1.0,0.5,.9)
        wks =sh[0] #while loop cycles back and we reset everything

hdict =	{}

gc = pygsheets.authorize(service_file='/Users/dauxg/downloads/creds.json') #authorization. Need to keys to usse google api. Contact me or google if you need help
sh = gc.open(input('Enter sheet name. Case Sensitve. Read Usage for more: ')) #open the google spreadsheet. Make sure to share sheet with service account and replace name when necessary

wks = sh[0] #select the first sheet
wks.refresh() #refreshes sheet to make sure up todate 
wks.link() #links sheet to the cloud for instant changes
filterIndex = ord(input('Enter column letter to filter games by. Case does not matter: ').lower()) - 97 #Column number of data that we are filtering by. IE if sorting people by favorite colors and user entered color into column a. filterIndex = 1
filterIndex2 = ord(input('Enter column letter to filter Gray vs Red. Case does not matter: ').lower()) - 97 #Column number of data that we are filtering by. IE if sorting people by favorite colors and user entered color into column a. filterIndex = 1
userIndex = int(input('Enter row number of when data starts. Most Likley 2: ')) #Starting Row Number. Usally 2 since row 1 will be questions.
placeholder = returnCellValue(1000,1) #tempoary cell. crucial that this cellis emptty
superCounter = 1 #counter to see how many users we have added
temp = ord(input('Enter column letter print information. Case does not matter: ').lower()) - 97
time1 = int(input('Enter sleep delay. 5 seconds min recomended: '))

start_time = time.time() #starts timer to see how long program goes
print("starting")

while (placeholder != returnCellValue(userIndex,1)):
    #print("User #" + superCounter) # DEBUG Print
    b = returnRow(userIndex) #contains all user data ie timestamp to last one
    gameList = (b[filterIndex]) #takes the games portion of user data
    colorList = (b[filterIndex2]) #takes the games portion of user data
    wks = sh[0]
    wks.refresh() #refreshes sheet to make sure up todate 
    charstoString(gameList,time1,temp, colorList) #main driver of program
    userIndex+=1 #update information and move to next person
    superCounter+=1 
print(superCounter) # DEBUG Print

print("\nIt took", time.time() - start_time, "to filter and replicate the data\n") # time end
for key, value in hdict.items(): # print out dictionary of page index and last empty row
    print(key, ' : ', value)
print("Number of users added " + str(superCounter))
#print(userIndex)
print("\nfin")

