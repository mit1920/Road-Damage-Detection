import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2

def road_damage_detection_app():
    # Load the YOLO model
    @st.cache_resource
    def load_model():
        return YOLO("best.pt")

    model = load_model()

    # App title and description
    st.title("Road Damage Detection")
    st.write("Upload an image, and the model will detect road damage.")

    # Image uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load and display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Run detection
        if st.button("Detect Road Damage"):
            with st.spinner("Processing..."):
                # Convert PIL image to NumPy array (YOLO expects NumPy arrays)
                image_np = np.array(image)
                
                # Perform prediction using the YOLO model
                results = model.predict(source=image_np, save=False, conf=0.25)
                
                # Extract the annotated image (OpenCV format) and convert it to RGB
                annotated_img = results[0].plot()
                annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

            # Display the annotated image
            st.image(annotated_img, caption="Detected Road Damage", use_column_width=True)
            st.success("Detection Complete!")

    # Footer
    st.markdown(
        """
        ---
        Developed using **YOLOv8** and **Streamlit**.
        """
    )

# Run the app function
if __name__ == "__main__":
    road_damage_detection_app()
