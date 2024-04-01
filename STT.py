from speech_api.utils import *
def content(file, header):
    import logging
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Uploading file...")
    audio_url = upload_file(file, header)        #upload file, get url
    logging.info("File uploaded.")

    polling_end = make_polling_endpoint(
    request_transcript(audio_url, header)
    )                           #create endpoint to get current status, after uploading file for transcript
    logging.info("Polling endpoint created.")

    wait_for_completion(polling_end, header)    #wait while transcription takes place
    logging.info("Transcription completed.")

    retrieved = get_paragraphs(polling_end, header)   #return transcripted data
    logging.info("Data retrieved.\n")
    return retrieved