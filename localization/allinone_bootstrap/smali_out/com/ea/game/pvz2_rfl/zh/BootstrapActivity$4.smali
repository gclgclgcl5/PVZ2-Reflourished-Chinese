.class Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;
.super Ljava/lang/Object;
.source "BootstrapActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->launchGame()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;


# direct methods
.method constructor <init>(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)V
    .registers 2
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010
        }
        names = {
            null
        }
    .end annotation

    .line 368
    iput-object p1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 5

    .line 371
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    # getter for: Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->started:Z
    invoke-static {v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->access$300(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)Z

    move-result v0

    if-eqz v0, :cond_9

    .line 372
    return-void

    .line 374
    :cond_9
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    const/4 v1, 0x1

    # setter for: Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->started:Z
    invoke-static {v0, v1}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->access$302(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;Z)Z

    .line 376
    :try_start_f
    new-instance v0, Landroid/content/Intent;

    invoke-direct {v0}, Landroid/content/Intent;-><init>()V

    .line 377
    iget-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    const-string v2, "com.popcap.PvZ2.PvZ2GameActivity"

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->setClassName(Landroid/content/Context;Ljava/lang/String;)Landroid/content/Intent;

    .line 378
    const/high16 v1, 0x14000000

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 379
    iget-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    invoke-virtual {v1, v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->startActivity(Landroid/content/Intent;)V

    .line 380
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    invoke-virtual {v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->finish()V
    :try_end_2a
    .catchall {:try_start_f .. :try_end_2a} :catchall_2b

    .line 383
    goto :goto_4c

    .line 381
    :catchall_2b
    move-exception v0

    .line 382
    iget-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$4;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    # getter for: Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;
    invoke-static {v1}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->access$100(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)Landroid/widget/TextView;

    move-result-object v1

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "\u65e0\u6cd5\u542f\u52a8\u6e38\u620f\uff1a"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 384
    :goto_4c
    return-void
.end method
