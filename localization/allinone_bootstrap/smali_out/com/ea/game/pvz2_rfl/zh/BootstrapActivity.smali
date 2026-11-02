.class public Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;
.super Landroid/app/Activity;
.source "BootstrapActivity.java"


# static fields
.field private static final ASSET_OBB:Ljava/lang/String; = "obb/main.675.com.ea.game.pvz2_rfl.obb"

.field private static final ASSET_RTON:Ljava/lang/String; = "cdn/LawnStrings-en-us.rton"

.field private static final ASSET_VERSION:Ljava/lang/String; = "pvz2_zh_payload.version"

.field private static final BUF:I = 0x800000

.field private static final CDN_NAMES:[Ljava/lang/String;

.field private static final GAME_ACTIVITY:Ljava/lang/String; = "com.popcap.PvZ2.PvZ2GameActivity"

.field private static final KEY_VERSION:Ljava/lang/String; = "payload_version"

.field private static final OBB_NAME:Ljava/lang/String; = "main.675.com.ea.game.pvz2_rfl.obb"

.field private static final OBB_VERSION_NAME:Ljava/lang/String; = "obbVersion"

.field private static final OBB_VERSION_VALUE:Ljava/lang/String; = "1.4.2-r01"

.field private static final PREFS:Ljava/lang/String; = "pvz2_zh_allinone"


# instance fields
.field private progressBar:Landroid/widget/ProgressBar;

.field private started:Z

.field private statusView:Landroid/widget/TextView;

.field private titleView:Landroid/widget/TextView;

.field private final ui:Landroid/os/Handler;


# direct methods
.method static constructor <clinit>()V
    .registers 4

    .line 38
    const-string v0, "LawnStrings-zh-hans.rton"

    const-string v1, "LawnStrings-zh-tw.rton"

    const-string v2, "LawnStrings-en-us.rton"

    const-string v3, "LawnStrings-zh-cn.rton"

    filled-new-array {v2, v3, v0, v1}, [Ljava/lang/String;

    move-result-object v0

    sput-object v0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->CDN_NAMES:[Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .registers 3

    .line 28
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 50
    new-instance v0, Landroid/os/Handler;

    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    move-result-object v1

    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    iput-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->ui:Landroid/os/Handler;

    return-void
.end method

.method static synthetic access$000(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)V
    .registers 1

    .line 28
    invoke-direct {p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->runBootstrap()V

    return-void
.end method

.method static synthetic access$100(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)Landroid/widget/TextView;
    .registers 1

    .line 28
    iget-object p0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;

    return-object p0
.end method

.method static synthetic access$200(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)Landroid/widget/ProgressBar;
    .registers 1

    .line 28
    iget-object p0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->progressBar:Landroid/widget/ProgressBar;

    return-object p0
.end method

.method static synthetic access$300(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)Z
    .registers 1

    .line 28
    iget-boolean p0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->started:Z

    return p0
.end method

.method static synthetic access$302(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;Z)Z
    .registers 2

    .line 28
    iput-boolean p1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->started:Z

    return p1
.end method

.method private assetSize(Ljava/lang/String;)J
    .registers 10
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 262
    const-wide/16 v0, 0x0

    :try_start_2
    invoke-virtual {p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v2

    invoke-virtual {v2, p1}, Landroid/content/res/AssetManager;->openFd(Ljava/lang/String;)Landroid/content/res/AssetFileDescriptor;

    move-result-object v2
    :try_end_a
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_a} :catch_27

    .line 264
    :try_start_a
    invoke-virtual {v2}, Landroid/content/res/AssetFileDescriptor;->getLength()J

    move-result-wide v3
    :try_end_e
    .catchall {:try_start_a .. :try_end_e} :catchall_22

    .line 265
    cmp-long v5, v3, v0

    if-lez v5, :cond_1d

    const-wide/16 v5, -0x1

    cmp-long v7, v3, v5

    if-eqz v7, :cond_1d

    .line 266
    nop

    .line 269
    :try_start_19
    invoke-virtual {v2}, Landroid/content/res/AssetFileDescriptor;->close()V

    .line 266
    return-wide v3

    .line 269
    :cond_1d
    invoke-virtual {v2}, Landroid/content/res/AssetFileDescriptor;->close()V

    .line 270
    nop

    .line 273
    goto :goto_28

    .line 269
    :catchall_22
    move-exception v3

    invoke-virtual {v2}, Landroid/content/res/AssetFileDescriptor;->close()V

    .line 270
    throw v3
    :try_end_27
    .catch Ljava/lang/Exception; {:try_start_19 .. :try_end_27} :catch_27

    .line 271
    :catch_27
    move-exception v2

    .line 274
    :goto_28
    nop

    .line 275
    invoke-virtual {p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v2

    invoke-virtual {v2, p1}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object p1

    .line 276
    const/high16 v2, 0x800000

    :try_start_33
    new-array v2, v2, [B

    .line 278
    :goto_35
    invoke-virtual {p1, v2}, Ljava/io/InputStream;->read([B)I

    move-result v3
    :try_end_39
    .catchall {:try_start_33 .. :try_end_39} :catchall_44

    if-lez v3, :cond_3e

    .line 279
    int-to-long v3, v3

    add-long/2addr v0, v3

    goto :goto_35

    .line 281
    :cond_3e
    if-eqz p1, :cond_43

    invoke-virtual {p1}, Ljava/io/InputStream;->close()V

    .line 282
    :cond_43
    return-wide v0

    .line 275
    :catchall_44
    move-exception v0

    if-eqz p1, :cond_4f

    :try_start_47
    invoke-virtual {p1}, Ljava/io/InputStream;->close()V
    :try_end_4a
    .catchall {:try_start_47 .. :try_end_4a} :catchall_4b

    goto :goto_4f

    :catchall_4b
    move-exception p1

    invoke-virtual {v0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_4f
    :goto_4f
    throw v0
.end method

.method private buildUi()V
    .registers 7

    .line 66
    new-instance v0, Landroid/widget/LinearLayout;

    invoke-direct {v0, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    .line 67
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setOrientation(I)V

    .line 68
    const/16 v1, 0x11

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setGravity(I)V

    .line 69
    const-string v2, "#1A1A1A"

    invoke-static {v2}, Landroid/graphics/Color;->parseColor(Ljava/lang/String;)I

    move-result v2

    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->setBackgroundColor(I)V

    .line 70
    const/16 v2, 0x18

    invoke-direct {p0, v2}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->dp(I)I

    move-result v2

    .line 71
    invoke-virtual {v0, v2, v2, v2, v2}, Landroid/widget/LinearLayout;->setPadding(IIII)V

    .line 73
    new-instance v2, Landroid/widget/TextView;

    invoke-direct {v2, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    iput-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->titleView:Landroid/widget/TextView;

    .line 74
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->titleView:Landroid/widget/TextView;

    const-string v3, "\u690d\u7269\u5927\u6218\u50f5\u5c382\uff1a\u8fd4\u8302 \u00b7 \u6c49\u5316\u5305"

    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 75
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->titleView:Landroid/widget/TextView;

    const/4 v3, -0x1

    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setTextColor(I)V

    .line 76
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->titleView:Landroid/widget/TextView;

    const/high16 v4, 0x41a00000    # 20.0f

    const/4 v5, 0x2

    invoke-virtual {v2, v5, v4}, Landroid/widget/TextView;->setTextSize(IF)V

    .line 77
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->titleView:Landroid/widget/TextView;

    invoke-virtual {v2, v1}, Landroid/widget/TextView;->setGravity(I)V

    .line 78
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->titleView:Landroid/widget/TextView;

    invoke-static {}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->lp()Landroid/widget/LinearLayout$LayoutParams;

    move-result-object v4

    invoke-virtual {v0, v2, v4}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 80
    new-instance v2, Landroid/widget/TextView;

    invoke-direct {v2, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    iput-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;

    .line 81
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;

    const-string v4, "\u6b63\u5728\u68c0\u67e5\u6570\u636e\u2026"

    invoke-virtual {v2, v4}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 82
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;

    const-string v4, "#CCCCCC"

    invoke-static {v4}, Landroid/graphics/Color;->parseColor(Ljava/lang/String;)I

    move-result v4

    invoke-virtual {v2, v4}, Landroid/widget/TextView;->setTextColor(I)V

    .line 83
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;

    const/high16 v4, 0x41600000    # 14.0f

    invoke-virtual {v2, v5, v4}, Landroid/widget/TextView;->setTextSize(IF)V

    .line 84
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;

    invoke-virtual {v2, v1}, Landroid/widget/TextView;->setGravity(I)V

    .line 85
    invoke-static {}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->lp()Landroid/widget/LinearLayout$LayoutParams;

    move-result-object v1

    .line 86
    const/16 v2, 0x10

    invoke-direct {p0, v2}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->dp(I)I

    move-result v2

    iput v2, v1, Landroid/widget/LinearLayout$LayoutParams;->topMargin:I

    .line 87
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;

    invoke-virtual {v0, v2, v1}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 89
    new-instance v1, Landroid/widget/ProgressBar;

    const/4 v2, 0x0

    const v4, 0x1010078

    invoke-direct {v1, p0, v2, v4}, Landroid/widget/ProgressBar;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;I)V

    iput-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->progressBar:Landroid/widget/ProgressBar;

    .line 90
    iget-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->progressBar:Landroid/widget/ProgressBar;

    const/16 v2, 0x3e8

    invoke-virtual {v1, v2}, Landroid/widget/ProgressBar;->setMax(I)V

    .line 91
    iget-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->progressBar:Landroid/widget/ProgressBar;

    const/4 v2, 0x0

    invoke-virtual {v1, v2}, Landroid/widget/ProgressBar;->setProgress(I)V

    .line 92
    invoke-static {}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->lp()Landroid/widget/LinearLayout$LayoutParams;

    move-result-object v1

    .line 93
    const/16 v2, 0x14

    invoke-direct {p0, v2}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->dp(I)I

    move-result v2

    iput v2, v1, Landroid/widget/LinearLayout$LayoutParams;->topMargin:I

    .line 94
    iput v3, v1, Landroid/widget/LinearLayout$LayoutParams;->width:I

    .line 95
    iget-object v2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->progressBar:Landroid/widget/ProgressBar;

    invoke-virtual {v0, v2, v1}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 97
    invoke-virtual {p0, v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->setContentView(Landroid/view/View;)V

    .line 98
    return-void
.end method

.method private copyAsset(Ljava/lang/String;Ljava/io/File;J[JJLjava/lang/String;)V
    .registers 29
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 194
    move-object/from16 v0, p2

    move-wide/from16 v1, p3

    move-object/from16 v3, p8

    new-instance v4, Ljava/io/File;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual/range {p2 .. p2}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, ".tmp"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-direct {v4, v5}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 195
    invoke-virtual {v4}, Ljava/io/File;->exists()Z

    move-result v5

    if-eqz v5, :cond_2b

    .line 197
    invoke-virtual {v4}, Ljava/io/File;->delete()Z

    .line 199
    :cond_2b
    invoke-virtual/range {p0 .. p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v5

    .line 200
    move-object/from16 v6, p1

    invoke-virtual {v5, v6}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v5

    .line 201
    :try_start_35
    new-instance v6, Ljava/io/FileOutputStream;

    invoke-direct {v6, v4}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    :try_end_3a
    .catchall {:try_start_35 .. :try_end_3a} :catchall_15b

    .line 202
    const/high16 v7, 0x800000

    :try_start_3c
    new-array v7, v7, [B

    .line 203
    nop

    .line 205
    const-wide/16 v10, 0x0

    const-wide/16 v12, 0x0

    .line 206
    :goto_43
    invoke-virtual {v5, v7}, Ljava/io/InputStream;->read([B)I

    move-result v14

    if-ltz v14, :cond_b7

    .line 207
    if-nez v14, :cond_4c

    .line 208
    goto :goto_43

    .line 210
    :cond_4c
    const/4 v15, 0x0

    invoke-virtual {v6, v7, v15, v14}, Ljava/io/OutputStream;->write([BII)V

    .line 211
    int-to-long v8, v14

    add-long/2addr v10, v8

    .line 212
    aget-wide v16, p5, v15

    add-long v16, v16, v8

    aput-wide v16, p5, v15

    .line 213
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v8
    :try_end_5c
    .catchall {:try_start_3c .. :try_end_5c} :catchall_14f

    .line 214
    sub-long v16, v8, v12

    const-wide/16 v18, 0xc8

    cmp-long v14, v16, v18

    if-lez v14, :cond_b0

    .line 215
    nop

    .line 216
    :try_start_65
    aget-wide v12, p5, v15

    move-wide/from16 v14, p6

    invoke-static {v12, v13, v14, v15}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->progressOf(JJ)I

    move-result v12

    .line 217
    new-instance v13, Ljava/lang/StringBuilder;

    invoke-direct {v13}, Ljava/lang/StringBuilder;-><init>()V

    move-object/from16 v16, v7

    const-string v7, "\u6b63\u5728\u91ca\u653e"

    invoke-virtual {v13, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    const-string v13, "\u2026 "

    invoke-virtual {v7, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    .line 218
    invoke-static {v10, v11}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->mb(J)Ljava/lang/String;

    move-result-object v13

    invoke-virtual {v7, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    const-string v13, " / "

    invoke-virtual {v7, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-static/range {p3 .. p4}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->mb(J)Ljava/lang/String;

    move-result-object v13

    invoke-virtual {v7, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    const-string v13, " MB"

    invoke-virtual {v7, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7
    :try_end_a4
    .catchall {:try_start_65 .. :try_end_a4} :catchall_ab

    .line 219
    move-object/from16 v13, p0

    :try_start_a6
    invoke-direct {v13, v7, v12}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->setStatus(Ljava/lang/String;I)V

    move-wide v12, v8

    goto :goto_b4

    .line 200
    :catchall_ab
    move-exception v0

    move-object/from16 v13, p0

    goto/16 :goto_150

    .line 214
    :cond_b0
    move-wide/from16 v14, p6

    move-object/from16 v16, v7

    .line 221
    :goto_b4
    move-object/from16 v7, v16

    goto :goto_43

    .line 222
    :cond_b7
    invoke-virtual {v6}, Ljava/io/OutputStream;->flush()V

    .line 223
    const-wide/16 v7, 0x0

    cmp-long v9, v1, v7

    if-lez v9, :cond_ec

    cmp-long v7, v10, v1

    if-nez v7, :cond_c5

    goto :goto_ec

    .line 224
    :cond_c5
    new-instance v0, Ljava/lang/IllegalStateException;

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v4, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, " \u5927\u5c0f\u4e0d\u5339\u914d\uff1a"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3, v10, v11}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, " != "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3, v1, v2}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_ec
    .catchall {:try_start_a6 .. :try_end_ec} :catchall_14f

    .line 226
    :cond_ec
    :goto_ec
    :try_start_ec
    invoke-virtual {v6}, Ljava/io/OutputStream;->close()V
    :try_end_ef
    .catchall {:try_start_ec .. :try_end_ef} :catchall_15b

    if-eqz v5, :cond_f4

    invoke-virtual {v5}, Ljava/io/InputStream;->close()V

    .line 227
    :cond_f4
    invoke-virtual/range {p2 .. p2}, Ljava/io/File;->exists()Z

    move-result v5

    if-eqz v5, :cond_11e

    invoke-virtual/range {p2 .. p2}, Ljava/io/File;->delete()Z

    move-result v5

    if-eqz v5, :cond_101

    goto :goto_11e

    .line 228
    :cond_101
    new-instance v1, Ljava/lang/IllegalStateException;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "\u65e0\u6cd5\u8986\u76d6\u5df2\u6709\u6587\u4ef6\uff1a"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual/range {p2 .. p2}, Ljava/io/File;->getName()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v1, v0}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    throw v1

    .line 230
    :cond_11e
    :goto_11e
    invoke-virtual {v4, v0}, Ljava/io/File;->renameTo(Ljava/io/File;)Z

    move-result v5

    if-nez v5, :cond_12a

    .line 231
    invoke-static {v4, v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->copyFile(Ljava/io/File;Ljava/io/File;)V

    .line 233
    invoke-virtual {v4}, Ljava/io/File;->delete()Z

    .line 235
    :cond_12a
    if-lez v9, :cond_14e

    invoke-virtual/range {p2 .. p2}, Ljava/io/File;->length()J

    move-result-wide v4

    cmp-long v0, v4, v1

    if-nez v0, :cond_135

    goto :goto_14e

    .line 236
    :cond_135
    new-instance v0, Ljava/lang/IllegalStateException;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, " \u843d\u76d8\u6821\u9a8c\u5931\u8d25"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 238
    :cond_14e
    :goto_14e
    return-void

    .line 200
    :catchall_14f
    move-exception v0

    :goto_150
    move-object v1, v0

    :try_start_151
    invoke-virtual {v6}, Ljava/io/OutputStream;->close()V
    :try_end_154
    .catchall {:try_start_151 .. :try_end_154} :catchall_155

    goto :goto_15a

    :catchall_155
    move-exception v0

    move-object v2, v0

    :try_start_157
    invoke-virtual {v1, v2}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_15a
    throw v1
    :try_end_15b
    .catchall {:try_start_157 .. :try_end_15b} :catchall_15b

    :catchall_15b
    move-exception v0

    move-object v1, v0

    if-eqz v5, :cond_168

    :try_start_15f
    invoke-virtual {v5}, Ljava/io/InputStream;->close()V
    :try_end_162
    .catchall {:try_start_15f .. :try_end_162} :catchall_163

    goto :goto_168

    :catchall_163
    move-exception v0

    move-object v2, v0

    invoke-virtual {v1, v2}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_168
    :goto_168
    throw v1
.end method

.method private static copyFile(Ljava/io/File;Ljava/io/File;)V
    .registers 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 241
    new-instance v0, Ljava/io/File;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {p1}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ".tmp"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 242
    new-instance v1, Ljava/io/FileInputStream;

    invoke-direct {v1, p0}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    .line 243
    :try_start_21
    new-instance p0, Ljava/io/FileOutputStream;

    invoke-direct {p0, v0}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    :try_end_26
    .catchall {:try_start_21 .. :try_end_26} :catchall_75

    .line 244
    const/high16 v2, 0x800000

    :try_start_28
    new-array v2, v2, [B

    .line 246
    :goto_2a
    invoke-virtual {v1, v2}, Ljava/io/InputStream;->read([B)I

    move-result v3

    if-lez v3, :cond_35

    .line 247
    const/4 v4, 0x0

    invoke-virtual {p0, v2, v4, v3}, Ljava/io/OutputStream;->write([BII)V

    goto :goto_2a

    .line 249
    :cond_35
    invoke-virtual {p0}, Ljava/io/OutputStream;->flush()V
    :try_end_38
    .catchall {:try_start_28 .. :try_end_38} :catchall_6b

    .line 250
    :try_start_38
    invoke-virtual {p0}, Ljava/io/OutputStream;->close()V
    :try_end_3b
    .catchall {:try_start_38 .. :try_end_3b} :catchall_75

    invoke-virtual {v1}, Ljava/io/InputStream;->close()V

    .line 251
    invoke-virtual {p1}, Ljava/io/File;->exists()Z

    move-result p0

    if-eqz p0, :cond_47

    .line 253
    invoke-virtual {p1}, Ljava/io/File;->delete()Z

    .line 255
    :cond_47
    invoke-virtual {v0, p1}, Ljava/io/File;->renameTo(Ljava/io/File;)Z

    move-result p0

    if-eqz p0, :cond_4e

    .line 258
    return-void

    .line 256
    :cond_4e
    new-instance p0, Ljava/lang/IllegalStateException;

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "\u65e0\u6cd5\u5199\u5165 "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {p1}, Ljava/io/File;->getName()Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 242
    :catchall_6b
    move-exception p1

    :try_start_6c
    invoke-virtual {p0}, Ljava/io/OutputStream;->close()V
    :try_end_6f
    .catchall {:try_start_6c .. :try_end_6f} :catchall_70

    goto :goto_74

    :catchall_70
    move-exception p0

    :try_start_71
    invoke-virtual {p1, p0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_74
    throw p1
    :try_end_75
    .catchall {:try_start_71 .. :try_end_75} :catchall_75

    :catchall_75
    move-exception p0

    :try_start_76
    invoke-virtual {v1}, Ljava/io/InputStream;->close()V
    :try_end_79
    .catchall {:try_start_76 .. :try_end_79} :catchall_7a

    goto :goto_7e

    :catchall_7a
    move-exception p1

    invoke-virtual {p0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_7e
    throw p0
.end method

.method private dp(I)I
    .registers 3

    .line 107
    invoke-virtual {p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    invoke-virtual {v0}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object v0

    iget v0, v0, Landroid/util/DisplayMetrics;->density:F

    .line 108
    int-to-float p1, p1

    mul-float p1, p1, v0

    const/high16 v0, 0x3f000000    # 0.5f

    add-float/2addr p1, v0

    float-to-int p1, p1

    return p1
.end method

.method private fail(Ljava/lang/String;)V
    .registers 4

    .line 358
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->ui:Landroid/os/Handler;

    new-instance v1, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;

    invoke-direct {v1, p0, p1}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;-><init>(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 365
    return-void
.end method

.method private launchGame()V
    .registers 3

    .line 368
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->ui:Landroid/os/Handler;

    new-instance v1, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;

    invoke-direct {v1, p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;-><init>(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)V

    invoke-virtual {v0, v1}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 386
    return-void
.end method

.method private static lp()Landroid/widget/LinearLayout$LayoutParams;
    .registers 2

    .line 101
    new-instance v0, Landroid/widget/LinearLayout$LayoutParams;

    const/4 v1, -0x2

    invoke-direct {v0, v1, v1}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    return-object v0
.end method

.method private static mb(J)Ljava/lang/String;
    .registers 4

    .line 344
    const-wide/32 v0, 0x100000

    div-long/2addr p0, v0

    const-wide/16 v0, 0x0

    invoke-static {v0, v1, p0, p1}, Ljava/lang/Math;->max(JJ)J

    move-result-wide p0

    invoke-static {p0, p1}, Ljava/lang/String;->valueOf(J)Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method

.method private static progressOf(JJ)I
    .registers 7

    .line 333
    const-wide/16 v0, 0x0

    cmp-long v2, p2, v0

    if-gtz v2, :cond_8

    .line 334
    const/4 p0, 0x0

    return p0

    .line 336
    :cond_8
    const-wide/16 v0, 0x3e8

    mul-long p0, p0, v0

    div-long/2addr p0, p2

    .line 337
    cmp-long p2, p0, v0

    if-lez p2, :cond_12

    .line 338
    goto :goto_13

    .line 337
    :cond_12
    move-wide v0, p0

    .line 340
    :goto_13
    long-to-int p0, v0

    return p0
.end method

.method private readAssetText(Ljava/lang/String;)Ljava/lang/String;
    .registers 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 286
    invoke-virtual {p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v0

    invoke-virtual {v0, p1}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object p1

    .line 287
    const/16 v0, 0x1000

    :try_start_a
    new-array v0, v0, [B

    .line 288
    invoke-virtual {p1, v0}, Ljava/io/InputStream;->read([B)I

    move-result v1

    .line 289
    if-gtz v1, :cond_1a

    .line 290
    const-string v0, ""
    :try_end_14
    .catchall {:try_start_a .. :try_end_14} :catchall_28

    .line 293
    if-eqz p1, :cond_19

    invoke-virtual {p1}, Ljava/io/InputStream;->close()V

    .line 290
    :cond_19
    return-object v0

    .line 292
    :cond_1a
    :try_start_1a
    new-instance v2, Ljava/lang/String;

    const-string v3, "UTF-8"

    const/4 v4, 0x0

    invoke-direct {v2, v0, v4, v1, v3}, Ljava/lang/String;-><init>([BIILjava/lang/String;)V
    :try_end_22
    .catchall {:try_start_1a .. :try_end_22} :catchall_28

    .line 293
    if-eqz p1, :cond_27

    invoke-virtual {p1}, Ljava/io/InputStream;->close()V

    .line 292
    :cond_27
    return-object v2

    .line 286
    :catchall_28
    move-exception v0

    if-eqz p1, :cond_33

    :try_start_2b
    invoke-virtual {p1}, Ljava/io/InputStream;->close()V
    :try_end_2e
    .catchall {:try_start_2b .. :try_end_2e} :catchall_2f

    goto :goto_33

    :catchall_2f
    move-exception p1

    invoke-virtual {v0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_33
    :goto_33
    throw v0
.end method

.method private static readTextFile(Ljava/io/File;)Ljava/lang/String;
    .registers 7

    .line 297
    const-string v0, ""

    if-eqz p0, :cond_3b

    invoke-virtual {p0}, Ljava/io/File;->isFile()Z

    move-result v1

    if-nez v1, :cond_b

    goto :goto_3b

    .line 300
    :cond_b
    :try_start_b
    new-instance v1, Ljava/io/FileInputStream;

    invoke-direct {v1, p0}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V
    :try_end_10
    .catch Ljava/lang/Exception; {:try_start_b .. :try_end_10} :catch_39

    .line 301
    const/16 p0, 0x40

    :try_start_12
    new-array p0, p0, [B

    .line 302
    invoke-virtual {v1, p0}, Ljava/io/InputStream;->read([B)I

    move-result v2
    :try_end_18
    .catchall {:try_start_12 .. :try_end_18} :catchall_2f

    .line 303
    if-gtz v2, :cond_1f

    .line 304
    nop

    .line 307
    :try_start_1b
    invoke-virtual {v1}, Ljava/io/InputStream;->close()V
    :try_end_1e
    .catch Ljava/lang/Exception; {:try_start_1b .. :try_end_1e} :catch_39

    .line 304
    return-object v0

    .line 306
    :cond_1f
    :try_start_1f
    new-instance v3, Ljava/lang/String;

    const-string v4, "UTF-8"

    const/4 v5, 0x0

    invoke-direct {v3, p0, v5, v2, v4}, Ljava/lang/String;-><init>([BIILjava/lang/String;)V

    invoke-virtual {v3}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object p0
    :try_end_2b
    .catchall {:try_start_1f .. :try_end_2b} :catchall_2f

    .line 307
    :try_start_2b
    invoke-virtual {v1}, Ljava/io/InputStream;->close()V
    :try_end_2e
    .catch Ljava/lang/Exception; {:try_start_2b .. :try_end_2e} :catch_39

    .line 306
    return-object p0

    .line 300
    :catchall_2f
    move-exception p0

    :try_start_30
    invoke-virtual {v1}, Ljava/io/InputStream;->close()V
    :try_end_33
    .catchall {:try_start_30 .. :try_end_33} :catchall_34

    goto :goto_38

    :catchall_34
    move-exception v1

    :try_start_35
    invoke-virtual {p0, v1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_38
    throw p0
    :try_end_39
    .catch Ljava/lang/Exception; {:try_start_35 .. :try_end_39} :catch_39

    .line 307
    :catch_39
    move-exception p0

    .line 308
    return-object v0

    .line 298
    :cond_3b
    :goto_3b
    return-object v0
.end method

.method private runBootstrap()V
    .registers 24

    .line 113
    move-object/from16 v10, p0

    const-string v0, "payload_version"

    :try_start_4
    const-string v1, "pvz2_zh_payload.version"

    invoke-direct {v10, v1}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->readAssetText(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v1

    .line 114
    invoke-virtual {v1}, Ljava/lang/String;->isEmpty()Z

    move-result v2

    if-eqz v2, :cond_18

    .line 115
    const-string v1, "unknown"

    move-object v11, v1

    goto :goto_19

    .line 114
    :cond_18
    move-object v11, v1

    .line 117
    :goto_19
    invoke-virtual/range {p0 .. p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->getObbDir()Ljava/io/File;

    move-result-object v1

    .line 118
    if-nez v1, :cond_25

    .line 119
    const-string v0, "\u65e0\u6cd5\u8bbf\u95ee OBB \u76ee\u5f55"

    invoke-direct {v10, v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->fail(Ljava/lang/String;)V

    .line 120
    return-void

    .line 122
    :cond_25
    new-instance v3, Ljava/io/File;

    const-string v2, "main.675.com.ea.game.pvz2_rfl.obb"

    invoke-direct {v3, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 123
    new-instance v12, Ljava/io/File;

    const-string v2, "obbVersion"

    invoke-direct {v12, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 124
    const/4 v2, 0x0

    invoke-virtual {v10, v2}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    move-result-object v2

    .line 125
    if-nez v2, :cond_40

    .line 126
    const-string v0, "\u65e0\u6cd5\u8bbf\u95ee\u5e94\u7528\u6587\u4ef6\u76ee\u5f55"

    invoke-direct {v10, v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->fail(Ljava/lang/String;)V

    .line 127
    return-void

    .line 129
    :cond_40
    new-instance v13, Ljava/io/File;

    const-string v4, "No_Backup/CDN.1.4.2"

    invoke-direct {v13, v2, v4}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 130
    new-instance v2, Ljava/io/File;

    sget-object v4, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->CDN_NAMES:[Ljava/lang/String;

    const/4 v14, 0x0

    aget-object v4, v4, v14

    invoke-direct {v2, v13, v4}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 132
    const-string v4, "obb/main.675.com.ea.game.pvz2_rfl.obb"

    invoke-direct {v10, v4}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->assetSize(Ljava/lang/String;)J

    move-result-wide v4

    .line 133
    const-string v6, "pvz2_zh_allinone"

    invoke-virtual {v10, v6, v14}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v15

    .line 134
    const-string v6, ""

    invoke-interface {v15, v0, v6}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6

    .line 135
    invoke-virtual {v11, v6}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v6
    :try_end_67
    .catchall {:try_start_4 .. :try_end_67} :catchall_1a3

    const-string v9, "1.4.2-r01"

    const-wide/16 v7, 0x0

    const/4 v14, 0x1

    if-eqz v6, :cond_96

    .line 136
    :try_start_6e
    invoke-virtual {v3}, Ljava/io/File;->isFile()Z

    move-result v6

    if-eqz v6, :cond_96

    .line 137
    invoke-virtual {v3}, Ljava/io/File;->length()J

    move-result-wide v17

    cmp-long v6, v17, v4

    if-nez v6, :cond_96

    .line 138
    invoke-virtual {v2}, Ljava/io/File;->isFile()Z

    move-result v6

    if-eqz v6, :cond_96

    .line 139
    invoke-virtual {v2}, Ljava/io/File;->length()J

    move-result-wide v17

    cmp-long v2, v17, v7

    if-lez v2, :cond_96

    .line 140
    invoke-static {v12}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->readTextFile(Ljava/io/File;)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v9, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_96

    const/4 v2, 0x1

    goto :goto_97

    :cond_96
    const/4 v2, 0x0

    .line 142
    :goto_97
    const/16 v6, 0x3e8

    if-eqz v2, :cond_a4

    .line 143
    const-string v0, "\u6570\u636e\u5df2\u5c31\u7eea\uff0c\u6b63\u5728\u542f\u52a8\u2026"

    invoke-direct {v10, v0, v6}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->setStatus(Ljava/lang/String;I)V

    .line 144
    invoke-direct/range {p0 .. p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->launchGame()V

    .line 145
    return-void

    .line 148
    :cond_a4
    invoke-virtual {v1}, Ljava/io/File;->exists()Z

    move-result v2

    if-nez v2, :cond_b6

    invoke-virtual {v1}, Ljava/io/File;->mkdirs()Z

    move-result v1

    if-nez v1, :cond_b6

    .line 149
    const-string v0, "\u65e0\u6cd5\u521b\u5efa OBB \u76ee\u5f55"

    invoke-direct {v10, v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->fail(Ljava/lang/String;)V

    .line 150
    return-void

    .line 152
    :cond_b6
    invoke-virtual {v13}, Ljava/io/File;->exists()Z

    move-result v1

    if-nez v1, :cond_c8

    invoke-virtual {v13}, Ljava/io/File;->mkdirs()Z

    move-result v1

    if-nez v1, :cond_c8

    .line 153
    const-string v0, "\u65e0\u6cd5\u521b\u5efa CDN \u76ee\u5f55"

    invoke-direct {v10, v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->fail(Ljava/lang/String;)V

    .line 154
    return-void

    .line 157
    :cond_c8
    const-string v1, "cdn/LawnStrings-en-us.rton"

    invoke-direct {v10, v1}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->assetSize(Ljava/lang/String;)J

    move-result-wide v17

    .line 158
    invoke-virtual {v3}, Ljava/io/File;->isFile()Z

    move-result v1

    if-eqz v1, :cond_df

    invoke-virtual {v3}, Ljava/io/File;->length()J

    move-result-wide v1

    cmp-long v19, v1, v4

    if-eqz v19, :cond_dd

    goto :goto_df

    :cond_dd
    const/4 v1, 0x0

    goto :goto_e0

    :cond_df
    :goto_df
    const/4 v1, 0x1

    .line 159
    :goto_e0
    if-eqz v1, :cond_e5

    move-wide/from16 v19, v4

    goto :goto_e7

    :cond_e5
    move-wide/from16 v19, v7

    :goto_e7
    add-long v19, v19, v17

    .line 160
    cmp-long v2, v19, v7

    if-gtz v2, :cond_f2

    .line 161
    const-wide/16 v19, 0x1

    move-wide/from16 v21, v19

    goto :goto_f4

    .line 160
    :cond_f2
    move-wide/from16 v21, v19

    .line 163
    :goto_f4
    new-array v2, v14, [J

    const/16 v16, 0x0

    aput-wide v7, v2, v16

    .line 165
    if-eqz v1, :cond_135

    .line 166
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v7, "\u6b63\u5728\u91ca\u653e\u6e38\u620f\u6570\u636e\u5305\uff08\u7ea6 "

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-static {v4, v5}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->mb(J)Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v7, " MB\uff09\u2026"

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    const/4 v7, 0x0

    invoke-direct {v10, v1, v7}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->setStatus(Ljava/lang/String;I)V

    .line 167
    const-string v7, "obb/main.675.com.ea.game.pvz2_rfl.obb"

    const-string v19, "\u6570\u636e\u5305"

    move-object/from16 v1, p0

    move-object/from16 v20, v2

    move-object v2, v7

    const/16 v7, 0x3e8

    move-object/from16 v6, v20

    const/16 v14, 0x3e8

    move-wide/from16 v7, v21

    move-object v14, v9

    move-object/from16 v9, v19

    invoke-direct/range {v1 .. v9}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->copyAsset(Ljava/lang/String;Ljava/io/File;J[JJLjava/lang/String;)V

    goto :goto_138

    .line 165
    :cond_135
    move-object/from16 v20, v2

    move-object v14, v9

    .line 171
    :goto_138
    invoke-static {v12, v14}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->writeTextFile(Ljava/io/File;Ljava/lang/String;)V

    .line 173
    const-string v1, "\u6b63\u5728\u5199\u5165\u4e2d\u6587\u6587\u6848\u2026"

    const/4 v2, 0x0

    aget-wide v3, v20, v2

    move-wide/from16 v7, v21

    invoke-static {v3, v4, v7, v8}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->progressOf(JJ)I

    move-result v2

    invoke-direct {v10, v1, v2}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->setStatus(Ljava/lang/String;I)V

    .line 174
    new-instance v12, Ljava/io/File;

    sget-object v1, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->CDN_NAMES:[Ljava/lang/String;

    const/4 v2, 0x0

    aget-object v1, v1, v2

    invoke-direct {v12, v13, v1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 175
    invoke-virtual {v12}, Ljava/io/File;->isFile()Z

    move-result v1

    if-eqz v1, :cond_16a

    invoke-virtual {v12}, Ljava/io/File;->length()J

    move-result-wide v1

    cmp-long v3, v1, v17

    if-eqz v3, :cond_162

    goto :goto_16a

    .line 178
    :cond_162
    const/4 v1, 0x0

    aget-wide v2, v20, v1

    add-long v2, v2, v17

    aput-wide v2, v20, v1

    goto :goto_178

    .line 176
    :cond_16a
    :goto_16a
    const-string v2, "cdn/LawnStrings-en-us.rton"

    const-string v9, "\u6587\u6848"

    move-object/from16 v1, p0

    move-object v3, v12

    move-wide/from16 v4, v17

    move-object/from16 v6, v20

    invoke-direct/range {v1 .. v9}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->copyAsset(Ljava/lang/String;Ljava/io/File;J[JJLjava/lang/String;)V

    .line 180
    :goto_178
    const/4 v14, 0x1

    :goto_179
    sget-object v1, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->CDN_NAMES:[Ljava/lang/String;

    array-length v1, v1

    if-ge v14, v1, :cond_18d

    .line 181
    new-instance v1, Ljava/io/File;

    sget-object v2, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->CDN_NAMES:[Ljava/lang/String;

    aget-object v2, v2, v14

    invoke-direct {v1, v13, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-static {v12, v1}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->copyFile(Ljava/io/File;Ljava/io/File;)V

    .line 180
    add-int/lit8 v14, v14, 0x1

    goto :goto_179

    .line 184
    :cond_18d
    invoke-interface {v15}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v1

    invoke-interface {v1, v0, v11}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->commit()Z

    .line 185
    const-string v0, "\u51c6\u5907\u5b8c\u6210\uff0c\u6b63\u5728\u542f\u52a8\u2026"

    const/16 v1, 0x3e8

    invoke-direct {v10, v0, v1}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->setStatus(Ljava/lang/String;I)V

    .line 186
    invoke-direct/range {p0 .. p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->launchGame()V
    :try_end_1a2
    .catchall {:try_start_6e .. :try_end_1a2} :catchall_1a3

    .line 189
    goto :goto_1be

    .line 187
    :catchall_1a3
    move-exception v0

    .line 188
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "\u91ca\u653e\u5931\u8d25\uff1a"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v10, v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->fail(Ljava/lang/String;)V

    .line 190
    :goto_1be
    return-void
.end method

.method private setStatus(Ljava/lang/String;I)V
    .registers 5

    .line 348
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->ui:Landroid/os/Handler;

    new-instance v1, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;

    invoke-direct {v1, p0, p1, p2}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;-><init>(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;Ljava/lang/String;I)V

    invoke-virtual {v0, v1}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 355
    return-void
.end method

.method private static writeTextFile(Ljava/io/File;Ljava/lang/String;)V
    .registers 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 313
    new-instance v0, Ljava/io/File;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {p0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ".tmp"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 314
    const-string v1, "UTF-8"

    invoke-virtual {p1, v1}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B

    move-result-object v1

    .line 315
    new-instance v2, Ljava/io/FileOutputStream;

    invoke-direct {v2, v0}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    .line 316
    :try_start_27
    invoke-virtual {v2, v1}, Ljava/io/OutputStream;->write([B)V

    .line 317
    invoke-virtual {v2}, Ljava/io/OutputStream;->flush()V
    :try_end_2d
    .catchall {:try_start_27 .. :try_end_2d} :catchall_8e

    .line 318
    invoke-virtual {v2}, Ljava/io/OutputStream;->close()V

    .line 319
    invoke-virtual {p0}, Ljava/io/File;->exists()Z

    move-result v1

    if-eqz v1, :cond_5a

    invoke-virtual {p0}, Ljava/io/File;->delete()Z

    move-result v1

    if-eqz v1, :cond_3d

    goto :goto_5a

    .line 320
    :cond_3d
    new-instance p1, Ljava/lang/IllegalStateException;

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "\u65e0\u6cd5\u66f4\u65b0 "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {p0}, Ljava/io/File;->getName()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {p1, p0}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 322
    :cond_5a
    :goto_5a
    invoke-virtual {v0, p0}, Ljava/io/File;->renameTo(Ljava/io/File;)Z

    move-result v1

    if-nez v1, :cond_66

    .line 323
    invoke-static {v0, p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->copyFile(Ljava/io/File;Ljava/io/File;)V

    .line 325
    invoke-virtual {v0}, Ljava/io/File;->delete()Z

    .line 327
    :cond_66
    invoke-static {p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->readTextFile(Ljava/io/File;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_71

    .line 330
    return-void

    .line 328
    :cond_71
    new-instance p1, Ljava/lang/IllegalStateException;

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {p0}, Ljava/io/File;->getName()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string v0, " \u5199\u5165\u6821\u9a8c\u5931\u8d25"

    invoke-virtual {p0, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {p1, p0}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 315
    :catchall_8e
    move-exception p0

    :try_start_8f
    invoke-virtual {v2}, Ljava/io/OutputStream;->close()V
    :try_end_92
    .catchall {:try_start_8f .. :try_end_92} :catchall_93

    goto :goto_97

    :catchall_93
    move-exception p1

    invoke-virtual {p0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_97
    throw p0
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .registers 4

    .line 55
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 56
    invoke-direct {p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->buildUi()V

    .line 57
    new-instance p1, Ljava/lang/Thread;

    new-instance v0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$1;

    invoke-direct {v0, p0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$1;-><init>(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)V

    const-string v1, "zh-bootstrap"

    invoke-direct {p1, v0, v1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 62
    invoke-virtual {p1}, Ljava/lang/Thread;->start()V

    .line 63
    return-void
.end method
