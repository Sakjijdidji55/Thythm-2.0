import os

import pygame

pygame.mixer.init()
music_list = {}

# for file in os.listdir("gamemusic"):
#     if file.endswith(".mp3"):
#         continue
#     for f in os.listdir("gamemusic/" + file):
#         # print(f)
#         author = f.split("-")[0]
#         # print(author)
#         name = f.split("-")[-1][:-4]
#         name = name.replace(" ", "_")
#         # print(name)
#         music_list[name]={
#             "music":os.path.join("gamemusic", file, f),
#             "author": author,
#             "cover": os.path.join("gamecover", file, f[:-4] + ".png"),
#             "image": os.path.join("gameimage", file, f[:-4] + ".png"),
#             }
# pygame.mixer.music.load(music_list[name]["music"])
# pygame.image.load(music_list[name]["cover"])
# pygame.image.load(music_list[name]["image"])
# music_list[f.split("-")[1][:-4]]=os.path.join("gamemusic", file, f)

# if not os.path.exists("enter"):
#     os.mkdir("enter")

# i = 0
# for file in os.listdir("newenter"):
#     if i % 5 == 0:
#         with open("enter/" + file, 'wb') as f:
#             f.write(open("newenter/" + file, 'rb').read())
#     i += 1

# music_notes = {}

# for k, v in music_list.items():
#     y, sr = librosa.load(v)
#     tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
#     beat_times = librosa.frames_to_time(beat_frames, sr=sr)
#     music_notes[k] = beat_times.tolist()


# import json
# with open("music_data/music_path.json", "w") as f:
#     json.dump(music_list, f)
# with open("music_data/music_notes.json", "w") as f:
#     json.dump(music_notes, f)


# beat_times = librosa.frames_to_time(beat_frames, sr=sr)


if not os.path.exists("switch"):
    os.mkdir("switch")

from PIL import Image

for file in os.listdir("nswitch"):
    img = Image.open("nswitch/" + file)
    img = img.convert("RGBA")

    pixels = img.load()

    width, height = img.size

    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if abs(r) < 5 and abs(g) < 5 and abs(b) < 5:
                pixels[x, y] = (0, 0, 0, 0)
            else:
                pixels[x, y] = (min(r + 10, 255), min(g + 10, 255), min(b + 10, 255), a)
    img.save("switch/" + file)
