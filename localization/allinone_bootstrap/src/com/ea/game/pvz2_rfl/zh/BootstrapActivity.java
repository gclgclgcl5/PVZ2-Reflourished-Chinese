package com.ea.game.pvz2_rfl.zh;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.AssetManager;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * First-launch extractor: copies embedded OBB + CDN LawnStrings from assets,
 * then starts the real game activity.
 */
public class BootstrapActivity extends Activity {
    private static final String PREFS = "pvz2_zh_allinone";
    private static final String KEY_VERSION = "payload_version";
    private static final String ASSET_VERSION = "pvz2_zh_payload.version";
    private static final String ASSET_OBB = "obb/main.675.com.ea.game.pvz2_rfl.obb";
    private static final String ASSET_RTON = "cdn/LawnStrings-en-us.rton";
    private static final String OBB_NAME = "main.675.com.ea.game.pvz2_rfl.obb";
    /** Must match OBBHelperJ.currentVersion or the game shows the OBB download UI. */
    private static final String OBB_VERSION_NAME = "obbVersion";
    private static final String OBB_VERSION_VALUE = "1.4.2-r01";
    private static final String[] CDN_NAMES = {
            "LawnStrings-en-us.rton",
            "LawnStrings-zh-cn.rton",
            "LawnStrings-zh-hans.rton",
            "LawnStrings-zh-tw.rton"
    };
    private static final String GAME_ACTIVITY = "com.popcap.PvZ2.PvZ2GameActivity";
    private static final int BUF = 8 * 1024 * 1024;

    private TextView titleView;
    private TextView statusView;
    private ProgressBar progressBar;
    private final Handler ui = new Handler(Looper.getMainLooper());
    private boolean started;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        buildUi();
        new Thread(new Runnable() {
            @Override
            public void run() {
                runBootstrap();
            }
        }, "zh-bootstrap").start();
    }

    private void buildUi() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setBackgroundColor(Color.parseColor("#1A1A1A"));
        int pad = dp(24);
        root.setPadding(pad, pad, pad, pad);

        titleView = new TextView(this);
        titleView.setText("植物大战僵尸2：返茂 · 汉化包");
        titleView.setTextColor(Color.WHITE);
        titleView.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20);
        titleView.setGravity(Gravity.CENTER);
        root.addView(titleView, lp());

        statusView = new TextView(this);
        statusView.setText("正在检查数据…");
        statusView.setTextColor(Color.parseColor("#CCCCCC"));
        statusView.setTextSize(TypedValue.COMPLEX_UNIT_SP, 14);
        statusView.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams sp = lp();
        sp.topMargin = dp(16);
        root.addView(statusView, sp);

        progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progressBar.setMax(1000);
        progressBar.setProgress(0);
        LinearLayout.LayoutParams pp = lp();
        pp.topMargin = dp(20);
        pp.width = ViewGroup.LayoutParams.MATCH_PARENT;
        root.addView(progressBar, pp);

        setContentView(root);
    }

    private static LinearLayout.LayoutParams lp() {
        return new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    private int dp(int v) {
        float d = getResources().getDisplayMetrics().density;
        return (int) (v * d + 0.5f);
    }

    private void runBootstrap() {
        try {
            String version = readAssetText(ASSET_VERSION).trim();
            if (version.isEmpty()) {
                version = "unknown";
            }
            File obbDir = getObbDir();
            if (obbDir == null) {
                fail("无法访问 OBB 目录");
                return;
            }
            File obbFile = new File(obbDir, OBB_NAME);
            File obbVersionFile = new File(obbDir, OBB_VERSION_NAME);
            File filesDir = getExternalFilesDir(null);
            if (filesDir == null) {
                fail("无法访问应用文件目录");
                return;
            }
            File cdnDir = new File(filesDir, "No_Backup/CDN.1.4.2");
            File primaryRton = new File(cdnDir, CDN_NAMES[0]);

            long expectedObb = assetSize(ASSET_OBB);
            SharedPreferences prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
            String installed = prefs.getString(KEY_VERSION, "");
            boolean ready = version.equals(installed)
                    && obbFile.isFile()
                    && obbFile.length() == expectedObb
                    && primaryRton.isFile()
                    && primaryRton.length() > 0
                    && OBB_VERSION_VALUE.equals(readTextFile(obbVersionFile));

            if (ready) {
                setStatus("数据已就绪，正在启动…", 1000);
                launchGame();
                return;
            }

            if (!obbDir.exists() && !obbDir.mkdirs()) {
                fail("无法创建 OBB 目录");
                return;
            }
            if (!cdnDir.exists() && !cdnDir.mkdirs()) {
                fail("无法创建 CDN 目录");
                return;
            }

            long rtonSize = assetSize(ASSET_RTON);
            boolean needObb = !(obbFile.isFile() && obbFile.length() == expectedObb);
            long total = (needObb ? expectedObb : 0) + rtonSize;
            if (total <= 0) {
                total = 1;
            }
            long[] done = {0};

            if (needObb) {
                setStatus("正在释放游戏数据包（约 " + mb(expectedObb) + " MB）…", 0);
                copyAsset(ASSET_OBB, obbFile, expectedObb, done, total, "数据包");
            }

            // OBBHelper.compareVersioning requires this before first game launch.
            writeTextFile(obbVersionFile, OBB_VERSION_VALUE);

            setStatus("正在写入中文文案…", progressOf(done[0], total));
            File finalRton = new File(cdnDir, CDN_NAMES[0]);
            if (!(finalRton.isFile() && finalRton.length() == rtonSize)) {
                copyAsset(ASSET_RTON, finalRton, rtonSize, done, total, "文案");
            } else {
                done[0] += rtonSize;
            }
            for (int i = 1; i < CDN_NAMES.length; i++) {
                copyFile(finalRton, new File(cdnDir, CDN_NAMES[i]));
            }

            prefs.edit().putString(KEY_VERSION, version).commit();
            setStatus("准备完成，正在启动…", 1000);
            launchGame();
        } catch (Throwable t) {
            fail("释放失败：" + t.getMessage());
        }
    }

    private void copyAsset(String assetPath, File dest, long expectedSize,
                           long[] done, long total, String label) throws Exception {
        File tmp = new File(dest.getAbsolutePath() + ".tmp");
        if (tmp.exists()) {
            //noinspection ResultOfMethodCallIgnored
            tmp.delete();
        }
        AssetManager am = getAssets();
        try (InputStream in = am.open(assetPath);
             OutputStream out = new FileOutputStream(tmp)) {
            byte[] buf = new byte[BUF];
            long written = 0;
            int n;
            long lastUi = 0;
            while ((n = in.read(buf)) >= 0) {
                if (n == 0) {
                    continue;
                }
                out.write(buf, 0, n);
                written += n;
                done[0] += n;
                long now = System.currentTimeMillis();
                if (now - lastUi > 200) {
                    lastUi = now;
                    final int p = progressOf(done[0], total);
                    final String msg = "正在释放" + label + "… "
                            + mb(written) + " / " + mb(expectedSize) + " MB";
                    setStatus(msg, p);
                }
            }
            out.flush();
            if (expectedSize > 0 && written != expectedSize) {
                throw new IllegalStateException(label + " 大小不匹配：" + written + " != " + expectedSize);
            }
        }
        if (dest.exists() && !dest.delete()) {
            throw new IllegalStateException("无法覆盖已有文件：" + dest.getName());
        }
        if (!tmp.renameTo(dest)) {
            copyFile(tmp, dest);
            //noinspection ResultOfMethodCallIgnored
            tmp.delete();
        }
        if (expectedSize > 0 && dest.length() != expectedSize) {
            throw new IllegalStateException(label + " 落盘校验失败");
        }
    }

    private static void copyFile(File src, File dest) throws Exception {
        File tmp = new File(dest.getAbsolutePath() + ".tmp");
        try (InputStream in = new java.io.FileInputStream(src);
             OutputStream out = new FileOutputStream(tmp)) {
            byte[] buf = new byte[BUF];
            int n;
            while ((n = in.read(buf)) > 0) {
                out.write(buf, 0, n);
            }
            out.flush();
        }
        if (dest.exists()) {
            //noinspection ResultOfMethodCallIgnored
            dest.delete();
        }
        if (!tmp.renameTo(dest)) {
            throw new IllegalStateException("无法写入 " + dest.getName());
        }
    }

    private long assetSize(String path) throws Exception {
        try {
            android.content.res.AssetFileDescriptor fd = getAssets().openFd(path);
            try {
                long len = fd.getLength();
                if (len > 0 && len != android.content.res.AssetFileDescriptor.UNKNOWN_LENGTH) {
                    return len;
                }
            } finally {
                fd.close();
            }
        } catch (Exception ignored) {
            // Compressed or unavailable — count stream
        }
        long n = 0;
        try (InputStream in = getAssets().open(path)) {
            byte[] buf = new byte[BUF];
            int r;
            while ((r = in.read(buf)) > 0) {
                n += r;
            }
        }
        return n;
    }

    private String readAssetText(String path) throws Exception {
        try (InputStream in = getAssets().open(path)) {
            byte[] buf = new byte[4096];
            int n = in.read(buf);
            if (n <= 0) {
                return "";
            }
            return new String(buf, 0, n, "UTF-8");
        }
    }

    private static String readTextFile(File file) {
        if (file == null || !file.isFile()) {
            return "";
        }
        try (InputStream in = new java.io.FileInputStream(file)) {
            byte[] buf = new byte[64];
            int n = in.read(buf);
            if (n <= 0) {
                return "";
            }
            return new String(buf, 0, n, "UTF-8").trim();
        } catch (Exception e) {
            return "";
        }
    }

    private static void writeTextFile(File dest, String text) throws Exception {
        File tmp = new File(dest.getAbsolutePath() + ".tmp");
        byte[] data = text.getBytes("UTF-8");
        try (OutputStream out = new FileOutputStream(tmp)) {
            out.write(data);
            out.flush();
        }
        if (dest.exists() && !dest.delete()) {
            throw new IllegalStateException("无法更新 " + dest.getName());
        }
        if (!tmp.renameTo(dest)) {
            copyFile(tmp, dest);
            //noinspection ResultOfMethodCallIgnored
            tmp.delete();
        }
        if (!text.equals(readTextFile(dest))) {
            throw new IllegalStateException(dest.getName() + " 写入校验失败");
        }
    }

    private static int progressOf(long done, long total) {
        if (total <= 0) {
            return 0;
        }
        long p = done * 1000L / total;
        if (p > 1000) {
            p = 1000;
        }
        return (int) p;
    }

    private static String mb(long bytes) {
        return String.valueOf(Math.max(0, bytes / (1024L * 1024L)));
    }

    private void setStatus(final String msg, final int progress) {
        ui.post(new Runnable() {
            @Override
            public void run() {
                statusView.setText(msg);
                progressBar.setProgress(progress);
            }
        });
    }

    private void fail(final String msg) {
        ui.post(new Runnable() {
            @Override
            public void run() {
                statusView.setText(msg);
                Toast.makeText(BootstrapActivity.this, msg, Toast.LENGTH_LONG).show();
            }
        });
    }

    private void launchGame() {
        ui.post(new Runnable() {
            @Override
            public void run() {
                if (started) {
                    return;
                }
                started = true;
                try {
                    Intent i = new Intent();
                    i.setClassName(BootstrapActivity.this, GAME_ACTIVITY);
                    i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
                    startActivity(i);
                    finish();
                } catch (Throwable t) {
                    statusView.setText("无法启动游戏：" + t.getMessage());
                }
            }
        });
    }
}
