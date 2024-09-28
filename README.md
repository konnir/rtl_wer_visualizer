# rtl_wer_visualizer

![image](https://github.com/user-attachments/assets/28eae762-383a-4143-b47d-f34fd4521469)


## Project Overview

This project, `rtl_stt_evaluator`, is designed to evaluate the performance of real-time speech-to-text systems. It provides tools and metrics to assess accuracy, latency, and other critical factors.

## Features

- Allow testing of STT server using a voice file and a text file with the actual translation.
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

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the Apache 2.0 License.
