from Record import record_to_file
from text2digits import text2digits
from tempfile import SpooledTemporaryFile
import re
from textual.app import App, ComposeResult
from textual.widgets import DataTable
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)
#timee = time.time()
class TableApp(App):

    def __init__(self,rows):
        self.rows = rows
        super().__init__()

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        rows = iter(self.rows)
        table.add_columns(*next(rows))
        table.add_rows(rows)


def transcribe_audio()->str:

    #audio = SpooledTemporaryFile(suffix=".wav")
    #audio = "check.wav"
    #record_to_file(audio)
    audio = open("check1.wav", "rb")
    audio.seek(0)

    model = Model("vosk_models/model")
    rec = KaldiRecognizer(model, 16000)

    rec.AcceptWaveform(audio.read())
    data = " "+rec.Result()[14:-3]
    audio.close()
    print(data)
    return data

def text_to_data(string)->list:
    t2d = text2digits.Text2Digits()

    #print(string) 
    output_string = t2d.convert(string.strip(".")).lower()
    output = output_string.split("next")
    
    output_processed = []
    for k,j in enumerate(output):
        output_processed.append(dict())
        if "for" in j and "of" in j:

            if j.find("of") < j.find("for"):
                output_processed[k]["quantity"], j = j.split("of")
            else:
                j, output_processed[k]["quantity"] = j.split("of")

            output_processed[k]["name"], output_processed[k]["price"] = j.replace("rupees", "").split('for')
            
        elif "for" in j:
            if j.find("rupees") < j.find("for"):
                output_processed[k]["price"], j = j.replace("rupees", "").split('for')
            else:
                j, output_processed[k]["price"] = j.replace("rupees", "").split('for')

            output_processed[k]["quantity"], output_processed[k]["name"] = re.split(
                "(?<=\d)\s(?=[a-zA-Z])", j, maxsplit=1)

    return output_processed


def main():
    string = transcribe_audio()
    processed = text_to_data(string)
    ROWS = [("Name","Quantity","Price")]
    ROWS.extend(
        [(x["name"], x["quantity"], x["price"]) for x in processed if len(x)==3])

    app = TableApp(rows=ROWS)
    app.run()

if __name__=="__main__":
    main()