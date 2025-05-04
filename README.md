# Получение rttm-файла из mp3

## Настройка под Windows.

Предварительно установить следующие программы.

- GNU [Unix Utils](http://unxutils.sourceforge.net/) для операций через makefile
- [Git for Windows](https://git-scm.com/download/win) для доступа к репозитарию исходных кодов.
- [Python3.10.11](https://www.python.org/downloads/release/python-31011/)
- [ffmpeg](https://ffmpeg.org/download.html) (распаковать архив и добавить в PATH)
- build tools by installing [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/)

## Настройка под Ubuntu. 22.04

```
sudo apt update
sudo apt-get install build-essential python3.10-venv python3-pip ffmpeg screen curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Установка программы

```bash
git clone https://github.com/vb64/nemo.rttm.git
cd nemo.rttm
make setup PYTHON_BIN=python3
```

## Ссылки

- Спецификация [формата RTTM](https://habr.com/ru/articles/900988/)
- [3D-Speaker](https://github.com/modelscope/3D-Speaker) Speaker Diarization
- [SpeechBrain](https://github.com/speechbrain)
- [Kaldi](https://www.assemblyai.com/blog/kaldi-speech-recognition-for-beginners-a-simple-tutorial)
- [How to get the duration of audio in Python?](https://www.geeksforgeeks.org/how-to-get-the-duration-of-audio-in-python/)
- [speaker-diarization-3.1](https://github.com/pyannote/hf-speaker-diarization-3.1) HUGGINGFACE TOKEN
