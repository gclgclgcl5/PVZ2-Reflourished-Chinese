.class Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;
.super Ljava/lang/Object;
.source "BootstrapActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->fail(Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

.field final synthetic val$msg:Ljava/lang/String;


# direct methods
.method constructor <init>(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;Ljava/lang/String;)V
    .registers 3
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x1010
        }
        names = {
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 358
    iput-object p1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    iput-object p2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;->val$msg:Ljava/lang/String;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 4

    .line 361
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    # getter for: Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;
    invoke-static {v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->access$100(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)Landroid/widget/TextView;

    move-result-object v0

    iget-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;->val$msg:Ljava/lang/String;

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 362
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    iget-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$3;->val$msg:Ljava/lang/String;

    const/4 v2, 0x1

    invoke-static {v0, v1, v2}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/Toast;->show()V

    .line 363
    return-void
.end method
