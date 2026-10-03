#!/usr/bin/env python3
"""Measure camera movement per shot in a reference video.

Splits the video into shots (ffmpeg scene detection), then tracks background
features with optical flow, excluding a central column where a centred hero
usually stands. Reports, per shot: pan, tilt, roll, push-in (background
expanding = camera moving forward), vertical bob and roll sway (oscillation
left after removing the linear trend), and how much the hero region drifts.

Usage:
    pip install --user opencv-python-headless
    python3 video-research/camera_motion.py VIDEO [--scene 0.25] [--extra-cuts 4.25,7.0]

Percentages are of frame width/height. Hidden match cuts (hero stays in place,
world changes) can fool scene detection; add them with --extra-cuts.
"""
import argparse
import re
import subprocess

import cv2
import numpy as np

W, H = 960, 540
CENTER = np.array([W / 2, H / 2], np.float32)


def detect_cuts(video, threshold):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", video, "-vf",
         f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    return [float(t) for t in re.findall(r"pts_time:([0-9.]+)", out)]


def read_frames(video):
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(cv2.resize(frame, (W, H)), cv2.COLOR_BGR2GRAY))
    return frames, fps


def masks():
    hero = np.zeros((H, W), np.uint8)
    hero[int(H * 0.15):, int(W * 0.33):int(W * 0.67)] = 255
    bg = 255 - hero
    bg[:int(H * 0.12), :int(W * 0.30)] = 0  # brand logo corner
    return bg, hero


def estimate(a, b, mask):
    """Similarity transform a->b about the frame centre: dx, dy, roll°, scale."""
    pts = cv2.goodFeaturesToTrack(a, 500, 0.01, 8, mask=mask)
    if pts is None or len(pts) < 8:
        return None
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pts, None)
    ok = st[:, 0] == 1
    if ok.sum() < 8:
        return None
    m, _ = cv2.estimateAffinePartial2D(pts[ok] - CENTER, nxt[ok] - CENTER,
                                       method=cv2.RANSAC, ransacReprojThreshold=2)
    if m is None:
        return None
    return m[0, 2], m[1, 2], np.degrees(np.arctan2(m[1, 0], m[0, 0])), np.hypot(m[0, 0], m[1, 0])


def detrended_ptp(values):
    v = np.asarray(values)
    if len(v) < 3:
        return 0.0
    t = np.arange(len(v))
    return float(np.ptp(v - np.polyval(np.polyfit(t, v, 1), t)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--scene", type=float, default=0.25)
    ap.add_argument("--extra-cuts", default="")
    args = ap.parse_args()

    frames, fps = read_frames(args.video)
    duration = len(frames) / fps
    extra = [float(x) for x in args.extra_cuts.split(",") if x.strip()]
    cuts = sorted({0.0, duration, *detect_cuts(args.video, args.scene), *extra})
    bg, hero = masks()

    print(f"{'shot':>4} {'start':>6} {'dur':>5} | {'pan%W':>6} {'tilt%H':>6} {'roll°':>6} "
          f"{'push%/s':>7} | {'bob%H':>5} {'sway°':>5} | {'heroΔ%W':>7} {'heroΔ%H':>7}")
    for n, (a, b) in enumerate(zip(cuts, cuts[1:]), 1):
        i0, i1 = int(a * fps) + 1, int(b * fps) - 1
        if i1 - i0 < 3:
            continue
        x = y = r = 0.0
        s = 1.0
        hx = hy = 0.0
        ys, rs = [], []
        for i in range(i0, i1):
            m = estimate(frames[i], frames[i + 1], bg)
            if m:
                x += m[0]; y += m[1]; r += m[2]; s *= m[3]
            ys.append(y); rs.append(r)
            h = estimate(frames[i], frames[i + 1], hero)
            if h:
                hx += h[0]; hy += h[1]
        dur = (i1 - i0) / fps
        print(f"{n:>4} {a:6.2f} {dur:5.2f} | {x / W * 100:+6.1f} {y / H * 100:+6.1f} {r:+6.2f} "
              f"{(s - 1) * 100 / dur:+7.1f} | {detrended_ptp(ys) / H * 100:5.1f} {detrended_ptp(rs):5.2f} | "
              f"{hx / W * 100:+7.1f} {hy / H * 100:+7.1f}")


if __name__ == "__main__":
    main()
