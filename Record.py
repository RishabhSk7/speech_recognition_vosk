def record(CHANNELS, RATE):
	import pyaudio
	import threading

	CHUNK = 1024
	FORMAT = pyaudio.paInt16

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

	print("Start recording")

	frames = []

	global exec
	exec = 1
	def run():
		while exec:
			frames.append(stream.read(CHUNK))

	t1 = threading.Thread(target=run)
	t2 = threading.Thread(target=input, args=("Enter stop when all values have been entered: ",))
	t1.start()
	t2.start()
	t2.join()
	exec = 0
	t1.join()

	sample_width = p.get_sample_size(FORMAT)
	
	stream.stop_stream()
	stream.close()
	p.terminate()
	
	return sample_width, frames

def record_to_file(file_path,CHANNELS=1,RATE = 44100):
	import wave
	wf = wave.open(file_path, 'wb')
	wf.setnchannels(1)
	sample_width, frames = record(1,16000)
	wf.setsampwidth(sample_width)
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

if __name__ == '__main__':
	print('#' * 80)
	print("Please speak word(s) into the microphone")
	print('Press Ctrl+C to stop the recording')
	
	record_to_file('Audiofiles/output.wav')
	
	print("Result written to output.wav")
	print('#' * 80)