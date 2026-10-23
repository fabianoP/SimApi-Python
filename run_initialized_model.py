import argparse
import json
import os
import time

import requests


def parse_args():
    parser = argparse.ArgumentParser(description="Run initialized SimApi models")
    parser.add_argument("model_name")
    parser.add_argument("--step-size", type=int, default=600)
    parser.add_argument("--duration", type=int, default=86400, help="simulation duration in seconds")
    parser.add_argument("--shade", type=float, default=1.0)
    parser.add_argument("--poll-interval", type=float, default=0.5)
    parser.add_argument("--poll-timeout", type=float, default=300)
    return parser.parse_args()


def graphql(session, url, query):
    response = session.post(url, json={"query": query}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]


def wait_for_output(session, graphql_url, model_name, time_step, interval, timeout):
    query = """
    {{
        outputs(modelN: "{0}", tStep: {1}) {{
            outputJson
        }}
    }}
    """.format(model_name, time_step)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        outputs = graphql(session, graphql_url, query)["outputs"]
        if outputs:
            return outputs
        time.sleep(interval)
    raise TimeoutError(f"No output for {model_name} at time step {time_step}")


def main():
    args = parse_args()
    base_url = os.getenv("SIMAPI_URL", "http://localhost:8000").rstrip("/")
    email = os.getenv("SIMAPI_EMAIL", "user@user.com")
    password = os.getenv("SIMAPI_PASSWORD", "user user88")

    with requests.Session() as session:
        login_response = session.post(
            f"{base_url}/login/",
            data={"username": email, "password": password},
            timeout=30,
        )
        login_response.raise_for_status()
        headers = {"Authorization": f"Token {login_response.json()['token']}"}
        graphql_url = f"{base_url}/graphql/"

        model_query = """
        {{
            fmuModels(modelN: "{0}") {{
                modelName
            }}
        }}
        """.format(args.model_name)
        models = graphql(session, graphql_url, model_query)["fmuModels"]
        model_names = [model["modelName"] for model in models]
        if not model_names:
            raise RuntimeError(f"No initialized models found for {args.model_name}")

        print(f"Running {len(model_names)} model(s): {model_names}")
        for time_step in range(0, args.duration, args.step_size):
            for model_name in model_names:
                input_payload = {"time_step": time_step, "yShadeFMU": args.shade}
                response = session.post(
                    f"{base_url}/input/",
                    headers=headers,
                    data={
                        "fmu_model": model_name,
                        "time_step": time_step,
                        "input_json": json.dumps(input_payload),
                    },
                    timeout=30,
                )
                response.raise_for_status()
                output = wait_for_output(
                    session,
                    graphql_url,
                    model_name,
                    time_step,
                    args.poll_interval,
                    args.poll_timeout,
                )
                print(f"Sim: {model_name} | Time: {time_step} | Output: {output}")


if __name__ == "__main__":
    main()
