import torch
from TTS.api import TTS

def text_to_speech(content):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2",).to(device)

    tts.tts_to_file(text=content,
                    file_path="audio/output.wav",
                    speaker_wav="ref_voice/ref.wav",
                    # speaker="Ana Florence",
                    gpt_cond_len=3,
                    language="en",
                    split_sentences=True
                    )
    return True