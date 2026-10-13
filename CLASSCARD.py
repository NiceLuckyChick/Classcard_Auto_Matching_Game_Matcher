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

# 🌟 사람처럼 한 글자씩 타이핑하는 함수 (로그인 딜레이는 봇 탐지 방지를 위해 약간만 줄임)
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        sleep(random.uniform(0.01, 0.05)) # 기존 0.05~0.15에서 속도 향상

def login(user_id, user_pwd):
    try:
        print(f"{YELLOW}로그인 페이지 로딩 대기 중...{RESET}")
        wait = WebDriverWait(driver, 10)

        try:
            driver.find_element(By.ID, "login_id")
        except:
            try:
                first_btn = driver.find_element(By.XPATH, "//*[contains(text(), '로그인') or contains(text(), 'Login')]")
                first_btn.click()
                sleep(1.0)
            except:
                pass

        print(f"{YELLOW}아이디 입력 중...{RESET}")
        id_box = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//input[@id='login_id' or @name='login_id' or contains(@placeholder, '아이디') or contains(@placeholder, '이메일')]"
        )))
        try: id_box.click() 
        except: pass 
        id_box.clear()
        human_typing(id_box, user_id)

        print(f"{YELLOW}비밀번호 입력 중...{RESET}")
        pwd_box = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@type='password' or @id='login_pwd' or @name='login_pwd']"
        )))
        try: pwd_box.click() 
        except: pass 
        pwd_box.clear()
        human_typing(pwd_box, user_pwd)
        
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
        sleep(1.5) 

    except Exception as e:
        print(f"\n{RED}로그인 요소 찾기 실패 Error: {e}{RESET}")
        input("오류가 발생했습니다. 종료하려면 엔터를 누르세요...")
        sys.exit()

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
            self.left = [
                driver.find_element(By.ID, f"left_card_{i}") for i in range(4)
            ]
            for i, e in enumerate(self.left):
                self.wordlist[i] = e.text.split("\n")[0]
                try:
                    audio_icon = e.find_element(By.CSS_SELECTOR, "i.cc.vol_on")
                    self.audiolist[i] = audio_icon.get_attribute("data-src")
                except:
                    self.audiolist[i] = ""
        except:
            pass
        return self.wordlist
    
    def meanings(self):
        try:
            self.right = [
                driver.find_element(By.ID, f"right_card_{i}") for i in range(4)
            ]
            for i, e in enumerate(self.right):
                self.meaninglist[i] = e.text
        except:
            pass
        return self.meaninglist
    
    def check_(self, word_num, meaning_num):
        try:
            return answers.get(self.wordlist[word_num]) == self.meaninglist[meaning_num]
        except:
            return False
    
    def check_audio(self, src_num, meaning_num):
        try:
            return str(audio_data.get(self.audiolist[src_num])).strip() == str(self.meaninglist[meaning_num]).strip()
        except:
            return False
    
    def find_(self):
        return [(i, j) for i in range(4) for j in range(4) if self.check_(i, j)]
    
    def find_audio(self):
        return [(i, j) for i in range(4) for j in range(4) if self.check_audio(i, j)]
    
    def do_click(self):
        try:
            inform = self.find_()
            if not inform: inform = self.find_audio()
            for i, j in inform:
                # JS 클릭을 사용하여 애니메이션 딜레이 무시 및 속도 극대화
                driver.execute_script("arguments[0].click();", self.left[i])
                driver.execute_script("arguments[0].click();", self.right[j])
                print(f"\r{GREEN}Count: {self.count} {RESET}/{YELLOW} Score: {self.score}{RESET}", end="")
                self.count += 1
                sleep(0.05) # 기존 0.6초 -> 0.05초로 대폭 단축 (인식 안되면 0.1로 늘리세요)
        except:
            pass
    
    # ... (all_source, bind_data, saveJson, Update 등은 원본과 동일)
    def all_source(self):
        self.word_all_list = [el.get_attribute("textContent").strip() for el in driver.find_elements(By.CSS_SELECTOR, ".ex_front")]
        self.meaning_all_list = [el.get_attribute("textContent").strip() for el in driver.find_elements(By.CSS_SELECTOR, ".ex_back")]
        self.audio_all_list = [card.find_element(By.CSS_SELECTOR, ".btn-audio").get_attribute("data-src") for card in driver.find_elements(By.CSS_SELECTOR, ".flip-card")]
    
    def bind_data(self):
        self.source_dic = {self.word_all_list[i]: self.meaning_all_list[i] for i in range(len(self.word_all_list))}
        self.audio_dic = {self.audio_all_list[i]: self.meaning_all_list[i] for i in range(len(self.audio_all_list))}
    
    def saveJson(self):
        with open('cardbot_Source.json', 'w', encoding='utf-8') as f: json.dump(self.source_dic, f, ensure_ascii=False, indent=4)
        with open('classcard_audio.json', 'w', encoding='utf-8') as f: json.dump(self.audio_dic, f, ensure_ascii=False, indent=4)
    
    def Update(self):
        try: self.score = driver.find_element(By.CLASS_NAME, "point").text
        except: pass

def set_status():
    global driver, get, answers, audio_data
    print(f"\n{YELLOW}==> 직접 학습할 단어장(/set/) 페이지로 들어가주세요. 대기 중...{RESET}")
    while True:
        try:
            if "/set/" in driver.current_url:
                print(f"{YELLOW}세트 데이터를 수집합니다...{RESET}")
                get.all_source(); get.bind_data(); get.saveJson()
                print(f"{GREEN}데이터 저장 완료! 이제 '매칭 게임'을 실행하세요.{RESET}")
                
                with open('cardbot_Source.json', 'r', encoding='utf-8') as f: answers = json.load(f)
                with open('classcard_audio.json', 'r', encoding='utf-8') as k: audio_data = json.load(k)
                break
        except Exception:
            pass
        sleep(0.5)

# ----------------- 본격적인 실행 파트 -----------------
try:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    
    # 불필요한 로그 제거로 속도 약간 향상
    chrome_options.add_argument('--log-level=3') 
    chrome_options.add_argument('--disable-logging')

    print(f"\n{YELLOW}크롬 브라우저를 실행 중입니다...{RESET}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.classcard.net/Login')

    get = Get()
    login(loginID, loginPWD)
    set_status()

    while True:
        try:
            C_url = driver.current_url
            try:
                outGame = driver.find_element(By.ID, "wrapper-learn").get_attribute("class")
                if not ('hide-header' in outGame): experience = 1
            except: pass

            if "/Match/" in C_url:
                if ('hide-header' in outGame) and (experience):
                    experience = 0
                    print(f"\n{RED}게임 상태가 변경되었습니다. 세트 데이터를 다시 불러옵니다.{RESET}")
                    set_status()

                get.words()
                get.meanings()
                get.do_click()
                get.Update()

            sleep(0.1) # 기존 0.75초 -> 0.1초로 메인 루프 속도 대폭 향상
        except Exception as e:
            sleep(0.1)

except Exception as e:
    print(f"\n{RED}[치명적 오류 발생]{RESET}")
    traceback.print_exc()
    input("\n프로그램이 강제 종료되었습니다. 엔터를 누르면 창이 닫힙니다...")