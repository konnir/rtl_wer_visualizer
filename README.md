# RTL_WER_VISUALIZER

![image](https://github.com/user-attachments/assets/eda9cbd8-aa84-4af3-81a8-67dc499e536b)

## Project Overview

This project, `rtl_wer_visualizer`, is designed to evaluate the performance of real-time speech-to-text systems. 
It allow to compare hypothesis text (output of stt system) nad reference text (the gorund truth usaully trianscribed by human). 
This is designed to RTL lanaguages specifically. 
The result is the hyphotesis text with: 
- **substitute** - the wrong word in 🔴 **RED** and below it the right word in 🟢 **GREEN**
- **insertions** - words that the hypothesis provided that are not in the reference in 🔵 **BLUE**
- **deletions** - words that the hypothesis did not mention but are in the reference in ⚪ **GRAY**

## Features

- Allow testing of STT server using a voice file and a text file with the actual transcription.
- Allow testing of STT output using a text file and a text file with the actual transcription.
- Enable visualization of the JIWER report.

## Installation

To install the project, clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/rtl_stt_evaluator.git
cd rtl_stt_evaluator
poetry install
```

Make sure you have Python 3.11 installed. You can manage your Python versions using tools like `pyenv`.

```bash
pyenv install 3.11.0
pyenv local 3.11.0
```

## Usage

To run the evaluation, use the following command:

```bash
uvicorn rtl_stt_server:app --host 0.0.0.0 --port 8000
```

## Viewing the UI

To view the user interface for the `rtl_stt_evaluator`, follow these steps:

1. Ensure the server is running using the command mentioned in the Usage section.
2. Open your web browser and navigate to `http://localhost:8000`.

You should now see the UI where you can upload voice files and text files for evaluation.

## Credits

This project utilizes the JIWER library for computing Word Error Rate (WER) and other related metrics. JIWER is an open-source library that simplifies the comparison between hypothesis and reference texts. You can find more information about it here: https://github.com/jitsi/jiwer .

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the Apache 2.0 License.
