import math
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pythonProject.src.variables import upgrade_container_xpath, price_inventory_case_xpath, price_upgrade_case_xpath, \
    name_inventory_case_xpath, name_upgrade_skin_xpath, percent_xpath, start_button_xpath, result_xpath, \
    inactive_start_button_xpath, button_history_xpath, button_inventory_xpath, \
    case_name_history_xpath, any_skin_in_inventory_xpath, balance_adjustment_slider_xpath, balance_xpath, \
    spending_balance_xpath, url


class Test_037_upgrade_with_coins:
    def test_037_upgrade_with_coins(self, driver, auth, clean_inventory_before_test, get_skin_to_the_inventory_10,
                                    clean_inventory_after_test, logout_after_test):
        """Ожидания, которые используются для использования элементов."""
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)
        wait_for_round = WebDriverWait(driver, 20)  # Ожидание апгрейда, жду когда анимация прокрутится.

        """Флаги и скины."""
        driver.get(f"{url}upgrade")  # Перехожу на страницу апгрейда.
        flag_win = False
        flag_lose = False
        flag_skin_count = 10

        skin_from_inventory = f"//div[@class='upgrade-inventories-container']/div[1]/div[3]/div/div/div[1]"  # Первый скин в инвентаре.
        skin_for_upgrade = f"//div[@class='upgrade-inventories-container']/div[2]/div[3]/div/div/div[6]"  # Шестой скин разделе в скинов для апгрейда.

        while not (flag_win and flag_lose):
            """Выбираю скин из инвентаря и скин для апгрейда."""
            wait.until(
                EC.visibility_of_element_located((By.XPATH, upgrade_container_xpath)))  # Жду появление инвентарь.
            driver.find_element(By.XPATH, skin_from_inventory).click()  # Нажал на выбранный скин.
            wait.until(EC.element_to_be_clickable((By.XPATH, skin_for_upgrade)))  # Жду появление скина для апгрейда.
            driver.find_element(By.XPATH, skin_for_upgrade).click()  # Нажал на скин для апгрейда.

            """Собираю данные об используемых скинах."""
            name_inventory_case = driver.find_element(By.XPATH,
                                                      name_inventory_case_xpath).text  # Взял имя скина из инвентаря.
            name_upgrade_case = driver.find_element(By.XPATH,
                                                    name_upgrade_skin_xpath).text  # Взял имя скина для апгрейда.
            price_inventory_case = float(
                driver.find_element(By.XPATH, price_inventory_case_xpath).text)  # Взял цену скина из инвентаря.
            price_upgrade_case = float(
                driver.find_element(By.XPATH, price_upgrade_case_xpath).text)  # Взял цену скина для апгрейда.

            """Беру баланс и процент до использования койнов."""
            wait.until(
                EC.visibility_of_element_located((By.XPATH, balance_xpath)))  # Жду появление баланса.
            balance = float(driver.find_element(By.XPATH,
                                                balance_xpath).text)  # Взял баланс.
            percent = driver.find_element(By.XPATH, percent_xpath).text  # Взял процент для апгрейда.
            percent = float(percent[:-1])
            spending_balance = float(driver.find_element(By.XPATH,
                                                         spending_balance_xpath).text)  # Взял баланс используемый для апгрейда - 0.0.

            """Проверки до использования койнов."""
            assert (price_inventory_case + spending_balance) <= (
                    price_upgrade_case * 0.6)  # Проверил, что вписываемся в 60%.
            assert percent == math.floor(((
                                                  price_inventory_case / price_upgrade_case) * 100) * 100) / 100  # Проверил, что написанный процент соответствует тому, что я высчитал, взяв цены с экрана.

            """Двигаю бегунок для изменения баланса."""
            balance_adjustment_slider = driver.find_element(By.XPATH,
                                                            balance_adjustment_slider_xpath)  # Взял слайдер настройки баланса для апгрейда.
            action = ActionChains(driver)  # Переменная действия которое будет двигать бегунок.
            action.click_and_hold(balance_adjustment_slider).move_by_offset(700,
                                                                            0).perform()  # Подвинул бегунок вправо.
            action.click_and_hold(balance_adjustment_slider).move_by_offset(-300,
                                                                            0).perform()  # Подвинул бегунок влево.
            action.click_and_hold(balance_adjustment_slider).move_by_offset(500,
                                                                            0).perform()  # Подвинул бегунок вправо.

            """Беру новый процент."""
            time.sleep(2)
            new_percent = driver.find_element(By.XPATH, percent_xpath).text  # Взял процент для апгрейда.
            new_percent = float(new_percent[:-1])
            new_spending_balance = float(driver.find_element(By.XPATH,
                                                             spending_balance_xpath).text)  # Взял новый баланс используемый для апгрейда.

            """Сравниваю новые данные со старыми данными."""
            time.sleep(0.5)
            assert new_percent > percent  # Проверил, что новый процент выигрыша больше старого процента выигрыша.
            assert (price_inventory_case + new_spending_balance) <= (
                    price_upgrade_case * 0.6)  # Проверил, что новый процент вписывается в 60 %.
            assert new_percent == math.floor((((
                                                       price_inventory_case + new_spending_balance) / price_upgrade_case) * 100) * 100) / 100  # Проверил, что написанный процент соответствует тому, что я высчитал, взяв цены с экрана.

            """Запуск апгрейда."""
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, start_button_xpath)))  # Жду отображения кнопки запуска апгрейда.

            driver.find_element(By.XPATH, start_button_xpath).click()  # Запустил апгрейд.
            wait_for_round.until(EC.visibility_of_element_located(
                (By.XPATH, result_xpath)))  # Жду появления надписи "Победа" или "Проигрыш".
            result = driver.find_element(By.XPATH, result_xpath).text  # Взял надпись "Победа" или "Проигрыш".
            wait_for_round.until(EC.visibility_of_element_located((By.XPATH,
                                                                   inactive_start_button_xpath)))  # Жду когда закончится анимация апгрейда и появится неактивная кнопка запуска апгрейда.
            """Беру новый баланс"""
            new_balance = float(driver.find_element(By.XPATH,
                                                    balance_xpath).text)  # Взял новый баланс.

            """Сравниваю баланс до и после апгрейда."""
            balance_and_new_spending_balance = round(balance - new_spending_balance, 2)
            assert new_balance == balance_and_new_spending_balance

            """Условия при победе и поражении."""
            if result == "Проигрыш":
                flag_skin_count -= 1  # Отнял один скин который потратили при апгрейде.
                flag_lose = True
                driver.get(f"{url}profile")
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, button_history_xpath)))  # Жду появления кнопки "Инвентарь".
                driver.find_element(By.XPATH, button_history_xpath).click()  # Нажал на кнопку "История".
                case_name_history = driver.find_element(By.XPATH,
                                                        case_name_history_xpath).text  # Взял имя первого скина из истории (то есть последнего, который попал в историю).
                assert case_name_history == name_inventory_case  # Сравнил имя скина который потратили при апгрейде и того, что взяли из истории.
                driver.get(f"{url}upgrade")  # Вернулся на страницу апгрейда.
                wait.until(
                    EC.visibility_of_element_located((By.XPATH, upgrade_container_xpath)))  # Жду появление инвентарь.
            else:
                flag_win = True
                driver.get(f"{url}profile")
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, button_history_xpath)))  # Жду появления кнопки "Инвентарь".
                driver.find_element(By.XPATH, button_history_xpath).click()  # Нажал на кнопку "История".
                case_name_history = driver.find_element(By.XPATH,
                                                        case_name_history_xpath).text  # Взял имя первого скина из истории (то есть последнего, который попал в историю).
                assert case_name_history == name_inventory_case  # Сравнил имя скина который потратили при апгрейде и того, что взяли из истории.
                driver.find_element(By.XPATH, button_inventory_xpath).click()  # Нажал на кнопку "Инвентарь".

                skins_in_inventory = len(
                    driver.find_elements(By.XPATH, any_skin_in_inventory_xpath))  # Узнал сколько скинов инвентаре.
                assert skins_in_inventory == flag_skin_count  # Проверил колличество скинов в инвентаре.

                names_in_inventory = driver.find_elements(By.XPATH,
                                                          "//div[@class='default-inventory-container']/div/div/div/div[2]/div")  # Взял имена всех скинов в инвентаре.
                names_in_inventory = [i.text for i in names_in_inventory]  # Перевёл имена в текст.
                assert name_upgrade_case in names_in_inventory  # Проверил наличие имени выигранного скина в инвентаре.

                driver.get(f"{url}upgrade")
                wait.until(
                    EC.visibility_of_element_located((By.XPATH, upgrade_container_xpath)))  # Жду появление инвентарь.