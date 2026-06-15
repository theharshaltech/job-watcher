import requests

def get_jobs():

    jobs = []

    try:

        response = requests.get(
            "https://careers.cognizant.com/global/en",
            timeout=10
        )

        if response.status_code == 200:

            jobs.append({
                "company": "Cognizant",
                "role": "Careers Page Reachable",
                "link": "https://careers.cognizant.com/global/en"
            })

    except Exception as e:
        print("Error:", e)

    return jobs