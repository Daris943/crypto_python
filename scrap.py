import requests
import concurrent.futures
import time

certCount = 0
baseUrl = "https://crt.sh/?jd=1"
max_certificates = 1000000  # Vous devez définir le nombre maximum de certificats ici

# Créez un sémaphore avec 2 autorisations pour limiter à 2 threads en même temps
semaphore = concurrent.futures.ThreadPoolExecutor(max_workers=2)

def fetch_certificate(i):
    wait_duration = 5
    url = baseUrl + str(i)
    
    print("Accessing cert nb " + str(i))
    
    # Get the url content
    response = requests.get(url)
    
    if response.status_code == 429:
        print("Sleeping for " + str(wait_duration) + " secondes because of too many requess")
        time.sleep(wait_duration)
        return False
    
    if response.status_code != 200:
        print("SKIPPING nb" + str(i))
        print(response.content)
        return False
    
    if certCount % 100 == 0:
        print("Got " + str(certCount) + " certificates")
    
    with open('certificates/cert-' + str(i) + ".pem", 'wb') as f:
        f.write(response.content)
    
    return True

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [semaphore.submit(fetch_certificate, i) for i in range(max_certificates)]
        
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                certCount += 1
