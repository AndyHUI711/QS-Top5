import pyaudio
import wave
import os
import time


def get_audio():    # 阻塞形式
    # aa = str(input("是否开始录音？   （是/否）"))
    # if aa == str("是") :
        input_filename = "voice.wav"  #audio input through microphone

        input_filepath = 'C:\\Users\\dell\\Desktop\\【改1】python代码\\'  # input file path
        filepath = input_filepath + input_filename
        CHUNK = 256
        FORMAT = pyaudio.paInt16    # 16 bit sampling depth
        CHANNELS = 1                # Track number 1
        RATE = 16000               # sampling rate
        RECORD_SECONDS = 15     # record time
        WAVE_OUTPUT_FILENAME = filepath
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("*"*10, "开始录音：请在15秒内输入语音")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("*"*10, "录音结束\n")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


# get_audio(in_path)