import json
import shutil
from logging import DEBUG, basicConfig, getLogger
from pathlib import Path

log = getLogger(__name__)
basicConfig(level=DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

for musplay_series in Path("./gamecover").iterdir():
    series_name = musplay_series.name
    for song_img in musplay_series.iterdir():
        song_name = song_img.stem
        dest_dir = Path("./musplays") / series_name / song_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            Path("./gamecover") / series_name / f"{song_name}.png",
            dest_dir / "cover.png",
        )
        shutil.copyfile(
            Path("./gameimage") / series_name / f"{song_name}.png",
            dest_dir / "image.png",
        )
        shutil.copyfile(
            Path("./gamemusic") / series_name / f"{song_name}.mp3",
            dest_dir / "music.mp3",
        )
    shutil.copyfile(
        Path("./themeimage") / f"{series_name}.png",
        Path("./musplays") / series_name / "image.png",
    )
    shutil.copyfile(
        Path("./themecover") / f"{series_name}.png",
        Path("./musplays") / series_name / "cover.png",
    )

with Path("./music_data/music_notes.json").open(encoding="utf-8") as file:
    musplay_notes_info: dict[str, list[float]] = json.load(file)

for musplay_name_suffix, note_info in musplay_notes_info.items():
    log.debug(musplay_name_suffix.replace("_", " "))
    found = False
    for musplay_series in Path("./musplays").iterdir():
        for musplay_name in musplay_series.iterdir():
            log.debug("\t%s", musplay_name.name)
            if (
                musplay_name.name.replace("_", " ")
                .lower()
                .endswith(musplay_name_suffix.replace("_", " ").lower())
            ):
                with (musplay_name / "notes.json").open(
                    "w", encoding="utf-8", newline=""
                ) as file:
                    json.dump(note_info, file, indent=4)
                found = True
                break
        if found:
            break
del musplay_notes_info

with Path("./music_data/music_path.json").open(encoding="utf-8") as file:
    musplay_metadata_info: dict[str, dict[str, str]] = json.load(file)

for musplay_name_suffix, note_info in musplay_metadata_info.items():
    log.debug(musplay_name_suffix.replace("_", " "))
    found = False
    for musplay_series in Path("./musplays").iterdir():
        for musplay_name in musplay_series.iterdir():
            log.debug("\t%s", musplay_name.name)
            if (
                musplay_name.name.replace("_", " ")
                .lower()
                .endswith(musplay_name_suffix.replace("_", " ").lower())
            ):
                with (musplay_name / "metadata.json").open(
                    "w", encoding="utf-8", newline=""
                ) as file:
                    json.dump({"author": note_info["author"]}, file, indent=4)
                found = True
                break
        if found:
            break
