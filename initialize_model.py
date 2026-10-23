import argparse
import os
from pathlib import Path

import requests


def parse_args():
    parser = argparse.ArgumentParser(description="Initialize a SimApi FMU model")
    parser.add_argument("model_name")
    parser.add_argument("--idf", type=Path, default=Path("test_setup_files/update.idf"))
    parser.add_argument("--epw", type=Path, default=Path("test_setup_files/update.epw"))
    parser.add_argument("--step-size", type=int, default=600)
    parser.add_argument("--final-time", type=float, default=24.0)
    return parser.parse_args()


def main():
    args = parse_args()
    base_url = os.getenv("SIMAPI_URL", "http://localhost:8000").rstrip("/")
    email = os.getenv("SIMAPI_EMAIL", "user@user.com")
    name = os.getenv("SIMAPI_USER", "user")
    password = os.getenv("SIMAPI_PASSWORD", "user user88")

    with requests.Session() as session:
        user_response = session.post(
            f"{base_url}/user/",
            data={"name": name, "email": email, "password": password},
            timeout=30,
        )
        if user_response.status_code not in {201, 400}:
            user_response.raise_for_status()

        login_response = session.post(
            f"{base_url}/login/",
            data={"username": email, "password": password},
            timeout=30,
        )
        login_response.raise_for_status()
        headers = {"Authorization": f"Token {login_response.json()['token']}"}

        with args.idf.open("rb") as idf_file, args.epw.open("rb") as epw_file:
            response = session.post(
                f"{base_url}/init_model/",
                headers=headers,
                data={
                    "model_name": args.model_name,
                    "step_size": args.step_size,
                    "final_time": args.final_time,
                },
                files={
                    "idf_file": (args.idf.name, idf_file),
                    "epw_file": (args.epw.name, epw_file),
                },
                timeout=120,
            )
        response.raise_for_status()
        print(response.text)


if __name__ == "__main__":
    main()
