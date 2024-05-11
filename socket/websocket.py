import asyncio
import websockets
import cv2
import rpyc

min_blue = 97
min_green = 88
min_red = 76
max_blue = 219
max_green = 255
max_red = 200
min_area_threshold = 800

async def communicate(websocket, path):
    print("Connection established from ESP32")
    conn = rpyc.connect("localhost", 18861)

    try:
        cap = cv2.VideoCapture(0)  # Open the camera
        
        while True:
            ret, frame = cap.read()  # Read a frame from the camera
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_frame, (min_blue, min_green, min_red), (max_blue, max_green, max_red))
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)

            position = list()
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area_threshold:
                    x_min, y_min, box_width, box_height = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x_min - 15, y_min - 15),
                                (x_min + box_width + 15, y_min + box_height + 15),
                                (0, 255, 0), 4)
                    
                    position.append([(x_min+box_width)/2, (y_min+box_height)/2])
            try:
                await websocket.send(f"{position[0][0]}")
            except: 
                await websocket.send(f"0")
            message = await websocket.recv()
            print(f"Message received from ESP32: {message}")

            try:
                # Get the answer from the server
                conn.root.setter(len(position), message)
                print(conn.root.getter())
                
            except Exception as error:
                # print(error)
                pass

            cv2.imshow('frame', frame)
            cv2.imshow('Mask Image', mask)
            key = cv2.waitKey(1)

            if key == ord('q'):
                break
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed unexpectedly from ESP32")


start_server_esp = websockets.serve(communicate, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server_esp)
asyncio.get_event_loop().run_forever()
