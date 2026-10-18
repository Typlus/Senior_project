import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import time
import math
import functions 
import reports
import inference
import os
import tempfile
from pathlib import Path
from google.api_core.exceptions import GoogleAPICallError
from audiodetect import make_streaming_detector_v4_inference_fn


from audiostreamer import (
    AudioDetectionEngine,
    GCSAudioStreamer,
    StreamlitAudioPlayerUI,
)

def main():
    st.set_page_config(page_title="ImmersaNET", layout="wide")
    st.title("ImmersaNET Insider Demo")
    st.caption("NOAA Bioacoustic Spectrogram Monitor")

    # Pass `inference_fn=None` (or omit it) to play audio-only without detections
    player = StreamlitAudioPlayerUI(
        bucket_name="noaa-passive-bioacoustic",
        blob_name="mbarc_bering/audio/mbarc_lmr_bering03-m2/audio/BERING03_M2___050425_130000.x.flac",
        inference_fn=make_streaming_detector_v4_inference_fn(),
    )
    
    player.render()

    st.subheader("Run inference on an audio file")
    uploaded_audio = st.file_uploader(
        "Upload an audio file",
        type=["wav", "mp3", "flac", "ogg", "m4a"],
        key="inference_audio_upload",
    )

    project_dir = Path(__file__).resolve().parent
    model_paths = sorted((project_dir / "models").glob("*.pth"))
    labels_path = project_dir / "labels.json"

    if model_paths:
        selected_model = st.selectbox(
            "Select inference model",
            model_paths,
            format_func=lambda path: path.name,
        )
    else:
        selected_model = None
        st.warning(f"No .pth model found in {project_dir / 'models'}.")

    if not labels_path.is_file():
        st.warning(f"labels.json not found at {labels_path}.")

    if st.button(
        "Run Model Inference",
        disabled=(uploaded_audio is None or selected_model is None or not labels_path.is_file()),
    ):
        temp_path = None
        try:
            suffix = os.path.splitext(uploaded_audio.name)[1] or ".audio"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as audio_file:
                audio_file.write(uploaded_audio.getvalue())
                temp_path = audio_file.name

            with st.spinner("Running model inference..."):
                inference_started = time.perf_counter()
                result = inference.run_inference(
                    audio_path=temp_path,
                    model_path=str(selected_model),
                    labels_path=str(labels_path),
                )
                inference_latency = time.perf_counter() - inference_started
                st.caption(f"Inference latency: {inference_latency:.3f} seconds")
            st.session_state["inference_results"] = result
            st.session_state["inference_filename"] = uploaded_audio.name
            for key in list(st.session_state.keys()):
                if key.startswith("prediction_select_"):
                    del st.session_state[key]
            st.session_state["predictions_saved"] = False
            st.success("Inference completed!")

         
        
        except Exception as exc:
            st.error(f"Inference failed: {exc}")
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
    if "inference_results" in st.session_state:
            results = st.session_state["inference_results"]
            filename = st.session_state["inference_filename"]

            st.subheader("Select Animal Predictions")

            st.caption(f"Audio file: {filename}")

            if not results:
                st.info("The model returned no predictions.")

            else:
                st.write(
                    "Select the animals you want to add to the results table."
                )

                with st.form("save_predictions_form"):
                    selected_indices = []

                    for i, prediction in enumerate(results):
                        species = prediction["label"]
                        confidence = prediction["probability"] * 100
                        detected = prediction["detected"]

                        col1, col2, col3 = st.columns([3, 2, 2])

                        with col1:
                            selected = st.checkbox(
                                species,
                                key=f"prediction_select_{i}",
                                disabled=st.session_state.get(
                                    "predictions_saved", False
                                ),
                            )

                        with col2:
                            st.write(f"{confidence:.2f}%")

                        with col3:
                            st.write(
                                "Detected" if detected else "Below threshold"
                            )

                        if selected:
                            selected_indices.append(i)

                    save_clicked = st.form_submit_button(
                        "Save Selected Predictions",
                        disabled=st.session_state.get(
                            "predictions_saved", False
                        ),
                    )

                if save_clicked:
                    if not selected_indices:
                        st.warning("Select at least one animal first.")

                    else:
                        for i in selected_indices:
                            prediction = results[i]

                            functions.add_result(
                                filename=filename,
                                species=prediction["label"],
                                confidence=round(
                                    prediction["probability"] * 100
                                ),
                            )

                        st.session_state["predictions_saved"] = True

                        st.success(
                            f"Saved {len(selected_indices)} prediction(s) "
                            f"for {filename}."
                        )

    # grab what species of animal they want to filter from the database
        # this can be done by either A: going through and outputing allt he unique species in the table or B have a running dictionary of them and pull from that
    
    with labels_path.open(encoding="utf-8") as labels_file:
        species_options = json.load(labels_file)
    
    user_selected_s = st.multiselect("Species to filter by:", species_options)
    user_selected_c = st.slider ("Confidence Score Threshold:", min_value=00, max_value=100 , value=0 , step=10, format="%d%%")

    # button to test report generation for demo
    if st.button("Generate Report"):
        pdf_data = reports.generate_report(1)

        if pdf_data:
            st.download_button(
                "Download Report",
                data=pdf_data,
                file_name="report_1.pdf",
                mime="application/pdf"
            )

    # create talbe header
    st.subheader("table")

    # create varible for all results, this varible can change later to when filter is added and allows for differnt changes
    if user_selected_s or user_selected_c > 0:  
        results= functions.results_by_filter(user_selected_s, user_selected_c)
    else:
        results = functions.get_all_results()

        
    tf = pd.DataFrame(
        results,
        columns=["ID","Species","Filename","Confidence"]
    )
    # set up for generate reports function later on. #TODO ADD FUNCTIONALTY TO HAVE IT CREATE A PDF WITH ALL THE EXPECTED QUALITES
    tf["Generate report"] = "Generate Report"

    # limits the page to 15 entries per page
    ROWS_PER_PAGE = 15
    total_pages = max(1, (len(tf) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE) #

    # 2. Render the interactive pagination buttons FIRST (on top)
    current_page = st.pagination(num_pages=total_pages)

    # 3. Slice the DataFrame based on the active button page
    start_idx = (current_page - 1) * ROWS_PER_PAGE
    end_idx = start_idx + ROWS_PER_PAGE
    sliced_tf = tf.iloc[start_idx:end_idx]

    st.dataframe(sliced_tf, width='stretch', hide_index=True, height=565)

    

##if user_selected_s or user_selected_c > 0:  
 #    results= functions.results_by_filter(user_selected_s, user_selected_c)
#else:
 #    results = functions.get_all_results()

if __name__ == "__main__":
    main()
