from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from pydub import AudioSegment
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    content = """<body>
                    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
                        <input name="files" type="file" accept=".mp3" multiple>
                        <input type="submit">
                    </form>
                </body>"""
    return HTMLResponse(content=content)


@app.post("/uploadfiles/")
async def upload_files(files: list[UploadFile], background_tasks: BackgroundTasks):
    saved_files = []
    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Process the file (dummy processing for this example)
        processed_file_location = process_file(file_location)
        saved_files.append(processed_file_location)

    # Schedule the deletion of files
    background_tasks.add_task(delete_files, saved_files)

    # For simplicity, return the first processed file
    return FileResponse(saved_files[0], media_type='audio/mpeg', filename=os.path.basename(saved_files[0]))



def process_file(file_path: str) -> str:
    # Load the audio file
    audio = AudioSegment.from_file(file_path, format="mp3")

    # Perform noise reduction or any processing (dummy processing in this example)
    processed_audio = audio  # No actual processing for this example

    # Save the processed audio
    processed_file_path = file_path.replace(".mp3", "_processed.mp3")
    processed_audio.export(processed_file_path, format="mp3")

    return processed_file_path

def delete_files(file_paths: list[str]):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

    # Delete the original files as well
    for file_path in file_paths:
        original_file_path = file_path.replace("_processed.mp3", ".mp3")
        if os.path.exists(original_file_path):
            os.remove(original_file_path)
