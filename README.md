# ��������� rttm-����� �� mp3

## ��������� ��� Windows.

�������������� ���������� ��������� ���������.

- GNU [Unix Utils](http://unxutils.sourceforge.net/) ��� �������� ����� makefile
- [Git for Windows](https://git-scm.com/download/win) ��� ������� � ����������� �������� �����.
- [Python3.10.11](https://www.python.org/downloads/release/python-31011/)
- [ffmpeg](https://ffmpeg.org/download.html) (����������� ����� � �������� � PATH)
- build tools by installing [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/)

## ��������� ��� Ubuntu. 22.04

```
sudo apt update
sudo apt-get install build-essential python3.10-venv python3-pip ffmpeg screen curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## ��������� ���������

```bash
git clone https://github.com/vb64/nemo.rttm.git
cd nemo.rttm
make setup PYTHON_BIN=python3
```
