from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", False)

driver = webdriver.Chrome(options=chrome_options)

driver.implicitly_wait(10)

driver.get('https://www.classcard.net/Login')

answers = {}
audio_data = {}

experience = 0

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def login(id, pwd):
    try:
        id_box = driver.find_element(By.CLASS_NAME, "login_id")
        id_box.click()
        id_box.clear()
        id_box.send_keys(id)
        sleep(0.5)

        pwd_box = driver.find_element(By.CLASS_NAME, "login_pwd")
        pwd_box.click()
        pwd_box.clear()
        pwd_box.send_keys(pwd)
        sleep(0.5)
        
        login_btn = driver.find_element(By.CLASS_NAME, "btn-login")
        login_btn.click()
    except:
        print(f"{RED}Login Error{RESET}")
        exit()

loginID = input("ID :")
loginPWD = input("PWD :")

print(f"{YELLOW}Received user data..{RESET}")

sleep(0.5)

login(loginID, loginPWD)

print(f"{GREEN}Login successed.{RESET}")

wm_list = {}
am_list = {}

class Get:
    def __init__(self):
        self.wordlist = ["", "", "", ""]
        self.meaninglist = ["", "", "", ""]
        self.audiolist = ["", "", "", ""]

        self.left = []
        self.right = []

        self.word_all_list = []
        self.meaning_all_list = []
        self.audio_all_list = []
        self.source_dic = {}
        self.audio_dic = {}
        
        self.count = 0
        self.score = 0
        pass

    def words(self):
        try:
            element_01 = driver.find_element(By.ID, "left_card_0")
            self.left_element_01 = element_01
            element_02 = driver.find_element(By.ID, "left_card_1")
            self.left_element_02 = element_02
            element_03 = driver.find_element(By.ID, "left_card_2")
            self.left_element_03 = element_03
            element_04 = driver.find_element(By.ID, "left_card_3")
            self.left_element_04 = element_04
            

            self.wordlist[0] = element_01.text
            self.wordlist[1] = element_02.text
            self.wordlist[2] = element_03.text
            self.wordlist[3] = element_04.text

            for i, e in enumerate(self.wordlist):
                self.wordlist[i] = e.split("\n")[0]

            self.left = []
            self.left.append(element_01)
            self.left.append(element_02)
            self.left.append(element_03)
            self.left.append(element_04)

            audio_icon_01 = self.left[0].find_element(By.CSS_SELECTOR, "i.cc.vol_on")
            self.src_01 = audio_icon_01.get_attribute("data-src")
            audio_icon_02 = self.left[1].find_element(By.CSS_SELECTOR, "i.cc.vol_on")
            self.src_02 = audio_icon_02.get_attribute("data-src")
            audio_icon_03 = self.left[2].find_element(By.CSS_SELECTOR, "i.cc.vol_on")
            self.src_03 = audio_icon_03.get_attribute("data-src")
            audio_icon_04 = self.left[3].find_element(By.CSS_SELECTOR, "i.cc.vol_on")
            self.src_04 = audio_icon_04.get_attribute("data-src")

            self.audiolist[0] = self.src_01
            self.audiolist[1] = self.src_02
            self.audiolist[2] = self.src_03
            self.audiolist[3] = self.src_04
        except:
            pass

        return self.wordlist
    
    def meanings(self):
        try:
            element_01 = driver.find_element(By.ID, "right_card_0")
            self.right_element_01 = element_01
            element_02 = driver.find_element(By.ID, "right_card_1")
            self.right_element_02 = element_02
            element_03 = driver.find_element(By.ID, "right_card_2")
            self.right_element_03 = element_03
            element_04 = driver.find_element(By.ID, "right_card_3")
            self.right_element_04 = element_04

            self.meaninglist[0] = element_01.text
            self.meaninglist[1] = element_02.text
            self.meaninglist[2] = element_03.text
            self.meaninglist[3] = element_04.text


            self.right = []
            self.right.append(element_01)
            self.right.append(element_02)
            self.right.append(element_03)
            self.right.append(element_04)
        except:
            pass

        return self.meaninglist
    
    def check_(self, word_num, meaning_num):
        try:
            word = self.wordlist[word_num]
            meaning = self.meaninglist[meaning_num]

            if answers[word] == meaning:
                return True

            return False
        except Exception as e:
            pass
    
    def check_audio(self, src_num, meaning_num):
        try:
            audio_src = self.audiolist[src_num]
            meaning = self.meaninglist[meaning_num]

            if str(audio_data[audio_src]).strip() == str(meaning).strip():
                return True

            return False
        except:
            pass
    
    def find_(self):
        result = []
        for i in range(4):
            for j in range(4):
                if self.check_(i,j): result.append((i, j))
        return result
    
    def find_audio(self):
        result = []
        for i in range(4):
            for j in range(4):
                if self.check_audio(i,j): result.append((i, j))
        return result
    
    def do_click(self):
        try:
            inform = self.find_()
            if inform == []: inform = self.find_audio()
            for i in range(len(inform)):
                self.left[inform[i][0]].click()
                self.right[inform[i][1]].click()
                print(f"\r{GREEN}Count: {self.count} {RESET}/{YELLOW} Score: {self.score}{RESET}", end="")
                self.count += 1
                sleep(0.6)
        except:
            pass
    
    def all_source(self):
        self.word_all_list = []
        self.meaning_all_list = []
        self.audio_all_list = []

        w = driver.find_elements(By.CSS_SELECTOR, ".ex_front")

        m = driver.find_elements(By.CSS_SELECTOR, ".ex_back")

        c = driver.find_elements(By.CSS_SELECTOR, ".flip-card")

        for el in w:
            self.word_all_list.append(el.get_attribute("textContent").strip())

        for el in m:
            self.meaning_all_list.append(el.get_attribute("textContent").strip())

        for card in c:
            self.audio_all_list.append(card.find_element(By.CSS_SELECTOR, ".btn-audio").get_attribute("data-src"))
    
    def bind_data(self):
        self.source_dic = {}
        for i, j in enumerate(self.word_all_list):
            self.source_dic[j] = self.meaning_all_list[i]

        self.audio_dic = {}
        for i, j in enumerate(self.audio_all_list):
            self.audio_dic[j] = self.meaning_all_list[i]
    
    def saveJson(self):
        with open('cardbot_Source.json', 'w', encoding='utf-8') as f:
            json.dump(self.source_dic, f, ensure_ascii=False, indent=4)
            
        with open('classcard_audio.json', 'w', encoding='utf-8') as f:
            json.dump(self.audio_dic, f, ensure_ascii=False, indent=4)
    
    def Update(self):
        try:
            score_element = driver.find_element(By.CLASS_NAME, "point")
            self.score = score_element.text
        except:
            pass


get = Get()

def set_status():
    global driver, get, answers, audio_data
    while True:
        C_url = driver.current_url
        if "/set/" in C_url:
            print(f"{YELLOW}Getting set data..{RESET}")
            get.all_source()
            print(f"{YELLOW}Binding data to dictionary form..{RESET}")
            get.bind_data()
            print(f"{YELLOW}Saving dictionary data by json..{RESET}")
            get.saveJson()
            print(f"{GREEN}Data Saved.{RESET}")
            with open('cardbot_Source.json', 'r', encoding='utf-8') as f:
                answers = json.load(f)

            with open('classcard_audio.json', 'r', encoding='utf-8') as k:
                audio_data = json.load(k)
            break

set_status()

while True:
    C_url = driver.current_url
    try:
        outGame = driver.find_element(By.ID, "wrapper-learn").get_attribute("class")
        if not ('hide-header' in outGame):
            experience = 1
    except:
        pass

    if "/Match/" in C_url:
        if ('hide-header' in outGame) and (experience):
            experience = 0
            print(f"\n{RED}Status Changed. {RESET}")
            set_status()

        w = get.words()
        m = get.meanings()
        get.do_click()
        get.Update()

    sleep(0.75)