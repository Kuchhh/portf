#!/usr/bin/env python3
"""Split a reference video into shots and build a contact sheet of mid-frames.

Usage:
    python3 video-research/shotmap.py VIDEO [--scene 0.25] [--out DIR]

Prints the cut times and shot-length stats, writes one labelled mid-frame per
shot and `<name>_shots.png` (4 columns). Hidden match cuts can slip past scene
detection; check long shots with dense frame strips.
"""
import argparse
import os
import re
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--scene", type=float, default=0.25)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()

    name = os.path.splitext(os.path.basename(args.video))[0]
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", args.video],
        capture_output=True, text=True).stdout)
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", args.video, "-vf",
         f"select='gt(scene,{args.scene})',showinfo", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    cuts = [0.0] + [float(t) for t in re.findall(r"pts_time:([0-9.]+)", log)] + [dur]

    mid_dir = os.path.join(args.out, f"{name}_mid")
    os.makedirs(mid_dir, exist_ok=True)
    for i, (a, b) in enumerate(zip(cuts, cuts[1:]), 1):
        label = f"S{i} {a:.2f}-{b:.2f}"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", f"{(a + b) / 2:.3f}", "-i", args.video,
             "-frames:v", "1", "-vf",
             f"scale=480:-2,drawtext=text='{label}':x=6:y=6:fontsize=22:fontcolor=yellow:"
             "box=1:boxcolor=black@0.6",
             os.path.join(mid_dir, f"{i:03d}.png")], check=True)
    rows = (len(cuts) - 2) // 4 + 1
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-pattern_type", "glob", "-i", os.path.join(mid_dir, "*.png"),
         "-vf", f"tile=4x{rows}:padding=4", "-frames:v", "1",
         os.path.join(args.out, f"{name}_shots.png")], check=True)

    lengths = sorted(b - a for a, b in zip(cuts, cuts[1:]))
    print(f"{name}: {len(lengths)} shots, {dur:.2f}s")
    print("cuts:", " ".join(f"{c:.2f}" for c in cuts))
    print(f"shot length: min {lengths[0]:.2f}  median {lengths[len(lengths) // 2]:.2f}  max {lengths[-1]:.2f}")


if __name__ == "__main__":
    main()
