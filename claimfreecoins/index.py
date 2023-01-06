import json, time, base64, requests, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def solveAntibotLinks (selfimage, listImage):
    jsonen = json.dumps({
        'self_image': selfimage,
        'image_list': str(base64.b64encode(json.dumps({
            "count_image": 4,
            "images": listImage
        }).encode())).replace("b'", '').replace("'", ''),
        'type_solve': '1'
    })
    encoded_string = str(base64.b64encode(jsonen.encode())).replace("b'", '').replace("'", '')
    data = {
    'type': 'antibotlinks',
    'data': encoded_string
    }
    solve = requests.post(url='https://tronghoa.dev/free-bypass-captcha/solve.php', data=data)
    if solve.json()['error'] == True:
        return [False, solve.json()['message']]
    else:
        return [True, json.loads(base64.b64decode(solve.json()["solution"]))]

def solveRecaptchav2GetTask ():
    data = json.dumps({
        'websiteURL': 'https://claimfreecoins.io/',
        'websiteKey': '',
        'isInvisible': 'false'
    }).encode()
    bs64 = str(base64.b64encode(data)).replace("b'", '').replace("'", '')
    url = 'https://tronghoa.dev/free-bypass-captcha/solve.php?type=recaptchav2&data={0}'.format(bs64)
    solve = requests.get(url)
    if solve.json()['error'] == True:
        return [False, solve.json()['message']]
    else:
        return [True, json.loads(base64.b64decode(solve.json()["taskId"]))]

def getConfig ():
    # read file config.json
    with open('config.json') as config:
        data = json.load(config)
        return data

def driver_create ():
    op = Options()
    # add extension
    op.add_extension("ads.crx")
    return webdriver.Chrome(options=op)

def driver_close (driver):
    driver.quit()

def resetTab (driver):
    child = driver.window_handles[0]
    driver.switch_to.window(child)

def closeTab (driver):
    driver.switch_to.window(driver.window_handles[1])
    driver.close()


def login (driver, wallet):
    if driver.page_source.find('Login') == -1:
        return False
    else:
        driver.find_element('name', 'address').send_keys(wallet)
        time.sleep(2)
        for x in range(2):
            try:
                driver.find_element('xpath', '//*[@id="faucet"]/div/form/input[2]').click()
                break
            except:
                time.sleep(1)
        for x in range(10):
            
            if driver.page_source.find('This faucet requires a') > -1:
                return None
            if driver.page_source.find('Logged In As:') == -1:
                time.sleep(1)
            if driver.page_source.find('You have reached the max claims per day. Please come back tomorow.') > -1:
                return None
            else:
                return True
        return False

def checkActive ():
    try:
        activeRq = requests.get('https://tronghoa.dev/free-bypass-captcha/active.php?mode=genLink').json()
        if activeRq['Status_Active'] == True:
            print(color.GREEN, 'You have activated the tool, please go to...')
            time.sleep(2)
            return True 
        else:
            print(color.BLUE, 'You have not activated the tool to use bypass, please activate via this link:')
            print(color.GREEN, activeRq['link'])
            return False
    except:
        return False
def solveRecaptchav2GetTask ():
    data = json.dumps({
        'websiteURL': 'https://claimfreecoins.io/',
        'websiteKey': '6LfDD6sbAAAAAEs1Qjg_OBkWgU0TQ2esQpAm-SFP',
        'isInvisible': 'false'
    }).encode()
    bs64 = str(base64.b64encode(data)).replace("b'", '').replace("'", '')
    url = 'https://tronghoa.dev/free-bypass-captcha/solve.php?type=recaptchav2&data={0}'.format(bs64)
    solve = requests.get(url)
    if solve.json()['error'] == True:
        return [False, solve.json()['message']]
    else:
        resultJson = json.loads(base64.b64decode(solve.json()["response_anycaptcha"]))
        if resultJson['errorId'] == 0:
            return [True, resultJson['taskId']]


def getResponseRecaptchav2(taskId):
    data = json.dumps({
        'task_number': taskId
    }).encode()
    bs64 = str(base64.b64encode(data)).replace("b'", '').replace("'", '')
    url = 'https://tronghoa.dev/free-bypass-captcha/solve.php?type=recaptchav2&data={0}'.format(bs64)
    solve = requests.get(url)
    if solve.json()['error'] == True:
        return [False, solve.json()['message']]
    else:
        resultJson = json.loads(base64.b64decode(solve.json()["response_anycaptcha"]))
        return [True, resultJson]

def solveRecaptcha():
    taskId = solveRecaptchav2GetTask()
    if taskId[0] == True:
        taskId = taskId[1]
        status = False
        for x in range(25):
            response = getResponseRecaptchav2(taskId)
            if response[0] == True:
                response = response[1]
                if response['status'] == 'processing':
                    print(color.YELLOW, 'Solving recaptcha v2...')
                    status = False
                elif response['status'] == 'ready':
                    print(color.GREEN, 'successfully solved recaptcha v2')
                    solutionResponse = response['solution']['gRecaptchaResponse']
                    status = True
                    return solutionResponse
                else:
                    status = False
                    print(color.RED, 'Status does not exist, there is an error (recaptcha v2)')
            else:
                status = False
                print(color.RED, 'Retrieving response failed (recaptcha v2)')
            if status == False:
                time.sleep(5)
        print(color.RED, 'solution fail completely (recaptcha v2)')
        return False
    else:
        print(color.RED, 'Unable to get taskId')
        return False

def claim (driver):
    try:
        time.sleep(3)
        driver.find_element('xpath', '//*[@id="faucet"]/div/form/button').click()
        selfImage = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-header.no-padding > div > img").src; return content;')
        selfImage = selfImage.replace('data:image/png;base64,','')
        img1 = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-body > div.row.no-margin.no-padding > div:nth-child(1) > a > img").src; return content;')
        img1 = img1.replace('data:image/png;base64,','')
        img2 = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-body > div.row.no-margin.no-padding > div:nth-child(2) > a > img").src; return content;')
        img2 = img2.replace('data:image/png;base64,','')
        img3 = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-body > div:nth-child(7) > div:nth-child(1) > a > img").src; return content;')
        img3 = img3.replace('data:image/png;base64,','')
        img4 = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-body > div:nth-child(7) > div:nth-child(2) > a > img").src; return content;')
        img4 = img4.replace('data:image/png;base64,','')
        imgs = [img1, img2, img3, img4]
        unique_list = []
        for element in imgs:
            if element not in unique_list:
                unique_list.append(element)
        if (len(imgs) != len(unique_list)):
            return False
        solveAnti = solveAntibotLinks(selfimage=selfImage, listImage=imgs)
        if solveAnti[0] == False:
            print(solveAnti[1])
            return False
        action = []
        for a in solveAnti[1]:
            if a == 1:
                action.append('document.querySelector("#antibot > div > div > div.modal-body > div.row.no-margin.no-padding > div:nth-child(1) > a > img").click()')
            elif a == 2:
                action.append('document.querySelector("#antibot > div > div > div.modal-body > div.row.no-margin.no-padding > div:nth-child(2) > a > img").click()')
            elif a == 3:
                action.append('document.querySelector("#antibot > div > div > div.modal-body > div:nth-child(7) > div:nth-child(1) > a > img").click()')
            elif a == 4:
                action.append('document.querySelector("#antibot > div > div > div.modal-body > div:nth-child(7) > div:nth-child(2) > a > img").click()')
        if len(action) != len(set(action)):
            return False
        for x in action:
            driver.execute_script(x)
            time.sleep(1)
        
        statusSolveRecaptcha = solveRecaptcha()
        if statusSolveRecaptcha == False:
            print(color.RED, 'Recaptcha failed')
            return False
        else:
            print(statusSolveRecaptcha)
            print(color.GREEN, 'successful recaptcha')
            driver.execute_script("document.getElementById('g-recaptcha-response').value = '{0}';".format(statusSolveRecaptcha))
            time.sleep(1)
            driver.find_element('xpath', '//*[@id="ncb"]/input').click()
            time.sleep(3)
            if driver.page_source.find('was sent to your') == -1:
                return False
            else:
                return True
    except:
        return False


conf = getConfig()
wallet = conf['wallet']
ite = iter(wallet)
cols = color()
if checkActive() == False:
    sys.exit()
def resetIterConfig ():
    global ite
    ite = iter(wallet)


# get all wallet and print the screen
for x in ite:
    print(cols.GREEN + '[' + x + '] ' + cols.BLUE + ' = ' + cols.END + wallet[x])
resetIterConfig()

tags = {
    'btc' : '/free-bitcoin/',
    'doge' : '/free-dogecoin/',
    'ltc': '/free-litecoin/',
    'trx': '/free-tron/',
    'bnb' : '/free-binance/',
    'sql' : '/free-solana/',
    'dash' : '/free-dash/',
    'usdt' : '/free-tether/',
    'zec' : '/free-zcash/',
    'dgb' : '/free-digibyte/',
    'eth' : '/free-ethereum/',
    'btcs' : '/free-bitcoin-cash/',
    'fey' : '/free-feyorra/'
}

drivers = driver_create()
time.sleep(3)
closeTab(drivers)
resetTab(drivers)

while True:
    for x in tags:
        for y in wallet:
            if x == y:
                while True:
                    try:
                        drivers.get('https://claimfreecoins.io' + tags[x])
                        log = login(drivers, wallet[y])
                        if log:
                            print(cols.GREEN + '[' + y + '] Login thanh cong')
                        elif log == None:
                            print(cols.RED + '[' + y + '] Chặn tính năng')
                            driver_close(drivers)
                            drivers = driver_create()
                            time.sleep(3)
                            closeTab(drivers)
                            resetTab(drivers)
                            break
                       
                        if claim(drivers) == False:
                            print(cols.RED + '[' + y + '] Claim that bai')
                        else:
                            print(cols.GREEN + '[' + y + '] Claim thanh cong')
                            break
                    except Exception as e:
                        print(e)
                        driver_close(drivers)
                        drivers = driver_create()
                        time.sleep(3)
                        closeTab(drivers)
                        resetTab(drivers)