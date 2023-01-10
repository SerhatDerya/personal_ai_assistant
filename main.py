import webbrowser
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from pydub import AudioSegment
import soundfile as sf
import pyrubberband as pyrb
import wikipedia
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

mail = input(email: )
password = input(password: )


wikipedia.set_lang("TR")
r = sr.Recognizer()
speed = 1.5
db=-0.5

def speak(sentence):
    tts = gTTS(sentence, lang="tr")
    tts.save("audio.mp3")
    sound = AudioSegment.from_mp3("audio.mp3")
    sound.export("audio.wav", format="wav")
    y, sr = sf.read("audio.wav")
    y_stretch = pyrb.time_stretch(y, sr, rate=speed)
    sf.write("analyzed_audio.wav", y_stretch, sr, format="wav")

    y, sr = sf.read("analyzed_audio.wav")
    y_new = pyrb.pitch_shift(y, sr, db)
    sf.write("analyzed_audio.wav", y_new, sr, format="wav")

    sound = AudioSegment.from_wav("analyzed_audio.wav")
    sound.export("analyzed_audio.mp3", format="mp3")
    playsound("analyzed_audio.mp3")
    os.remove("audio.mp3")
    os.remove("audio.wav")
    os.remove("analyzed_audio.mp3")
    os.remove("analyzed_audio.wav")

def listen():
  with sr.Microphone() as mic:
    try:
        r.adjust_for_ambient_noise(mic, duration=0.5)
        audio = r.listen(mic)
        audio = r.recognize_google(audio, language="TR-tr")
        audio = audio.lower()

        print(audio)
        return audio

    except sr.UnknownValueError:
        speak("Ne dediğini anlayamadım lütfen tekrar eder misin?")
        r.adjust_for_ambient_noise(mic, duration=0.5)
        audio = r.listen(mic)
        audio = r.recognize_google(audio, language="TR-tr")
        audio = audio.lower()

        print(audio)
        return audio


def respond(audio):

    if "kimdir" in audio:
        subject = audio.split("kimdir", maxsplit=1)[0]
        summary = wikipedia.summary(subject)
        speak(summary)

    elif "internette ara" in audio:
        search = audio.replace("internette ara", "")
        url = "https://www.google.com/search?q=" + search
        webbrowser.get().open(url)

    elif ("youtube'a gir" in audio) or ("youtube'u aç" in audio):
        url = "https://www.youtube.com"
        webbrowser.get().open(url)

    elif "saat kaç" in audio:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        speak("saat" + current_time)

    elif "kampüs sistemine gir" in audio:
        driver = webdriver.Firefox(executable_path="/home/serhat/İndirilenler/geckodriver-v0.31.0-linux64/geckodriver")
        driver.get("https://kampus.izu.edu.tr/login")

        username_box = driver.find_element(by=By.ID, value="user_name")
        username_box.send_keys(mail)

        password_box = driver.find_element(by=By.NAME, value="password")
        password_box.send_keys(password)

        login_button = driver.find_element(by=By.CLASS_NAME, value="submit")
        login_button.click()

    elif "ortalamamı söyle" in audio:
        driver = webdriver.Firefox(executable_path="/home/serhat/İndirilenler/geckodriver-v0.31.0-linux64/geckodriver")
        driver.get("https://kampus.izu.edu.tr/login")

        username_box = driver.find_element(by=By.ID, value="user_name")
        username_box.send_keys("example.mail@std.izu.edu.tr")

        password_box = driver.find_element(by=By.NAME, value="password")
        password_box.send_keys("password")

        login_button = driver.find_element(by=By.CLASS_NAME, value="submit")
        login_button.click()

        transcript=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sanal")))
        transcript.click()

        agno = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "Ortalama"))).text
        agno = agno.split(".")[0] + "nokta" + agno.split(".")[1]
        speak("ortalaman" + agno)

        dropdown = driver.find_element_by_xpath("/html/body/div[1]/header/div/ul[6]/li/a")
        dropdown.click()

        close = driver.find_element_by_id("login_close")
        close.click()

        time.sleep(0.5)
        driver.close()

    elif (("duyuru oku" in audio) or ("duyuruyu oku" in audio) or ("son duyuru" in audio)):
        driver = webdriver.Firefox(executable_path="/home/serhat/İndirilenler/geckodriver-v0.31.0-linux64/geckodriver")
        driver.get("https://kampus.izu.edu.tr/login")

        username_box = driver.find_element(by=By.ID, value="user_name")
        username_box.send_keys("derya.serhat@std.izu.edu.tr")

        password_box = driver.find_element(by=By.NAME, value="password")
        password_box.send_keys("Tahres.2bin1")

        login_button = driver.find_element(by=By.CLASS_NAME, value="submit")
        login_button.click()

        driver.implicitly_wait(2)

        #title = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]").text
        name = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]").text
        subject = driver.find_element_by_css_selector("div.panel:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)").text

        question =  name + "tarafından oluşturulmuş" + subject[:-10] + "adlı duyuruyu okumamı ister misin?"
        speak(question)
        answer = listen()
        if ("evet" or "oku " or "istiyorum" or "isterim") in answer:
            announcement = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]").text
            speak(announcement)
        elif ("hayır" or "istemiyorum" or "okuma ") in answer:
            speak("Tamam, nasıl istersen.")

        dropdown = driver.find_element_by_xpath("/html/body/div[1]/header/div/ul[6]/li/a")
        dropdown.click()

        close = driver.find_element_by_id("login_close")
        close.click()

        time.sleep(0.5)
        driver.close()

    else:
        speak("üzgünüm bunu yapabileceğimi sanmıyorum. başka nasıl yardımcı olabilirim?")
        audio = listen()
        respond(audio)



speak("Nasıl yardımcı olabilirim?")
audio=listen()
respond(audio)

