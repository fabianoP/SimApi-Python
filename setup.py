import requests


class Setup:
    user_url = 'http://0.0.0.0:8000/user/'
    login_url = 'http://0.0.0.0:8000/login/'
    init_url = 'http://0.0.0.0:8000/init_model/'
    input_url = 'http://0.0.0.0:8000/input/'
    output_url = 'http://0.0.0.0:8000/output/'
    graphql_url = 'http://0.0.0.0:8000/graphql/'

    def create_user(self, user_email='user@user.com', user_name='user', user_password='user user88'):
        json_data = {
            "name": user_name,
            "email": user_email,
            "password": user_password
        }

        return requests.post(self.user_url, data=json_data)

    def login(self, username="user@user.com", password="user user88"):
        # login details for user
        data = {"username": username,  # username = email
                "password": password}

        resp = requests.post(self.login_url, data=data)

        json_resp = resp.json()

        token = json_resp['token']  # get validation token
        return {'Authorization': 'Token ' + token}  # set request header
