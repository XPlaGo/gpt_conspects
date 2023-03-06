from pdf2image import convert_from_path
import openai
from pytesseract import pytesseract
from transformers import GPT2TokenizerFast


print("converting pdf to images...")

first_page = int(input("first page: "))
last_page = int(input("last page: "))
filename = input("filepath: ")
out_filename = input("output filename: ")

images = convert_from_path(
    filename,
    500,
    poppler_path=r'D:\Program Files\poppler-0.68.0\bin',
    first_page=first_page,
    last_page=last_page
)

print("pdf was converted...")

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
openai.api_key = "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"  # my private api key ... ok, you can use it)
model_engine = "text-davinci-003"

print("starting text recognition...")


def num_tokens_from_messages(message):
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    number_of_tokens = len(tokenizer(message)['input_ids'])
    return number_of_tokens


def request_chatgpt(req_str):
    print(" -- requesting ChatGPT")
    tokens = num_tokens_from_messages(req_str)
    print(" -- req len: " + str(tokens))
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=req_str,
        max_tokens=(4097 - tokens),
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion.choices[0].text


def image_recognition(image):
    return pytesseract.image_to_string(image, lang="rus", config=tessdata_dir_config)


with open(out_filename, "w", encoding="utf-8") as file:
    for (i, image) in enumerate(images):
        print(str(first_page + i) + " page converting")
        text = image_recognition(image)
        print(" -- completed")
        req = "Сделай конспект по тексту:\n \"" + str(text) + "\""
        res = request_chatgpt(req)
        file.write("\n\n" + str({i + first_page}) + ":\n\n")
        file.write(str(res))
        file.flush()
        print(" -- done")

file.close()
