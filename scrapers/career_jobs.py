import requests

def get_jobs():

    jobs = []

    companies = [
        ("Cognizant", "https://careers.cognizant.com/global/en"),
        ("Infosys", "https://careers.infosys.com"),
        ("Accenture", "https://www.accenture.com/in-en/careers"),
        ("Wipro", "https://careers.wipro.com"),
        ("Capgemini", "https://www.capgemini.com/careers")
    ]

    for company, url in companies:

        try:

            response = requests.get(
                url,
                timeout=10
            )

            if response.status_code == 200:

                jobs.append({
                    "company": company,
                    "role": "Career Page Updated V2",
                    "link": url
                })

        except Exception as e:
            print(company, e)

    return jobs