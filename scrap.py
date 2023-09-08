import requests

certCount = 0
global i
i = 0
baseUrl = "https://crt.sh/?d="
url = url = baseUrl + str(i)

def fetch_certificate() :
    global i
    global certCount
    i += 1
    
    # get the url content
    response = requests.get(url)
    
    if response.status_code != 200 :
        print("SKIPPING nb" + str(i))
        return False
    
    if certCount % 100 == 0 :
        print("Got " + str(certCount) + " certificats")
    
    open('certificates/cert-' + str(certCount) + ".pem", 'wb').write(response.content)
    
    certCount += 1

while certCount < 1_000_000 :
    url = baseUrl + str(i)
    fetch_certificate()