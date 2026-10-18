"""Dashboard API contract checks. Roboflow calls are replaced with fixtures."""
import base64
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
from PIL import Image
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "files/lesson-03"))
from app import app
from core import normalize_response
from workflow import WorkflowError, request_predictions
import requests


def frame(index=0):
    buffer = io.BytesIO()
    Image.new("RGB", (64, 36), "gray").save(buffer, "JPEG")
    return {"index": index, "timestamp": index / 2,
            "jpeg": base64.b64encode(buffer.getvalue()).decode()}


def prediction(label="car", confidence=.93):
    result = {"class": label, "confidence": confidence, "x": 32, "y": 18,
              "width": 20, "height": 12}
    if label == "line":
        result["points"] = [{"x": 24, "y": 12}, {"x": 40, "y": 12}, {"x": 55, "y": 35}, {"x": 5, "y": 35}]
    return result


def response(count=1):
    return Mock(ok=True, status_code=200, json=lambda: {"outputs": [
        {"predictions": {"image": {"width": 64, "height": 36},
                         "predictions": [prediction("car"), prediction("line"), prediction("lampr")]}}
        for _ in range(count)
    ]})


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.body = {"workspace": "test-space", "workflow": "test-workflow",
                     "api_key": "private-test-key", "frames": [frame()]}

    def test_static_dashboard_and_module_are_served(self):
        for url in ("/", "/assets/dashboard.css", "/assets/dashboard.mjs", "/assets/perception.mjs"):
            self.assertEqual(self.client.get(url).status_code, 200, url)
        self.assertIn("DRIVE", self.client.get("/").text)
        self.assertEqual(self.client.get("/assets/../app.py").status_code, 404)

    def test_config_never_returns_key(self):
        with patch.dict(os.environ, {"ROBOFLOW_API_KEY": "secret-value", "ROBOFLOW_WORKSPACE": "sample"}):
            output = self.client.get("/api/config")
        self.assertTrue(output.json()["has_key"])
        self.assertNotIn("secret-value", output.text)

    @patch("workflow.requests.post")
    def test_batch_contract_header_mapping_and_polygons(self, post):
        post.return_value = response(2)
        self.body["frames"] = [frame(0), frame(1)]
        output = self.client.post("/api/infer", json=self.body)
        self.assertEqual(output.status_code, 200, output.text)
        self.assertEqual(len(output.json()["results"]), 2)
        self.assertEqual(output.json()["results"][1]["timestamp"], .5)
        self.assertEqual(output.json()["results"][0]["predictions"][0]["box"], [22, 12, 42, 24])
        self.assertEqual(len(output.json()["results"][0]["predictions"][1]["points"]), 4)
        post.assert_called_once()
        args, kwargs = post.call_args
        self.assertEqual(args[0], "https://serverless.roboflow.com/test-space/workflows/test-workflow")
        self.assertEqual(kwargs["headers"], {"Authorization": "Bearer private-test-key"})
        self.assertEqual(len(kwargs["json"]["inputs"]["image"]), 2)
        self.assertNotIn("api_key", kwargs["json"])

    @patch("workflow.requests.post", return_value=response())
    def test_environment_key_and_custom_output(self, post):
        self.body["api_key"] = ""
        self.body["output_name"] = "road_result"
        post.return_value = Mock(ok=True, json=lambda: {"outputs": [{"road_result": {"predictions": []}}]})
        with patch.dict(os.environ, {"ROBOFLOW_API_KEY": "from-environment"}):
            output = self.client.post("/api/infer", json=self.body)
        self.assertEqual(output.status_code, 200)
        self.assertEqual(output.json()["results"][0]["predictions"], [])
        self.assertEqual(post.call_args.kwargs["headers"]["Authorization"], "Bearer from-environment")

    @patch("workflow.requests.post")
    def test_api_error_is_safe_and_not_retried(self, post):
        post.return_value = Mock(ok=False, status_code=401, text="secret-token")
        output = self.client.post("/api/infer", json=self.body)
        self.assertEqual(output.status_code, 502)
        self.assertIn("401", output.text)
        self.assertNotIn("secret-token", output.text)
        post.assert_called_once()

    @patch("workflow.requests.post", side_effect=requests.Timeout("private-test-key"))
    def test_timeout_never_echoes_key(self, post):
        output = self.client.post("/api/infer", json=self.body)
        self.assertEqual(output.status_code, 502)
        self.assertNotIn("private-test-key", output.text)

    @patch("workflow.requests.post", return_value=response(2))
    def test_wrong_output_count_fails(self, post):
        output = self.client.post("/api/infer", json=self.body)
        self.assertEqual(output.status_code, 502)
        self.assertIn("outputs", output.json()["detail"])

    @patch("workflow.requests.post")
    def test_visualization_output_rejected(self, post):
        post.return_value = Mock(ok=True, json=lambda: {"outputs": [{"predictions": "base64-image"}]})
        self.assertEqual(self.client.post("/api/infer", json=self.body).status_code, 502)

    @patch("workflow.requests.post")
    def test_invalid_image_does_not_call_api(self, post):
        self.body["frames"][0]["jpeg"] = "this-is-not-jpeg"
        self.assertEqual(self.client.post("/api/infer", json=self.body).status_code, 502)
        post.assert_not_called()

    @patch("workflow.requests.post")
    def test_validation_redacts_body_and_limits_batch(self, post):
        self.body["frames"] = [frame(i) for i in range(17)]
        output = self.client.post("/api/infer", json=self.body)
        self.assertEqual(output.status_code, 422)
        self.assertNotIn("private-test-key", output.text)
        post.assert_not_called()

    @patch("workflow.requests.post")
    def test_duplicate_slots_invalid_timestamp_and_cross_origin(self, post):
        self.body["frames"] = [frame(), frame()]
        self.assertEqual(self.client.post("/api/infer", json=self.body).status_code, 422)
        self.body["frames"] = [frame()]
        self.body["frames"][0]["timestamp"] = -1
        self.assertEqual(self.client.post("/api/infer", json=self.body).status_code, 422)
        self.assertEqual(self.client.post("/api/infer", json=self.body, headers={"Origin": "https://unrelated.example"}).status_code, 403)
        post.assert_not_called()

    def test_line_requires_polygon_and_unknown_class_is_dropped(self):
        invalid = prediction("line")
        invalid.pop("points")
        result, notices = normalize_response({"image": {"width": 64, "height": 36},
            "predictions": [invalid, prediction("other"), prediction("lampy")]}, (64, 36))
        self.assertEqual([p["class"] for p in result["predictions"]], ["lampy"])
        self.assertEqual(len(notices), 2)

    def test_coordinates_scale_to_input_size(self):
        result, _ = normalize_response({"image": {"width": 64, "height": 36},
                                      "predictions": [prediction("line")]}, (128, 72))
        self.assertEqual(result["predictions"][0]["points"][0], [48, 24])
        self.assertEqual(result["predictions"][0]["box"], [44, 24, 84, 48])

    @patch("workflow.requests.post")
    def test_invalid_workflow_cannot_change_endpoint(self, post):
        self.body["workflow"] = "../another"
        self.assertEqual(self.client.post("/api/infer", json=self.body).status_code, 422)
        post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
