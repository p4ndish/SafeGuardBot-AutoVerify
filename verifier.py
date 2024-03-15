# TOdo: make a functionality to switch to the iframe based on this link
# ref: https://stackoverflow.com/questions/7534622/select-iframe-using-python-selenium

from logging import exception
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options

import asyncio
import json
import time

class Verifier:
    def __init__(self, session_value) -> None:
        self.url = "https://web.telegram.org/k/" 
        self.key_value_pairs = session_value

    



        
    async def browse(self):
        # Open Chrome browser
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        wait = WebDriverWait(driver, timeout=22)


        try:
            # Open the Telegram web page
            driver.get(self.url)

            # Wait for the page to load
            # time.sleep(5)

            # Execute JavaScript to set local storage
            for key, value in self.key_value_pairs.items():
                # print("key -> ", key, "\n value: -> ", value)
                # print()
                script = f"localStorage.setItem('{key}', '{value}');"
                # print(script)
                driver.execute_script(script)

            # Refresh the page to apply changes
            driver.refresh()
            time.sleep(5)
            driver.get("https://web.telegram.org/k/#5434266369")
            time.sleep(5)
            if driver.current_url != "https://web.telegram.org/k/#5434266369":
                driver.get("https://web.telegram.org/k/#@SafeguardRobot")
                
            dummy_value = driver.find_element(By.CLASS_NAME, "row.no-wrap.row-with-padding.row-clickable.hover-effect.rp.chatlist-chat.chatlist-chat-bigger.row-big")

            wait.until(lambda x: dummy_value.is_displayed())
            # time.sleep(9)

            # dts =driver.find_elements(By.CLASS_NAME, "bubble.with-reply-markup.hide-name.photo.is-in.can-have-tail.is-group-first.is-group-last")

            # wait.until(lambda x: dts[0].is_displayed())

            # for dates in dts:
            #     print(dates.get_attribute("data-timestamp"))
            #     print()
            # print("\n\n")

            reply_keyboards = driver.find_elements(By.CLASS_NAME, "is-web-view.is-first.is-last.reply-markup-button.rp")
            safeguard_verify_Url = reply_keyboards[-1]
            safeguard_verify_Url.click()
            driver.implicitly_wait(10)

            if driver.find_element(By.CLASS_NAME, "popup.popup-peer.popup-confirmation.active"): 
                # CLICK LAUNCH
                driver.find_element(By.XPATH, "/html/body/div[7]/div/div[2]/button[1]/div").click()
            driver.implicitly_wait(10)

            time.sleep(5)


            popover = driver.find_element(By.CLASS_NAME, "popup.popup-payment.popup-payment-verification.popup-web-app.active")

            wait.until(lambda x: popover.is_displayed())

            # print(popover.get_attribute("outerHTML"))

            if popover:
                popover_iframe = popover.find_element(By.CLASS_NAME, "popup-body")

                driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@class='payment-verification']"))


                
                # time.sleep(9)
                time.sleep(2)
                x = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div/button")
                
                wait.until(lambda a: x.is_displayed())
                time.sleep(2)
                x.click()

                # prove the iframe is gone

                time.sleep(2)
                
                # popover = driver.find_element(By.CLASS_NAME, "popup.popup-payment.popup-payment-verification.popup-web-app.active")
                wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "popup.popup-payment.popup-payment-verification.popup-web-app.active")))
                

                driver.switch_to.default_content() 
                print("[+] Passed waiting for Iframe disappear")

                try:
                    popover = driver.find_element( By.CLASS_NAME, "popup.popup-payment.popup-payment-verification.popup-web-app.active")
                    print("[-] Failed scraping")
                    # time.sleep(40)
                    return False 

                except Exception as e :
                    print("[+] Sucessfull done scraping")
                    return True 

                    print("it disappears thanks god ")
                time.sleep(2)

                print("Done")
                return True 
            else:
                print("[-] Failed scraping")
                return False 

        except Exception as e:
            print(f"[-] Failed scraping Error: {e}")
            return False 

        finally:
            # Close the browser
            driver.quit()



# async def main():
#     f = open("sessions.json")
#     localstorage_data = json.load(f)
# # print(localstorage_data)
#     c = Verifier(localstorage_data)
#     await c.browse()


# asyncio.run(main())
