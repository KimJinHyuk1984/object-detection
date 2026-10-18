"""Regression tests: real API calls are replaced; no key or network is needed."""
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "files/lesson-03"
sys.path.insert(0, str(APP))
from PIL import Image
import core
from demo import make_demo


class ImageTests(unittest.TestCase):
    def test_orientation_and_alpha(self):
        image = Image.new("RGB", (10, 20), "red")
        exif = Image.Exif()
        exif[274] = 6
        buffer = io.BytesIO()
        image.save(buffer, "JPEG", exif=exif)
        self.assertEqual(core.prepare_image(buffer.getvalue()).size, (20, 10))
        transparent = Image.new("RGBA", (2, 2), (0, 0, 0, 0))
        self.assertEqual(core.prepare_image(core.png_bytes(transparent)).getpixel((0,0)), (255,255,255))

    def test_bad_and_oversized_inputs(self):
        for data in [b"not an image", b"", b"x" * (core.MAX_FILE_BYTES+1)]:
            with self.assertRaises(ValueError):
                core.prepare_image(data)
        huge = Image.new("RGB", (1800, 1000))
        prepared = core.prepare_image(core.png_bytes(huge))
        self.assertEqual(prepared.size, (1600, 889))

    def test_response_scale_and_masks(self):
        image, payload = make_demo()
        result, warnings = core.normalize_response(payload, (480,270))
        self.assertFalse(warnings)
        self.assertEqual(len(result["predictions"]),9)
        road = next(p for p in result["predictions"] if p["class"]=="line")
        self.assertEqual(road["points"][0],[215,105])
        vehicle = next(p for p in result["predictions"] if p["class"]=="car")
        self.assertEqual(vehicle["box"],[84,161.5,139,217])
        drawn = core.render_predictions(image, core.normalize_response(payload,image.size)[0]["predictions"])
        self.assertNotEqual(drawn.getpixel((480,500)),image.getpixel((480,500)))
        self.assertEqual(drawn.getpixel((900,500)),image.getpixel((900,500)))

    def test_empty_missing_and_malformed_results(self):
        result, messages = core.normalize_response({"image":{"width":20,"height":20},"predictions":[]},(20,20))
        self.assertEqual(result["predictions"],[])
        self.assertFalse(messages)
        for data in [{}, {"image":{"width":0,"height":20},"predictions":[]}, {"predictions":[]}]:
            with self.assertRaises(ValueError):
                core.normalize_response(data,(20,20))
        image,payload=make_demo()
        payload["predictions"][-1].pop("points")
        payload["predictions"][0]["confidence"]=float("nan")
        result,messages=core.normalize_response(payload,image.size)
        self.assertEqual(len(result["predictions"]),7)
        self.assertTrue(messages)
        self.assertNotIn("line",[p["class"] for p in result["predictions"]])

    def test_confidence_and_identity(self):
        image,payload=make_demo()
        result,_=core.normalize_response(payload,image.size)
        self.assertEqual(len(core.visible_predictions(result,.4,list(core.CLASSES))),8)
        self.assertEqual(len(core.visible_predictions(result,.7,list(core.CLASSES))),6)
        self.assertEqual(len(core.visible_predictions(result,.9,list(core.CLASSES))),2)
        self.assertEqual(core.visible_predictions(result,.05,[]),[])
        a=core.context_id(image,"real","road/1","key")
        self.assertNotEqual(a,core.context_id(image,"real","road/2","key"))
        self.assertNotEqual(a,core.context_id(image,"real","road/1","other"))
        self.assertNotEqual(a,core.context_id(Image.new("RGB",image.size),"real","road/1","key"))

    def test_sdk_contract_and_redacted_failure(self):
        image,payload=make_demo()
        with patch("inference_sdk.InferenceHTTPClient") as client:
            client.return_value.infer.return_value=payload
            self.assertEqual(core.infer_image(image,"road/1","test-key"),payload)
            configuration=client.return_value.configure.call_args.args[0]
            self.assertEqual(configuration.confidence_threshold,.05)
            self.assertEqual(configuration.response_mask_format,"polygon")
            client.return_value.infer.assert_called_once_with(image,model_id="road/1")
            client.return_value.infer.side_effect=RuntimeError("url?api_key=DO-NOT-LEAK")
            with self.assertRaises(core.InferenceFailure) as raised:
                core.infer_image(image,"road/1","test-key")
            self.assertNotIn("DO-NOT-LEAK",str(raised.exception))


class AppTests(unittest.TestCase):
    def setUp(self):
        from streamlit.testing.v1 import AppTest
        self.app=AppTest.from_file(str(APP/"app.py"),default_timeout=20)

    def test_demo_controls_and_mode_reset(self):
        with patch("core.infer_image") as inference:
            app=self.app.run()
            app.radio(key="mode").set_value("예제 결과로 연습").run()
            self.assertFalse(app.exception)
            app.button(key="analyze").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.session_state.prediction_result["predictions"]),9)
            app.slider(key="threshold").set_value(.9).run()
            self.assertFalse(app.exception)
            app.multiselect(key="classes").set_value([]).run()
            self.assertFalse(app.exception)
            self.assertTrue(any("현재 조건" in x.value for x in app.info))
            inference.assert_not_called()
            app.radio(key="mode").set_value("내 모델로 분석").run()
            app.radio(key="input_type").set_value("이미지 한 장").run()
            self.assertTrue(app.button(key="analyze").disabled)
            self.assertNotIn("prediction_result",app.session_state)

    def test_real_request_once_rerender_and_invalidation(self):
        image,payload=make_demo()
        self.app.secrets["ROBOFLOW_API_KEY"]="test-key"
        self.app.secrets["ROBOFLOW_MODEL_ID"]="road/1"
        with patch("streamlit.file_uploader",return_value=io.BytesIO(core.png_bytes(image))), \
             patch("core.infer_image",return_value=payload) as inference:
            app=self.app.run()
            app.radio(key="mode").set_value("내 모델로 분석").run()
            app.radio(key="input_type").set_value("이미지 한 장").run()
            self.assertFalse(app.button(key="analyze").disabled)
            app.button(key="analyze").click().run()
            self.assertFalse(app.exception)
            inference.assert_called_once()
            app.slider(key="threshold").set_value(.9).run()
            app.slider(key="opacity").set_value(.5).run()
            self.assertFalse(app.exception)
            inference.assert_called_once()
            app.text_input(key="model_id").set_value("road/2").run()
            self.assertNotIn("prediction_result",app.session_state)
            app.button(key="analyze").click().run()
            self.assertEqual(inference.call_count,2)
            inference.side_effect=core.InferenceFailure("요청 실패")
            app.button(key="analyze").click().run()
            self.assertNotIn("prediction_result",app.session_state)
            self.assertTrue(app.error)
            self.assertFalse(app.exception)


if __name__=="__main__":
    unittest.main(verbosity=2)
