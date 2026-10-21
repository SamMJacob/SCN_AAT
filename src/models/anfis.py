"""First-order Takagi-Sugeno ANFIS with hybrid learning, from scratch in PyTorch.

Each rule r has a Gaussian MF per input (center c_r, sigma s_r), as in MATLAB
genfis2/genfis3 cluster-based FIS. Firing strengths are computed in log space:
    log w_r = -sum_j (x_j - c_rj)^2 / (2 s_rj^2),   w_bar = softmax(log w)
Output: y = sum_r w_bar_r (a_r . x + b_r).

Hybrid learning, per epoch:
  1. premise fixed  -> consequents by ridge least squares on Phi = [w_bar_r x, w_bar_r]
  2. consequents fixed -> one Adam pass over mini-batches on centers and log-sigmas (MSE)
After the last epoch the consequents are re-solved once for the final premise.
"""
from __future__ import annotations

import copy
import warnings

import numpy as np
import torch
from torch import nn

torch.set_num_threads(4)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ANFIS(nn.Module):
    def __init__(self, centers: np.ndarray, sigmas: np.ndarray, sigma_min: float = 1e-3):
        super().__init__()
        centers = np.asarray(centers, dtype=np.float64)
        sigmas = np.broadcast_to(np.asarray(sigmas, dtype=np.float64), centers.shape)
        self.R, self.d = centers.shape
        if self.R > 100:
            warnings.warn(f"ANFIS with {self.R} rules: Phi has {self.R * (self.d + 1)} columns")
        self.sigma_min = sigma_min
        self.centers = nn.Parameter(torch.tensor(centers, dtype=torch.float32))
        self.log_sigma = nn.Parameter(torch.tensor(np.log(np.maximum(sigmas, sigma_min)),
                                                   dtype=torch.float32))
        self.register_buffer("theta", torch.zeros(self.R * (self.d + 1), dtype=torch.float32))

    @property
    def sigmas(self) -> torch.Tensor:
        return self.log_sigma.exp().clamp_min(self.sigma_min)

    def norm_firing(self, x: torch.Tensor) -> torch.Tensor:
        z = (x[:, None, :] - self.centers[None]) / self.sigmas[None]
        return torch.softmax(-0.5 * (z ** 2).sum(-1), dim=1)          # [N, R]

    def design(self, x: torch.Tensor, wbar: torch.Tensor | None = None) -> torch.Tensor:
        """Phi = [w_bar_r * x, w_bar_r] flattened per rule -> [N, R*(d+1)]."""
        if wbar is None:
            wbar = self.norm_firing(x)
        xa = torch.cat([x, torch.ones_like(x[:, :1])], dim=1)           # [N, d+1]
        return (wbar[:, :, None] * xa[:, None, :]).reshape(len(x), -1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.design(x) @ self.theta

    # ---- hybrid learning steps ------------------------------------------------
    @torch.no_grad()
    def lse_step(self, x: torch.Tensor, y: torch.Tensor, ridge: float = 1e-6,
                 chunk: int = 8192) -> None:
        P = self.R * (self.d + 1)
        A = torch.zeros(P, P, dtype=torch.float64, device=x.device)
        b = torch.zeros(P, dtype=torch.float64, device=x.device)
        for i in range(0, len(x), chunk):
            phi = self.design(x[i:i + chunk]).double()
            A += phi.T @ phi
            b += phi.T @ y[i:i + chunk].double()
        A += ridge * torch.eye(P, dtype=torch.float64, device=x.device)
        self.theta.copy_(torch.linalg.solve(A, b).float())

    def gd_pass(self, x: torch.Tensor, y: torch.Tensor, opt: torch.optim.Optimizer,
                batch_size: int, gen: torch.Generator) -> None:
        perm = torch.randperm(len(x), generator=gen, device="cpu").to(x.device)
        for i in range(0, len(x), batch_size):
            idx = perm[i:i + batch_size]
            opt.zero_grad()
            loss = ((self(x[idx]) - y[idx]) ** 2).mean()
            loss.backward()
            opt.step()


def fit_anfis(centers, sigmas, X, y, epochs: int = 1, lr: float = 1e-2, batch_size: int = 512,
              ridge: float = 1e-6, sigma_min: float = 1e-3, X_val=None, y_val=None,
              patience: int = 2, seed: int = 0, device=DEVICE):
    """Train an ANFIS with the hybrid rule. Early stopping applies when X_val is given."""
    torch.manual_seed(seed)
    model = ANFIS(centers, sigmas, sigma_min).to(device)
    xt = torch.as_tensor(X, dtype=torch.float32, device=device)
    yt = torch.as_tensor(y, dtype=torch.float32, device=device)
    has_val = X_val is not None
    if has_val:
        xv = torch.as_tensor(X_val, dtype=torch.float32, device=device)
        yv = torch.as_tensor(y_val, dtype=torch.float32, device=device)
    opt = torch.optim.Adam([model.centers, model.log_sigma], lr=lr)
    gen = torch.Generator().manual_seed(seed)
    model.init_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    best, best_state, bad, history = np.inf, None, 0, []
    for ep in range(epochs):
        model.lse_step(xt, yt, ridge)
        model.gd_pass(xt, yt, opt, batch_size, gen)
        if has_val:
            model.lse_step(xt, yt, ridge)
            with torch.no_grad():
                v = float(((model(xv) - yv) ** 2).mean())
            history.append(v)
            if v < best - 1e-6:
                best, best_state, bad = v, copy.deepcopy(model.state_dict()), 0
            else:
                bad += 1
                if bad >= patience:
                    break
    if has_val and best_state is not None:
        model.load_state_dict(best_state)
    else:
        model.lse_step(xt, yt, ridge)
    model.epochs_run = ep + 1
    model.val_history = history
    return model


@torch.no_grad()
def predict(model: ANFIS, X, batch: int = 65536) -> np.ndarray:
    dev = model.centers.device
    out = [model(torch.as_tensor(X[i:i + batch], dtype=torch.float32, device=dev)).cpu().numpy()
           for i in range(0, len(X), batch)]
    return np.concatenate(out) if out else np.zeros(0)
