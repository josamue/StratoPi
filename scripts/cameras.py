import cv2
import time
from multiprocessing import Process
import os
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# videoLeft = cv2.VideoWriter('VidLeft.avi', fourcc, 24.0, (1920,  1080))

def createVideo(name):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(f'{name}.avi', fourcc, 10.0, (1280,  720))
    return video

def createCamera(port):
    cam = cv2.VideoCapture(port)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    return cam


def getImage(camera, video=None):
    ret, frame = camera.read()
    if ret:
        if video != None:
            video.write(frame)
        return frame
    return None

# def overlayImage(image, data, video):
#     acceleration, geigerCounts, position, ozone, pressureData, co2Data = data
#     accel_x, accel_y, accel_z = acceleration['x'], acceleration['y'], acceleration['z']
#     text = f"X: {accel_x:.2f} Y: {accel_y:.2f} Z: {accel_z:.2f}"
#     cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 2)
#     video.write(image)
#     return image

def overlayImage(image, data, video):
    acceleration, geigerCounts, position, ozone, pressureData, co2Data = data
    accel_x, accel_y, accel_z = acceleration['x'], acceleration['y'], acceleration['z']
    lat, lon, alt = position[0], position[1], position[2] / 1000
    press, temp = pressureData
    
    # overlay = image.copy()
    height, width, _ = image.shape
    
    # Create a semi-transparent rectangle at the bottom
    overlay_color = (0, 0, 0)  # Black background
    alpha = 0.7
    # cv2.rectangle(overlay, (10, height - 130), (width - 10, height - 10), overlay_color, -1)
    
    # Merge overlay with original image
    # cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    
    # Define text parameters
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    color = (255, 255, 255)  # White text
    thickness = 2
    
    # Organize text into two columns
    text_lines = [
        [f"Temperature: {temp:.3f} C", f"Pressure: {press:.3f} hPa"],
        [f"Acceleration: X: {accel_x:.2f} Y: {accel_y:.2f} Z: {accel_z:.2f}", f"Position: Lat: {lat:.5f}; Lon: {lon:.5f}; Alt: {alt:.1f}m"],
        [f"CO2: {co2Data}ppm", f"Ozone: {ozone}ppb"],
        [f"Geiger Counter: {geigerCounts}CPM", ""]
    ]
    
    y_offset = height - 100
    col1_x = 20
    col2_x = width // 2 + 20
    line_spacing = 25
    
    for i, (text1, text2) in enumerate(text_lines):
        cv2.putText(image, text1, (col1_x, y_offset + i * line_spacing), font, font_scale, color, thickness)
        if text2:
            cv2.putText(image, text2, (col2_x, y_offset + i * line_spacing), font, font_scale, color, thickness)
    
    # Write to video
    origin = (400, 300)
    endX = (int(origin[0] - accel_x * 10), origin[1])
    endY = (origin[0], int(origin[1] + accel_z*10))
    cv2.arrowedLine(image, origin, endX, (0, 0, 255), 5, tipLength=0.2)
    cv2.arrowedLine(image, origin, endY, (0, 0, 255), 5, tipLength=0.2)

    # z_length = int(abs(accel_y * 10))
    # cv2.circle(frame, (center_x, center_y), z_length, (255, 0, 0), 2)

    # video.write(image)
    
    return image



def image_saver(camPort):
    camLeft = createCamera(camPort)
    counter = int(camPort / 2)

    # Stelle sicher, dass der Ordner existiert
    os.makedirs("images", exist_ok=True)

    while True:
        try:
            image = getImage(camLeft)
            filename = f"images/image_{counter:06d}.jpg"
            cv2.imwrite(filename, image)
            counter += 2
        except Exception as e:
            print(f"Error saving image: {e}")
        time.sleep(0.5)

def recordVideosPicam():
    picam2 = Picamera2()

    # Erstelle die Video-Konfiguration
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)

    # Wähle den H.264-Encoder (oder wähle einen anderen Encoder, je nach Bedarf)
    encoder = H264Encoder(bitrate=10000000)

    picam2.start()  # Kamera starten

    while True:
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"./recordedVideos/video_{timestamp}.h264"

            # Video mit Encoder starten
            picam2.start_recording(output = filename, encoder=encoder)
            print(f"Recording started: {filename}")
            time.sleep(60)  # 10 Sekunden aufnehmen
            picam2.stop_recording()
            print(f"Recording completed: {filename}")

        except Exception as e:
            print(f"Error Saving Video: {e}")