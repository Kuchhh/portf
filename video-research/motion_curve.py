#!/usr/bin/env python3
"""Camera-motion curve inside one shot, in short windows.

Usage:
    python3 video-research/motion_curve.py VIDEO START END [WINDOW_SECONDS]

Per window: pan (%W/s, + means the scene slides right, i.e. the camera turns or
trucks left), tilt (%H/s), roll (°/s) and zoom (%/s, + means the frame grows:
push-in or zoom-in). The dominant motion is estimated on the whole frame, so a
subject filling most of the frame (or a wall passing the lens) pollutes that
window; read such windows together with the frames. A window that contains a
cut shows nonsense values.
"""
import sys

import cv2
import numpy as np


def main():
    video, start, end = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    window = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(start * fps))
    frames = []
    for _ in range(int((end - start) * fps) + 1):
        ok, frame = cap.read()
        if not ok:
            break
        width = 960
        frames.append(cv2.cvtColor(cv2.resize(frame, (width, int(width * frame.shape[0] / frame.shape[1]))),
                                   cv2.COLOR_BGR2GRAY))
    h, w = frames[0].shape
    centre = np.array([w / 2, h / 2], np.float32)

    def estimate(a, b):
        pts = cv2.goodFeaturesToTrack(a, 600, 0.01, 7)
        if pts is None or len(pts) < 10:
            return None
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pts, None)
        ok = st[:, 0] == 1
        if ok.sum() < 10:
            return None
        m, _ = cv2.estimateAffinePartial2D(pts[ok] - centre, nxt[ok] - centre,
                                           method=cv2.RANSAC, ransacReprojThreshold=2)
        if m is None:
            return None
        return m[0, 2], m[1, 2], np.degrees(np.arctan2(m[1, 0], m[0, 0])), np.hypot(m[0, 0], m[1, 0])

    step = max(1, int(round(window * fps)))
    print(f"{video} {start}-{end}s, window {step / fps:.2f}s")
    print(f"{'t':>6} {'pan%W/s':>8} {'tilt%H/s':>9} {'roll°/s':>8} {'zoom%/s':>8}")
    for s in range(0, len(frames) - 1, step):
        x = y = r = 0.0
        scale = 1.0
        n = 0
        for i in range(s, min(s + step, len(frames) - 1)):
            m = estimate(frames[i], frames[i + 1])
            if m:
                x += m[0]; y += m[1]; r += m[2]; scale *= m[3]; n += 1
        dt = n / fps if n else 1
        print(f"{start + s / fps:6.2f} {x / w * 100 / dt:+8.1f} {y / h * 100 / dt:+9.1f} "
              f"{r / dt:+8.2f} {(scale - 1) * 100 / dt:+8.1f}")


if __name__ == "__main__":
    main()
