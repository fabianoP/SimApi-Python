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
