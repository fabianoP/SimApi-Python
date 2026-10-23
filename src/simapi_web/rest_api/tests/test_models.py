from django.test import TestCase

from rest_api.models import FmuModel, Input, Output, User


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="Test User",
            email="testuser@example.com",
            password="test password",
        )
        self.model = FmuModel.objects.create(
            model_name="test_model",
            user=self.user,
            step_size=600,
            final_time=72.0,
        )

    def test_user_manager_and_display_names(self):
        self.assertEqual(self.user.get_full_name(), self.user.name)
        self.assertEqual(self.user.get_short_name(), self.user.name)
        self.assertEqual(str(self.user), self.user.email)
        self.assertTrue(self.user.check_password("test password"))

        superuser = User.objects.create_superuser(
            name="Admin User",
            email="admin@example.com",
            password="admin password",
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_fmu_model_display_name(self):
        self.assertEqual(str(self.model), self.model.model_name)

    def test_input_stores_structured_json(self):
        payload = {"yshade": 1.0, "enabled": True}

        model_input = Input.objects.create(
            user=self.user,
            fmu_model=self.model,
            time_step=600,
            input_json=payload,
        )

        model_input.refresh_from_db()
        self.assertEqual(model_input.input_json, payload)

    def test_output_stores_structured_json(self):
        payload = {"dry_bulb": 5.0, "zones": [1.2, 1.8]}

        model_output = Output.objects.create(
            user=self.user,
            fmu_model=self.model,
            time_step=800,
            output_json=payload,
        )

        model_output.refresh_from_db()
        self.assertEqual(model_output.output_json, payload)
