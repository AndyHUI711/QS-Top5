import time
import voice_record
import datetime
from asr_json import *
from SMS import SMS_send
from face_emotion import face_emotion
from Serial import *

csv_record = open('record.csv', 'a')

if __name__ == "__main__":  # main function
    # serialStart()
    my_face = face_emotion()  # instantiation
    sad_count = 0
    tic = time.perf_counter()  # tic initialization
    el_name = '郝小子'
    sent_flag = 'False'

    ser = serial.Serial(find_com(), 9600, timeout=0.1)  # Open the serial port
    initSerial(ser)
    serialCMD(ser, 'PASSION_MUSIC')     # play PASSION_MUSIC file
    while 1:
        emotion = my_face.learning_face(1, "test_data/9.mp4")  # 0 camera mode，1 video mode，2 picture mode
        print(emotion)
        voice_record.get_audio()
        word, NLP_result = voice_API()
        print('NLP_result[0] = ' + str(NLP_result))
        now_time = datetime.datetime.now()
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.datetime.now().strftime('%H:%M')
        # recording the emotion status
        print('sad_count = ' + str(sad_count))
        if NLP_result == '0':
            word = 'None'
            sentiment = 'None'
            confidence = 'None'
            negative_prob = 'None'
        else:
            sentiment = NLP_result[0]['sentiment']
            confidence = NLP_result[0]['confidence']
            negative_prob = NLP_result[0]['negative_prob']
        if emotion == 'Sad':
            tic = time.perf_counter()
            sad_count += 1
        if time.perf_counter() - tic >= 10 * 60:  # if there's no sad emotion after 10 mins, set sad_count to 0
            sad_count = 0
        if sad_count >= 1:  # send message and play the music when detecting sad emotions
            serialCMD(ser, 'SOFT_MUSIC')    # play soft_music
            sent_flag = 'Ture'
            sad_count = 0
            print('发送中')
            SMS_send('郝', '郝小子')
            print('发送成功')
        csv_record = open('record.csv', 'a')
        csv_record.write('\n' +
                         date_str + ', ' + time_str + ', ' + el_name + ', ' + emotion + ', ' + word + ', ' + str(
                        sentiment) + ', ' \
                         + str(confidence) + ', ' + str(negative_prob) + ', ' + sent_flag)
        csv_record.close()
        sent_flag = 'False'
