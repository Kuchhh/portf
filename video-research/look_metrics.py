#!/usr/bin/env python3
"""Look metrics of a reference video, sampled every 0.5 s.

Usage:
    python3 video-research/look_metrics.py VIDEO [--skip 15.5-21,30-32]

Medians over sampled frames (flat graphic cards are dropped automatically,
--skip removes other ranges such as end cards):
  edges%     share of Canny edge pixels: how busy and detailed the frame is
  bg/centre  Laplacian variance of the border vs the centre: below 1 means
             the background is softer than the subject (shallow depth of field)
  black/white  2nd and 98th luma percentiles (0-255): crushed vs lifted shadows
  meanY      overall brightness
  colorful   Hasler-Süsstrunk colourfulness
  warm       mean R minus mean B: positive is warm
"""
import argparse

import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--skip", default="")
    args = ap.parse_args()
    skips = [tuple(float(x) for x in r.split("-")) for r in args.skip.split(",") if r.strip()]

    cap = cv2.VideoCapture(args.video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    rows = []
    for fi in range(0, total, max(1, int(fps / 2))):
        if any(a <= fi / fps < b for a, b in skips):
            continue
        cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.resize(frame, (960, int(960 * frame.shape[0] / frame.shape[1])))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 60, 150).mean() / 255
        if edges < 0.01:
            continue
        h, w = gray.shape
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        centre = lap[h // 4:3 * h // 4, w // 4:3 * w // 4].var()
        border = np.ones_like(gray, bool)
        border[h // 4:3 * h // 4, w // 4:3 * w // 4] = False
        b, g, r = [frame[..., i].astype(float) for i in range(3)]
        rg, yb = r - g, 0.5 * (r + g) - b
        colourful = np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean())
        rows.append((edges * 100, lap[border].var() / (centre + 1e-6), np.percentile(gray, 2),
                     np.percentile(gray, 98), gray.mean(), colourful, r.mean() - b.mean()))
    m = np.median(np.array(rows), axis=0)
    print(f"edges% {m[0]:.1f} | bg/centre {m[1]:.2f} | black {m[2]:.0f} white {m[3]:.0f} | "
          f"meanY {m[4]:.0f} | colorful {m[5]:.0f} | warm {m[6]:+.1f}  ({len(rows)} frames)")


if __name__ == "__main__":
    main()
