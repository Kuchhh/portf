#!/usr/bin/env python3
"""Estimate a frame's focal length from vanishing points of straight lines.

Usage:
    python3 video-research/lens_vp.py FRAME.png

Finds up to four vanishing points (LSD segments + RANSAC), draws each set of
lines in its own colour into FRAME_vp.jpg, and for every pair of vanishing
points prints the focal length implied IF those two line directions are
perpendicular in the real world: f = sqrt(-(v1-c)·(v2-c)).

Look at the picture and keep only pairs that really are perpendicular, e.g.
two walls of a room corner, or a building's horizontals plus its verticals.
A frame shot square-on (one-point perspective) has no usable pair. The
full-frame equivalent assumes a 16:9 crop of a 36x24 sensor (frame height
20.25 mm); convert to Seedance FOV anchors (107/84/63/47/29°) by the printed hFOV.
"""
import itertools
import sys

import cv2
import numpy as np


def main():
    path = sys.argv[1]
    img = cv2.imread(path)
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    segs = cv2.createLineSegmentDetector(0).detect(gray)[0].reshape(-1, 4)
    length = np.hypot(segs[:, 2] - segs[:, 0], segs[:, 3] - segs[:, 1])
    keep = length > 0.035 * w
    segs, length = segs[keep], length[keep]

    def to_line(s):
        p, q = np.array([s[0], s[1], 1.0]), np.array([s[2], s[3], 1.0])
        l = np.cross(p, q)
        return l / np.hypot(l[0], l[1])

    lines = np.array([to_line(s) for s in segs])

    def inliers(v, idx, tol_deg=1.5):
        out = []
        for i in idx:
            s = segs[i]
            mid = np.array([(s[0] + s[2]) / 2, (s[1] + s[3]) / 2])
            d = np.array([s[2] - s[0], s[3] - s[1]])
            d /= np.linalg.norm(d)
            t = v[:2] / v[2] - mid if abs(v[2]) > 1e-9 else v[:2].copy()
            n = np.linalg.norm(t)
            if n > 1e-6 and np.degrees(np.arccos(min(1.0, abs((t / n) @ d)))) < tol_deg:
                out.append(i)
        return out

    def ransac(idx, iters=1500):
        rng = np.random.default_rng(0)
        best_v, best_in = None, []
        for _ in range(iters):
            a, b = rng.choice(idx, 2, replace=False)
            v = np.cross(lines[a], lines[b])
            if abs(v[2]) < 1e-9:
                v = v / np.linalg.norm(v)
            inl = inliers(v, idx)
            if len(inl) > len(best_in):
                best_v, best_in = v, inl
        if len(best_in) < 6:
            return None, []
        _, _, vt = np.linalg.svd(lines[best_in] * length[best_in][:, None])
        return vt[-1], best_in

    remaining, vps = list(range(len(segs))), []
    for _ in range(4):
        if len(remaining) < 6:
            break
        v, inl = ransac(remaining)
        if v is None:
            break
        vps.append((v, inl))
        remaining = [i for i in remaining if i not in inl]

    colours = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]
    names = ["red", "green", "blue", "yellow"]
    vis = img.copy()
    for k, (v, inl) in enumerate(vps):
        for i in inl:
            s = segs[i].astype(int)
            cv2.line(vis, (s[0], s[1]), (s[2], s[3]), colours[k], 3)
        where = f"({v[0] / v[2]:.0f},{v[1] / v[2]:.0f})" if abs(v[2]) > 1e-9 else "at infinity"
        print(f"VP{k} {names[k]}: {len(inl)} lines, {where}")
    cv2.imwrite(path.rsplit(".", 1)[0] + "_vp.jpg", cv2.resize(vis, (960, int(960 * h / w))))

    c = np.array([w / 2, h / 2])
    for (a, va), (b, vb) in itertools.combinations(enumerate(vps), 2):
        if abs(va[0][2]) < 1e-9 or abs(vb[0][2]) < 1e-9:
            continue
        d = -((va[0][:2] / va[0][2] - c) @ (vb[0][:2] / vb[0][2] - c))
        if d <= 0:
            print(f"  VP{a}+VP{b}: same side of centre, cannot both be perpendicular")
            continue
        f = np.sqrt(d)
        hfov = 2 * np.degrees(np.arctan((h * 16 / 9) / (2 * f)))
        print(f"  VP{a}+VP{b} if perpendicular: f={f:.0f}px, hFOV(16:9)={hfov:.0f}°, "
              f"full-frame ≈ {20.25 * f / h:.0f} mm")


if __name__ == "__main__":
    main()
