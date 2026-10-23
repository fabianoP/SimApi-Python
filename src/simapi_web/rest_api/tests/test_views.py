from django.test import Client
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rest_api.models import FmuModel, Input, Output, User


class JsonApiViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="test password",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.model = FmuModel.objects.create(
            model_name="test_model",
            user=self.user,
            container_id="simulator",
            step_size=600,
            final_time=72.0,
        )

    def test_model_creation_uses_authenticated_user(self):
        response = self.client.post(
            "/init_model/",
            {
                "model_name": "simulator_test",
                "container_id": "simulator",
                "step_size": 800,
                "final_time": "72.0",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = FmuModel.objects.get(model_name="simulator_test")
        self.assertEqual(created.user, self.user)

    def test_model_creation_defaults_to_compose_simulator(self):
        response = self.client.post(
            "/init_model/",
            {
                "model_name": "simulator_default",
                "step_size": 600,
                "final_time": "24.0",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = FmuModel.objects.get(model_name="simulator_default")
        self.assertEqual(created.container_id, "simulator")

    def test_input_creation_stores_input_json(self):
        payload = {"yshade": 1.0, "schedule": [0, 1, 1]}

        response = self.client.post(
            "/input/",
            {
                "fmu_model": self.model.model_name,
                "time_step": 600,
                "input_json": payload,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        model_input = Input.objects.get()
        self.assertEqual(model_input.user, self.user)
        self.assertEqual(model_input.input_json, payload)
        self.assertEqual(response.data["input_json"], payload)

    def test_output_creation_stores_output_json(self):
        payload = {"dry_bulb": 5.0, "zones": {"office": 21.5}}

        response = self.client.post(
            "/output/",
            {
                "fmu_model": self.model.model_name,
                "time_step": 800,
                "output_json": payload,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        model_output = Output.objects.get()
        self.assertEqual(model_output.user, self.user)
        self.assertEqual(model_output.output_json, payload)
        self.assertEqual(response.data["output_json"], payload)

    def test_login_returns_auth_token(self):
        self.client.credentials()
        response = self.client.post(
            "/login/",
            {
                "username": self.user.email,
                "password": "test password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], self.token.key)

    def test_graphql_filters_zero_time_step(self):
        Input.objects.create(
            user=self.user,
            fmu_model=self.model,
            time_step=0,
            input_json={"time_step": 0, "yShadeFMU": 1.0},
        )
        Input.objects.create(
            user=self.user,
            fmu_model=self.model,
            time_step=600,
            input_json={"time_step": 600, "yShadeFMU": 0.5},
        )
        Output.objects.create(
            user=self.user,
            fmu_model=self.model,
            time_step=0,
            output_json={"temp": 20.0},
        )
        Output.objects.create(
            user=self.user,
            fmu_model=self.model,
            time_step=600,
            output_json={"temp": 21.5},
        )

        response = self.client.post(
            "/graphql/",
            {
                "query": """
                {
                    inputs(modelN: "test_model", tStep: 0) {
                        timeStep
                        inputJson
                    }
                    outputs(modelN: "test_model", tStep: 0) {
                        timeStep
                        outputJson
                    }
                }
                """
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]
        self.assertEqual(len(data["inputs"]), 1)
        self.assertEqual(data["inputs"][0]["timeStep"], 0)
        self.assertEqual(len(data["outputs"]), 1)
        self.assertEqual(data["outputs"][0]["timeStep"], 0)

    def test_graphql_post_allows_csrf_exempt_clients(self):
        csrf_client = Client(enforce_csrf_checks=True, HTTP_HOST="localhost")
        response = csrf_client.post(
            "/graphql/",
            data='{"query": "{ fmuModels(modelN: \\"test_model\\") { modelName } }"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["data"]["fmuModels"],
            [{"modelName": "test_model"}],
        )


