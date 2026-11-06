#!/usr/bin/env python3
"""Minimal GUI for reproduce_zh (OBB) and reproduce_zh_apk (APK).

Requires: Python 3.10+ tkinter, zstandard; APK path also needs apktool/JDK/SDK.
"""
from __future__ import annotations

import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from apk_toolchain import check_apk_deps  # noqa: E402
from obb_layout_142 import OBB_NAME  # noqa: E402
from reproduce_zh import reproduce as reproduce_obb  # noqa: E402
from reproduce_zh_apk import ZH_APK_NAME  # noqa: E402
from reproduce_zh_apk import reproduce as reproduce_apk  # noqa: E402

DEFAULT_OUT = Path(r"F:\sen_work\out_reproduce_zh")


class _QueueWriter:
    def __init__(self, q: queue.Queue[str]) -> None:
        self._q = q

    def write(self, s: str) -> int:
        if s:
            self._q.put(s)
        return len(s)

    def flush(self) -> None:
        pass


class ReproduceApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PvZ2 1.4.2 一键复刻（OBB + APK）")
        self.geometry("800x640")
        self.minsize(660, 500)

        self._log_q: queue.Queue[str] = queue.Queue()
        self._worker: threading.Thread | None = None
        self._busy = False

        self.obb_var = tk.StringVar()
        self.apk_var = tk.StringVar()
        self.out_var = tk.StringVar(
            value=str(DEFAULT_OUT if DEFAULT_OUT.parent.is_dir() else Path.cwd() / "out_zh")
        )

        self._build()
        self.after(100, self._drain_log)
        self.after(200, self._show_dep_hints)

    def _build(self) -> None:
        pad = {"padx": 10, "pady": 4}
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="输出目录（OBB / APK 共用）").grid(
            row=0, column=0, sticky=tk.W, **pad
        )
        ttk.Entry(frm, textvariable=self.out_var).grid(
            row=0, column=1, sticky=tk.EW, **pad
        )
        ttk.Button(frm, text="浏览…", command=self._browse_out).grid(
            row=0, column=2, **pad
        )

        ttk.Separator(frm, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=3, sticky=tk.EW, pady=6
        )

        ttk.Label(frm, text="OBB：原版 → 汉化 OBB + CDN RTON").grid(
            row=2, column=0, columnspan=3, sticky=tk.W, **pad
        )
        ttk.Label(frm, text="原版 OBB").grid(row=3, column=0, sticky=tk.W, **pad)
        ttk.Entry(frm, textvariable=self.obb_var).grid(
            row=3, column=1, sticky=tk.EW, **pad
        )
        ttk.Button(frm, text="浏览…", command=self._browse_obb).grid(
            row=3, column=2, **pad
        )

        obb_btns = ttk.Frame(frm)
        obb_btns.grid(row=4, column=0, columnspan=3, sticky=tk.W, **pad)
        self.obb_btn = ttk.Button(obb_btns, text="开始复刻 OBB", command=self._start_obb)
        self.obb_btn.pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(obb_btns, text="复制 OBB/CDN adb", command=self._copy_adb_obb).pack(
            side=tk.LEFT
        )

        ttk.Separator(frm, orient=tk.HORIZONTAL).grid(
            row=5, column=0, columnspan=3, sticky=tk.EW, pady=6
        )

        ttk.Label(frm, text="APK：原版 → CDN skip + Glyph 重签（需 apktool/JDK/SDK）").grid(
            row=6, column=0, columnspan=3, sticky=tk.W, **pad
        )
        ttk.Label(frm, text="原版 APK").grid(row=7, column=0, sticky=tk.W, **pad)
        ttk.Entry(frm, textvariable=self.apk_var).grid(
            row=7, column=1, sticky=tk.EW, **pad
        )
        ttk.Button(frm, text="浏览…", command=self._browse_apk).grid(
            row=7, column=2, **pad
        )

        apk_btns = ttk.Frame(frm)
        apk_btns.grid(row=8, column=0, columnspan=3, sticky=tk.W, **pad)
        self.apk_btn = ttk.Button(apk_btns, text="开始打 APK", command=self._start_apk)
        self.apk_btn.pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(apk_btns, text="复制 adb install", command=self._copy_adb_apk).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        self.open_btn = ttk.Button(
            apk_btns, text="打开输出目录", command=self._open_out, state=tk.DISABLED
        )
        self.open_btn.pack(side=tk.LEFT)

        ttk.Label(frm, text="日志").grid(row=9, column=0, sticky=tk.NW, **pad)
        self.log = scrolledtext.ScrolledText(
            frm, height=18, wrap=tk.WORD, state=tk.DISABLED
        )
        self.log.grid(row=10, column=0, columnspan=3, sticky=tk.NSEW, **pad)

        tip = (
            "完整三件套 = 汉化 APK + 汉化 OBB + LawnStrings-en-us.rton。"
            "换签名后需先卸载旧包；单体 all-in-one 不在此窗口。"
        )
        ttk.Label(frm, text=tip, wraplength=740).grid(
            row=11, column=0, columnspan=3, sticky=tk.W, **pad
        )

        frm.columnconfigure(1, weight=1)
        frm.rowconfigure(10, weight=1)

    def _show_dep_hints(self) -> None:
        msgs = check_apk_deps()
        if msgs:
            self._append_log("[APK 依赖提示 — 不影响只跑 OBB]\n")
            for m in msgs:
                self._append_log(f"  - {m}\n")
            self._append_log("\n")
        else:
            self._append_log("[APK 依赖：apktool / keytool / build-tools 已就绪]\n\n")

    def _browse_obb(self) -> None:
        path = filedialog.askopenfilename(
            title="选择原版 OBB",
            filetypes=[("OBB", "*.obb"), ("All", "*.*")],
        )
        if path:
            self.obb_var.set(path)

    def _browse_apk(self) -> None:
        path = filedialog.askopenfilename(
            title="选择原版 APK",
            filetypes=[("APK", "*.apk"), ("All", "*.*")],
        )
        if path:
            self.apk_var.set(path)

    def _browse_out(self) -> None:
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.out_var.set(path)

    def _append_log(self, text: str) -> None:
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, text)
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _drain_log(self) -> None:
        try:
            while True:
                self._append_log(self._log_q.get_nowait())
        except queue.Empty:
            pass
        self.after(100, self._drain_log)

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        state = tk.DISABLED if busy else tk.NORMAL
        self.obb_btn.configure(state=state)
        self.apk_btn.configure(state=state)

    def _run_job(self, label: str, fn) -> None:
        if self._busy:
            return
        out_dir = Path(self.out_var.get().strip())
        if not self.out_var.get().strip():
            messagebox.showerror("错误", "请填写输出目录")
            return

        self.log.configure(state=tk.NORMAL)
        self.log.delete("1.0", tk.END)
        self.log.configure(state=tk.DISABLED)
        self.open_btn.configure(state=tk.DISABLED)
        self._set_busy(True)
        self._append_log(f"{label}\nOUT: {out_dir}\n\n")

        def work() -> None:
            writer = _QueueWriter(self._log_q)
            old_out, old_err = sys.stdout, sys.stderr
            sys.stdout = sys.stderr = writer  # type: ignore[assignment]
            err: BaseException | None = None
            try:
                fn(out_dir)
            except BaseException as e:
                err = e
                print(f"\nFAILED: {e}")
            finally:
                sys.stdout, sys.stderr = old_out, old_err
                self.after(0, lambda: self._on_done(err, out_dir))

        self._worker = threading.Thread(target=work, daemon=True)
        self._worker.start()

    def _start_obb(self) -> None:
        obb = Path(self.obb_var.get().strip())
        if not obb.is_file():
            messagebox.showerror("错误", f"找不到 OBB：\n{obb}")
            return

        def job(out_dir: Path) -> None:
            reproduce_obb(obb, out_dir)

        self._run_job(f"OBB: {obb}", job)

    def _start_apk(self) -> None:
        apk = Path(self.apk_var.get().strip())
        if not apk.is_file():
            messagebox.showerror("错误", f"找不到 APK：\n{apk}")
            return

        def job(out_dir: Path) -> None:
            reproduce_apk(apk, out_dir)

        self._run_job(f"APK: {apk}", job)

    def _on_done(self, err: BaseException | None, out_dir: Path) -> None:
        self._set_busy(False)
        if err is None:
            self.open_btn.configure(state=tk.NORMAL)
            messagebox.showinfo("完成", f"已写出到：\n{out_dir}")
        else:
            messagebox.showerror("失败", str(err))

    def _open_out(self) -> None:
        out_dir = Path(self.out_var.get().strip())
        if not out_dir.is_dir():
            messagebox.showwarning("提示", f"目录不存在：\n{out_dir}")
            return
        if sys.platform == "win32":
            subprocess.Popen(["explorer", str(out_dir)])
        else:
            subprocess.Popen(["xdg-open", str(out_dir)])

    def _copy_adb_obb(self) -> None:
        out_dir = Path(self.out_var.get().strip())
        obb = out_dir / OBB_NAME
        rton = out_dir / "LawnStrings-en-us.rton"
        ver = out_dir / "obbVersion"
        pkg = "com.ea.game.pvz2_rfl"
        text = "\n".join(
            [
                f'adb push "{obb}" /sdcard/Android/obb/{pkg}/{OBB_NAME}',
                f'adb push "{ver}" /sdcard/Android/obb/{pkg}/obbVersion',
                f'adb push "{rton}" /sdcard/Android/data/{pkg}/files/No_Backup/CDN.1.4.2/LawnStrings-en-us.rton',
            ]
        )
        self.clipboard_clear()
        self.clipboard_append(text)
        self._append_log("\n[已复制 OBB/CDN adb 到剪贴板]\n")

    def _copy_adb_apk(self) -> None:
        out_dir = Path(self.out_var.get().strip())
        apk = out_dir / ZH_APK_NAME
        text = "\n".join(
            [
                "# 若签名不同，先卸载旧包：",
                "adb uninstall com.ea.game.pvz2_rfl",
                f'adb install -r "{apk}"',
            ]
        )
        self.clipboard_clear()
        self.clipboard_append(text)
        self._append_log("\n[已复制 adb install 到剪贴板]\n")


def main() -> None:
    app = ReproduceApp()
    app.mainloop()


if __name__ == "__main__":
    main()
