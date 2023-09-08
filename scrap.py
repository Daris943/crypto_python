import requests

certCount = 0
baseUrl = "https://crt.sh/?d="

while certCount < 1_000_000 :
    url = baseUrl + str(certCount)
    response = requests.get(url)
    
    if response.status_code != 200 :
        print("SKIPPING nb" + str(certCount))
        continue
    
    print("Creating certificate nb" + str(certCount))
    
    open('certificates/cert-' + str(certCount) + ".pem", 'wb').write(response.content)
    certCount += 1