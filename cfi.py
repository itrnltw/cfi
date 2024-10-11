try:
    import sys as s
    import urllib.parse
    import requests
    import json
    import time
    import os
    from colorama import Fore, Back, Style, init
    bright = Style.BRIGHT
except Exception as e:
    s.exit(f"Some library {e} not installed | pip install -r requirements.txt")

headers = {
    'Content-Type': 'application/json',
    'Origin': 'https://g.cyberfin.xyz',
    'Referer': 'https://g.cyberfin.xyz/',
    'Secret-Key': 'cyberfinance',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

def read_tgWebAppData():
    if os.path.exists('initData.txt'):
        with open('initData.txt', 'r') as file:
            return file.read().splitlines()
    else:
        print("File 'initData.txt' tidak ditemukan.")
        return []

def initData(data):
    URL = "https://api.cyberfin.xyz/api/v1/game/initdata"
    res = requests.post(URL, headers=headers, json={"initData": data})
    return res.json()

def gameData(token):
    headers['Authorization'] = f"Bearer {token}"
    URL = "https://api.cyberfin.xyz/api/v1/game/mining/gamedata"
    res = requests.get(URL, headers=headers)
    return res.json()

def claim(token):
    headers['Authorization'] = f"Bearer {token}"
    URL = "https://api.cyberfin.xyz/api/v1/mining/claim"
    res = requests.get(URL, headers=headers)
    return res.json()

def upHammer(token):
    headers['Authorization'] = f"Bearer {token}"
    URL = "https://api.cyberfin.xyz/api/v1/mining/boost/apply"
    res = requests.post(URL, headers=headers, json={"boostType": "HAMMER"})
    return res.json()

def getDaily(token):
    headers['Authorization'] = f"Bearer {token}"
    URL = "https://api.cyberfin.xyz/api/v1/mining/claim/daily"
    res = requests.post(URL, headers=headers)
    return res.json()

def remaining(waktunya):
    # Dapatkan waktu saat ini dalam detik sejak epoch
    waktu_sekarang = int(time.time())

    # Hitung jumlah jam, menit, dan detik yang tersisa
    waktu_tersisa = waktunya - waktu_sekarang
    jam_tersisa = waktu_tersisa // 3600
    sisa_setelah_jam = waktu_tersisa % 3600
    menit_tersisa = sisa_setelah_jam // 60
    detik_tersisa = sisa_setelah_jam % 60

    return f"{jam_tersisa}:{menit_tersisa}:{detik_tersisa}"

def runTask(uuids, token):
    headers['Authorization'] = f"Bearer {token}"
    URL = "https://api.cyberfin.xyz/api/v1/gametask/complete/"
    for uuid in uuids:
        response = requests.patch(f"{URL}{uuid}", headers=headers)
        response_data = response.json()
        if response.status_code == 200:    
            print(f"{Fore.GREEN+Style.BRIGHT}Sukses | {uuid}")
        else:
            print(f"{Fore.RED+Style.BRIGHT}Gagal | {uuid} | {response_data['message']}")

def allTask(token):
    headers['Authorization'] = f"Bearer {token}"
    URL = "https://api.cyberfin.xyz/api/v1/gametask/all"
    res = requests.get(URL, headers=headers)
    if res.status_code == 200:
        tasks = res.json()['message']
        return [task['uuid'] for task in tasks if not task['isCompleted']]
    else:
        print("Failed to fetch tasks")
        return []

def main():
    init(autoreset=True)
    for tgWebAppData in read_tgWebAppData():
        
        username = json.loads(urllib.parse.unquote(urllib.parse.parse_qs(tgWebAppData)['user'][0]))['username']

        try:
            token = initData(tgWebAppData)['message']['accessToken']
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        

        dataGame = gameData(token)
        daily = getDaily(token)
        balance = dataGame['message']['userData']['balance']
        miningRate = float(dataGame['message']['miningData']['miningRate'])*3600
        crackTime = remaining(dataGame['message']['miningData']['crackTime'])
        klaim = claim(token)
        upgradeHammer = upHammer(token)

        print(f"=== {Fore.GREEN+bright+username+Style.RESET_ALL} ===")
        # print(f"Run Task:\n {runTask(allTask(token), token)}")
        print(f"Claim Daily\t: {Fore.GREEN+bright + 'Day-' + str(daily['message']['day']) +' | '+ str(daily['message']['reward']) if 'code' in daily and daily['code'] == 200 else Fore.RED+bright + daily['message']}{Style.RESET_ALL}")
        print(f"Balance\t\t: {Fore.GREEN+bright+ balance +Style.RESET_ALL}")
        print(f"$xCFI\t\t: {miningRate}/h")
        print(f"Crack Time\t: {Fore.YELLOW+bright+ crackTime +Style.RESET_ALL}")
        print(f"Claim\t\t: {Fore.YELLOW+bright}{klaim.get('message', '-')}{Style.RESET_ALL}")
        print(f"UpHammer\t: {Fore.YELLOW+bright}{upgradeHammer.get('message', '-')}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
    print("\n===  KELUAR  ===")