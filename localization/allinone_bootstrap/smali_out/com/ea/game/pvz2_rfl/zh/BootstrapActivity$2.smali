.class Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;
.super Ljava/lang/Object;
.source "BootstrapActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->setStatus(Ljava/lang/String;I)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

.field final synthetic val$msg:Ljava/lang/String;

.field final synthetic val$progress:I


# direct methods
.method constructor <init>(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;Ljava/lang/String;I)V
    .registers 4
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x1010,
            0x1010
        }
        names = {
            null,
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 348
    iput-object p1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    iput-object p2, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;->val$msg:Ljava/lang/String;

    iput p3, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;->val$progress:I

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 3

    .line 351
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    # getter for: Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->statusView:Landroid/widget/TextView;
    invoke-static {v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->access$100(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)Landroid/widget/TextView;

    move-result-object v0

    iget-object v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;->val$msg:Ljava/lang/String;

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 352
    iget-object v0, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;->this$0:Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;

    # getter for: Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->progressBar:Landroid/widget/ProgressBar;
    invoke-static {v0}, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;->access$200(Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity;)Landroid/widget/ProgressBar;

    move-result-object v0

    iget v1, p0, Lcom/ea/game/pvz2_rfl/zh/BootstrapActivity$2;->val$progress:I

    invoke-virtual {v0, v1}, Landroid/widget/ProgressBar;->setProgress(I)V

    .line 353
    return-void
.end method
