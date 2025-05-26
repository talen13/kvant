import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os
import ultralytics#библиотека “ultralytics” для обнаружения объектов, решает задачи отслеживания объектов, сегментации экземпляров
from tkinter import filedialog#с помощью метода filedialog можно определить директорию файлов
from tkinter import *# с помощью tkinter я создаю интерфейс
from tkinter import ttk#
from os import startfile# импортирую метод открывания файла
import supervision as sv# инструмент для компьютерного зрения
from ultralytics import YOLO# загружаю YOLO
import cv2
import numpy as np#
from tkinter.messagebox import showinfo,showerror
import argparse


os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
temp1 = "yolov8n.pt"
def opencurfile():# определяем функцию для вызова интерфейса
  root = Tk()# создаем поле
  root.title("")#
  root.geometry("800x600")# определяем размеры поля
  open_button = ttk.Button(text="Обработка в режиме реального времени", command=lambda: settings_window())# создаем кнопку для открытия файла
  open_button1 = ttk.Button(text = "Постобработка видео", command=lambda: click())# создаем кнопку для аннотирования всего видеo
  open_button1.pack(anchor=CENTER)# задаем ее местоположение
  open_button.pack(anchor=S,side = BOTTOM)# задаем ее местоположение
  root.mainloop()# для отображения окна и взаимодействия пользователя с ним вызываем метод mainloop()
def proverka(window1,entry1, entry2, entry3, entry4,entry5,path):
    #showinfo(title="аннотация", message='Нажмите')
    annoturovanie(window1,entry1, entry2, entry3, entry4,entry5,path)
def annoturovanie(window1,entry1, entry2, entry3, entry4,entry5,path):
    ultralytics.checks()  # проверяем правильную установку “ultralytics”
    SOURCE_VIDEO_PATH = path  # директория + название
    entry5val = entry5.get()
    entry5val = entry5val + ".mp4"
    model = YOLO(f'{temp1}')  # выбор модели yolo
    CLASS_NAMES_DICT = model.model.names  # записываем имена которые в данной модели присутствуют
    SELECTED_CLASS_NAMES = ['person']  # выбранные имена
    SELECTED_CLASS_IDS = [  # определяем их айди
        {value: key for key, value in CLASS_NAMES_DICT.items()}[class_name]
        for class_name
        in SELECTED_CLASS_NAMES
    ]
    TARGET_VIDEO_PATH = entry5val  # конечное название файла,которое мы получим после обработки
    byte_tracker = sv.ByteTrack(  # используем встроенную функцию для отслеживания людей
        track_activation_threshold=0.25,
        lost_track_buffer=30,
        minimum_matching_threshold=0.8,
        frame_rate=30,
        minimum_consecutive_frames=3)
    byte_tracker.reset()  # перезапускаем байтетрек
    video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)  # записываем значение в переменную,которое является информацией о видео(количество кадров,размеры видео и т.д.)
    width = video_info.width
    height = video_info.height
    if entry1.get().isdigit() and entry2.get().isdigit() and entry3.get().isdigit() and entry4.get().isdigit() :
        entry1val = float(entry1.get())
        entry2val = float(entry2.get())
        entry3val = float(entry3.get())
        entry4val = float(entry4.get())
    else:
        showerror(title='Ошибка',message="Указаны неверные значения для линии,значения выбраны по умолчанию")
        entry1val = width * 0.5
        entry2val = 0
        entry3val = width * 0.5
        entry4val = height
    LINE_START = sv.Point(entry1val, entry2val)  # задаем начальные координаты линии
    LINE_END = sv.Point(entry3val, entry4val)  # задаем конечные координаты линии
    window1.destroy()
    line_zone = sv.LineZone(start=LINE_END, end=LINE_START)  # используем метод для создания определяющей линии
    box_annotator = sv.BoxAnnotator(thickness=4)  # рисование рамок
    label_annotator = sv.LabelAnnotator(text_thickness=2, text_scale=1.5,
                                        text_color=sv.Color.BLACK)  # используется для создания текстовых меток
    line_zone_annotator = sv.LineZoneAnnotator(thickness=4, text_thickness=4,
                                               text_scale=2)  # создает визуальную линию для восприятия человеком
    def callback(frame: np.ndarray, index: int) -> np.ndarray:
        results = model(frame, verbose=False)[0]  # записываем результат
        detections = sv.Detections.from_ultralytics(results)  # определяем и находим людей
        detections = detections[np.isin(detections.class_id, SELECTED_CLASS_IDS)]  # записываем айди
        detections = byte_tracker.update_with_detections(detections)  # обновляем слежение
        labels = [
            f"# {model.model.names[class_id]} {confidence:0.2f}" # записываем информацию для отображении на рамках
            for confidence, class_id,   #
            in zip(detections.confidence, detections.class_id, )
        ]
        annotated_frame = frame.copy()  # копируем отформатированный кадр
        annotated_frame = box_annotator.annotate(  # создаем рамки для готового кара
            scene=annotated_frame, detections=detections)
        annotated_frame = label_annotator.annotate(
            scene=annotated_frame, detections=detections, labels=labels)
        line_zone.trigger(detections)  # проход через линию
        return line_zone_annotator.annotate(annotated_frame, line_counter=line_zone)  # возвращаем результат

    sv.process_video(  # #аннотируем все видео
        source_path=SOURCE_VIDEO_PATH,
        target_path=TARGET_VIDEO_PATH,
        callback=callback
    )
    showinfo(title="аннотация", message='Видео аннотировалось')
def opredvideo():
    window2 = Tk()
    window2.title("Новое окно")
    window2.geometry("800x600")
    Label1 = ttk.Label(window2,text= 'Выберите видео для аннотации')
    Label1.pack(anchor= CENTER)
    Button3 = ttk.Button(window2,text = "выбрать",command= lambda:filepath(window2,))
    Button3.pack(anchor=CENTER)
def filepath(window2):
    filepath = filedialog.askopenfilename()
    path = filepath
    print(path)
    window2.destroy()
    click(path,)
def n():
    global temp1
    temp1 = 'yolov8n.pt'
    return (temp1)
def m():
    global temp1
    temp1 = 'yolov8m.pt'
    return (temp1)
def x():
    global temp1
    temp1 = 'yolov8x.pt'
    return (temp1)
def click():
    filepath = filedialog.askopenfilename()
    path = filepath
    window1 = Tk()
    window1.title("Новое окно")
    window1.geometry("800x600")
    open_button12 = ttk.Button(window1,text="запуск", command=lambda: proverka(window1,entry1, entry2, entry3, entry4,entry5,path,))
    open_button12.pack(anchor=CENTER)  # задаем ее местоположение
    inflabel = ttk.Label(window1,text = 'В первых двух полях необходимо указать начальные координаты триггерной линии,а в двух последних конечные координаты')
    inflabel.pack(anchor= CENTER)
    entry1 = ttk.Entry(window1)
    entry1.pack(anchor=CENTER)
    entry2 = ttk.Entry(window1)
    entry2.pack(anchor=CENTER)
    entry3 = ttk.Entry(window1)
    entry3.pack(anchor=CENTER)
    entry4 = ttk.Entry(window1)
    entry4.pack(anchor=CENTER)
    SOURCE_VIDEO_PATH = path  # директория + название
    video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)
    resulutionlabel = ttk.Label(window1,text = f"Расширение видео : {video_info.resolution_wh} ")
    resulutionlabel.pack(anchor=CENTER)
    Label12 = ttk.Label(window1, text="Выберите модель")
    Label12.pack(anchor=CENTER)
    Button4 = ttk.Button(window1, text=f'yolov8n',command=set_model_n)
    Button4.pack(anchor=CENTER)
    Button5 = ttk.Button(window1, text=f'yolov8m',command=set_model_m)
    Button5.pack(anchor=CENTER)
    Button6 = ttk.Button(window1, text=f'yolov8x',command=set_model_x)
    Button6.pack(anchor=CENTER)
    Label13 = ttk.Label(window1, text="Выберите конечный путь файла")
    Label13.pack(anchor=CENTER)
    entry5 = ttk.Entry(window1)
    entry5.pack(anchor=CENTER)
def set_model_n():
    global temp1
    temp1 = "yolov8n.pt"
def set_model_m():
    global temp1
    temp1 = "yolov8m.pt"
def set_model_x():
    global temp1
    temp1 = "yolov8x.pt"
def parse_arguments():
    parser = argparse.ArgumentParser(description="YOLOv8 Live Multi-Camera")
    parser.add_argument("--webcam-resolution", default=[640, 480], nargs=2, type=int)
    return parser.parse_args()

def check_available_cameras(max_test=5):
    available = []
    print("Проверка доступных камер...")
    for i in range(max_test):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Камера {i} доступна")
            available.append(i)
            cap.release()
        else:
            print(f"Камера {i} НЕДОСТУПНА")
    return available

def run_camera(index, line_start, line_end, model_name):
    print(f"[INFO] Запуск камеры {index}...")

    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"[Ошибка] Не удалось открыть камеру {index}")
        return

    args = parse_arguments()
    width, height = args.webcam_resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, 15)

    model = YOLO(model_name)
    box_annotator = sv.BoxAnnotator(thickness=2)
    label_annotator = sv.LabelAnnotator(text_thickness=2, text_scale=1.5,
                                        text_color=sv.Color.BLACK)
    line_zone = sv.LineZone(start=line_start, end=line_end)
    line_annotator = sv.LineZoneAnnotator(thickness=4, text_thickness=4, text_scale=2)

    byte_tracker = sv.ByteTrack(track_activation_threshold=0.25,
                                lost_track_buffer=30,
                                minimum_matching_threshold=0.8,
                                frame_rate=15)

    window_name = f"Camera {index}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"[Ошибка] Не удалось получить кадр с камеры {index}")
            break

        result = model(frame, classes=[0], verbose=False)[0]
        detections = sv.Detections.from_ultralytics(result)
        detections = detections[np.isin(detections.class_id, [0])]  # Только люди
        tracked_detections = byte_tracker.update_with_detections(detections)

        annotated_frame = box_annotator.annotate(scene=frame.copy(), detections=tracked_detections)
        labels = [f"{conf:.2f}" for conf in tracked_detections.confidence]
        annotated_frame = label_annotator.annotate(annotated_frame, detections=tracked_detections, labels=labels)

        line_zone.trigger(tracked_detections)
        line_annotator.annotate(annotated_frame, line_counter=line_zone)

        cv2.imshow(window_name, annotated_frame)

        if cv2.waitKey(1) == 27:  # Esc
            break

    cap.release()
    cv2.destroyWindow(window_name)
    print(f"[INFO] Камера {index} остановлена")

def start_tracking(entry_fields, window_settings, available_cams):
    args = parse_arguments()
    width, height = args.webcam_resolution
    if entry_fields[0].get().isdigit() and entry_fields[1].get().isdigit() and entry_fields[2].get().isdigit() and entry_fields[3].get().isdigit() :
        entry1val = float(entry_fields[0].get())
        entry2val = float(entry_fields[0].get())
        entry3val = float(entry_fields[0].get())
        entry4val = float(entry_fields[0].get())
    else:
        showerror(title='Ошибка',message="Указаны неверные значения для линии,значения выбраны по умолчанию")
        entry1val = width * 0.5
        entry2val = 0
        entry3val = width * 0.5
        entry4val = height
    try:
        num_cams = int(entry_fields[4].get())

        if num_cams > len(available_cams):
            messagebox.showerror("Ошибка", f"Запрошено {num_cams} камер, но доступно только {len(available_cams)}")


    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные значения.")


    window_settings.destroy()

    line_start = sv.Point(entry1val, entry2val)
    line_end = sv.Point(entry3val, entry4val)

    # Запуск камер в потоках
    threads = []
    for i in range(num_cams):
        cam_index = available_cams[i]
        thread = threading.Thread(target=run_camera, args=(cam_index, line_start, line_end, temp1))
        thread.start()
        threads.append(thread)
        time.sleep(0.5)  # пауза между запусками камер

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    print("[INFO] Все камеры остановлены")
    cv2.destroyAllWindows()


def settings_window():
    available_cams = check_available_cameras()
    if not available_cams:
        messagebox.showerror("Ошибка", "Нет доступных камер!")
        return

    args = parse_arguments()
    width, height = args.webcam_resolution

    window = tk.Tk()
    window.title("Настройки трекинга")
    window.geometry("800x600")

    tk.Label(window, text="Координаты триггерной линии (X1,Y1,X2,Y2):").pack(pady=5)
    entries = []
    for _ in range(4):
        entry = ttk.Entry(window)
        entry.pack()
        entries.append(entry)
    resulutionlabel = ttk.Label(window, text=f"Расширение видео : {width, height} ")
    resulutionlabel.pack(anchor=CENTER)
    tk.Label(window, text="Количество камер:").pack()
    entry_cam = ttk.Entry(window)
    entry_cam.insert(0, "1")
    entry_cam.pack()
    entries.append(entry_cam)

    tk.Button(window, text="Запуск", command=lambda: start_tracking(entries, window, available_cams)).pack()

    tk.Label(window, text="Выберите модель:").pack()
    ttk.Button(window, text="YOLOv8n", command=set_model_n).pack()
    ttk.Button(window, text="YOLOv8m", command=set_model_m).pack()
    ttk.Button(window, text="YOLOv8x", command=set_model_x).pack()

    window.mainloop()

opencurfile()