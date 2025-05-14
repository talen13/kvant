import os#библиотека “os” позволяет работать с файлами,которые находятся на компьютере
import ultralytics#библиотека “ultralytics” для обнаружения объектов, решает задачи отслеживания объектов, сегментации экземпляров
from tkinter import filedialog#с помощью метода filedialog можно определить директорию файлов
from tkinter import *# с помощью tkinter я создаю интерфейс
from tkinter import ttk#
from os import startfile# импортирую метод открывания файла
import supervision as sv# инструмент для компьютерного зрения
from ultralytics import YOLO# загружаю YOLO
import numpy as np#
from tkinter.messagebox import showinfo,showerror
def opencurfile():# определяем функцию для вызова интерфейса
  root = Tk()# создаем поле
  root.title("")#
  root.geometry("800x600")# определяем размеры поля
  def open_file():#определяем функцию для открытия файла
      filepath = filedialog.askopenfilename()# задаем значение переменной,которое равно директории выбранного для открытия файла
      if filepath != "":#если файл существует
          startfile(filepath)#запускаем файл
  open_button = ttk.Button(text="Открыть файл", command=open_file)# создаем кнопку для открытия файла
  open_button1 = ttk.Button(text = "Запустить аннотирование", command=lambda: opredvideo())# создаем кнопку для аннотирования всего видеo
  open_button1.pack(anchor=CENTER)# задаем ее местоположение
  open_button.pack(anchor=S,side = BOTTOM)# задаем ее местоположение
  root.mainloop()# для отображения окна и взаимодействия пользователя с ним вызываем метод mainloop()
def proverka(window1,entry1, entry2, entry3, entry4,entry5,path):
    #showinfo(title="аннотация", message='Нажмите')
    annoturovanie(window1,entry1, entry2, entry3, entry4,entry5,path)
def annoturovanie(window1,entry1, entry2, entry3, entry4,entry5,path):
    ultralytics.checks()  # проверяем правильную установку “ultralytics”
    HOME = os.getcwd()  # задаем значение переменной, которое является директорией исполняемого файла .py
    SOURCE_VIDEO_PATH = path  # директория + название
    entry5val = entry5.get()
    model = YOLO(f'{temp1}')  # выбор модели yolo
    CLASS_NAMES_DICT = model.model.names  # записываем имена которые в данной модели присутствуют
    SELECTED_CLASS_NAMES = ['person']  # выбранные имена
    SELECTED_CLASS_IDS = [  # определяем их айди
        {value: key for key, value in CLASS_NAMES_DICT.items()}[class_name]
        for class_name
        in SELECTED_CLASS_NAMES
    ]
    TARGET_VIDEO_PATH = f'{entry5val}.mp4'  # конечное название файла,которое мы получим после обработки
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
    #generator = sv.get_video_frames_generator(SOURCE_VIDEO_PATH)  # создаем генератор для итерации видео
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
def filepath(window2,):
    filepath = filedialog.askopenfilename()
    path = filepath
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
def click(path):
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
    Button4 = ttk.Button(window1, text=f'yolov8n',command=n)
    Button4.pack(anchor=CENTER)
    Button5 = ttk.Button(window1, text=f'yolov8m',command=m)
    Button5.pack(anchor=CENTER)
    Button6 = ttk.Button(window1, text=f'yolov8x',command=x)
    Button6.pack(anchor=CENTER)
    Label13 = ttk.Label(window1, text="Выберите конечный путь файла")
    Label13.pack(anchor=CENTER)
    entry5 = ttk.Entry(window1)
    entry5.pack(anchor=CENTER)
opencurfile()#запускаем программу