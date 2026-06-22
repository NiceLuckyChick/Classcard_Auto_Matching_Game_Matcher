#아 졸리다
#제 원작은 아닙니다. 분명 컴퓨터에 있는 코드인데 누가 만들었는지 까먹었어요, 원작자분께는 정말 죄송합니다. 포크해야되는데..
import traceback
import sys
import random
from time import sleep

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

print(f"{YELLOW}=== 클래스카드 매칭 매크로 준비 ==={RESET}")
loginID = input("👉 클래스카드 ID를 입력하세요 : ")
loginPWD = input("👉 클래스카드 비밀번호를 입력하세요 : ")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import json
except ImportError:
    print(f"\n{RED}[오류] 필요 라이브러리(selenium)가 설치되어 있지 않습니다.{RESET}")
    print("명령 프롬프트(cmd)에서 아래 명령어를 입력해 설치해주세요:")
    print("pip install selenium")
    input("종료하려면 엔터를 누르세요...")
    sys.exit()

answers = {}
audio_data = {}
experience = 0

# 🌟 사람처럼 한 글자씩 타이핑하는 함수 추가
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        # 0.05초 ~ 0.15초 사이의 랜덤한 시간 동안 대기 (사람 타건 속도 묘사)
        sleep(random.uniform(0.05, 0.15))

def login(user_id, user_pwd):
    try:
        print(f"{YELLOW}로그인 페이지 로딩 대기 중...{RESET}")
        wait = WebDriverWait(driver, 10)

        # 1단계: 메인 페이지 우회
        try:
            driver.find_element(By.ID, "login_id")
        except:
            try:
                first_btn = driver.find_element(By.XPATH, "//*[contains(text(), '로그인') or contains(text(), 'Login')]")
                first_btn.click()
                sleep(1.5)
            except:
                pass

        # 2단계: 아이디 입력
        print(f"{YELLOW}아이디 입력 중...{RESET}")
        id_box = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//input[@id='login_id' or @name='login_id' or contains(@placeholder, '아이디') or contains(@placeholder, '이메일')]"
        )))
        try: 
            id_box.click() 
        except: 
            pass 
        id_box.clear()
        
        # 한 번에 입력하던 방식을 사람 타이핑으로 변경
        human_typing(id_box, user_id)
        sleep(0.5)

        # 3단계: 비밀번호 입력
        print(f"{YELLOW}비밀번호 입력 중...{RESET}")
        pwd_box = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@type='password' or @id='login_pwd' or @name='login_pwd']"
        )))
        try: 
            pwd_box.click() 
        except: 
            pass 
        pwd_box.clear()
        
        # 한 번에 입력하던 방식을 사람 타이핑으로 변경
        human_typing(pwd_box, user_pwd)
        sleep(0.5)
        
        # 4단계: 로그인 버튼 클릭
        print(f"{YELLOW}로그인 버튼 클릭 중...{RESET}")
        try:
            login_btn = driver.find_element(By.CSS_SELECTOR, ".btn-login")
        except:
            try:
                login_btn = driver.find_element(By.XPATH, "//*[@id='btn_login' or @name='btn_login']")
            except:
                login_btn = driver.find_element(By.XPATH, "//button[contains(text(), '로그인')] | //a[contains(text(), '로그인')]")
        
        try: 
            login_btn.click()
        except: 
            driver.execute_script("arguments[0].click();", login_btn) 
            
        print(f"{GREEN}로그인 완료!{RESET}")
        sleep(2) # 로그인 후 화면 전환 대기

    except Exception as e:
        print(f"\n{RED}로그인 요소 찾기 실패 Error: {e}{RESET}")
        input("오류가 발생했습니다. 종료하려면 엔터를 누르세요...")
        exit()


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

    def words(self):
        try:
            element_01 = driver.find_element(By.ID, "left_card_0")
            element_02 = driver.find_element(By.ID, "left_card_1")
            element_03 = driver.find_element(By.ID, "left_card_2")
            element_04 = driver.find_element(By.ID, "left_card_3")

            self.wordlist[0] = element_01.text
            self.wordlist[1] = element_02.text
            self.wordlist[2] = element_03.text
            self.wordlist[3] = element_04.text

            for i, e in enumerate(self.wordlist):
                self.wordlist[i] = e.split("\n")[0]

            self.left = [element_01, element_02, element_03, element_04]

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
            element_02 = driver.find_element(By.ID, "right_card_1")
            element_03 = driver.find_element(By.ID, "right_card_2")
            element_04 = driver.find_element(By.ID, "right_card_3")

            self.meaninglist[0] = element_01.text
            self.meaninglist[1] = element_02.text
            self.meaninglist[2] = element_03.text
            self.meaninglist[3] = element_04.text

            self.right = [element_01, element_02, element_03, element_04]
        except:
            pass
        return self.meaninglist
    
    def check_(self, word_num, meaning_num):
        try:
            word = self.wordlist[word_num]
            meaning = self.meaninglist[meaning_num]
            if answers.get(word) == meaning:
                return True
            return False
        except:
            return False
    
    def check_audio(self, src_num, meaning_num):
        try:
            audio_src = self.audiolist[src_num]
            meaning = self.meaninglist[meaning_num]
            if str(audio_data.get(audio_src)).strip() == str(meaning).strip():
                return True
            return False
        except:
            return False
    
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

def set_status():
    global driver, get, answers, audio_data
    print(f"\n{YELLOW}==> 직접 학습할 단어장(/set/) 페이지로 들어가주세요. 대기 중...{RESET}")
    while True:
        try:
            C_url = driver.current_url
            if "/set/" in C_url:
                print(f"{YELLOW}세트 데이터를 수집합니다...{RESET}")
                get.all_source()
                get.bind_data()
                get.saveJson()
                print(f"{GREEN}데이터 저장 완료! 이제 '매칭 게임'을 실행하세요.{RESET}")
                
                with open('cardbot_Source.json', 'r', encoding='utf-8') as f:
                    answers = json.load(f)
                with open('classcard_audio.json', 'r', encoding='utf-8') as k:
                    audio_data = json.load(k)
                break
        except Exception as e:
            pass
        sleep(0.5)

# ----------------- 본격적인 실행 파트 -----------------
try:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    print(f"\n{YELLOW}크롬 브라우저를 실행 중입니다...{RESET}")
    driver = webdriver.Chrome(options=chrome_options)
    
    # URL 접속
    driver.get('https://www.classcard.net/Login')

    get = Get()

    # 아이디 비번 쳐서 로그인 진행
    login(loginID, loginPWD)
    
    # 단어장 페이지 접속 대기
    set_status()

    # 매칭 게임 실행 루프
    while True:
        try:
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
                    print(f"\n{RED}게임 상태가 변경되었습니다. 세트 데이터를 다시 불러옵니다.{RESET}")
                    set_status()

                w = get.words()
                m = get.meanings()
                get.do_click()
                get.Update()

            sleep(0.75)
        except Exception as e:
            sleep(0.5)

except Exception as e:
    print(f"\n{RED}[치명적 오류 발생]{RESET}")
    traceback.print_exc()
    input("\n프로그램이 강제 종료되었습니다. 엔터를 누르면 창이 닫힙니다...")
