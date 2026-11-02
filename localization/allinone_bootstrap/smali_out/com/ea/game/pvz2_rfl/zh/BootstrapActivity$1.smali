.class Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$1;
.super Ljava/lang/Object;
.source "BootstrapActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->onCreate(Landroid/os/Bundle;)V
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

    .line 57
    iput-object p1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$1;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 2

    .line 60
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$1;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    # invokes: Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->runBootstrap()V
    invoke-static {v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->access$000(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)V

    .line 61
    return-void
.end method
