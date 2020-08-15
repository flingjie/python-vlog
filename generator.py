from moviepy.editor import (
    ImageClip,
    ImageSequenceClip,
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
import os


def generate_title(title, link):
    print(f"title: {title}")
    title_clip = TextClip(title, color=config.TITLE['color'],
                          font=config.TITLE['font'], kerning=5,
                          fontsize=config.TITLE['font-size'],
                          stroke_color=config.TITLE['stroke-color'],
                          stroke_width=5)
    image_clip = ImageClip(link)
    clip = CompositeVideoClip([image_clip, title_clip.set_pos('center')],
                              size=config.SIZE)
    clip.duration = 2
    return clip


def get_vtuber(duration):
    vtuber = ImageSequenceClip(config.VTUBER_IMAGES * int(duration), fps=3)
    return vtuber


def generate_clip_with_subtitle(image_path, text):
    print(f"clip text: {text}")
    clip = ImageClip(image_path).resize(width=config.SIZE[0])
    audio = AudioFileClip(text2wav(text))
    txt_clip = TextClip(text.replace(" ", ""), font=config.SUBTITLE['font'],
                        color=config.SUBTITLE['color'], fontsize=config.SUBTITLE['font-size'],
                        stroke_color=config.SUBTITLE['stroke-color'],
                        stroke_width=3)
    video = CompositeVideoClip([clip.set_pos("center"), txt_clip.set_pos(('center', 'top'))],
                               size=config.SIZE)
    video.audio = audio
    video.duration = audio.duration
    return video


def generate_text_clip(text):
    print(f"title: {text}")

    def rot_matrix(a):
        return np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])

    def damping(t):
        return 1.0 / (0.3 + t ** 8)

    def vortex(screenpos, i, nletters):
        a = i * np.pi / nletters  # angle of the movement
        v = rot_matrix(a).dot([-1, 0])
        if i % 2:
            v[1] = -v[1]
        return lambda t: screenpos + 400 * damping(t) * rot_matrix(0.5 * damping(t) * a).dot(v)

    def move_letters(letters, funcpos):
        return [letter.set_pos(funcpos(letter.screenpos, i, len(letters)))
                for i, letter in enumerate(letters)]

    title_clip = TextClip(text, color=config.TEXT_CLIP['color'], font=config.TEXT_CLIP['font'],
                          kerning=5, fontsize=config.TEXT_CLIP['font-size'])
    cvc = CompositeVideoClip([title_clip.set_pos('center')], size=config.SIZE)
    clip = CompositeVideoClip(move_letters(findObjects(cvc), vortex),
                              size=config.SIZE).subclip(0, 2.6)
    return clip


def load_video(video_path):
    clip = VideoFileClip(video_path)
    return CompositeVideoClip([clip.set_pos("center")], size=config.SIZE)


def generate_ending(image_path="data/ending.png", text="听说点赞带来好运"):
    print(f"ending: {text}")
    title_clip = TextClip(text, color=config.ENDING['color'], font=config.ENDING['font'],
                          kerning=5, fontsize=config.ENDING['font-size'])
    img_clip = ImageClip(image_path)
    clip = CompositeVideoClip([img_clip, title_clip.set_pos('center')],
                              size=config.SIZE)
    clip.duration = 2
    return clip


def generate_vlog(filename, output_path):
    clips = []
    result = parser.parse(filename)
    title = result['title']['text']
    link = result['title']['link']
    title_clip = generate_title(title, link)
    for item in result['content']:
        if item['text']:
            clips.append(generate_text_clip(item['text']))
        if item['type'] == 'image':
            clips.append(generate_clip_with_subtitle(item['link'], item['subtitle']))
        elif item['type'] == 'video':
            clips.append(load_video(item['link']))

    clips.append(generate_ending())
    result = concatenate_videoclips(clips, method="compose")
    vtuber_clip = get_vtuber(result.duration)
    content_clip = CompositeVideoClip([result,
                                       vtuber_clip.set_pos(('left', 'bottom'))])
    ending_clip = generate_ending()
    video = concatenate_videoclips([title_clip, content_clip, ending_clip],
                                   method="compose")
    video.write_videofile(os.path.join(output_path, f"{title}.mp4"),
                          fps=24, audio_codec="aac")
