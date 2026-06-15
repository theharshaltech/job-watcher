import requests

def get_jobs():

    jobs = []

    try:

        response = requests.get(
            "https://careers.cognizant.com/global/en"
        )

        if response.status_code == 200:

            jobs.append({
                "company": "Cognizant",
                "role": "Careers Page Updated",
                "link": "https://careers.cognizant.com/global/en"
            })

    except Exception as e:
        print(e)

    return jobs