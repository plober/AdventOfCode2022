# AdventOfCode2022
Intentos novatos para Advent of Code
* [READMe.md markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

## Cosas de Bash
```
curl -o "input#1.txt" https://adventofcode.com/2022/day/[10-15]/input   -H 'authority: adventofcode.com'   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'accept-language: en-US,en;q=0.9,es;q=0.8'   -H 'cache-control: no-cache'   -H 'cookie: session=(Tomada de Firefox)'   -H 'dnt: 1'   -H 'pragma: no-cache'   -H 'sec-ch-ua: "Chromium";v="108", "Not?A_Brand";v="8"'   -H 'sec-ch-ua-mobile: ?0'   -H 'sec-ch-ua-platform: "Windows"'   -H 'sec-fetch-dest: document'   -H 'sec-fetch-mode: navigate'   -H 'sec-fetch-site: none'   -H 'sec-fetch-user: ?1'   -H 'upgrade-insecure-requests: 1'   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'   --compressed
```
## Traducción a Python
```
import requests

cookies = {'session': 'Misterio'}

headers = {
    'authority': 'adventofcode.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="108", "Not?A_Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

for ejercicio in range(16, 26):
    response = requests.get(f'https://adventofcode.com/2022/day/{ejercicio}/input', cookies=cookies, headers=headers)
    with open(f'input{ejercicio}.txt', 'wb') as f: f.write(response.content)
```