import requests

def get_jobs():
    jobs = []

    jobs.append({
        "company": "Cognizant",
        "role": "Programmer Analyst Trainee",
        "link": "https://careers.cognizant.com"
    })

    jobs.append({
        "company": "Infosys",
        "role": "System Engineer",
        "link": "https://careers.infosys.com"
    })

    return jobs
    