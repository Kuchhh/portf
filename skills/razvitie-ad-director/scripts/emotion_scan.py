#!/usr/bin/env python3
"""Scan a video for faces and read their expressions over time: FACS-like action units and emotions.

Usage:
    python3 video-research/emotion_scan.py VIDEO [--step 0.1] [--scene 0.25] [--out DIR]
                                           [--landmarker PATH] [--emotion PATH]

Per sampled frame (every --step seconds) every face is measured with two models:
  * MediaPipe Face Landmarker — 52 blendshapes, mapped below to FACS action units (AU1 inner brow raiser,
    AU12 lip-corner puller, …), plus head turn/tilt from the face transform;
  * HSEmotion (EfficientNet-B0 trained on AffectNet) — 8 emotion probabilities plus valence and arousal.
Faces are tracked inside each shot (cuts by ffmpeg scene detection). Writes to DIR:
  <name>_emotions.csv  — one row per face per sample;
  <name>_emotions.md   — per shot and face: size, emotions, AU peaks with timing, blinks, head and gaze;
  <name>_faces.png     — contact sheet of face crops at the start, apex and end of each face track.

Models (not in the repo):
  face_landmarker.task  — https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
  enet_b0_8_va_mtl.onnx — models/affectnet_emotions/onnx/ in github.com/av-savchenko/face-emotion-recognition
                          (sparse clone: git clone --depth 1 --filter=blob:none --sparse …; git sparse-checkout set models/affectnet_emotions/onnx)
Needs: pip install --user mediapipe onnxruntime opencv-python-headless; apt-get install libegl1 libgles2.

Machine readings are a guide, not ground truth: check the contact sheet and the frames before writing a description.
"""
import argparse
import csv
import math
import os
import re
import subprocess

import cv2
import numpy as np

EMOTIONS = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]

# FACS action unit ← MediaPipe blendshapes (left/right averaged; asymmetry reported separately for AU12).
AU_MAP = {
    "AU1 inner brow up": ["browInnerUp"],
    "AU2 outer brow up": ["browOuterUpLeft", "browOuterUpRight"],
    "AU4 brow lowerer": ["browDownLeft", "browDownRight"],
    "AU5 upper lid raiser": ["eyeWideLeft", "eyeWideRight"],
    "AU6 cheek raiser": ["cheekSquintLeft", "cheekSquintRight"],
    "AU7 lid tightener": ["eyeSquintLeft", "eyeSquintRight"],
    "AU9 nose wrinkler": ["noseSneerLeft", "noseSneerRight"],
    "AU12 lip corner puller": ["mouthSmileLeft", "mouthSmileRight"],
    "AU14 dimpler": ["mouthDimpleLeft", "mouthDimpleRight"],
    "AU15 lip corner depressor": ["mouthFrownLeft", "mouthFrownRight"],
    "AU17 chin raiser": ["mouthShrugLower"],
    "AU18 lip pucker": ["mouthPucker"],
    "AU20 lip stretcher": ["mouthStretchLeft", "mouthStretchRight"],
    "AU24 lip pressor": ["mouthPressLeft", "mouthPressRight"],
    "AU26 jaw drop": ["jawOpen"],
    "AU43 eyes closed": ["eyeBlinkLeft", "eyeBlinkRight"],
}
AU_SHORT = {k: k.split()[0] for k in AU_MAP}


def cuts_of(video, scene):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                video], capture_output=True, text=True).stdout)
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-vf", f"select='gt(scene,{scene})',showinfo",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    return [0.0] + [float(t) for t in re.findall(r"pts_time:([0-9.]+)", log)] + [dur]


def euler(m):
    """Yaw (+ = face turns to frame left), pitch (+ = up), roll from a 4×4 face transform."""
    r = np.array(m)[:3, :3]
    sy = math.hypot(r[0, 0], r[1, 0])
    pitch = math.degrees(math.atan2(r[2, 1], r[2, 2]))
    yaw = math.degrees(math.atan2(-r[2, 0], sy))
    roll = math.degrees(math.atan2(r[1, 0], r[0, 0]))
    return yaw, pitch, roll


def softmax(x):
    e = np.exp(x - x.max())
    return e / e.sum()


def emotion_of(sess, rgb, box):
    x0, y0, x1, y1 = box
    cx, cy, s = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) * 1.25
    h, w = rgb.shape[:2]
    a, b = int(max(0, cx - s / 2)), int(max(0, cy - s / 2))
    c, d = int(min(w, cx + s / 2)), int(min(h, cy + s / 2))
    crop = rgb[b:d, a:c]
    if crop.size == 0:
        return None, None
    x = cv2.resize(crop, (224, 224)).astype(np.float32) / 255
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    out = sess.run(None, {"input": x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    return softmax(out[:8]), (float(out[8]), float(out[9])), crop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--step", type=float, default=0.1)
    ap.add_argument("--scene", type=float, default=0.25)
    ap.add_argument("--min-face", type=float, default=0.07, help="min face height, share of frame height")
    ap.add_argument("--out", default=".")
    home = os.path.expanduser("~/.cache/emotion-models")
    ap.add_argument("--landmarker", default=os.path.join(home, "face_landmarker.task"))
    ap.add_argument("--emotion", default=os.path.join(home, "enet_b0_8_va_mtl.onnx"))
    args = ap.parse_args()

    import mediapipe as mp
    import onnxruntime as ort
    from mediapipe.tasks import python as mpp
    from mediapipe.tasks.python import vision

    opts = vision.FaceLandmarkerOptions(
        base_options=mpp.BaseOptions(model_asset_path=args.landmarker, delegate=mpp.BaseOptions.Delegate.CPU),
        running_mode=vision.RunningMode.IMAGE, num_faces=4, output_face_blendshapes=True,
        output_facial_transformation_matrixes=True, min_face_detection_confidence=0.35,
        min_face_presence_confidence=0.35)
    lm = vision.FaceLandmarker.create_from_options(opts)
    sess = ort.InferenceSession(args.emotion, providers=["CPUExecutionProvider"])

    name = os.path.splitext(os.path.basename(args.video))[0]
    os.makedirs(args.out, exist_ok=True)
    cuts = cuts_of(args.video, args.scene)
    cap = cv2.VideoCapture(args.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    every = max(1, round(args.step * fps))
    rows, crops, tracks, next_id = [], {}, {}, {}
    idx = -1
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        idx += 1
        if idx % every:
            continue
        t = idx / fps
        shot = max(i for i, c in enumerate(cuts[:-1], 1) if t >= c - 1e-6)
        H, W = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
        for k, pts in enumerate(res.face_landmarks):
            xs = [p.x * W for p in pts]
            ys = [p.y * H for p in pts]
            box = (min(xs), min(ys), max(xs), max(ys))
            fh = (box[3] - box[1]) / H
            if fh < args.min_face:
                continue
            cx, cy = (box[0] + box[2]) / 2 / W, (box[1] + box[3]) / 2 / H
            prev = tracks.get(shot, [])
            best = min(prev, key=lambda tr: math.hypot(tr[1] - cx, tr[2] - cy), default=None)
            if best and math.hypot(best[1] - cx, best[2] - cy) < 0.18 and t - best[3] < 0.6:
                tid = best[0]
                prev.remove(best)
            else:
                next_id[shot] = next_id.get(shot, 0) + 1
                tid = f"S{shot}{chr(64 + next_id[shot])}"
            prev.append((tid, cx, cy, t))
            tracks[shot] = prev
            bs = {b.category_name: b.score for b in res.face_blendshapes[k]}
            yaw, pitch, roll = euler(res.facial_transformation_matrixes[k])
            probs, va, crop = emotion_of(sess, rgb, box)
            if probs is None:
                continue
            row = dict(t=round(t, 2), shot=shot, track=tid, face_h=round(fh, 3), cx=round(cx, 3), cy=round(cy, 3),
                       yaw=round(yaw, 1), pitch=round(pitch, 1), roll=round(roll, 1),
                       valence=round(va[0], 3), arousal=round(va[1], 3))
            for e, p in zip(EMOTIONS, probs):
                row[e] = round(float(p), 3)
            for au, keys in AU_MAP.items():
                row[AU_SHORT[au]] = round(float(np.mean([bs.get(k, 0.0) for k in keys])), 3)
            row["AU12_asym"] = round(bs.get("mouthSmileLeft", 0) - bs.get("mouthSmileRight", 0), 3)
            row["gaze_lr"] = round((bs.get("eyeLookOutLeft", 0) + bs.get("eyeLookInRight", 0)
                                    - bs.get("eyeLookInLeft", 0) - bs.get("eyeLookOutRight", 0)) / 2, 3)
            row["gaze_ud"] = round((bs.get("eyeLookUpLeft", 0) + bs.get("eyeLookUpRight", 0)
                                    - bs.get("eyeLookDownLeft", 0) - bs.get("eyeLookDownRight", 0)) / 2, 3)
            rows.append(row)
            crops[(tid, row["t"])] = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)
    lm.close()

    if not rows:
        print(f"{name}: no faces")
        return
    with open(os.path.join(args.out, f"{name}_emotions.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    md = [f"# {name}: мимика по кадрам", "",
          f"Шаг {args.step} с, лица от {args.min_face:.0%} высоты кадра. Склейки: "
          + ", ".join(f"{c:.2f}" for c in cuts[1:-1]), ""]
    sheet = []
    by_track = {}
    for r in rows:
        by_track.setdefault(r["track"], []).append(r)
    for tid, rs in sorted(by_track.items(), key=lambda kv: kv[1][0]["t"]):
        if len(rs) < 3:
            continue
        ts = np.array([r["t"] for r in rs])
        probs = np.array([[r[e] for e in EMOTIONS] for r in rs]).mean(0)
        order = np.argsort(-probs)
        val = np.array([r["valence"] for r in rs])
        aro = np.array([r["arousal"] for r in rs])
        md.append(f"## {tid}: {ts[0]:.1f}–{ts[-1]:.1f} с, лицо {np.mean([r['face_h'] for r in rs]):.0%} высоты кадра")
        md.append("")
        md.append(f"- Эмоции (среднее): " + ", ".join(f"{EMOTIONS[i]} {probs[i]:.0%}" for i in order[:3]))
        md.append(f"- Валентность {val.mean():+.2f} (от {val.min():+.2f} до {val.max():+.2f}), "
                  f"возбуждение {aro.mean():+.2f} (от {aro.min():+.2f} до {aro.max():+.2f})")
        peaks = []
        for au in AU_MAP:
            s = AU_SHORT[au]
            v = np.array([r[s] for r in rs])
            base = np.percentile(v, 15)
            if v.max() >= 0.25 and v.max() - base >= 0.15:
                on = ts[np.argmax(v >= base + 0.5 * (v.max() - base))]
                peaks.append(f"{au} {base:.2f}→{v.max():.2f} (с {on:.1f} с, пик {ts[v.argmax()]:.1f} с)")
            elif v.mean() >= 0.3:
                peaks.append(f"{au} держится {v.mean():.2f}")
        md.append("- Мышцы (AU): " + ("; ".join(peaks) if peaks else "лицо почти неподвижно"))
        blink = np.array([r["AU43"] for r in rs])
        blinks = int(((blink[1:] > 0.5) & (blink[:-1] <= 0.5)).sum())
        asym = np.array([r["AU12_asym"] for r in rs])
        smile = np.array([r["AU12"] for r in rs])
        if smile.max() > 0.25 and abs(asym[smile.argmax()]) > 0.2:
            side = "левый" if asym[smile.argmax()] > 0 else "правый"
            md.append(f"- Улыбка несимметричная: сильнее {side} угол рта (со стороны героя)")
        yaw = np.array([r["yaw"] for r in rs])
        pitch = np.array([r["pitch"] for r in rs])
        glr = np.array([r["gaze_lr"] for r in rs])
        md.append(f"- Моргания: {blinks}; голова: поворот {yaw.min():+.0f}…{yaw.max():+.0f}°, наклон "
                  f"{pitch.min():+.0f}…{pitch.max():+.0f}°; взгляд в сторону {glr.mean():+.2f}")
        md.append("")
        key = np.array([r["AU12"] + r["AU1"] + r["AU4"] + r["AU5"] + r["AU26"] + abs(r["valence"]) for r in rs])
        for label, i in (("начало", 0), ("пик", int(key.argmax())), ("конец", len(rs) - 1)):
            r = rs[i]
            img = cv2.resize(crops[(tid, r["t"])], (220, 220))
            top = EMOTIONS[int(np.argmax([r[e] for e in EMOTIONS]))]
            cv2.rectangle(img, (0, 0), (220, 34), (0, 0, 0), -1)
            cv2.putText(img, f"{tid} {label} {r['t']:.1f}s", (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 255), 1)
            cv2.putText(img, f"{top} v{r['valence']:+.2f} a{r['arousal']:+.2f}", (4, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.42, (255, 255, 255), 1)
            sheet.append(img)
    with open(os.path.join(args.out, f"{name}_emotions.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    if sheet:
        cols = 6
        while len(sheet) % cols:
            sheet.append(np.zeros_like(sheet[0]))
        grid = np.vstack([np.hstack(sheet[i:i + cols]) for i in range(0, len(sheet), cols)])
        cv2.imwrite(os.path.join(args.out, f"{name}_faces.png"), grid)
    print(f"{name}: {len(rows)} face samples, {len(by_track)} face tracks")


if __name__ == "__main__":
    main()
