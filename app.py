import streamlit as st
import cv2
from face_recognition import load_image_file
from face_recognition import face_encodings
from face_recognition import compare_faces
from face_recognition import face_locations

def search(target_path, search_path):
    target_image = load_image_file(target_path)
    search_image = load_image_file(search_path)

    target_encoding = face_encodings(target_image)[0]
    all_faces_encoding = face_encodings(search_image)

    matches = compare_faces(all_faces_encoding, target_encoding)

    all_face_locations = face_locations(search_image)
    search_image_cv2 = cv2.imread(search_path)
    all_seach_image_cv2 = cv2.imread(search_path)

    true_index = None
    for i in range(len(all_face_locations)):
        if matches[i] == True:
            true_index = i

    if true_index != None:
        (top, right, bottom, left) = all_face_locations[true_index]
        cv2.rectangle(search_image_cv2, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(search_image_cv2, "Target", (left+6, bottom-6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    i = 0
    for (top, right, bottom, left) in all_face_locations:
        cv2.rectangle(all_search_image_cv2, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(all_search_image_cv2, "Target " + str(i), (left+6, bottom-6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        i += 1

    return true_index, search_image_cv2, all_search_image_cv2

st.sidebar.title("OSINT Facial Recognition")
target = st.sidebar.file_uploader("Choose target image")
search = st.sidebar.file_uploader("Choose search image")

if target is not None and search is not None:
    if st.sidebar.button("Find"):
        true_index, search_image_cv2, all_search_image_cv2 = search(target, search)
        st.header("All targets")
        st.image(all_search_image_cv2)

        st.header("Searched")
        if true_index != None:
            st.success("Target found in image.")
            st.image(search_image_cv2)
        else:
            st.warning("Target not found in image.")
