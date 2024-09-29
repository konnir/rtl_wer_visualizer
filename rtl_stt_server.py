import json
from typing import Optional

import httpx
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse


from service.rtl_checker_service import RtlCheckerService

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rtl_checker_service = RtlCheckerService()

@app.post("/evaluate")
async def evaluate(
        voiceFile: Optional[UploadFile] = File(None),  # Optional
        referenceFile: UploadFile = File(...),  # Required
        serverUrl: str = Form(...),  # Required
        hypothesisFile: Optional[UploadFile] = File(None)  # Optional
    ):
    print("Received files")
    if voiceFile:
        stt_server_url = f"{serverUrl}/pstt/sync/file"

        # Read the binary content of the voice file
        voice_file_content = await voiceFile.read()

        # Prepare the file to send as multipart/form-data with the correct key (audio_file)
        files = {
            'audio_file': ('voice_file.wav', voice_file_content, voiceFile.content_type)  # Send with key 'audio_file'
        }

        # Send the file to the external API using multipart/form-data
        async with httpx.AsyncClient() as client:
            response = await client.post(
                stt_server_url,  # Your external API endpoint
                files=files,  # Multipart/form-data with the voice file
                timeout=120
            )

            # Process the response
            if response.status_code == 200:
                decoded_string = response.content.decode('utf-8')
                parsed_json = json.loads(decoded_string)


                # texts = [segment['text'] for segment in parsed_json['speech_segments']]

                if "speech_segments" in parsed_json:
                    speech_segments = parsed_json.get("speech_segments", [])
                    texts = [segment.get("text", "") for segment in speech_segments]
                else:
                    texts = [parsed_json.get("speakerA", '')]
                
                text = "\n ".join([text_segment for text_segment in texts])
                encoded_text = rtl_checker_service.check_rtl_text(referenceFile.file.read().decode('utf-8'), text)

                return JSONResponse(content={"calculated_text": encoded_text})
            else:
                return {"error": f"Failed with status code {response.status_code}"}
    elif hypothesisFile:
        encoded_text = rtl_checker_service.check_rtl_text(referenceFile.file.read().decode('utf-8'), hypothesisFile.file.read().decode('utf-8'))
        return JSONResponse(content={"calculated_text": encoded_text})


# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("rtl_stt_server:app", host="0.0.0.0", port=8002, reload=True)
# Run the server with: uvicorn rtl_stt_server:app --reload
