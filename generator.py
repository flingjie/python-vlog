from moviepy.editor import (
    ImageClip, 
    AudioFileClip,
    VideoFileClip,
    TextClip,
    concatenate_videoclips,
    CompositeVideoClip
)
from moviepy.video.tools.segmenting import findObjects
import parser
from tts import text2wav
import numpy as np
import config


def generate_title(title):
    print(f"title: {title}")
    
    def cascade(screenpos, i):
        v = np.array([0, -1])
        d = lambda t: 1 if t < 0 else abs(np.sinc(t) / (1 + t ** 4))
        return lambda t: screenpos + v * 400 * d(t - 0.15 * i)

    def move_letters(letters, funcpos):
        return [letter.set_pos(funcpos(letter.screenpos, i))
                for i, letter in enumerate(letters)]

    size = (1280, 720)
    title_clip = TextClip(title, color=config.TITLE['color'],
                          font=config.TITLE['font'], kerning=5,
                          fontsize=config.TITLE['font-size'])
    cvc = CompositeVideoClip([title_clip.set_pos('center')], size=size)
    letters = findObjects(cvc)
    clip = CompositeVideoClip(move_letters(letters, cascade), size=size).subclip(0, 5)
    return clip


def generate_clip_with_subtitle(image_path, text):
    print(f"clip text: {text}")
    clip = ImageClip(image_path)
    audio = AudioFileClip(text2wav(text))
    txt_clip = TextClip(text.replace(" ", ""), font=config.SUBTITLE['font'],
                        color=config.SUBTITLE['color'], fontsize=config.SUBTITLE['font-size'])
    video = CompositeVideoClip([clip, txt_clip.set_pos(('center', 'bottom'))])
    video.audio = audio
    video.duration = audio.duration
    return video


def generate_text_clip(text):
    print(f"title: {text}")

    def arrive(screenpos, i):
        v = np.array([-1, 0])
        d = lambda t: max(0, 3 - 3 * t)
        return lambda t: screenpos - 400 * v * d(t - 0.2 * i)

    def move_letters(letters, funcpos):
        return [letter.set_pos(funcpos(letter.screenpos, i))
                for i, letter in enumerate(letters)]

    size = (1280, 720)
    title_clip = TextClip(text, color=config.TEXT_CLIP['color'], font=config.TEXT_CLIP['font'],
                          kerning=5, fontsize=config.TEXT_CLIP['font-size'])
    cvc = CompositeVideoClip([title_clip.set_pos('center')], size=size)
    letters = findObjects(cvc)
    clip = CompositeVideoClip(move_letters(letters, arrive), size=size).subclip(0, 5)
    return clip


def load_video(video_path):
    return VideoFileClip(video_path)


def generate_ending(text="听说点赞带来好运"):
    print(f"ending: {text}")
    size = (1280, 720)
    title_clip = TextClip(text, color=config.ENDING['color'], font=config.ENDING['font'],
                          kerning=5, fontsize=config.ENDING['font-size'])
    clip = CompositeVideoClip([title_clip.set_pos('center')], size=size)
    clip.duration = 1
    return clip


def generate_vlog(filename, output_path):
    clips = []
    result = parser.parse(filename)
    title_clip = generate_title(result['title'])
    clips.append(title_clip)
    for item in result['content']:
        if item['text']:
            clips.append(generate_text_clip(item['text']))
        if item['type'] == 'image':
            clips.append(generate_clip_with_subtitle(item['link'], item['subtitle']))
        elif item['type'] == 'video':
            clips.append(load_video(item['link']))
    clips.append(generate_ending())
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_path, fps=24, audio_codec="aac")


