import requests

# URL de connexion et de la page cible
login_url = "https://menthorq.com/login/"
base_url = "https://menthorq.com/account/"

def connect(log, pwd):
    payload = {
        "log": log,
        "pwd": pwd,
        "wp-submit": "Log In",
        "redirect_to": "/account/",
        "mepr_process_login_form": "true",
        "mepr_is_login_page": "false",
    }

    with requests.Session() as s:
        s.get(base_url) 
        s.post(login_url, data=payload)
        r = s.get(base_url)

        if r.status_code == 200:
            html = r.text
            if "You are unauthorized to view this page." not in html:
                f = open("./html/main.html", "w")
                f.write(html)
                f.close()
                print("Site récupéré !")
            else: print("Erreur de connexion (mauvais identifiants)")
        else: print("ERREUR :", r.status_code)