"""Video decoding/encoding and AppTest; Roboflow is always mocked."""
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/"files/lesson-03"
sys.path.insert(0,str(APP))
import av
from PIL import Image
import video
from core import CLASSES, InferenceFailure
from demo import make_demo


def clip():
    output=io.BytesIO()
    with av.open(output,mode="w",format="mp4") as container:
        stream=container.add_stream("libx264",rate=10)
        stream.width=160
        stream.height=90
        stream.pix_fmt="yuv420p"
        for n in range(30):
            image=Image.new("RGB",(160,90),(n*8,0,0))
            for packet in stream.encode(av.VideoFrame.from_image(image)):
                container.mux(packet)
        for packet in stream.encode():
            container.mux(packet)
    return output.getvalue()


class VideoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=clip()

    def test_timestamp_sampling_and_limits(self):
        info=video.video_info(self.data)
        self.assertAlmostEqual(info["duration"],3)
        batch=video.sample_frames(self.data,1,1,2)
        self.assertEqual(len(batch["frames"]),2)
        self.assertAlmostEqual(batch["frames"][0]["timestamp"],1)
        self.assertAlmostEqual(batch["frames"][1]["timestamp"],1.5)
        self.assertEqual(len(video.sample_frames(self.data,2.5,10,2)["frames"]),1)
        for data in [b"",b"invalid video"]:
            with self.assertRaises(ValueError): video.video_info(data)
        with self.assertRaises(ValueError): video.sample_plan(info,3,1,2)
        with self.assertRaises(ValueError): video.sample_plan({"duration":100},0,20,5)
        with self.assertRaises(ValueError): video.sample_plan(info,float("nan"),1,2)
        with patch.object(video,"MAX_VIDEO_BYTES",10):
            with self.assertRaises(ValueError): video.video_info(self.data)

    def test_model_result_and_h264_export(self):
        batch=video.sample_frames(self.data,0,1,2)
        _,payload=make_demo()
        from unittest.mock import Mock
        inference=Mock(return_value=payload)
        result=video.analyze_frames(batch,inference)
        self.assertEqual(inference.call_count,2)
        self.assertNotIn("result",batch["frames"][0])
        self.assertEqual(len(result["frames"][0]["result"]["predictions"]),9)
        output=video.encode_video(result,.4,list(CLASSES),.3)
        with av.open(io.BytesIO(output)) as container:
            stream=container.streams.video[0]
            self.assertEqual(stream.codec_context.name,"h264")
            self.assertEqual(stream.pix_fmt,"yuv420p")
            decoded=list(container.decode(stream))
            self.assertEqual(len(decoded),2)
            self.assertAlmostEqual(float(container.duration/av.time_base),1)
        record=video.export_record(result,"road/1",.4,list(CLASSES),.3)
        self.assertNotIn("jpeg",record["frames"][0])
        self.assertNotIn("api_key",str(record))
        inference.side_effect=InferenceFailure("secret-url")
        with self.assertRaises(InferenceFailure) as raised:
            video.analyze_frames(batch,inference)
        self.assertNotIn("secret-url",str(raised.exception))

    def test_context_invalidation(self):
        args=[self.data,"real","road/1","key",0,10,2]
        identity=video.video_context(*args)
        for index,value in enumerate([b"different","check","road/2","other-key",1,5,1]):
            changed=args.copy();changed[index]=value
            self.assertNotEqual(identity,video.video_context(*changed))

    def test_video_ui_calls_and_export_reset(self):
        from streamlit.testing.v1 import AppTest
        app=AppTest.from_file(str(APP/"app.py"),default_timeout=20)
        app.secrets["ROBOFLOW_API_KEY"]="test-key"
        app.secrets["ROBOFLOW_MODEL_ID"]="road/1"
        _,payload=make_demo()
        with patch("streamlit.file_uploader",return_value=io.BytesIO(self.data)),              patch("video_ui.infer_image",return_value=payload) as inference:
            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.radio(key="mode").value,"영상 업로드 확인")
            app.button(key="analyze_video").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.session_state.video_batch["frames"]),6)
            inference.assert_not_called()
            self.assertNotIn("result",app.session_state.video_batch["frames"][0])
            app.button(key="make_video").click().run()
            self.assertTrue(app.session_state.video_export)
            app.radio(key="mode").set_value("내 모델로 분석").run()
            self.assertNotIn("video_batch",app.session_state)
            app.button(key="analyze_video").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(inference.call_count,6)
            app.slider(key="threshold").set_value(.9).run()
            app.slider(key="opacity").set_value(.5).run()
            app.select_slider(key="frame_index").set_value(1).run()
            self.assertFalse(app.exception)
            self.assertEqual(inference.call_count,6)
            app.button(key="make_video").click().run()
            self.assertTrue(app.session_state.video_export)
            app.slider(key="threshold").set_value(.4).run()
            self.assertNotIn("video_export",app.session_state)
            self.assertEqual(inference.call_count,6)
            app.number_input(key="video_start").set_value(1.0).run()
            self.assertNotIn("video_batch",app.session_state)
            app.button(key="analyze_video").click().run()
            self.assertEqual(inference.call_count,10)
            inference.side_effect=InferenceFailure("secret-url")
            app.button(key="analyze_video").click().run()
            self.assertNotIn("video_batch",app.session_state)
            self.assertTrue(app.error)
            self.assertFalse(app.exception)
            app.text_input(key="model_id").set_value("road/2").run()
            app.radio(key="mode").set_value("영상 업로드 확인").run()
            app.button(key="analyze_video").click().run()
            self.assertNotIn("result",app.session_state.video_batch["frames"][0])

if __name__=="__main__":
    unittest.main(verbosity=2)
