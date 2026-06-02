from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile as wavfile

print("Loading Dzongkha TTS model...")

model = VitsModel.from_pretrained("facebook/mms-tts-dzo")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-dzo")


def text_to_speech(text, output_file):
    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        waveform = model(**inputs).waveform

    audio = waveform.squeeze().cpu().numpy()

    wavfile.write(
        output_file,
        rate=model.config.sampling_rate,
        data=audio
    )

    print(f"Saved: {output_file}")


texts = [
    (
        "text1.wav",
        "འབྲུག་རྒྱལ་གཞུང་གཙུག་ལག་སློབ་སྡེའི་འོག་ལུ་ཡོད་པའི་ཚན་རིག་དང་འཕྲུལ་རིག་མཐོ་རིམ་སློབ་གྲྭའི་གློག་རིག་དང་འཕྲུལ་རིག་ལས་ཁུངས།"
    ),
    (
        "text2.wav",
        "རང་བཞིན་གྱིས་བློ་སླབ་པའི་ངོས་ལེན་གྱིས་རྫོང་ཁ་གི་བློ་སླབ་མི་ཚིག་ཚུ་འབྲི་ཡི་གུ་ལུ་འགྱུར་བཅོས་འབད་ཚུགསཔ་བཟོཝ་ཨིན།"
    ),
    (
        "text3.wav",
        "འབྲུག་གི་གཞུང་འབྲེལ་གྱི་ཁ་སྐད་ཨིན་པའི་རྫོང་ཁ་འདི་ ལམ་སྲོལ་དང་སྐད་ཡིག་ནང་ ཧ་ཅང་གི་ཁག་ཆེ་བའི་ཡན་ལག་ཅིག་ཡོད།"
    ),
    (
        "text4.wav",
        "རྫོང་ཁ་དང་ཨིང་ལིཤ་གི་བར་ན་ཡིག་ཆ་སྐད་སྒྱུར་འདི་འཇམ་ཏོང་ཏོ་བཟོཝ་ཨིན།"
    ),
    (
        "text5.wav",
        "ཡིག་ཆ་སྐད་ཆ་ལུ་ཡིག་ཆ་འདི་ལག་ལེན་པ་ཚུ་ལུ་ཡིག་ཆ་འབྲི་མི་ནང་ཡིག་ཆ་འདི་རང་བཞིན་གྱི་སྐད་སྒྲ་སླབ་མི་ཚིག་ལུ་བསྒྱུར་བཅོས་འབད་ནི་གི་གོ་སྐབས་བྱིན་མས། ཨ་ནཱི་ལག་ལེན་འདི་གིས་ཉན་ཆས་ཀྱི་ཉམས་མྱོང་སྤྲོ་བ་ཅན་ཅིག་བྱིན་མི་གིས་ལག་ལེན་པ་ཚུ་ལུ་ཡིག་ཆ་ཀྱི་དོན་ཆས་ཉན་ནི་དང་ཡང་ན་མཐོང་ཚུགས་མི་མི་མི་ལུ་བརྡ་དོན་འཐོབ་ནི་ལུ་ཆ་རོགས་འབད་ཚུགསཔ་བཟོ་ནུག།"
    ), 
    (

        "text6.wav",
        "ང་བཅས་ཀྱི་ རྫོང་ཁ་ཨེན་ཨེལ་པི་ལས་འགུལ་ཚུ་དང་གཅིག་ཁར་ རྫོང་ཁ་སྐད་ཡིག་གི་གནས་སྡུད་ལས་ ཡོན་ཏན་ཧ་གོ་ཚུགས་ནི།"

    )

]

for filename, text in texts:
    text_to_speech(text, filename)

print("All audio files generated.")