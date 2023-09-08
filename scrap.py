import requests

certCount = 0
i = -1
baseUrl = "https://crt.sh/?d="

while i < 1_000_000 :
    i += 1
    url = baseUrl + str(i)
    response = requests.get(url)
    
    if response.status_code != 200 :
        print("SKIPPING nb" + str(i))
        continue
    
    print("Creating certificate nb" + str(certCount))
    
    open('certificates/cert-' + str(certCount) + ".pem", 'wb').write(response.content)
    certCount += 1