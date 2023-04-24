import requests
import random
import time
from faker import Faker
from datetime import datetime

fake = Faker()

def solve_captcha(api_key, site_key, url):
    captcha_request_url = 'https://2captcha.com/in.php'
    captcha_request_data = {
        'key': api_key,
        'method': 'userrecaptcha',
        'googlekey': site_key,
        'pageurl': url,
        'json': 1
    }
    response = requests.post(captcha_request_url, data=captcha_request_data)
    response_json = response.json()

    if response_json['status'] == 1:
        request_id = response_json['request']
        while True:
            time.sleep(5)
            result_url = f'https://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1'
            result_response = requests.get(result_url)
            result_json = result_response.json()

            if result_json['status'] == 1:
                return result_json['request']
            elif result_json['request'] == 'CAPCHA_NOT_READY':
                continue
            else:
                print("Erreur lors de la résolution du CAPTCHA")
                return None
    else:
        print("Erreur lors de l'envoi du CAPTCHA")
        return None

def create_account(api_key):
    username = fake.user_name()
    password = fake.password()
    gender = random.choice(["Male", "Female"])
    birth_year = random.randint(1960, 2008)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)

    signup_url = "https://auth.roblox.com/v2/signup"
    site_key = "6LhmtOgZAAAAADtS5C5M5Mzq1wY0Y4vf4KZ65i1Q"
    captcha_solution = solve_captcha(api_key, site_key, signup_url)

    if captcha_solution is None:
        print("Échec de la résolution du CAPTCHA")
        return None

    signup_data = {
        "username": username,
        "password": password,
        "gender": gender,
        "dateOfBirth": f"{birth_year}-{birth_month}-{birth_day}",
        "g-recaptcha-response": captcha_solution
    }

    response = requests.post(signup_url, json=signup_data)

    if response.status_code == 200:
        print(f"Compte créé avec succès : {username}")
        return username, password
    else:
        print("Échec de la création du compte")
        print(response.text)
        return None

def main():
    num_accounts = 10  # Nombre de comptes à créer
    output_file = "accounts.txt"
    api_key = "your_2captcha_api_key"

    with open(output_file, "a") as f:
        for _ in range(num_accounts):
            account_info = create_account(api_key)
            if account_info is not None:
                f.write(f"{account_info[0]}:{account_info[1]}\n")

if __name__ == "__main__":
    main()
