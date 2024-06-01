import atexit
import json
import argparse
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import requests
import traceback

class BlazeDoubleBot:
    def __init__(self, config):
        self.username = config['username']
        self.password = config['password']
        self.bet_amount = config['bet_amount']
        self.stop_loss_ratio = config['stop_loss_ratio']
        self.stop_win_ratio = config['stop_win_ratio']
        self.wait_after_bet = config['wait_after_bet']
        self.martingale = config['martingale']
        self.strategies = config['strategies']
        self.language = config.get('language', 'en')
        self.headless = config.get('headless', True)

        self.color_dict = {'black': 'B', 'red': 'R', 'white': 'W'}
        print(self.get_text('Initializing the robot ...'))
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
            
        self.driver = uc.Chrome(options=chrome_options)    
        print(self.get_text('Accessing website ...'))
        self.driver.get('https://blaze1.space/nt/games/double')
        sleep(10)
        print(self.get_text('Logging in ...'))
        self.login()
        sleep(10)
        print(self.get_text('Logged ...'))

        self.initial_balance = self.get_balance()
        self.current_balance = self.initial_balance
        self.stop_loss = self.initial_balance * self.stop_loss_ratio
        self.stop_win = self.initial_balance * self.stop_win_ratio
        atexit.register(self.close_driver)
    def get_color(self,color):
        colors = {
            'B':'⚫',
            'R':'🔴',
            'W':'⚪'
            }
        return colors[color]

    def get_text(self, text):
        texts = {
            'Initializing the robot ...': {'en': 'Initializing the robot ...', 'pt': 'Inicializando o robô ...'},
            'Accessing website ...': {'en': 'Accessing website ...', 'pt': 'Acessando o site ...'},
            'Logging in ...': {'en': 'Logging in ...', 'pt': 'Logando ...'},
            'Logged ...': {'en': 'Logged ...', 'pt': 'Logado ...'},
            'Clicking to login': {'en': 'Clicking to login', 'pt': 'Clicando para logar'},
            'Entering username': {'en': 'Entering username', 'pt': 'Inserindo nome de usuário'},
            'Entering password': {'en': 'Entering password', 'pt': 'Inserindo senha'},
            'Logging in': {'en': 'Logging in', 'pt': 'Logando'},
            'Error getting history:': {'en': 'Error getting history:', 'pt': 'Erro ao obter histórico:'},
            'Bet on Red': {'en': 'Bet on 🔴', 'pt': 'Apostar no 🔴'},
            'Bet on Black': {'en': 'Bet on ⚫', 'pt': 'Apostar no ⚫'},
            'Completed': {'en': 'Completed', 'pt': 'Concluído'},
            'Waiting for result ...': {'en': 'Waiting for result ...', 'pt': 'Esperando o resultado ...'},
            'Win ->': {'en': 'Win ->', 'pt': 'Ganhou ->'},
            'Loss ->': {'en': 'Loss ->', 'pt': 'Perdeu ->'},
            'Balance: $': {'en': 'Balance: $', 'pt': 'Saldo: $'},
            'Waiting seconds to restart analysis ...': {'en': f'Waiting {self.wait_after_bet} seconds to restart analysis ...', 'pt': f'Esperando {self.wait_after_bet} segundos para reiniciar a análise ...'},
            'Analyzes restarted! ->': {'en': f'Analyzes restarted! -> {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}', 'pt': f'Análises reiniciadas! -> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'},
            'Initial Balance: $': {'en': 'Initial Balance: $', 'pt': 'Saldo Inicial: $'},
            'Stop Loss: $': {'en': 'Stop Loss: $', 'pt': 'Stop Loss: $'},
            'Stop Win: $': {'en': 'Stop Win: $', 'pt': 'Stop Win: $'},
            'Bet Amount: $': {'en': 'Bet Amount: $', 'pt': 'Quantia de Aposta: $'},
            'Final Balance: $': {'en': 'Final Balance: $', 'pt': 'Saldo Final: $'},
            'Blaze Double Bet Bot Started': {'en': 'Blaze Double Bet Bot Started', 'pt': 'Robô de Aposta Blaze Double Iniciado'},
            'Blaze Double Bet Bot Finished': {'en': 'Blaze Double Bet Bot Finished', 'pt': 'Robô de Aposta Blaze Double Finalizado'},
            'Betting strategy -> ':{'en':'Betting strategy -> ','pt':'Estratégia de aposta -> '},
            'dateTimeNow':{'en': f'{datetime.now().strftime("%Y/%d/%m %H:%M:%S")}','pt':f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'},
            'Press ENTER to exit':{'en':'Press ENTER to exit','pt':'Aperte ENTER para sair'}
        }
        return texts.get(text, {}).get(self.language, text)

    def login(self):
        sleep(5)
        self.driver.find_element(By.XPATH, "//a[@class='link']").click()
        print(self.get_text('Clicking to login'))
        sleep(5)
        self.driver.find_element(By.XPATH, "//input[contains(@name,'username')]").send_keys(self.username)
        print(self.get_text('Entering username'))
        sleep(5)
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(self.password)
        print(self.get_text('Entering password'))
        sleep(5)
        self.driver.find_element(By.CLASS_NAME, "red.submit.shared-button-custom.css-12vlaew").click()
        print(self.get_text('Logging in'))
        sleep(5)

    def close_driver(self):
        self.driver.close()  
        self.driver.quit()   

    def is_time_to_bet(self):
        timer_text = self.driver.find_element(By.ID, "roulette-timer").text.lower()
        if 'rolling in' in timer_text:
            print(timer_text)
            return True
        return False

    def is_time_to_bet_api(self):
        info = requests.get('https://blaze1.space/api/roulette_games/current').json()
        if info['status'] == 'waiting':
            return True
        return False

    def get_history_api(self):
        colors = {0: 'W', 1: 'R', 2: 'B'}
        history = requests.get('https://blaze1.space/api/roulette_games/recent').json()
        history_list = [h['color'] for h in history]
        return [colors[n] for n in history_list]

    def choose_color(self, color):
        bet_buttons = self.driver.find_elements(By.CLASS_NAME, color)
        for btn in bet_buttons:
            if 'x2' in btn.text:
                btn.click()
                break

    def place_bet(self, amount):
        self.driver.find_element(By.CLASS_NAME, 'input-field').clear()
        sleep(0.5)
        self.driver.find_element(By.CLASS_NAME, 'input-field').send_keys(amount)
        sleep(0.5)
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        sleep(0.5)
        for b in buttons:
            if 'shared-button-custom css-1apb7jj' in b.get_attribute('class'):
                actions = ActionChains(self.driver)
                sleep(0.5)
                actions.click(b).perform()
                break

    def print_bet(self, color):
        print(f'''{self.get_text("Bet on Red" if color == "red" else "Bet on Black")}
{self.get_text("Completed")} {self.get_text("dateTimeNow")}
{self.get_text("Waiting for result ...")}
''')

    def print_bet_result(self, history, color):
        print(f'{self.get_text("Win ->")} {[self.get_color(c) for c in history]}' if history[-1] == self.color_dict[color] else f'{self.get_text("Loss ->")} {[self.get_color(c) for c in history]}')

    def get_balance(self):
        return float(self.driver.find_element(By.CLASS_NAME, 'amount').text.replace(',', '.').split(' ')[-1])

    def strategy(self, history):
        for color, sequences in self.strategies.items():
            for sequence in sequences:
                size = len(sequence)
                if history[:size][::-1] == sequence:
                    return size,color
        return None,None


    def print_initialization_text(self):
        print(f'''
{50 * "*"}

***  {self.get_text('Blaze Double Bet Bot Started')}   ***
{self.get_text("dateTimeNow")}

{self.get_text('Initial Balance: $')} {round(self.initial_balance, 2)}

{self.get_text('Stop Loss: $')} {round(self.stop_loss, 2)}

{self.get_text('Stop Win: $')} {round(self.stop_win, 2)}

{self.get_text('Bet Amount: $')} {round(self.bet_amount, 2)}

{50 * "*"}

''')

    def print_final_text(self):
        print(f'''
{50 * "*"}

***  {self.get_text('Blaze Double Bet Bot Finished')}   ***

{self.get_text('Initial Balance: $')} {round(self.initial_balance, 2)}

{self.get_text('Final Balance: $')} {round(self.current_balance, 2)}

{self.get_text("dateTimeNow")}

{50 * "*"}

''')

    def wait_for_next_round(self):
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, 'time-left').find_element(By.TAG_NAME, 'span').text
            except:
                break

        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, 'time-left').find_element(By.TAG_NAME, 'span').text
                return True
            except:
                pass

    def run(self):
        try:  
            self.print_initialization_text()
            
            while True:
                if self.stop_loss <= self.current_balance <= self.stop_win and self.current_balance - self.bet_amount >= 0:
                    if self.wait_for_next_round():
                        history = self.get_history_api()
                        size,color = self.strategy(history)
                        if color:
                            self.choose_color(color)
                            self.place_bet(self.bet_amount)
                            print(self.get_text('Betting strategy -> '),[self.get_color(c) for c in history[:size][::-1]])
                            print()
                            self.print_bet(color)
                            self.wait_for_next_round()
                            #sleep(1)
                            history = self.get_history_api()[:size][::-1]
                            self.current_balance = self.get_balance()
                            for m in range(self.martingale):
                                
                                if history[-1] != self.color_dict[color] and self.stop_loss <= self.current_balance <= self.stop_win and self.current_balance - self.bet_amount >= 0:
                                    self.place_bet((2**(m+1)) * self.bet_amount)
                                    print(f'Gale {m + 1} -> ',[self.get_color(c) for c in history],f'$ {(2**(m+1)) * self.bet_amount}')
                                    self.wait_for_next_round()
                                    #sleep(1)
                                    history = self.get_history_api()[:size][::-1]
                                    self.current_balance = self.get_balance()
                                    
                            self.print_bet_result(history, color)
                            sleep(8)
                            self.current_balance = self.get_balance()
                            print(self.get_text('Balance: $'),self.current_balance)
                            print(self.get_text("dateTimeNow"))
                            if self.stop_loss <= self.current_balance <= self.stop_win and self.current_balance - self.bet_amount >= 0:
                                print(f'{self.get_text("Waiting seconds to restart analysis ...")}\n')
                                sleep(self.wait_after_bet)
                                print(50*'*')
                                print(self.get_text('Analyzes restarted! -> '),self.get_text("dateTimeNow"))
                    
                            
                else:
                    self.print_final_text()
                    self.close_driver()
                    input(self.get_text('Press ENTER to exit'))
                    break
                
                
                sleep(2)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.print_final_text()
            self.close_driver()
            input(self.get_text('Press ENTER to exit'))
            

def main():
    parser = argparse.ArgumentParser(description='Blaze Double Bot')
    parser.add_argument('--config', type=str, default='config.json', help='config.json')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    bot = BlazeDoubleBot(config)
    bot.run()

if __name__ == "__main__":
    main()
