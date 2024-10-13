import cv2
import face_recognition
import os
def load_images_from_folder(folder):
    images = []
    encodings = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = face_recognition.load_image_file(path)
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                encoding = face_encodings[0]
                images.append(image)
                encodings.append(encoding)
    return images, encodings
def is_authorized(face_encoding, known_encodings):
    matches = face_recognition.compare_faces(known_encodings, face_encoding)
    return any(matches)
video_capture = cv2.VideoCapture(0)

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Replace with your desired width
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Replace with your desired height

video_capture.set(cv2.CAP_PROP_FPS, 30)
dossier_chemin = r'images\autorisé\personne1'
images, encodages = load_images_from_folder(dossier_chemin)
while True:
    ret, frame = video_capture.read()
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (haut, droite, bas, gauche), encodage_visage in zip(face_locations, face_encodings):
        if is_authorized(encodage_visage, encodages):
            couleur = (0, 255, 0)  # Vert pour les personnes autorisées
            etiquette = "Autorisé"
        else:
            couleur = (0, 0, 255)  # Rouge pour les personnes non autorisées
            etiquette = "Non autorisé"

        # Dessiner un rectangle autour du visage détecté
        cv2.rectangle(frame, (gauche, haut), (droite, bas), couleur, 2)
        cv2.putText(frame, etiquette, (gauche, haut - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, couleur, 2)

    # Afficher la vidéo
    cv2.imshow('Video', frame)

    # Quitter la boucle si 'q' est pressé
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
video_capture.release()
cv2.destroyAllWindows()
