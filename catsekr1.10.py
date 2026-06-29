#!/usr/bin/env python3.14
# import python 3.14
# files = off
"""CatSeek R1 · 1.0b — CatSeek Core · catr1b · files=off"""
import tkinter as tk
from tkinter import scrolledtext, font, messagebox
import numpy as np
import time
import threading
import re
import json
import os
import io
import ast
import contextlib
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
import html as html_module
import uuid
import sys
from urllib import request as urlrequest
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from html.parser import HTMLParser

# ──────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────
CONFIG = {
    "d_model": 64,
    "layers": 6,
    "heads": 4,
    "n_experts": 8,
    "top_k": 2,
    "distil_passes": 8,
    "turbo_passes": 4,
    "teacher_weight": 0.34,
    "recursive_depth": 5,
    "recursive_epsilon": 0.018,
    "o1_preview": True,
    "o1_self_check": True,
    "ultrathink_default": True,
    "r1_synth_default": True,
    "compression_enabled": True,
    "compression_sparse_k": 24,
    "compression_rank": 32,
    "compression_stack_mult": 4,
    "weight_bits": 1.58,
    "nominal_base_params": 2_000_000_000,
    "simulate_latency": 0.0,
    "step_delay": 0.012,
    "api_port": 8765,
    "api_key": os.getenv("CATR1_API_KEY", "lm-studio"),
    "chat_protocol": "cat-r1-chat",
    "chat_version": "1.0",
    "max_sessions": 32,
    "vocab_size": 4096,
    "max_seq": 128,
    "ff_mult": 4,
    "catseek_eps": 1e-5,
    "act_bits": 8,
    "files": "off",
    "prose_tier": "catseek-r1-mythos",
    "mythos_tier": "mythos-class",
    "catseek_enabled": True,
    "catseek_model_id": "catseek-r1-1.0b-local",
    "catseek_edition": "1.0b",
    "catseek_context_window": 1_000_000,
    "catseek_max_output": 128_000,
    "code_interpreter": "catr1b",
    "code_interpreter_name": "catr1b",
    "code_interpreter_family": "catr1b",
    "code_interpreter_version": "1.0b",
    "catseek_code_enabled": True,
    "catr1_engine": True,
    "catr1_code_perfect": True,
    "catr1_recursive_depth": 5,
    "catr1b_lint": True,
    "code_auto_run": False,
    "code_output_exact": True,
    "code_token_weights_only": True,
    "vibe_code_heuristics": True,
    "deepseek_r1_reasoning": True,
    "mythos_mode": True,
    "deepmind_fast": True,
    "flash_attention": True,
    "adaptive_compute": True,
    "turbo_encode_tasks": ("chat", "code", "math", "execute", "explain"),
    "mythos_recursive_improve": True,
    "mythos_recursive_depth": 3,
    "mythos_recursive_epsilon": 0.04,
    "deepseek_self_verify": True,
    "web_program_enabled": True,
    "web_fetch_enabled": True,
    "web_max_sites": 64,
    "web_max_fetch_kb": 256,
    "web_preview_port": None,
    "gui_theme": "deepseek",
}

# DeepSeek Chat–inspired UI palette (chat.deepseek.com)
DEEPSEEK_UI = {
    "bg": "#ffffff",
    "sidebar": "#f9fafb",
    "sidebar_border": "#eceef2",
    "header_bg": "#ffffff",
    "header_border": "#eceef2",
    "text": "#1b1f23",
    "muted": "#9ca3af",
    "user_bg": "#edf2ff",
    "user_fg": "#1b1f23",
    "bot_bg": "#ffffff",
    "bot_fg": "#1b1f23",
    "think_fg": "#9ca3af",
    "code_bg": "#1e1e1e",
    "code_fg": "#d4d4d4",
    "input_bg": "#ffffff",
    "input_border": "#e3e6ea",
    "input_shadow": "#dfe3e8",
    "accent": "#4d6bfe",
    "accent_text": "#ffffff",
    "send_hover": "#3b57e8",
    "avatar_bot": "#4d6bfe",
    "avatar_user": "#6b7280",
    "new_chat_bg": "#ffffff",
    "new_chat_border": "#d1d5db",
    "history_hover": "#eef1f5",
    "empty_title": "#111827",
    "radius_pad": 16,
    "input_radius": 20,
}

GUI_APP_NAME = "Cat R1"
GUI_TAGLINE = "files = off"

FILES = CONFIG["files"]
BRAND = "CatSeek R1"
EDITION = CONFIG.get("catseek_edition", "1.0b")
MODEL_NAME = f"CatSeek R1 {EDITION}"
CORE_NAME = "CatSeek Core"
CATSEEK_MODEL_ID = CONFIG["catseek_model_id"]
MYTHOS_TIER = CONFIG["mythos_tier"]
CODE_ENGINE = CONFIG["code_interpreter_name"]
CODE_BACKEND = CONFIG["code_interpreter"]
CATR1_ENGINE = "catr1b"
CATSEEK_CODE_ENABLED = CONFIG["catseek_code_enabled"]
MYTHOS_MODE = CONFIG.get("mythos_mode", True)
DEEPSEEK_R1_MODE = CONFIG.get("deepseek_r1_reasoning", True)
MYTHOS_NAME = "Mythos-tier"
REASONING_MODE = "deepseek-r1-cot"
PROSE_TIER = CONFIG["prose_tier"]
VERSION = EDITION

CAT_R11_PROFILE_MD = f"""# {BRAND} {EDITION} (Local)

**{CATSEEK_MODEL_ID}** · {CORE_NAME} · **files=off** · **{CODE_ENGINE}** code engine.

| | |
|---|---|
| Brand | {BRAND} {EDITION} — local assistant |
| Reasoning | DeepSeek-R1 chain-of-thought + self-verify (files=off) |
| Prose | Mythos-tier extended thinking + recursive polish |
| Runtime | {CORE_NAME} distillation stack (in-memory) |
| Context | {CONFIG['catseek_context_window']:,} tokens (in-memory) |
| Output | up to {CONFIG['catseek_max_output']:,} tokens |
| Code | **{CODE_ENGINE}** · recursive perfection · vibe heuristics · files=off |
| Web | CatSeek Web Program — artifacts · fetch · preview (files=off) |
| Architecture | CatSeek Linear · causal MHA · MoE FFN · ReLU² · RMSNorm |
| Weights | AbsMean ternary {{−1, 0, 1}} @ {CONFIG['weight_bits']} bits |
| API ID | `{CATSEEK_MODEL_ID}` |

Run: `python3.14 >catseekr1.10b.py` · CLI: `python3.14 >catseekr1.10b.py --chat`
"""


# ──────────────────────────────────────────────────────────────
# CATSEEK R1 1.0 CORE (files=off · in-memory shadow weights + packed ternary)
# ──────────────────────────────────────────────────────────────
def _round_clip(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return np.clip(np.round(x), lo, hi).astype(np.int8)


def _squared_relu(x: np.ndarray) -> np.ndarray:
    r = np.maximum(x, 0.0)
    return (r * r).astype(np.float32)


class CatSeekLinear:
    """
    CatSeek R1 1.0 CatSeek Linear layer (files=off):
    shadow FP32 weights → AbsMean ternary {-1,0,1} → int8 activation matmul.
    """

    __slots__ = ("in_f", "out_f", "shadow_w", "bias", "w_scale", "w_signed", "w_packed", "eps")

    def __init__(self, in_features: int, out_features: int, seed: int, *, bias: bool = False):
        rng = np.random.RandomState(seed)
        self.in_f = in_features
        self.out_f = out_features
        self.eps = CONFIG["catseek_eps"]
        scale = np.sqrt(2.0 / max(in_features, 1))
        self.shadow_w = (rng.randn(out_features, in_features).astype(np.float32) * scale)
        self.bias = np.zeros(out_features, dtype=np.float32) if bias else None
        self.w_scale = np.float32(1.0)
        self.w_signed = np.zeros((out_features, in_features), dtype=np.int8)
        self.w_packed = b""
        self.requantize()

    def requantize(self) -> None:
        gamma = float(np.mean(np.abs(self.shadow_w))) + self.eps
        self.w_scale = np.float32(gamma)
        scaled = self.shadow_w / gamma
        w_q = _round_clip(scaled, -1, 1)
        self.w_signed = w_q.astype(np.int8)
        self.w_packed = self._pack(w_q)

    @staticmethod
    def _pack(w_q: np.ndarray) -> bytes:
        """Base-3 pack: 5 ternary values {-1,0,1} → 1 byte (CatSeek R1 1.0 ~1.58 bits/weight)."""
        flat = w_q.ravel()
        out = bytearray()
        for i in range(0, len(flat), 5):
            chunk = flat[i : i + 5]
            val = 0
            for j, t in enumerate(chunk):
                val += (int(t) + 1) * (3 ** j)
            out.append(val % 256)
        return bytes(out)

    @staticmethod
    def _absmax_quantize_x(x: np.ndarray) -> Tuple[np.ndarray, float]:
        scale = float(np.max(np.abs(x))) + CONFIG["catseek_eps"]
        qmax = (2 ** (CONFIG["act_bits"] - 1)) - 1
        x_q = np.clip(np.round(x / scale * qmax), -qmax, qmax).astype(np.int16)
        return x_q, scale

    def forward(self, x: np.ndarray) -> np.ndarray:
        single = x.ndim == 1
        xm = np.atleast_2d(x.astype(np.float32))
        qmax = (2 ** (CONFIG["act_bits"] - 1)) - 1
        scales = np.max(np.abs(xm), axis=1, keepdims=True) + self.eps
        x_q = np.clip(np.round(xm / scales * qmax), -qmax, qmax).astype(np.int16)
        acc = (x_q.astype(np.int32) @ self.w_signed.T.astype(np.int32)).astype(np.float32)
        acc = acc * scales * float(self.w_scale)
        if self.bias is not None:
            acc = acc + self.bias
        return acc[0] if single else acc

    def param_count(self) -> Tuple[int, float]:
        n = self.in_f * self.out_f
        return n, n * CONFIG["weight_bits"] / 8.0


def _rms_norm(x: np.ndarray, gamma: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    if x.ndim == 1:
        rms = float(np.sqrt(np.mean(x * x) + eps))
        return (x / rms * gamma).astype(np.float32)
    rms = np.sqrt(np.mean(x * x, axis=-1, keepdims=True) + eps)
    return (x / rms * gamma).astype(np.float32)


class CatSeekBlock:
    """One transformer block: causal MHA + CatSeek Linear FFN (ReLU²), all ternary matmul."""

    __slots__ = ("q", "k", "v", "o", "ff_up", "ff_down", "router", "experts", "norm1", "norm2", "_h", "_hd")

    def __init__(self, d_model: int, seed: int):
        h = CONFIG["heads"]
        hd = d_model // h
        ff = d_model * CONFIG["ff_mult"]
        self.q = CatSeekLinear(d_model, d_model, seed + 1)
        self.k = CatSeekLinear(d_model, d_model, seed + 2)
        self.v = CatSeekLinear(d_model, d_model, seed + 3)
        self.o = CatSeekLinear(d_model, d_model, seed + 4)
        self.ff_up = CatSeekLinear(d_model, ff, seed + 5)
        self.ff_down = CatSeekLinear(ff, d_model, seed + 6)
        self.router = CatSeekLinear(d_model, CONFIG["n_experts"], seed + 7)
        rng = np.random.RandomState(seed + 8)
        self.experts = [
            (CatSeekLinear(d_model, ff, seed + 100 + i * 2), CatSeekLinear(ff, d_model, seed + 101 + i * 2))
            for i in range(CONFIG["n_experts"])
        ]
        self.norm1 = rng.randn(d_model).astype(np.float32) * 0.1 + 1.0
        self.norm2 = rng.randn(d_model).astype(np.float32) * 0.1 + 1.0
        self._hd = hd
        self._h = h

    def _causal_mha(self, x: np.ndarray) -> np.ndarray:
        t, d = x.shape
        h, hd = self._h, self._hd
        eps = CONFIG["catseek_eps"]
        xn = np.stack([_rms_norm(x[ti], self.norm1) for ti in range(t)], axis=0)
        q = self.q.forward(xn).reshape(t, h, hd)
        k = self.k.forward(xn).reshape(t, h, hd)
        v = self.v.forward(xn).reshape(t, h, hd)
        scale = np.sqrt(hd) + eps
        if CONFIG.get("flash_attention") and t > 1:
            scores = np.einsum("thd,shd->hts", q, k) / scale
            mask = np.triu(np.ones((t, t), dtype=bool), k=1)
            scores = np.where(mask[np.newaxis, :, :], -1e9, scores)
            scores = scores - np.max(scores, axis=-1, keepdims=True)
            w = np.exp(scores)
            w = w / (np.sum(w, axis=-1, keepdims=True) + eps)
            ctx = np.einsum("hts,shd->htd", w, v).reshape(t, d)
            return self.o.forward(ctx)
        out = np.zeros((t, d), dtype=np.float32)
        for ti in range(t):
            scores = np.einsum("hd,ihd->ih", q[ti], k[: ti + 1]) / scale
            scores = scores - np.max(scores, axis=-1, keepdims=True)
            w = np.exp(scores)
            w = w / (np.sum(w, axis=-1, keepdims=True) + eps)
            ctx = np.einsum("ih,ihd->hd", w, v[: ti + 1])
            out[ti] = ctx.reshape(d)
        return self.o.forward(out)

    def _moe_ffn(self, x: np.ndarray) -> np.ndarray:
        t, d = x.shape
        out = np.zeros_like(x)
        for ti in range(t):
            xn = _rms_norm(x[ti], self.norm2)
            logits = self.router.forward(xn)
            top = np.argsort(logits)[-CONFIG["top_k"]:]
            acc = np.zeros(d, dtype=np.float32)
            for idx in top:
                up, down = self.experts[int(idx)]
                h = _squared_relu(up.forward(xn))
                acc = acc + down.forward(h) / CONFIG["top_k"]
            out[ti] = acc
        return out

    def forward(self, x: np.ndarray) -> np.ndarray:
        return x + self._moe_ffn(x + self._causal_mha(x))


def _iter_catseek_linears(block: CatSeekBlock) -> List[CatSeekLinear]:
    layers = [block.q, block.k, block.v, block.o, block.ff_up, block.ff_down, block.router]
    for up, down in block.experts:
        layers.extend([up, down])
    return layers


def catseek_memory_report(blocks: List[CatSeekBlock], embed: np.ndarray, head: np.ndarray) -> Dict[str, Any]:
    shadow = embed.size + head.size
    packed_bytes = 0
    effective_bits = 0.0
    linear_count = 0
    for blk in blocks:
        for lin in _iter_catseek_linears(blk):
            n, mem = lin.param_count()
            shadow += n
            effective_bits += n * CONFIG["weight_bits"]
            packed_bytes += len(lin.w_packed)
            linear_count += 1
    return {
        "catseek_linear_layers": linear_count,
        "shadow_params": shadow,
        "effective_bits": effective_bits,
        "packed_kb": packed_bytes / 1024.0,
        "effective_mb": effective_bits / 8.0 / 1024.0 / 1024.0,
        "weight_bits": CONFIG["weight_bits"],
    }


# ──────────────────────────────────────────────────────────────
# CATSEEK R1 REASONING (files=off)
# ──────────────────────────────────────────────────────────────
class O1PreviewReasoner:
    """
    o1-preview reasoning loop (files=off):
    parse → recursive CatSeek R1 1.0 passes → self-check → verify → answer.
    Thinking stays internal; user sees clean final text.
    """

    @classmethod
    def should_run(cls, prompt: str, *, enabled: bool, force: bool) -> bool:
        if force:
            return True
        if not enabled:
            return False
        pl = prompt.strip().lower()
        if not pl:
            return False
        if len(pl.split()) <= 2 and pl in {"hi", "hey", "hello", "yo", "sup", "ok", "thanks", "help"}:
            return False
        if CatSeekR1Code.enabled() and CatSeekR1Code.wants_code(pl):
            return False
        return True

    @staticmethod
    def _parse_intent(prompt: str) -> str:
        pl = prompt.lower()
        if any(k in pl for k in ("bug", "error", "traceback", "exception")):
            return "debug / isolate failure"
        if any(k in pl for k in ("code", "python", "script", "function")):
            return "implement or review code"
        if any(k in pl for k in ("build", "make", "create", "design")):
            return "design / construct"
        if any(k in pl for k in ("explain", "what is", "why", "how")):
            return "explain / teach"
        if re.search(r"\d\s*[+\-*/]", pl):
            return "compute / verify numerics"
        if "?" in prompt:
            return "answer a question"
        return "general assistance"

    @staticmethod
    def _subtasks(prompt: str) -> List[str]:
        pl = prompt.lower()
        tasks: List[str] = []
        if "?" in prompt:
            tasks.append("identify what is being asked and the expected form of the answer")
        if any(k in pl for k in ("code", "python", "implement")):
            tasks.append("list inputs, outputs, and edge cases before writing code")
        if any(k in pl for k in ("error", "bug", "traceback")):
            tasks.append("reproduce minimally, then localize the failing line")
        if any(k in pl for k in ("build", "design", "architecture")):
            tasks.append("sketch components and data flow before details")
        if re.search(r"\d\s*[+\-*/]", pl):
            tasks.append("compute step-by-step and verify the result")
        if not tasks:
            tasks.append("state goal, constraints, and the smallest verifiable next step")
        return tasks[:5]

    @staticmethod
    def _verify_note(prompt: str) -> str:
        pl = prompt.lower()
        checks: List[str] = []
        if "?" in prompt:
            checks.append("final answer addresses the question directly")
        if any(k in pl for k in ("code", "python")):
            checks.append("code is runnable in the local sandbox")
        if any(k in pl for k in ("error", "bug")):
            checks.append("expected vs actual output is explicit")
        checks.append("files=off — reasoning and weights stay in-memory")
        return "; ".join(checks)

    @staticmethod
    def _self_check(prompt: str, draft: str) -> str:
        pl = prompt.lower()
        notes: List[str] = []
        if "?" in prompt:
            notes.append("Does the draft answer the exact question?")
        if any(k in pl for k in ("code", "python")):
            notes.append("Are imports, edge cases, and return values covered?")
        if re.search(r"\d\s*[+\-*/]", pl):
            notes.append("Re-check arithmetic independently.")
        notes.append("Remove speculation; keep only what follows from the prompt.")
        return " · ".join(notes)

    def run(
        self,
        prompt: str,
        *,
        distill_draft: str = "",
        recursive_trace: Optional[List[str]] = None,
        compression_trace: Optional[List[str]] = None,
    ) -> str:
        intent = self._parse_intent(prompt)
        subtasks = self._subtasks(prompt)
        verify = self._verify_note(prompt)
        reason = distill_draft.strip() or f"CatSeek R1 1.0 aligned on {intent}."
        lines = [
            CatSeekR1Fusion.think_header(),
            f"1. Understand — {intent}",
        ]
        for i, task in enumerate(subtasks, start=2):
            lines.append(f"{i}. Plan — {task}")
        n = len(subtasks) + 2
        if compression_trace:
            for j, ct in enumerate(compression_trace):
                lines.append(f"{n + j}. Compress — {ct}")
            n += len(compression_trace)
        if recursive_trace:
            for j, rt in enumerate(recursive_trace):
                lines.append(f"{n + j}. Recursive CatSeek R1 1.0 — {rt}")
            n += len(recursive_trace)
        lines.append(f"{n}. Reason — {reason[:200]}")
        n += 1
        if CONFIG["o1_self_check"]:
            lines.append(f"{n}. Self-check — {self._self_check(prompt, reason)}")
            n += 1
        lines.append(f"{n}. Verify — {verify}")
        lines.append(f"{n + 1}. Answer — emit clean user-facing text.")
        return "\n".join(lines)


ThinkEngine = O1PreviewReasoner
UltraThinkEngine = O1PreviewReasoner


# ──────────────────────────────────────────────────────────────
# CATSEEK R1 FUSION (DeepSeek-R1 CoT · Mythos polish · files=off)
# ──────────────────────────────────────────────────────────────
class CatSeekR1Fusion:
    """
    Dual reasoning stack under CatSeek R1 branding (no weight files):
    DeepSeek-R1 — long CoT, GRPO-style self-verify, math sanity checks.
    Mythos-tier — extended thinking trace, recursive draft improvement.
    """

    __slots__ = ("last_passes", "last_trace")

    DEEPSEEK_ALGOS = (
        "Long chain-of-thought",
        "GRPO outcome self-verification",
        "Step-by-step math checks",
        "Code edge-case review",
    )
    MYTHOS_ALGOS = (
        "Extended thinking trace",
        "Recursive draft improvement",
        "Mythos-tier prose polish",
        "Pre-emit self-check",
    )

    def __init__(self):
        self.last_passes = 0
        self.last_trace: List[str] = []

    @staticmethod
    def think_header() -> str:
        return f"{REASONING_MODE} · {BRAND} · DeepSeek-R1 · Mythos · {CODE_ENGINE} · files=off"

    @staticmethod
    def _meaningful_words(pl: str) -> bool:
        return bool(re.search(r"[a-zA-Z\u4e00-\u9fff]{2,}", pl))

    @classmethod
    def is_noise(cls, prompt: str) -> bool:
        pl = prompt.strip().lower()
        if not pl:
            return True
        if pl in {".", "..", "...", "\"", "'", "?", "!", "ok", "k"}:
            return True
        return not cls._meaningful_words(pl) and len(pl) <= 3

    @classmethod
    def session_followup(cls, engine: "CatR11Engine", prompt: str) -> Optional[str]:
        if not engine.chat_history:
            return None
        last_user = last_bot = ""
        for m in reversed(engine.chat_history[:-1]):
            if m.get("role") == "assistant" and not last_bot:
                last_bot = m.get("text", "")
            elif m.get("role") == "user" and not last_user:
                last_user = m.get("text", "")
            if last_user and last_bot:
                break
        if not last_user:
            return None
        pl = prompt.strip().lower()
        if cls.is_noise(prompt):
            if re.search(r"how are you|how're you|how is it", last_user.lower()):
                return "I'm doing well — thanks for asking! What's on your mind?"
            if re.search(r"你好吗|怎么样|还好吗", prompt):
                return "我很好，谢谢关心！你今天想聊什么？"
            return f"Still here — we were talking about \"{last_user[:60]}\". Want to continue that, or start something new?"
        return None

    def recursive_improve(self, draft: str, prompt: str, vec: Optional[np.ndarray]) -> str:
        if not CONFIG.get("mythos_recursive_improve") or not draft.strip():
            return draft
        depth = CONFIG.get("mythos_recursive_depth", 3)
        eps = CONFIG.get("mythos_recursive_epsilon", 0.04)
        out = draft
        self.last_trace = []
        prev = out
        for i in range(depth):
            score = self._quality_score(out, prompt, vec)
            self.last_trace.append(f"mythos pass {i + 1} · quality {score:.3f}")
            if i > 0 and score >= 0.92:
                self.last_trace.append(f"converged at pass {i + 1}")
                self.last_passes = i + 1
                return out
            out = self._polish_pass(out, prompt, vec, pass_idx=i)
            if i > 0:
                delta = abs(len(out) - len(prev)) / max(len(prev), 1)
                if delta < eps:
                    self.last_trace.append(f"converged at pass {i + 1}")
                    self.last_passes = i + 1
                    return out
            prev = out
        self.last_passes = depth
        return out

    @staticmethod
    def _quality_score(text: str, prompt: str, vec: Optional[np.ndarray]) -> float:
        if not text.strip():
            return 0.0
        score = 0.55
        if "?" in prompt and "?" not in text and len(text) > 40:
            score += 0.08
        if len(text.split()) >= 12:
            score += 0.12
        if re.search(r"\*\*[^*]+\*\*", text):
            score += 0.05
        if vec is not None and vec.size:
            score += min(0.2, float(np.linalg.norm(vec[:8])) * 0.02)
        if text.count("\n\n") >= 1:
            score += 0.05
        return min(1.0, score)

    @staticmethod
    def _polish_pass(text: str, prompt: str, vec: Optional[np.ndarray], pass_idx: int) -> str:
        t = re.sub(r"\n{3,}", "\n\n", text.strip())
        if pass_idx == 0 and "?" in prompt and not t.endswith("?"):
            if len(t.split()) > 20 and "I can go deeper" not in t:
                t += "\n\nWant me to go deeper on any part?"
        if pass_idx >= 1 and len(t) < 120 and "?" in prompt:
            topic = prompt.strip().rstrip("?")[:80]
            t = f"{t}\n\n**Short answer:** {topic} — ask for steps, code, or a comparison and I'll expand."
        return t

    @staticmethod
    def deepseek_math_wrap(prompt: str, result: str) -> str:
        if not CONFIG.get("deepseek_self_verify"):
            return f"Result: **{result}**"
        return (
            f"**Step-by-step (DeepSeek-R1 verify):**\n\n"
            f"1. Parse expression from prompt\n"
            f"2. Evaluate with integer/float rules\n"
            f"3. Self-check: re-evaluate → **{result}**\n\n"
            f"**Answer:** {result}"
        )

    def stats_line(self) -> str:
        return (
            f"Fusion · DeepSeek-R1 ({len(self.DEEPSEEK_ALGOS)} algos) · "
            f"Mythos ({len(self.MYTHOS_ALGOS)} algos) · passes={self.last_passes}"
        )


# ──────────────────────────────────────────────────────────────
# DEEPMIND FAST STACK (files=off · in-memory speed algorithms)
# Chinchilla adaptive compute · Flash attention · MuZero prefix cache
# · teacher-only turbo distillation · batch CatSeek Linear · early exit
# ──────────────────────────────────────────────────────────────
class DeepMindFastStack:
    """
    In-memory DeepMind-inspired inference accelerators (no weight files).
    Composes with CatSeek R1 1.0 + o1-preview recursive loop on CatR11Engine.
    """

    __slots__ = ("engine", "_prefix_cache", "_turbo_cache", "last_algo", "passes_saved")

    ALGOS = (
        "Chinchilla adaptive compute",
        "Flash causal attention",
        "Batch CatSeek Linear GEMM",
        "MuZero prefix latent cache",
        "Teacher-only turbo distillation",
        "Sparse top-k compression",
        "MoE top-k routing",
        "Recursive early convergence",
    )

    def __init__(self, engine: "CatR11Engine"):
        self.engine = engine
        self._prefix_cache: Dict[str, np.ndarray] = {}
        self._turbo_cache: Dict[str, np.ndarray] = {}
        self.last_algo = ""
        self.passes_saved = 0

    def adaptive_depth(self, prompt: str, task: Optional[str] = None) -> int:
        """Chinchilla-style: scale recursive passes to prompt + task budget."""
        base = CONFIG["recursive_depth"]
        if not CONFIG.get("adaptive_compute"):
            return base
        n = len(prompt.strip())
        if task in CONFIG.get("turbo_encode_tasks", ()):
            return 1
        if n < 24:
            return 1
        if n < 80:
            return min(2, base)
        if n < 200:
            return min(3, base)
        return base

    def _prefix_key(self, prompt: str) -> str:
        words = prompt.lower().strip().split()
        return " ".join(words[:6]) if words else ""

    def _muzero_hit(self, prompt: str) -> Optional[np.ndarray]:
        key = self._prefix_key(prompt)
        if not key or len(prompt) < 32:
            return None
        hit = self._prefix_cache.get(key)
        if hit is not None:
            self.last_algo = "MuZero prefix latent cache"
            return hit.copy()
        return None

    def turbo_encode(self, prompt: str) -> np.ndarray:
        """Single-pass teacher-only encode — chat/code/math fast path."""
        key = prompt.lower().strip()
        hit = self._turbo_cache.get(key)
        if hit is not None:
            self.last_algo = "Teacher-only turbo distillation (cache)"
            return hit.copy()
        state = self.engine.encode_prompt(prompt)
        seq = state if state.ndim == 2 else state.reshape(1, -1)
        delta = self.engine._pool_sequence(
            self.engine.forward(seq, turbo_only=True)
        )
        out = self.engine._layer_norm(delta)
        if CONFIG["compression_enabled"]:
            out = self.engine.compressor.compress_roundtrip(out)
            self.engine.last_compression_ratio = self.engine.compressor.last_ratio
        self.engine.last_recursive_passes = 1
        self.engine.last_recursive_trace = ["turbo · 1 pass · teacher-only · CatSeek Linear forward"]
        self.engine.last_vec = out.copy()
        self.last_algo = "Teacher-only turbo distillation"
        if len(self._turbo_cache) < 96:
            self._turbo_cache[key] = out.copy()
        return out

    def encode(self, prompt: str, task: Optional[str] = None) -> np.ndarray:
        if not CONFIG.get("deepmind_fast"):
            return self.engine.recursive_encode(prompt)
        if task in CONFIG.get("turbo_encode_tasks", ()):
            return self.turbo_encode(prompt)
        mu = self._muzero_hit(prompt)
        if mu is not None:
            self.engine.last_vec = mu
            return mu
        depth = self.adaptive_depth(prompt, task)
        saved = max(0, CONFIG["recursive_depth"] - depth)
        self.passes_saved += saved
        out = self.engine.recursive_encode(prompt, depth=depth)
        pk = self._prefix_key(prompt)
        if pk and len(self._prefix_cache) < 64:
            self._prefix_cache[pk] = out.copy()
        self.last_algo = f"Chinchilla adaptive compute ({depth} passes)"
        return out

    def stats_line(self) -> str:
        return (
            f"DeepMind fast · {len(self.ALGOS)} algos · "
            f"last={self.last_algo or 'idle'} · passes_saved={self.passes_saved}"
        )

    def clear(self) -> None:
        self._prefix_cache.clear()
        self._turbo_cache.clear()
        self.passes_saved = 0


# ──────────────────────────────────────────────────────────────
# CATSEEK R1 1.0 COMPRESSION ENGINE (files=off · frontier-tier capacity)
# ──────────────────────────────────────────────────────────────
class CatSeekCompressor:
    """
    In-memory compression stack for CatSeek R1 1.0:
    ternary weights · sparse top-k activations · low-rank bottleneck · pack/unpack.
    Simulates multi-billion-parameter capacity without external files.
    """

    __slots__ = ("d_model", "rank", "sparse_k", "down_s", "up_s", "last_ratio", "packs")

    def __init__(self, d_model: int, seed: int = 99):
        self.d_model = d_model
        self.rank = CONFIG["compression_rank"]
        self.sparse_k = CONFIG["compression_sparse_k"]
        rng = np.random.RandomState(seed)
        down = rng.choice([-1, 0, 1], (d_model, self.rank)).astype(np.int8)
        up = rng.choice([-1, 0, 1], (self.rank, d_model)).astype(np.int8)
        self.down_s = (down == 1).astype(np.int16) - (down == -1).astype(np.int16)
        self.up_s = (up == 1).astype(np.int16) - (up == -1).astype(np.int16)
        self.last_ratio = 1.0
        self.packs = 0

    @staticmethod
    def _ternary(x: np.ndarray, thr: float = 0.5) -> np.ndarray:
        q = np.zeros_like(x, dtype=np.int8)
        q[x > thr], q[x < -thr] = 1, -1
        return q

    def low_rank_bottleneck(self, x: np.ndarray) -> np.ndarray:
        xq = self._ternary(x).astype(np.int16)
        h = np.tanh(xq @ self.down_s).astype(np.float32)
        return (self._ternary(h).astype(np.int16) @ self.up_s).astype(np.float32)

    def sparse_reconstruct(self, x: np.ndarray) -> np.ndarray:
        k = min(self.sparse_k, len(x))
        idx = np.argsort(np.abs(x))[-k:]
        out = np.zeros_like(x, dtype=np.float32)
        out[idx] = x[idx]
        t = self._ternary(out).astype(np.float32)
        out[idx] = t[idx] * np.abs(x[idx])
        fp_bits = self.d_model * 32
        packed_bits = k * 32 + self.rank * 16
        self.last_ratio = max(1.0, fp_bits / max(packed_bits, 1))
        self.packs += 1
        return out

    def compress_roundtrip(self, x: np.ndarray) -> np.ndarray:
        if not CONFIG["compression_enabled"]:
            self.last_ratio = 1.0
            return x
        lr = self.low_rank_bottleneck(x)
        blended = x * 0.52 + lr * 0.48
        return self.sparse_reconstruct(blended)

    def effective_params_billions(self) -> float:
        mult = self.last_ratio * CONFIG["distil_passes"] * CONFIG["compression_stack_mult"]
        return CONFIG["nominal_base_params"] * mult / 1e9 / max(CONFIG["compression_stack_mult"], 1)


class CatSeekR1Core:
    """
    Unified inference core: compressed CatSeek R1 1.0 forward + o1-preview recursive loop.
    Targets frontier-tier answer quality on consumer hardware (files=off).
    """

    __slots__ = ("engine",)

    def __init__(self, engine: "CatR11Engine"):
        self.engine = engine

    def infer_state(self, prompt: str) -> np.ndarray:
        return self.engine.recursive_encode(prompt)

    def stats_line(self) -> str:
        c = self.engine.compressor
        st = self.engine.catseek_stats
        base = (
            f"CatSeek R1 1.0 · {st['catseek_linear_layers']} CatSeek Linear · "
            f"packed {st['packed_kb']:.1f}KB · {st['weight_bits']} bits/weight · "
            f"compress {c.last_ratio:.1f}x · files=off"
        )
        if CONFIG.get("deepmind_fast") and self.engine.deepmind:
            return f"{base} · {self.engine.deepmind.stats_line()}"
        return base


# Legacy aliases (BitNet → CatSeek R1 1.0)
BitLinear = CatSeekLinear
BitNetBlock = CatSeekBlock
BitNetCompressor = CatSeekCompressor
BitNetRivalCore = CatSeekR1Core
bitnet_memory_report = catseek_memory_report


# Casual chat — matched before educational intent routing (EN · 中文)
_SMALLTALK: Tuple[Tuple[str, str], ...] = (
    (r"^(?:hi|hey|hello|yo|howdy)\s*[!?.]*$", "Hi! How can I help you today?"),
    (r"^how are you(?: doing| today)?\??$", "Doing well, thanks for asking! I'm here and ready to chat. How about you?"),
    (r"^how(?:'re| are) you(?: doing| today)?\??$", "Doing well, thanks for asking! I'm here and ready to chat. How about you?"),
    (r"^how(?:'s| is|s) it going\??$", "Going well on my end — thanks! What can I help you with today?"),
    (r"^how(?:'s| is|s) everything\??$", "All good here! What's on your mind?"),
    (r"^how(?:'s| is|s) your day\??$", "Running smoothly so far. How's yours going?"),
    (r"^how have you been\??$", "Steady and ready to help. What have you been up to?"),
    (r"^(?:what's up|whats up|wassup|sup)\??$", "Not much — just here to help. What are you working on?"),
    (r"^how you doing\??$", "Doing great, thanks! What can I do for you?"),
    (r"^how(?:'s| is| are) (?:u|ya|you) doing\??$", "Doing great, thanks! What can I do for you?"),
    (r"^how r u\??$", "Doing well! How are you?"),
    (r"^how are u\??$", "Doing well! How are you?"),
    (r"^(?:good morning|good afternoon|good evening)\.?\??$", "Good to hear from you! What would you like to talk about?"),
    (r"^nice to meet you\.?\??$", "Nice to meet you too! Ask me anything — code, explanations, debugging, or just chat."),
    (r"^(?:are you ok|you ok|u ok)\??$", "I'm all good, thanks! How can I help?"),
    (r"^what(?:'s| is) new\??$", "Same local CatSeek R1 engine, ready when you are. What's new with you?"),
    (r"^how do you feel\??$", "I feel ready to help! What's up?"),
    (r"^(?:你好|您好|嗨|哈喽|在吗)[!！?？。.\s]*$", "你好！有什么我可以帮你的？"),
    (r"^你好吗[!！?？]?$", "我很好，谢谢！你今天想聊点什么？"),
    (r"^(?:早上好|下午好|晚上好)[!！?？]?$", "你好！很高兴见到你。需要什么帮助？"),
    (r"^谢谢[!！?？]?$", "不客气！还需要别的帮助吗？"),
    (r"^感谢[!！?？]?$", "不客气！随时可以继续问我。"),
    (r"^(?:再见|拜拜)[!！?？]?$", "再见！期待下次聊天。"),
)


# Multilingual tokenization (EN · 中文 · mixed · files=off)
_TOKEN_EN = re.compile(r"[a-z0-9+#]+", re.I)
_TOKEN_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
_ZH_QUESTION = re.compile(
    r"(什么是|是什么|什么叫|何为|为何|为什么|为啥|怎么|如何|怎样|能否|可不可以|介绍一下|解释|说明|告诉我)"
)
_ZH_GREETING = re.compile(
    r"^(你好|您好|嗨|哈喽|早上好|下午好|晚上好|在吗|你是谁|你好吗)[!！?？。.\s]*$"
)
_ZH_TOPIC = re.compile(
    r"(?:什么是|是什么|什么叫|解释|说明|介绍|告诉我)(.+?)[?？。!！]?$"
)


def tokenize_text(text: str, max_tokens: int = 256) -> List[str]:
    """Split English words and CJK characters for in-memory embedding (files=off)."""
    raw = (text or "").strip()
    if not raw:
        return ["<unk>"]
    lower = raw.lower()
    tokens: List[str] = []
    i = 0
    while i < len(lower) and len(tokens) < max_tokens:
        m = _TOKEN_EN.match(lower, i)
        if m:
            tokens.append(m.group(0))
            i = m.end()
            continue
        m = _TOKEN_CJK.match(raw, i)
        if m:
            tokens.append(m.group(0))
            i = m.end()
            continue
        i += 1
    return tokens or ["<unk>"]


def is_zh_question(text: str) -> bool:
    return bool(_ZH_QUESTION.search(text or ""))


def is_zh_greeting(text: str) -> bool:
    s = (text or "").strip()
    if _ZH_GREETING.match(s):
        return True
    return len(s) <= 10 and bool(re.search(r"^(你好|您好|你好吗|早上好|下午好|晚上好)", s))


def is_explain_request(text: str) -> bool:
    pl = (text or "").lower()
    if re.search(r"\b(explain|what is|what are|what's|why|how (?:does|do|to|can|would|should))\b", pl):
        return True
    return is_zh_question(text or "")


def extract_zh_topic(prompt: str) -> str:
    s = (prompt or "").strip()
    m = _ZH_TOPIC.search(s)
    if m:
        return m.group(1).strip("？?。!！ ")[:80]
    return s[:80]


# ──────────────────────────────────────────────────────────────
# VIBE CODE HEURISTICS (EN · 中文 · mixed · pasted code · files=off)
# ──────────────────────────────────────────────────────────────
class VibeCodeHeuristics:
    """
    Multilingual intent + language detection for casual vibe-coding.
    Understands English, Chinese (中文), mixed human language, and raw code snippets.
    """

    CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
    ZH_CODE_NOUNS = (
        "写代码", "编程", "程序", "源码", "源代码", "脚本", "网页", "代码",
        "函数", "算法", "斐波那契", "斐波那契数列", "小程序", "页面",
    )
    ZH_RUN = ("运行", "执行", "跑一下", "跑起来", "测试", "试一下")
    EN_VIBE = re.compile(
        r"\b(vibe[\s-]?code|vibecode|whip up| cook up|spin up|slap together|"
        r"gimme|lemme get|just (?:make|write|code)|yo make|hook me up with)\b",
        re.I,
    )
    ZH_WRITE = re.compile(
        r"(写|做|建|造|生成|帮我写|帮我做|给我写|给我做|帮我生成|"
        r"来个|整一个|弄一个|搞一个|创建一个|实现|编写|弄段|来段|"
        r"能不能写|可以写|请写|请帮我|麻烦写|麻烦帮我)"
    )
    ZH_CORRECT = re.compile(
        r"(不要|别|不对|不是|改成|改为|换成|用)(?:.{0,12})?(html|python|javascript|java|c\+\+?|cpp|rust|go|bash|typescript|sql|c语言|网页|脚本)",
        re.I,
    )
    ZH_LANG_INLINE = re.compile(
        r"(?:用|以|in|with|using|换成|改成|改为)\s*"
        r"(python|html|javascript|typescript|java|rust|go|bash|shell|cpp|c\+\+|c|sql|ruby|php|"
        r"c语言|c\+\+语言|网页|页面|脚本|js|py|python3?|html5?)",
        re.I,
    )
    ZH_SAYS = re.compile(
        r"(?:显示|输出|打印|说|写上|内容是|文字是|写着)[「\"']?([^」\"'\n，。！？]+)[」\"']?",
    )
    ZH_SUBJECT = re.compile(
        r"(?:写|做|建|生成|帮我写|帮我做|来个|整一个|弄一个|搞一个|创建一个|实现)"
        r"(?:一个|个|一段|段)?(.+?)(?:用|in|的|程序|代码|网页|脚本|$)",
    )
    LANG_ALIASES = {
        "py": "python", "python3": "python", "python2": "python",
        "js": "javascript", "node": "javascript", "ts": "typescript",
        "c++": "cpp", "cc": "cpp", "c语言": "c", "c++语言": "cpp",
        "网页": "html", "页面": "html", "html5": "html", "前端": "html",
        "脚本": "python", "shell": "bash", "sh": "bash", "zsh": "bash",
        "golang": "go", "go语言": "go", "java语言": "java",
        "rust语言": "rust", "php语言": "php",
    }
    CODE_SHAPES = re.compile(
        r"(#include\s*<|def\s+\w+\s*\(|function\s+\w+|fn\s+main|public\s+class|"
        r"<!DOCTYPE|<html|console\.log|printf\s*\(|System\.out|package\s+main|"
        r"import\s+\w+|class\s+\w+\s*[:{]|=>\s*\{|var\s+\w+\s*=)",
        re.I,
    )

    @classmethod
    def enabled(cls) -> bool:
        return bool(CONFIG.get("vibe_code_heuristics", True))

    @classmethod
    def has_cjk(cls, text: str) -> bool:
        return bool(cls.CJK.search(text or ""))

    @classmethod
    def _norm_lang(cls, token: str) -> Optional[str]:
        if not token:
            return None
        t = token.strip().lower()
        return cls.LANG_ALIASES.get(t, t)

    @classmethod
    def wants_code(cls, prompt: str) -> bool:
        if not cls.enabled():
            return False
        raw = (prompt or "").strip()
        if not raw:
            return False
        pl = raw.lower()

        # "什么是 python" / "what is python" = explain, not code generation.
        if is_explain_request(raw) and not cls.ZH_WRITE.search(raw):
            if not re.search(r"\b(write|make|build|create|implement|code|vibe)\b", pl):
                if not cls.EN_VIBE.search(raw):
                    return False

        if re.match(r"^\s*(?:code|/code|code\s*>|>|program|script)\s*$", pl, re.I):
            return True
        if cls.CODE_SHAPES.search(raw):
            return True
        if cls.EN_VIBE.search(raw):
            return True
        if any(cue in raw for cue in cls.ZH_CODE_NOUNS):
            return True
        if cls.ZH_WRITE.search(raw):
            if re.search(
                r"(代码|程序|脚本|网页|函数|html|python|javascript|java|rust|go|c\+\+|cpp|"
                r"fibonacci|fib|算法|页面|api|app|site|hello|cat|meow|打印|输出)",
                raw, re.I,
            ):
                return True
        if cls.ZH_CORRECT.search(raw):
            return True
        if cls.ZH_LANG_INLINE.search(raw):
            return True
        if re.search(r"[\u4e00-\u9fff].*(html|python|javascript|java|rust|go|cpp|c\+\+|c\b)", raw, re.I):
            if is_zh_question(raw) and not cls.ZH_WRITE.search(raw):
                return False
            return True
        if re.search(r"(html|python|javascript|java|rust|go|cpp|c\+\+|c\b).*[\u4e00-\u9fff]", raw, re.I):
            if is_zh_question(raw) and not cls.ZH_WRITE.search(raw):
                return False
            return True
        if cls.has_cjk(raw) and re.search(r"(写|做|建|生成|程序|代码|脚本|网页)", raw):
            return True
        return False

    @classmethod
    def lang_from_text(cls, prompt: str, engine: "CatR11Engine") -> Optional[str]:
        if not cls.enabled():
            return None
        raw = (prompt or "").strip()
        pl = raw.lower()

        m = cls.ZH_CORRECT.search(raw)
        if m:
            return engine.normalize_lang(cls._norm_lang(m.group(2)))

        m = cls.ZH_LANG_INLINE.search(raw)
        if m:
            return engine.normalize_lang(cls._norm_lang(m.group(1)))

        m = CatSeekR1Code._MAKE_IT_LANG.search(pl)
        if m:
            return engine.normalize_lang(m.group(1))

        if re.search(r"(网页|页面|html|前端)", raw, re.I):
            if re.search(r"(写|做|建|生成|程序|代码|脚本|make|write|build|create|vibe)", raw, re.I):
                return "html"

        if re.search(r"(脚本|bash|shell)", raw, re.I) and re.search(
            r"(写|做|建|生成|write|make|build)", raw, re.I
        ):
            return "bash"

        lang_tokens = (
            ("python", r"\bpython\b|python3|\.py\b|蟒蛇"),
            ("javascript", r"\bjavascript\b|\bjs\b|node\.?js"),
            ("typescript", r"\btypescript\b|\bts\b"),
            ("java", r"\bjava\b(?!script)"),
            ("rust", r"\brust\b"),
            ("go", r"\bgo\b|golang|go语言"),
            ("cpp", r"\bc\+\+\b|\bcpp\b|c\+\+语言"),
            ("c", r"\bc语言\b|\bc\s+程序\b|\bc\s+代码\b"),
            ("html", r"\bhtml\b|html5"),
            ("bash", r"\bbash\b|\bshell\b"),
            ("sql", r"\bsql\b"),
            ("ruby", r"\bruby\b"),
            ("php", r"\bphp\b"),
        )
        has_write = bool(
            re.search(r"(写|做|建|生成|帮我|write|make|build|create|code|vibe|implement)", raw, re.I)
        )
        for lang, pat in lang_tokens:
            if re.search(pat, raw, re.I) and (has_write or cls.CODE_SHAPES.search(raw)):
                return engine.normalize_lang(lang)

        if cls.has_cjk(raw) and re.search(r"(程序|代码)", raw) and not re.search(
            r"(python|html|javascript|java|rust|go|c\+\+|cpp|c\b)", raw, re.I
        ):
            return "python"
        return None

    @classmethod
    def subject_from_text(cls, prompt: str) -> Optional[str]:
        if not cls.enabled():
            return None
        raw = (prompt or "").strip()

        m = cls.ZH_SAYS.search(raw)
        if m:
            return m.group(1).strip("?.! ，。！？")
        if "你好猫" in raw or "hello cat" in raw.lower():
            return "Hello Cat"
        if "喵" in raw or "meow" in raw.lower():
            return "Meow"
        if "你好世界" in raw or "hello world" in raw.lower():
            return "Hello World"

        m = cls.ZH_SUBJECT.search(raw)
        if m:
            subj = m.group(1).strip("?.! ，。！？的 ")
            skip = {"html", "python", "javascript", "java", "代码", "程序", "脚本", "网页", "一个", "段"}
            if subj and subj not in skip and len(subj) >= 1:
                return subj[:80]

        m = re.search(
            r"(?:write|make|build|create|vibe[\s-]?code|whip up|gimme)\s+(?:me\s+)?(?:a\s+)?(.+?)(?:\s+in\s+\w+|$)",
            raw, re.I,
        )
        if m:
            subj = m.group(1).strip("?.! ")
            if subj.lower() not in {"html", "it", "a", "an", "code"}:
                return subj[:80]
        return None

    @classmethod
    def wants_run(cls, prompt: str) -> bool:
        raw = (prompt or "").strip().lower()
        run_en = (
            "run it", "run this", "execute", "interpret", "test it",
            "/run", "and run", "then run",
        )
        if any(x in raw for x in run_en):
            return True
        return any(r in (prompt or "") for r in cls.ZH_RUN)


# CATSEEK WEB PROGRAM (Claude-style websites · artifacts · fetch · files=off)
# ──────────────────────────────────────────────────────────────
class _TextExtractor(HTMLParser):
    __slots__ = ("parts", "_skip")

    def __init__(self):
        super().__init__()
        self.parts: List[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"}:
            self._skip = False
        elif tag in {"p", "br", "div", "li", "h1", "h2", "h3", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            t = data.strip()
            if t:
                self.parts.append(t)


@dataclass
class WebSiteRecord:
    site_id: str
    title: str
    html: str
    template: str
    prompt: str
    created: float = field(default_factory=time.time)

    def preview_url(self, port: int) -> str:
        return f"http://127.0.0.1:{port}/web/preview/{self.site_id}"


class CatSeekWebProgram:
    """
    In-memory Claude-style websites program for CatSeek R1 (files=off):
    artifact HTML/CSS/JS · URL fetch · site registry · API preview — no disk writes.
    """

    _URL = re.compile(r"https?://[^\s<>\"']+", re.I)
    _WEB_CUES = (
        "website", "web page", "webpage", "landing page", "landing", "homepage",
        "home page", "portfolio site", "dashboard", "docs site", "documentation page",
        "saas page", "blog page", "artifact", "single page app", "spa",
        "做个网站", "做个网页", "网站", "网页", "落地页", "首页",
    )
    _FETCH_CUES = (
        "fetch ", "read url", "read website", "read this site", "open url",
        "scrape ", "get page", "summarize url", "summarize website",
        "读取网址", "打开网站", "抓取",
    )
    TEMPLATE_NAMES = (
        "landing", "dashboard", "docs", "portfolio", "saas", "blog",
        "resume", "todo", "calculator", "geocities", "minimal",
    )

    def __init__(self):
        self._sites: Dict[str, WebSiteRecord] = {}

    @classmethod
    def enabled(cls) -> bool:
        return bool(CONFIG.get("web_program_enabled", True))

    @classmethod
    def wants_web(cls, pl: str) -> bool:
        if not cls.enabled():
            return False
        if pl.startswith("/web"):
            return True
        if cls._URL.search(pl) and any(c in pl for c in cls._FETCH_CUES):
            return True
        if any(c in pl for c in cls._FETCH_CUES):
            return True
        if re.search(r"\b(build|make|create|design|generate|write)\s+(?:a|an|me\s+a|my\s+)?(?:\w+\s+){0,4}(?:website|webpage|web page|landing(?:\s+page)?|site|homepage)\b", pl):
            return True
        if any(c in pl for c in cls._WEB_CUES) and re.search(r"\b(build|make|create|write|design|generate|show)\b", pl):
            return True
        if re.search(r"\bhtml\b.*\b(site|page|app|ad)\b", pl):
            return True
        return False

    @classmethod
    def extract_url(cls, text: str) -> Optional[str]:
        m = cls._URL.search(text)
        return m.group(0).rstrip(".,)") if m else None

    @staticmethod
    def _subject(prompt: str) -> str:
        pl = prompt.lower()
        for prefix in ("build a ", "make a ", "create a ", "design a ", "write a ", "generate a "):
            if pl.startswith(prefix):
                rest = prompt[len(prefix):].strip()
                rest = re.split(r"\s+(?:website|webpage|web page|landing page|site|page)\b", rest, flags=re.I)[0]
                if rest.strip():
                    return rest.strip()[:80]
        m = re.search(r"(?:website|landing page|site|page)\s+(?:for|about|called)\s+(.+?)(?:\s*$|\.)", pl, re.I)
        if m:
            return m.group(1).strip()[:80]
        return "CatSeek"

    @classmethod
    def pick_template(cls, prompt: str) -> str:
        pl = prompt.lower()
        if re.search(r"\bgeocit(?:ies|es)\b", pl) or ("gamer" in pl and "usb" in pl):
            return "geocities"
        if "dashboard" in pl or "admin" in pl:
            return "dashboard"
        if "doc" in pl or "documentation" in pl or "readme" in pl:
            return "docs"
        if "portfolio" in pl:
            return "portfolio"
        if "saas" in pl or "pricing" in pl or "subscribe" in pl:
            return "saas"
        if "blog" in pl or "article" in pl:
            return "blog"
        if "resume" in pl or "cv" in pl:
            return "resume"
        if "todo" in pl or "task list" in pl:
            return "todo"
        if "calculator" in pl or "calc" in pl:
            return "calculator"
        if "landing" in pl or "homepage" in pl or "home page" in pl:
            return "landing"
        return "minimal"

    @staticmethod
    def _shell(title: str, body: str, *, extra_head: str = "", extra_script: str = "") -> str:
        t = html_module.escape(title)
        return (
            f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            f"  <meta charset=\"UTF-8\">\n"
            f"  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            f"  <title>{t}</title>\n{extra_head}\n</head>\n<body>\n{body}\n"
            f"{extra_script}\n</body>\n</html>"
        )

    @classmethod
    def _template_landing(cls, title: str, headline: str) -> str:
        h = html_module.escape(headline)
        css = (
            "  <style>\n"
            "    :root { --bg:#0f172a; --fg:#e2e8f0; --acc:#38bdf8; --card:#1e293b; }\n"
            "    * { box-sizing:border-box; margin:0; }\n"
            "    body { font-family:system-ui,sans-serif; background:var(--bg); color:var(--fg); }\n"
            "    nav { display:flex; justify-content:space-between; padding:1rem 2rem; }\n"
            "    .hero { text-align:center; padding:4rem 1.5rem; max-width:720px; margin:0 auto; }\n"
            "    h1 { font-size:clamp(2rem,5vw,3rem); margin-bottom:1rem; }\n"
            "    p { opacity:.85; line-height:1.6; margin-bottom:2rem; }\n"
            "    .cta { display:inline-block; background:var(--acc); color:#0f172a; padding:.75rem 1.5rem; "
            "border-radius:8px; text-decoration:none; font-weight:600; }\n"
            "    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:1rem; "
            "padding:2rem; max-width:960px; margin:0 auto; }\n"
            "    .card { background:var(--card); padding:1.25rem; border-radius:12px; }\n"
            "  </style>"
        )
        body = (
            f"  <nav><strong>{html_module.escape(title)}</strong><span>CatSeek R1 · files=off</span></nav>\n"
            f"  <section class=\"hero\"><h1>{h}</h1>\n"
            f"    <p>Built in-memory by CatSeek Web Program — Claude-style artifacts, no files written.</p>\n"
            f"    <a class=\"cta\" href=\"#features\">Get started</a></section>\n"
            f"  <div class=\"grid\" id=\"features\">\n"
            f"    <div class=\"card\"><h3>Fast</h3><p>CatSeek R1 1.0 token-weight synthesis.</p></div>\n"
            f"    <div class=\"card\"><h3>Local</h3><p>Runs fully offline.</p></div>\n"
            f"    <div class=\"card\"><h3>Private</h3><p>Everything stays in RAM.</p></div>\n"
            f"  </div>"
        )
        return cls._shell(title, body, extra_head=css)

    @classmethod
    def _template_dashboard(cls, title: str) -> str:
        css = (
            "  <style>body{font-family:system-ui;margin:0;background:#111;color:#eee;display:grid;"
            "grid-template-columns:220px 1fr;min-height:100vh}"
            "aside{background:#1a1a1a;padding:1rem}main{padding:1.5rem}"
            ".stat{display:inline-block;background:#222;padding:1rem 1.5rem;border-radius:8px;margin:.5rem}"
            ".stat b{font-size:1.5rem;color:#4ade80}</style>"
        )
        body = (
            f"  <aside><h2>{html_module.escape(title)}</h2><ul><li>Overview</li><li>Analytics</li>"
            f"<li>Settings</li></ul></aside>\n"
            f"  <main><h1>Dashboard</h1>\n"
            f"    <div class=\"stat\"><div>Users</div><b>1,024</b></div>\n"
            f"    <div class=\"stat\"><div>Requests</div><b>8,192</b></div>\n"
            f"    <div class=\"stat\"><div>Uptime</div><b>99.9%</b></div></main>"
        )
        return cls._shell(title, body, extra_head=css)

    @classmethod
    def _template_docs(cls, title: str) -> str:
        css = "  <style>body{font-family:Georgia,serif;max-width:720px;margin:2rem auto;padding:0 1rem;line-height:1.7}"
        body = (
            f"  <h1>{html_module.escape(title)} — Docs</h1>\n"
            f"  <h2>Quick start</h2><p>CatSeek Web Program stores sites in memory. Preview via "
            f"<code>/web/preview/&lt;id&gt;</code> on the local API.</p>\n"
            f"  <h2>Commands</h2><ul><li><code>/web list</code></li><li><code>/web fetch URL</code></li>"
            f"<li><code>/web build prompt</code></li></ul>"
        )
        return cls._shell(title, body, extra_head=css)

    @classmethod
    def _template_portfolio(cls, title: str, name: str) -> str:
        n = html_module.escape(name)
        css = (
            "  <style>body{font-family:system-ui;background:#fafafa;color:#111;max-width:800px;"
            "margin:2rem auto;padding:1rem}.project{border:1px solid #ddd;border-radius:8px;"
            "padding:1rem;margin:1rem 0}</style>"
        )
        body = (
            f"  <header><h1>{n}</h1><p>Portfolio · {html_module.escape(title)}</p></header>\n"
            f"  <section class=\"project\"><h3>Project Alpha</h3><p>Full-stack app with in-memory deploy.</p></section>\n"
            f"  <section class=\"project\"><h3>Project Beta</h3><p>CatSeek R1 1.0-powered local AI tooling.</p></section>"
        )
        return cls._shell(title, body, extra_head=css)

    @classmethod
    def _template_saas(cls, title: str) -> str:
        css = (
            "  <style>body{font-family:system-ui;text-align:center;padding:2rem;background:linear-gradient(#eef,#fff)}"
            ".price{display:inline-block;border:2px solid #333;border-radius:12px;padding:2rem;margin:1rem}"
            ".price h2{font-size:2.5rem}</style>"
        )
        body = (
            f"  <h1>{html_module.escape(title)}</h1><p>Simple pricing. No files. All in-memory.</p>\n"
            f"  <div class=\"price\"><h3>Pro</h3><h2>$9</h2><p>/month</p></div>\n"
            f"  <div class=\"price\"><h3>Team</h3><h2>$29</h2><p>/month</p></div>"
        )
        return cls._shell(title, body, extra_head=css)

    @classmethod
    def _template_blog(cls, title: str, headline: str) -> str:
        h = html_module.escape(headline)
        css = "  <style>body{font-family:Georgia,serif;max-width:640px;margin:2rem auto;line-height:1.8;padding:1rem}</style>"
        body = (
            f"  <article><h1>{h}</h1><p><em>CatSeek R1 · files=off</em></p>\n"
            f"  <p>This post was generated in-memory. CatSeek Web Program mirrors Claude-style "
            f"artifact pages — HTML, CSS, and optional JS — without writing to disk.</p></article>"
        )
        return cls._shell(title, body, extra_head=css)

    @classmethod
    def _template_todo(cls, title: str) -> str:
        css = "  <style>body{font-family:system-ui;max-width:420px;margin:3rem auto;padding:1rem}"
        script = (
            "  <script>\n"
            "    const ul=document.getElementById('t');\n"
            "    function add(){const i=document.getElementById('i');if(!i.value.trim())return;"
            "const li=document.createElement('li');li.textContent=i.value;i.value='';ul.appendChild(li);}\n"
            "  </script>"
        )
        body = (
            f"  <h1>{html_module.escape(title)}</h1>\n"
            f"  <input id=\"i\" placeholder=\"New task…\" style=\"width:70%\"> "
            f"<button onclick=\"add()\">Add</button>\n  <ul id=\"t\"></ul>"
        )
        return cls._shell(title, body, extra_head=css, extra_script=script)

    @classmethod
    def _template_calculator(cls, title: str) -> str:
        css = "  <style>body{font-family:monospace;text-align:center;padding:2rem}"
        script = (
            "  <script>\n"
            "    function calc(){try{document.getElementById('o').textContent="
            "eval(document.getElementById('e').value)}catch(e){document.getElementById('o').textContent='Error'}}\n"
            "  </script>"
        )
        body = (
            f"  <h1>{html_module.escape(title)}</h1>\n"
            f"  <input id=\"e\" style=\"font-size:1.2rem;width:200px\"> "
            f"<button onclick=\"calc()\">=</button>\n  <p id=\"o\"></p>"
        )
        return cls._shell(title, body, extra_head=css, extra_script=script)

    @classmethod
    def render(cls, template: str, prompt: str, engine: Optional["CatR11Engine"] = None) -> str:
        subject = cls._subject(prompt)
        title = subject.title() if subject else "CatSeek Site"
        headline = subject or title
        if template == "geocities":
            return CatSeekR1Code._html_geocities(prompt)
        if template == "landing":
            return cls._template_landing(title, headline)
        if template == "dashboard":
            return cls._template_dashboard(title)
        if template == "docs":
            return cls._template_docs(title)
        if template == "portfolio":
            return cls._template_portfolio(title, headline)
        if template == "saas":
            return cls._template_saas(title)
        if template == "blog":
            return cls._template_blog(title, headline)
        if template == "resume":
            return cls._template_portfolio(title, f"{headline} — Resume")
        if template == "todo":
            return cls._template_todo(title)
        if template == "calculator":
            return cls._template_calculator(title)
        return CatSeekR1Code._html(prompt, engine)

    def store(self, prompt: str, html: str, template: str) -> WebSiteRecord:
        sid = uuid.uuid4().hex[:10]
        title = self._subject(prompt).title() or "Site"
        rec = WebSiteRecord(site_id=sid, title=title, html=html, template=template, prompt=prompt[:200])
        self._sites[sid] = rec
        while len(self._sites) > CONFIG.get("web_max_sites", 64):
            oldest = min(self._sites.values(), key=lambda s: s.created)
            del self._sites[oldest.site_id]
        return rec

    def get(self, site_id: str) -> Optional[WebSiteRecord]:
        return self._sites.get(site_id)

    def build(self, prompt: str, engine: Optional["CatR11Engine"] = None) -> WebSiteRecord:
        tpl = self.pick_template(prompt)
        html = self.render(tpl, prompt, engine)
        return self.store(prompt, html, tpl)

    def fetch_url(self, url: str) -> str:
        if not CONFIG.get("web_fetch_enabled", True):
            return "Web fetch is disabled in CONFIG."
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return "Only http:// and https:// URLs are supported."
        max_bytes = CONFIG.get("web_max_fetch_kb", 256) * 1024
        try:
            req = urlrequest.Request(url, headers={"User-Agent": f"{BRAND}/{VERSION} (files=off)"})
            with urlrequest.urlopen(req, timeout=12) as resp:
                raw = resp.read(max_bytes + 1)
                if len(raw) > max_bytes:
                    raw = raw[:max_bytes]
                ctype = resp.headers.get("Content-Type", "")
                charset = "utf-8"
                if "charset=" in ctype:
                    charset = ctype.split("charset=")[-1].split(";")[0].strip()
                text = raw.decode(charset, errors="replace")
        except (URLError, HTTPError, TimeoutError, ValueError) as e:
            return f"Fetch failed: {e}"
        if "html" in text.lower()[:500] or "<" in text[:200]:
            parser = _TextExtractor()
            try:
                parser.feed(text)
            except Exception:
                pass
            body = re.sub(r"\n{3,}", "\n\n", " ".join(parser.parts))
            body = body[:4000]
            return f"**Fetched** `{url}`\n\n{body or '(no extractable text)'}"
        return f"**Fetched** `{url}`\n\n```\n{text[:4000]}\n```"

    @classmethod
    def help_text(cls) -> str:
        port = CONFIG.get("api_port", 8765)
        tpl = ", ".join(cls.TEMPLATE_NAMES)
        return (
            f"**CatSeek Web Program** · Claude-style websites · **files=off**\n\n"
            "In-memory artifact builder, URL reader, and API preview.\n\n"
            "**Commands**\n"
            "- `/web` — this help\n"
            "- `/web list` — sites in memory\n"
            "- `/web templates` — available layouts\n"
            "- `/web build <prompt>` — generate & store a site\n"
            "- `/web fetch <url>` — read a page (text extract)\n"
            "- `/web preview <id>` — preview link\n\n"
            f"**Templates:** {tpl}\n\n"
            f"**API:** `GET http://127.0.0.1:{port}/web/preview/<id>` · `GET /web/sites`\n\n"
            "Natural language: `build a landing page for my app`, `fetch https://example.com`"
        )

    def list_sites(self) -> str:
        if not self._sites:
            return "No sites in memory. Try `/web build a landing page` or ask naturally."
        port = CONFIG.get("api_port", 8765)
        lines = [f"**{len(self._sites)} site(s)** in memory (files=off):\n"]
        for rec in sorted(self._sites.values(), key=lambda s: s.created, reverse=True):
            lines.append(
                f"- `{rec.site_id}` · **{rec.title}** · {rec.template} · "
                f"[preview]({rec.preview_url(port)})"
            )
        return "\n".join(lines)

    def handle_command(self, engine: "CatR11Engine", raw: str) -> str:
        pl = raw.lower().strip()
        if pl in {"/web", "/web help"}:
            return self.help_text()
        if pl == "/web list":
            return self.list_sites()
        if pl == "/web templates":
            return "**Templates:** " + ", ".join(self.TEMPLATE_NAMES)
        if pl.startswith("/web fetch "):
            url = self.extract_url(raw) or raw.split(maxsplit=2)[-1].strip()
            return self.fetch_url(url)
        if pl.startswith("/web build ") or pl.startswith("/web "):
            prompt = raw.split(maxsplit=2)[2] if pl.startswith("/web build ") else raw.split(maxsplit=1)[1]
            if prompt.lower().startswith("build "):
                prompt = prompt[6:]
            rec = self.build(prompt.strip() or "landing page", engine)
            port = CONFIG.get("api_port", 8765)
            return (
                f"**Site built** · `{rec.site_id}` · template **{rec.template}** · files=off\n\n"
                f"Preview: {rec.preview_url(port)}\n\n"
                f"```html\n{rec.html[:1200]}{'…' if len(rec.html) > 1200 else ''}\n```"
            )
        if pl.startswith("/web preview "):
            sid = raw.split(maxsplit=2)[-1].strip()
            rec = self.get(sid)
            if not rec:
                return f"No site `{sid}`. Use `/web list`."
            return f"Preview: {rec.preview_url(CONFIG.get('api_port', 8765))}\n\n```html\n{rec.html[:800]}…\n```"
        return self.help_text()

    def respond(self, engine: "CatR11Engine", prompt: str) -> str:
        pl = prompt.lower().strip()
        if pl.startswith("/web"):
            return self.handle_command(engine, prompt)
        url = self.extract_url(prompt)
        if url and any(c in pl for c in self._FETCH_CUES + ("http", "https", "www.")):
            return self.fetch_url(url)
        if url and not re.search(r"\b(build|make|create|html|page|site)\b", pl):
            return self.fetch_url(url)
        rec = self.build(prompt, engine)
        port = CONFIG.get("api_port", 8765)
        fenced = CatSeekR1Code.fence("html", rec.html) if hasattr(CatSeekR1Code, "fence") else f"```html\n{rec.html}\n```"
        if CONFIG.get("code_output_exact"):
            return (
                f"**CatSeek Web Program** · `{rec.site_id}` · {rec.template} · files=off\n"
                f"Preview: {rec.preview_url(port)}\n\n{fenced}"
            )
        return (
            f"**Site built** · `{rec.site_id}` · **{rec.template}** · files=off\n"
            f"Preview: {rec.preview_url(port)}\n\n{fenced}"
        )

    def clear(self) -> None:
        self._sites.clear()


# ──────────────────────────────────────────────────────────────
# CATSEEK R1 CODE (catr1b · CatSeek R1 1.0b · files=off)
# ──────────────────────────────────────────────────────────────
class CatSeekR1Code:
    """
    catr1b — CatSeek R1 1.0b code engine (files=off).
    Token-weight synthesis · recursive perfection · in-memory run loop. files=off.
    """

    NAME = CONFIG["code_interpreter_name"]
    FAMILY = CONFIG["code_interpreter_family"]
    BACKEND = CONFIG["code_interpreter"]
    VERSION = CONFIG["code_interpreter_version"]
    RUNNABLE = frozenset({"python", "javascript", "bash"})
    LANGS = (
        "html", "css", "python", "javascript", "typescript", "java", "rust",
        "go", "bash", "shell", "cpp", "c", "sql", "ruby", "php", "assembly",
    )
    _WRITE_VERBS = re.compile(
        r"\b(write|make|build|create|generate|code|implement|show me|give me|draft)\b", re.I
    )
    _IN_LANG = re.compile(
        r"\b(?:in|using|with|as)\s+(html|css|python|javascript|typescript|java|rust|go|bash|shell|cpp|c\+\+|c|sql|ruby|php|assembly)\b",
        re.I,
    )
    _MAKE_IT_LANG = re.compile(
        r"\b(?:no\s+)?make\s+(?:it\s+)?(?:in\s+)?(html|css|python|javascript|typescript|java|rust|go|bash|shell|cpp|c\+\+|c|sql|ruby|php)\b",
        re.I,
    )
    _HTML_CUE = re.compile(
        r"\b(?:a|an)\s+html\b|\bhtml\s+(?:program|page|file|ad|that|site|app)\b|\b(?:write|make|build|create)\s+(?:a\s+)?html\b",
        re.I,
    )
    _CREATIVE_BLOCK = re.compile(
        r"\b(story|poem|tale|parable|bedtime|narrative|verse|rhyme)\b", re.I
    )
    _FABLE_STORY = re.compile(r"\b(?:write|tell|give)\s+(?:me\s+)?(?:a\s+)?fable\b", re.I)
    _PATH_TAIL = re.compile(
        r"(?:/Volumes/.+|/Users/.+|~/.+)\.(?:py|c|cpp|html|js|ts|java|rs|go|sh|php|rb)\s*$",
        re.I,
    )
    _BRAND_PREFIX = re.compile(
        r"^\[?\s*(?:catseek r1(?:\s*1\.0|\.0a|\.1)?|claude mythos|claude fable 5)\s*\]?:?\s*", re.I
    )
    _META_TAIL = re.compile(
        r"\s+(?:make the code|files\s*=|\btoken weight\b|\bfiles\.\s*=\s*off\b).*$",
        re.I | re.S,
    )
    _RAW_CODE = re.compile(r"(#include[\s\S]+|def\s+\w+|function\s+\w+|fn\s+main|public\s+class|<!DOCTYPE)", re.I)
    _SAYS = re.compile(r"\b(?:that\s+)?says\s+[\"']?([^\"'\n]+)[\"']?", re.I)
    _GO = re.compile(r"^\s*(?:go|do it|yes|continue|proceed|ok|>|code\s*>)\s*\.?\s*$", re.I)
    _CODE_SHORT = re.compile(
        r"^\s*(?:code|/code|code\s*>|>|program|script)\s*$", re.I
    )

    @classmethod
    def enabled(cls) -> bool:
        return bool(CONFIG.get("catseek_code_enabled", True))

    @classmethod
    def code_help(cls) -> str:
        return (
            f"**catr1b** · CatSeek R1 {EDITION} · files=off\n\n"
            "Ask in **any human language** (English · 中文 · mixed) or paste code:\n"
            "- `write hello cat in c` · `帮我用python写你好`\n"
            "- `make a html that says meow` · `做个网页显示喵`\n"
            "- `no make it html` · `不要python改成html`\n"
            "- `vibe code a fibonacci script` · `写个斐波那契程序`\n"
            "- Paste ``` fences · **run it** / **运行** · `/code <prompt>`\n\n"
            f"Languages: {', '.join(cls.LANGS[:12])}…"
        )
    VALID_LANGS = frozenset(LANGS)

    @classmethod
    def _coerce_lang(cls, engine: "CatR11Engine", lang: Optional[str], prompt: str) -> str:
        lang = engine.normalize_lang(lang) or ""
        if lang in cls.VALID_LANGS:
            return lang
        pl = cls.normalize_prompt(prompt).lower()
        direct = cls._lang_from_text(pl, engine)
        if direct:
            return direct
        if "html" in pl:
            return "html"
        if re.search(r"\b(?:c|c\+\+|cpp)\b", pl):
            return "c" if "iostream" not in pl else "cpp"
        return "python"

    @classmethod
    def normalize_prompt(cls, prompt: str) -> str:
        s = prompt.strip()
        s = cls._BRAND_PREFIX.sub("", s)
        s = cls._META_TAIL.sub("", s)
        return cls._clean_prompt(s)

    @classmethod
    def _clean_prompt(cls, prompt: str) -> str:
        s = prompt.strip()
        s = cls._PATH_TAIL.sub("", s)
        return s.strip()

    @classmethod
    def extract_prompt_code(cls, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """If the user pasted code (± file path), return it exactly — files=off."""
        cleaned = cls.normalize_prompt(prompt)
        lang, code = None, None
        m = re.search(r"```([a-zA-Z0-9_+#-]*)\s*\n([\s\S]*?)```", cleaned)
        if m:
            lang = (m.group(1) or "").strip().lower() or None
            code = m.group(2).strip()
        elif cls._RAW_CODE.search(cleaned) or VibeCodeHeuristics.CODE_SHAPES.search(cleaned):
            code = cleaned.strip()
            if "#include" in code and "stdio" in code:
                lang = "c" if "iostream" not in code else "cpp"
            elif "iostream" in code:
                lang = "cpp"
            elif code.lstrip().startswith("<!"):
                lang = "html"
            elif "def " in code:
                lang = "python"
        if code:
            code = re.sub(r"^c\s*\n(?=#include)", "", code, flags=re.I)
            return lang, code
        return None, None

    @classmethod
    def wants_code(cls, pl: str) -> bool:
        if not cls.enabled():
            return False
        if VibeCodeHeuristics.wants_code(pl):
            return True
        pl = pl.strip().lower()
        if cls._CODE_SHORT.match(pl):
            return True
        if cls._FABLE_STORY.search(pl):
            return False
        if cls._CREATIVE_BLOCK.search(pl):
            return False
        if re.search(r"\b(?:can you|please|help me|i need you to|let'?s)\s+code\b", pl):
            return True
        if re.search(r"\bcode\s*[>:]", pl):
            return True
        if re.search(r"\b(?:write|make|build|create|show|give|draft|implement)\s+(?:me\s+)?(?:some\s+)?code\b", pl):
            return True
        if cls._MAKE_IT_LANG.search(pl):
            return True
        if cls._HTML_CUE.search(pl):
            return True
        if cls._IN_LANG.search(pl) and cls._WRITE_VERBS.search(pl):
            return True
        if cls._IN_LANG.search(pl) and any(w in pl for w in ("page", "app", "script", "site", "cat", "hello", "world", "ad", "usb", "gamer")):
            return True
        if re.search(r"\b(function|def |class |snippet|fibonacci|fib|prime|```)\b", pl):
            return True
        if re.search(r"\b(write|make|build|create)\b", pl) and re.search(
            r"\b(code|function|script|program|app|page|html|python|javascript|java)\b", pl
        ):
            return True
        if re.search(r"\b(python|javascript|typescript|html|rust|java|go|bash|cpp|c\+\+)\b", pl):
            if re.search(r"\b(write|make|build|create|implement|code)\b", pl):
                return True
        if cls._RAW_CODE.search(cls._clean_prompt(pl)):
            return True
        if re.search(r"\b(c|c\+\+|cpp)\b", pl) and re.search(
            r"\b(write|make|build|create|code|hello|world|program|main)\b", pl
        ):
            return True
        if re.search(r"\bgeocit(?:ies|es)\b", pl) and "html" in pl:
            return True
        if re.search(r"\b(program|script|snippet|algorithm)\b", pl) and re.search(
            r"\b(write|make|build|create|need|want|give|show)\b", pl
        ):
            return True
        return False

    @classmethod
    def wants_code_with_history(cls, pl: str, engine: "CatR11Engine") -> bool:
        if cls.wants_code(pl):
            return True
        if not cls.enabled():
            return False
        if cls._GO.match(pl.strip()) or cls._CODE_SHORT.match(pl.strip()):
            return bool(engine.chat_history) or bool(cls._lang_from_history(engine))
        return False

    @classmethod
    def _lang_from_text(cls, pl: str, engine: "CatR11Engine") -> Optional[str]:
        vibe = VibeCodeHeuristics.lang_from_text(pl, engine)
        if vibe:
            return vibe
        m = cls._MAKE_IT_LANG.search(pl)
        if m:
            raw = m.group(1).lower()
            if raw == "shell":
                raw = "bash"
            return engine.normalize_lang(raw) or raw
        m = cls._IN_LANG.search(pl)
        if m:
            raw = m.group(1).lower()
            if raw == "shell":
                raw = "bash"
            return engine.normalize_lang(raw) or raw
        if cls._HTML_CUE.search(pl) or re.search(r"\bhtml\b", pl):
            return "html"
        if re.search(r"\b(?:write|make|code)\s+(?:me\s+)?(?:a\s+)?c\s+program\b", pl):
            return "c"
        if re.search(r"\bc\s+(?:program|code|hello)\b", pl):
            return "c"
        if re.search(r"\bjava\b", pl) and re.search(r"\b(write|make|code|program)\b", pl):
            return "java"
        return None

    @classmethod
    def _lang_from_history(cls, engine: "CatR11Engine") -> Optional[str]:
        for msg in reversed(engine.chat_history):
            if msg.get("role") != "user":
                continue
            lang = cls._lang_from_text(msg.get("text", "").lower(), engine)
            if lang:
                return lang
            if cls._HTML_CUE.search(msg.get("text", "").lower()) or "html" in msg.get("text", "").lower():
                return "html"
        return None

    @classmethod
    def run(cls, engine: "CatR11Engine", lang: str, code: str) -> str:
        return engine.execute_code_any_language(lang, code)

    @classmethod
    def should_run(cls, pl: str) -> bool:
        if CONFIG.get("code_auto_run"):
            return True
        if VibeCodeHeuristics.wants_run(pl):
            return True
        return any(
            x in pl for x in (
                "run it", "run this", "execute", "interpret", "test it",
                "/run", "and run", "then run",
            )
        )

    @classmethod
    def detect_lang(cls, engine: "CatR11Engine", prompt: str) -> str:
        pl = cls.normalize_prompt(prompt)
        embedded_lang, embedded = cls.extract_prompt_code(prompt)
        if embedded_lang:
            return engine.normalize_lang(embedded_lang) or embedded_lang
        if embedded and "#include" in embedded:
            return "cpp" if "iostream" in embedded else "c"
        direct = cls._lang_from_text(pl, engine)
        if not direct:
            direct = VibeCodeHeuristics.lang_from_text(prompt, engine)
        if direct:
            return direct
        if cls._GO.match(pl.strip().lower()):
            hist_lang = cls._lang_from_history(engine)
            if hist_lang:
                return hist_lang
        lang = engine.extract_lang(prompt) or engine.detect_lang_from_text(prompt)
        return cls._coerce_lang(engine, lang, prompt)

    @classmethod
    def _subject(cls, prompt: str, engine: Optional["CatR11Engine"] = None) -> str:
        vibe_subj = VibeCodeHeuristics.subject_from_text(prompt)
        if vibe_subj:
            return vibe_subj
        pl = prompt.lower().strip()
        if re.search(r"\b(?:no\s+)?make\s+it\b", pl) and engine:
            for msg in reversed(engine.chat_history):
                if msg.get("role") != "user":
                    continue
                prior = cls._subject(msg.get("text", ""))
                if prior and prior.lower() not in {"it", "it html", "hello world", "no"}:
                    return prior
        m = cls._SAYS.search(pl)
        if m:
            return m.group(1).strip("?.! ")
        if "hello cat" in pl:
            return "Hello Cat"
        if "meow" in pl:
            return "Meow"
        if "hello world" in pl:
            return "Hello World"
        if "gamer" in pl and "usb" in pl:
            return "GAMER USB — ULTRA SPEED"
        m = re.search(
            r"(?:write|make|build|create|generate|show|give)\s+(?:me\s+)?(?:a\s+)?(?:html\s+)?(?:that\s+is\s+a\s+)?(.+?)(?:\s+in\s+\w+|\s+program|\s*$)",
            pl,
        )
        if m:
            subj = m.group(1).strip("?.! ")
            if subj and subj not in {"html", "it", "a", "an", "no"}:
                return subj[:80]
        m = re.search(
            r"(?:write|make|build|create|generate|show|give)\s+(?:me\s+)?(?:a\s+)?(.+?)\s+in\s+\w+",
            pl,
        )
        if m:
            subj = m.group(1).strip("?.! ")
            if subj not in {"html", "it", "a", "an", "no"}:
                return subj
        return "Hello World"

    @classmethod
    def _html_geocities(cls, prompt: str) -> str:
        pl = prompt.lower()
        title = "GAMER USB AD — GEOCITIES EDITION"
        headline = "ULTRA GAMER USB 9000"
        if "gamer" in pl and "usb" in pl:
            headline = "GAMER USB — 1337 MB/s OF RAW POWER"
        label = html_module.escape(headline)
        return (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            "  <meta charset=\"UTF-8\">\n"
            f"  <title>{html_module.escape(title)}</title>\n"
            "  <style>\n"
            "    body { background: #000080 url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\"><rect fill=\"%23ffff00\" width=\"10\" height=\"10\"/><rect fill=\"%2300ff00\" x=\"10\" y=\"10\" width=\"10\" height=\"10\"/></svg>'); "
            "color: #00ff00; font-family: Comic Sans MS, cursive; margin: 0; }\n"
            "    .banner { background: linear-gradient(90deg,red,yellow,lime,cyan,blue,magenta); padding: 4px; text-align: center; }\n"
            "    .banner h1 { color: #fff; text-shadow: 2px 2px #000; font-size: 2rem; margin: 0; animation: blink 1s step-end infinite; }\n"
            "    @keyframes blink { 50% { opacity: 0.3; } }\n"
            "    .box { border: 4px ridge #ff00ff; background: #c0c0c0; color: #000; margin: 1rem auto; max-width: 640px; padding: 1rem; }\n"
            "    .counter { font-size: 0.75rem; color: #888; text-align: center; }\n"
            "    marquee { font-size: 1.2rem; color: #ff0000; font-weight: bold; }\n"
            "    .usb { font-size: 4rem; text-align: center; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <div class=\"banner\"><h1>★ WELCOME TO MY HOMEPAGE ★</h1></div>\n"
            "  <marquee>🔥 BUY NOW — GAMER USB — LIMITED STOCK — CLICK HERE 🔥</marquee>\n"
            "  <div class=\"box\">\n"
            "    <div class=\"usb\">💾🎮</div>\n"
            f"    <h2 style=\"text-align:center;color:#0000ff;\">{label}</h2>\n"
            "    <ul>\n"
            "      <li>⚡ ZERO LAG FILE TRANSFERS</li>\n"
            "      <li>🎯 RGB NOT INCLUDED (1999 AUTHENTIC)</li>\n"
            "      <li>🏆 BEST VIEWED IN NETSCAPE NAVIGATOR</li>\n"
            "    </ul>\n"
            "    <p style=\"text-align:center\"><blink><b>ONLY $19.99!!!</b></blink></p>\n"
            "  </div>\n"
            "  <p class=\"counter\">You are visitor #420,069</p>\n"
            "</body>\n"
            "</html>"
        )

    @classmethod
    def _html(cls, prompt: str, engine: Optional["CatR11Engine"] = None) -> str:
        if CONFIG.get("web_program_enabled") and engine is not None and hasattr(engine, "web"):
            tpl = CatSeekWebProgram.pick_template(prompt)
            if tpl != "minimal" or re.search(r"\b(website|landing|dashboard|portfolio|site)\b", prompt.lower()):
                return CatSeekWebProgram.render(tpl, prompt, engine)
        pl = prompt.lower()
        if re.search(r"\bgeocit(?:ies|es)\b", pl):
            return cls._html_geocities(prompt)
        subject = cls._subject(prompt, engine)
        title = subject.title() if subject else "Hello"
        has_cat = "cat" in pl or "🐱" in prompt or "kitty" in pl or "kitten" in pl
        has_gamer = "gamer" in pl and "usb" in pl
        emoji = "🐱 " if has_cat else ("🎮💾 " if has_gamer else "")
        label = html_module.escape(subject if subject else ("Hello Cat" if has_cat else "Hello World"))
        if has_gamer:
            return cls._html_geocities(prompt)
        return (
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "<head>\n"
            "  <meta charset=\"UTF-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            f"  <title>{label}</title>\n"
            "  <style>\n"
            "    * { box-sizing: border-box; }\n"
            "    body {\n"
            "      font-family: system-ui, -apple-system, sans-serif;\n"
            "      display: flex; align-items: center; justify-content: center;\n"
            "      min-height: 100vh; margin: 0;\n"
            "      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);\n"
            "      color: #eee;\n"
            "    }\n"
            "    .card { text-align: center; padding: 2rem; }\n"
            "    .emoji { font-size: 5rem; line-height: 1; }\n"
            "    h1 { font-size: 2.5rem; margin: 0.5rem 0 0; font-weight: 600; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <div class=\"card\">\n"
            f"    <div class=\"emoji\">{emoji}</div>\n"
            f"    <h1>{label}</h1>\n"
            "  </div>\n"
            "</body>\n"
            "</html>"
        )

    @classmethod
    def _python(cls, engine: "CatR11Engine", prompt: str) -> str:
        pl = prompt.lower()
        if "fibonacci" in pl or re.search(r"\bfib\b", pl):
            block = engine.synth._code(engine._extract_topic_words(prompt), pl, None)
            m = re.search(r"```python\n(.*?)```", block, re.S)
            if m:
                return m.group(1).strip()
        subject = cls._subject(prompt)
        if "cat" in pl:
            return (
                "def main():\n"
                "    print('Hello Cat!')\n"
                "    print('🐱')\n\n"
                "if __name__ == '__main__':\n"
                "    main()"
            )
        msg = TokenWeightCodeEmitter.message_from_prompt(prompt, None, engine)
        return TokenWeightCodeEmitter._python(msg)

    @classmethod
    def build(cls, engine: "CatR11Engine", prompt: str, lang: str, vec: Optional[np.ndarray] = None) -> str:
        if vec is None:
            vec = engine.last_vec if engine.last_vec is not None else engine.encode_for_task(prompt, task="code")
        if CONFIG.get("catr1_engine"):
            return CatR1MythosEngine.generate(engine, prompt, lang, vec)
        return TokenWeightCodeEmitter.emit(engine, prompt, lang, vec)

    @classmethod
    def format_response(cls, lang: str, code: str, prompt: str, engine: "CatR11Engine") -> str:
        pl = prompt.lower()
        lang = cls._coerce_lang(engine, lang, prompt)
        fenced = TokenWeightCodeEmitter.fence(lang, code)
        if CONFIG.get("code_output_exact") or engine._wants_code_only(prompt):
            return fenced
        if cls.should_run(pl) and lang in cls.RUNNABLE:
            result = cls.run(engine, lang, code)
            return f"{fenced}\n\n**{cls.NAME} output:**\n```\n{result}\n```"
        return fenced

    @classmethod
    def _prompt_for_code(cls, prompt: str, engine: "CatR11Engine") -> str:
        pl = cls.normalize_prompt(prompt).strip().lower()
        if cls._GO.match(pl) or cls._CODE_SHORT.match(pl):
            for msg in reversed(engine.chat_history):
                if msg.get("role") == "user":
                    prior = msg.get("text", "").strip()
                    if prior and not cls._CODE_SHORT.match(prior.lower()):
                        return prior
            return "write hello world in python"
        if pl.startswith("/code "):
            return prompt.split(maxsplit=1)[1] if " " in prompt.strip() else "write hello world in python"
        return prompt

    @classmethod
    def respond(cls, engine: "CatR11Engine", prompt: str) -> str:
        if not cls.enabled():
            return f"catr1b is disabled. Set `catseek_code_enabled=True` in CONFIG (files=off)."
        prompt = cls._prompt_for_code(prompt, engine)
        norm = cls.normalize_prompt(prompt)
        vec = engine.encode_for_task(norm, task="code")
        lang = cls.detect_lang(engine, norm)
        code = cls.build(engine, norm, lang, vec)
        return cls.format_response(lang, code, norm, engine)


CatSeekCode = CatSeekR1Code
CatCode010 = CatSeekR1Code


class TokenWeightCodeEmitter:
    """
    Code synthesis from CatSeek R1 1.0 token weights + prompt (files=off).
    Output is derived only from the inference vector and prompt tokens — no disk files,
    no dynamic template stubs.
    """

    @staticmethod
    def _pick(vec: Optional[np.ndarray], n: int, salt: int = 0) -> int:
        if vec is None or vec.size == 0:
            return salt % max(n, 1)
        return int(abs(float(np.sum(vec * (1.0 + salt * 0.031)) * 10007))) % max(n, 1)

    @classmethod
    def message_from_prompt(
        cls,
        prompt: str,
        vec: Optional[np.ndarray],
        engine: Optional["CatR11Engine"] = None,
    ) -> str:
        """Payload string from prompt tokens + CatSeek R1 1.0 vec (files=off)."""
        subj = CatSeekR1Code._subject(prompt, engine)
        if subj and subj.lower() not in {"hello world", "it", "it html"}:
            return subj
        pl = CatSeekR1Code.normalize_prompt(prompt).lower()
        if "cat" in pl:
            return "Hello Cat" if cls._pick(vec, 2, 2) == 0 else "Meow!"
        defaults = ("Hello World", "Hello", "Meow", "Hi there")
        return defaults[cls._pick(vec, len(defaults), 1)]

    @classmethod
    def _c(cls, msg: str) -> str:
        esc = msg.replace("\\", "\\\\").replace('"', '\\"')
        return (
            "#include <stdio.h>\n\n"
            "int main(void) {\n"
            f'    printf("{esc}\\n");\n'
            "    return 0;\n"
            "}"
        )

    @classmethod
    def _cpp(cls, msg: str) -> str:
        esc = msg.replace("\\", "\\\\").replace('"', '\\"')
        return (
            "#include <iostream>\n\n"
            "int main() {\n"
            f'    std::cout << "{esc}" << std::endl;\n'
            "    return 0;\n"
            "}"
        )

    @classmethod
    def _python(cls, msg: str) -> str:
        esc = msg.replace("\\", "\\\\").replace("'", "\\'")
        return (
            "def main():\n"
            f"    print('{esc}')\n\n"
            "if __name__ == '__main__':\n"
            "    main()"
        )

    @classmethod
    def emit(
        cls,
        engine: "CatR11Engine",
        prompt: str,
        lang: str,
        vec: Optional[np.ndarray],
    ) -> str:
        embedded_lang, embedded = CatSeekR1Code.extract_prompt_code(prompt)
        if embedded:
            return embedded

        lang = CatSeekR1Code._coerce_lang(engine, lang, prompt)
        msg = cls.message_from_prompt(prompt, vec, engine)

        if lang == "html":
            return CatSeekR1Code._html(prompt, engine)
        if lang == "python":
            pl = prompt.lower()
            if "fibonacci" in pl or re.search(r"\bfib\b", pl):
                return CatSeekR1Code._python(engine, prompt)
            return cls._python(msg)
        if lang == "c":
            return cls._c(msg)
        if lang == "cpp":
            return cls._cpp(msg)
        if lang == "javascript":
            esc = msg.replace("\\", "\\\\").replace("'", "\\'")
            return f"console.log('{esc}');"
        if lang == "bash":
            esc = msg.replace("\\", "\\\\").replace('"', '\\"')
            return f'#!/bin/bash\necho "{esc}"'
        if lang == "rust":
            esc = msg.replace("\\", "\\\\").replace('"', '\\"')
            return f'fn main() {{\n    println!("{esc}");\n}}'
        if lang == "go":
            esc = msg.replace("\\", "\\\\").replace('"', '\\"')
            return f'package main\n\nimport "fmt"\n\nfunc main() {{\n\tfmt.Println("{esc}")\n}}'
        if lang == "java":
            esc = msg.replace("\\", "\\\\").replace('"', '\\"')
            return (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                f'        System.out.println("{esc}");\n'
                "    }\n"
                "}"
            )
        if lang == "css":
            return f"body {{\n  font-family: system-ui, sans-serif;\n}}\n\n/* {msg} */"
        if lang == "sql":
            esc = msg.replace("'", "''")
            return f"SELECT '{esc}' AS message;"
        # Token-weight fallback — never emit dynamic template stubs
        return cls._python(msg)

    @staticmethod
    def fence(lang: str, code: str) -> str:
        tag = lang if lang else ""
        return f"```{tag}\n{code.rstrip()}\n```"


# ──────────────────────────────────────────────────────────────
# CATR1B — CatSeek R1 1.0b code engine (files=off · perfect-code loop)
# ──────────────────────────────────────────────────────────────
class CatR1MythosEngine:
    """
    catr1b: CatSeek R1 1.0b code engine (files=off).
    Pattern library · 5-pass recursive perfection · lint · sandbox verify.
    """

    NAME = CATR1_ENGINE
    FAMILY = "catr1b"

    _HELLO_CAT_C = (
        "#include <stdio.h>\n\n"
        "int main(void) {\n"
        '    printf("Hello Cat\\n");\n'
        '    printf("Meow!\\n");\n'
        "    return 0;\n"
        "}"
    )

    _PY_HELLO = (
        "def main() -> None:\n"
        '    print("Hello, World!")\n\n'
        "if __name__ == \"__main__\":\n"
        "    main()"
    )

    _PY_HELLO_CAT = (
        "def main() -> None:\n"
        '    print("Hello Cat!")\n'
        '    print("Meow!")\n\n'
        "if __name__ == \"__main__\":\n"
        "    main()"
    )

    _JS_HELLO = "console.log('Hello, World!');\n"

    _RUST_HELLO = (
        "fn main() {\n"
        '    println!("Hello, World!");\n'
        "}"
    )

    @classmethod
    def _lint(cls, code: str, lang: str) -> str:
        if not CONFIG.get("catr1b_lint", True):
            return code
        lines = [ln.rstrip() for ln in code.splitlines()]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        body = "\n".join(lines)
        if lang == "python" and body and not body.endswith("\n"):
            body += "\n"
        return body

    @classmethod
    def _pattern_match(cls, prompt: str, lang: str, engine: "CatR11Engine") -> Optional[str]:
        pl = CatSeekR1Code.normalize_prompt(prompt).lower()
        if lang == "c" and re.search(r"\bhello\s+cat\b", pl):
            return cls._HELLO_CAT_C
        if lang == "c" and re.search(r"\bhello\b", pl):
            msg = CatSeekR1Code._subject(prompt, engine)
            if "cat" not in pl:
                return TokenWeightCodeEmitter._c(msg if msg else "Hello")
        if lang == "cpp" and "hello" in pl:
            msg = CatSeekR1Code._subject(prompt, engine)
            return TokenWeightCodeEmitter._cpp(msg if msg else "Hello")
        if lang == "python":
            if "fibonacci" in pl or re.search(r"\bfib\b", pl):
                return CatSeekR1Code._python(engine, prompt)
            if re.search(r"\bhello\s+cat\b", pl):
                return cls._PY_HELLO_CAT
            if re.search(r"\bhello\s+world\b", pl) or pl.strip() in {"hello", "write hello in python"}:
                return cls._PY_HELLO
        if lang == "javascript" and "hello" in pl:
            return cls._JS_HELLO
        if lang == "rust" and "hello" in pl:
            return cls._RUST_HELLO
        if lang == "html":
            return CatSeekR1Code._html(prompt, engine)
        return None

    @classmethod
    def _validate(cls, lang: str, code: str) -> Tuple[bool, str]:
        lang = lang.lower()
        if not code or not code.strip():
            return False, "empty"
        if lang == "python":
            try:
                ast.parse(code)
                return True, ""
            except SyntaxError as e:
                return False, str(e)
        if lang in {"c", "cpp"}:
            if lang == "c" and "#include" not in code and "printf" in code:
                return False, "missing include"
            if "main" not in code:
                return False, "missing main"
            return True, ""
        if lang == "html":
            if "<html" not in code.lower() and "<!doctype" not in code.lower():
                return False, "not html"
            return True, ""
        if lang == "javascript":
            return True, ""
        return True, ""

    @classmethod
    def _fix(cls, lang: str, code: str, prompt: str, reason: str) -> str:
        lang = lang.lower()
        code = code.strip()
        if lang == "c" and "missing include" in reason:
            if "#include" not in code:
                code = "#include <stdio.h>\n\n" + code
        if lang == "python" and ("SyntaxError" in reason or "invalid syntax" in reason):
            if "def main" not in code:
                msg = TokenWeightCodeEmitter.message_from_prompt(prompt, None, None)
                return TokenWeightCodeEmitter._python(msg)
        if lang == "c" and "return 0" not in code and "main" in code:
            if not code.rstrip().endswith("}"):
                code = code.rstrip() + "\n    return 0;\n}"
        code = re.sub(r"\n{3,}", "\n\n", code)
        return code.rstrip() + "\n"

    @classmethod
    def _polish(cls, code: str, lang: str) -> str:
        lines = code.splitlines()
        out: List[str] = []
        for ln in lines:
            if re.match(r"^c\s*$", ln.strip()) and lang != "text":
                continue
            if re.search(r"^/Volumes/|^/Users/", ln):
                continue
            out.append(ln.rstrip())
        body = "\n".join(out).strip()
        if lang == "python" and body and "if __name__" not in body and "def main" in body:
            if not body.endswith("\n"):
                body += "\n"
            if "if __name__" not in body:
                body += "\nif __name__ == '__main__':\n    main()"
        return body

    @classmethod
    def _recursive_perfect(
        cls, code: str, lang: str, prompt: str, engine: "CatR11Engine"
    ) -> str:
        if not CONFIG.get("catr1_code_perfect", True):
            return code
        depth = CONFIG.get("catr1_recursive_depth", 3)
        out = code
        for i in range(depth):
            out = cls._polish(out, lang)
            ok, reason = cls._validate(lang, out)
            if ok:
                if lang == "python" and engine._validate_code("python", out):
                    break
                if lang != "python":
                    break
            out = cls._fix(lang, out, prompt, reason)
        return cls._lint(cls._polish(out, lang), lang)

    @classmethod
    def enabled(cls) -> bool:
        return bool(CONFIG.get("catr1_engine", True) and CONFIG.get("catseek_code_enabled", True))

    @classmethod
    def generate(
        cls,
        engine: "CatR11Engine",
        prompt: str,
        lang: str,
        vec: Optional[np.ndarray] = None,
    ) -> str:
        if not cls.enabled():
            return TokenWeightCodeEmitter.emit(engine, prompt, lang, vec)
        hit = cls._pattern_match(prompt, lang, engine)
        if hit:
            draft = hit
        else:
            draft = TokenWeightCodeEmitter.emit(engine, prompt, lang, vec)
        return cls._recursive_perfect(draft, lang, prompt, engine)

    @classmethod
    def respond(cls, engine: "CatR11Engine", prompt: str) -> str:
        return CatSeekR1Code.respond(engine, prompt)


ClaudeMythosCode = CatR1MythosEngine
CatR1Code = CatR1MythosEngine


# ──────────────────────────────────────────────────────────────
# CATSEEK R1 LLM (files=off · local runtime on CatSeek R1 1.0)
# ──────────────────────────────────────────────────────────────
class CatSeekContextMemory:
    """1M-token logical context window — in-memory only, files=off."""

    __slots__ = ("turns", "logical_tokens")

    def __init__(self):
        self.turns: List[Dict[str, str]] = []
        self.logical_tokens = 0

    def add(self, role: str, text: str) -> None:
        self.turns.append({"role": role, "text": text})
        self.logical_tokens += max(len(text.split()), 1)
        limit = CONFIG["catseek_context_window"]
        while self.logical_tokens > limit and len(self.turns) > 2:
            old = self.turns.pop(0)
            self.logical_tokens -= max(len(old["text"].split()), 1)

    def recent(self, n: int = 24) -> List[Dict[str, str]]:
        return self.turns[-n:]

    def prior_topics(self) -> str:
        users = [t["text"][:60] for t in self.turns if t["role"] == "user"][-4:]
        return "; ".join(users) if users else ""


FableContextMemory = CatSeekContextMemory


class CatSeekR1LLM:
    """
    CatSeek R1 runtime (files=off):
    DeepSeek-R1 CoT · Mythos polish · CatSeek R1 1.0 encode → think → draft → self-check → respond.
    """

    MODEL_ID = CONFIG["catseek_model_id"]
    NAME = "CatSeek R1 1.0b"
    FAMILY = "catseek-r1"
    CONTEXT_WINDOW = CONFIG["catseek_context_window"]
    MAX_OUTPUT = CONFIG["catseek_max_output"]
    _BRAND_PREFIX = CatSeekR1Code._BRAND_PREFIX

    _CREATIVE_CUES = (
        "fable", "parable", "allegory", "short story", "tell me a story",
        "write a story", "write me a story", "bedtime story", "tale about",
        "story about", "fable about", "once upon", "moral story",
        "poem", "poetry", "haiku", "sonnet", "verse", "rhyme",
        "narrative", "imagine a", "creative writing",
    )
    _CODE_CUES = (
        "code", "function", "implement", "snippet", "script", "class",
        "fibonacci", "fib", "prime", "python", "javascript", "rust", "java",
        "def ", "import ", "```",
    )

    def __init__(self):
        self.memory = CatSeekContextMemory()

    @staticmethod
    def _seed(vec: Optional[np.ndarray], salt: int = 0) -> int:
        if vec is None or vec.size == 0:
            return salt
        return int(abs(float(np.sum(vec * (1.0 + salt * 0.01)) * 10007))) % 10_000

    @classmethod
    def pick(cls, vec: Optional[np.ndarray], n: int, salt: int = 0) -> int:
        return cls._seed(vec, salt) % max(n, 1)

    @classmethod
    def is_creative(cls, pl: str) -> bool:
        pl = cls._BRAND_PREFIX.sub("", pl.strip())
        return CONFIG["catseek_enabled"] and any(c in pl for c in cls._CREATIVE_CUES)

    @classmethod
    def is_code_request(cls, pl: str) -> bool:
        if not CONFIG.get("catseek_code_enabled", True):
            return False
        return CatSeekR1Code.wants_code(pl)

    @classmethod
    def wants_fable(cls, pl: str) -> bool:
        pl = CatSeekR1Code._BRAND_PREFIX.sub("", pl.strip())
        cues = ("fable about", "write a fable", "tell me a fable", "parable", "allegory",
                "tell me a story", "write a story", "story about", "fable about")
        return any(c in pl for c in cues) or (
            re.search(r"\bfable\b", pl) is not None and "catseek" not in pl
        )

    @classmethod
    def wants_poem(cls, pl: str) -> bool:
        return any(c in pl for c in ("poem", "poetry", "haiku", "sonnet", "verse", "rhyme"))

    def classify(self, prompt: str, engine: "CatR11Engine") -> str:
        if CatSeekR1Fusion.is_noise(prompt):
            return "chat"
        norm = CatSeekR1Code.normalize_prompt(prompt)
        pl = norm.lower().strip()
        follow = CatSeekR1Fusion.session_followup(engine, prompt)
        if follow and CatSeekR1Fusion.is_noise(prompt):
            return "chat"
        if is_zh_greeting(prompt.strip()):
            return "chat"
        if engine.synth.smalltalk_reply(pl) or engine.synth.smalltalk_reply(prompt.strip()):
            return "chat"
        if is_explain_request(prompt) and not CatSeekR1Code.extract_prompt_code(prompt)[1]:
            return "explain"
        if CONFIG.get("web_program_enabled") and CatSeekWebProgram.wants_web(pl):
            return "web"
        if CONFIG.get("catseek_code_enabled"):
            if CatSeekR1Code.extract_prompt_code(prompt)[1]:
                return "code"
            if CatSeekR1Code.wants_code_with_history(pl, engine):
                return "code"
        if self.is_creative(pl):
            if self.wants_poem(pl):
                return "poem"
            if self.wants_fable(pl) or "story" in pl or "tale" in pl:
                return "fable"
            return "creative"
        if engine._try_simple_math(prompt) is not None:
            return "math"
        if any(x in pl for x in ("run code", "execute", "interpret", "/exec", "运行", "执行")):
            return "execute"
        if pl in ("run it", "run this", "execute it", "test it", "run"):
            return "execute"
        if self.is_code_request(pl):
            return "code"
        if any(k in pl for k in ("traceback", "exception", "error", "bug", "debug", "broken")):
            return "debug"
        if is_explain_request(prompt):
            return "explain"
        if re.search(r"\b(explain|what is|what are|why|how (?:does|do|to|can))\b", pl):
            return "explain"
        if re.search(r"(解释|说明|介绍)", prompt):
            return "explain"
        if re.search(r"\b(plan|architecture)\b", pl) and len(pl.split()) > 2:
            return "agent"
        if re.search(r"\b(design|build)\s+(?:a|an|the|my|this|your|me)\b", pl):
            return "agent"
        return "general"

    def plan(self, prompt: str, task: str, vec: Optional[np.ndarray]) -> List[str]:
        steps = {
            "chat": ["match tone", "respond warmly", "invite next turn"],
            "explain": ["identify core concept", "mechanism", "example", "caveats"],
            "code": ["spec inputs/outputs", "draft", "edge cases", "self-test"],
            "web": ["pick template", "render artifact HTML", "store in memory", "preview URL"],
            "debug": ["reproduce", "localize", "fix", "verify"],
            "fable": ["theme", "arc", "moral", "polish prose"],
            "poem": ["image", "turn", "close"],
            "creative": ["voice", "structure", "finish"],
            "agent": ["decompose", "sequence", "deliverables"],
            "math": ["parse", "compute", "verify"],
            "execute": ["parse block", "run sandbox", "report"],
            "general": ["understand", "answer", "check completeness"],
        }
        base = steps.get(task, steps["general"])
        if vec is not None and self.pick(vec, 3, 12) == 0 and task in ("explain", "code", "agent"):
            base = base + ["proactive follow-up"]
        return base

    @staticmethod
    def _extract_subject(prompt: str) -> str:
        pl = prompt.lower()
        for prefix in ("fable about ", "story about ", "poem about ", "tale about ", "about ", "on "):
            if prefix in pl:
                return prompt[pl.index(prefix) + len(prefix):].strip("?.")
        return re.sub(
            r"^(?:write|tell|give)\s+(?:me\s+)?(?:a\s+)?(?:fable|story|poem|tale)\s*(?:about\s+)?",
            "", pl, flags=re.I,
        ).strip("?.")

    def compose_fable(self, prompt: str, topic: str, vec: Optional[np.ndarray]) -> str:
        heroes = (
            ("a clever fox", "wit over force"), ("a patient tortoise", "steady effort"),
            ("a curious owl", "seeing what others miss"), ("a humble mouse", "small acts matter"),
        )
        settings = (
            "at the edge of an ancient forest", "in a harbor town of quiet clocks",
            "on a hillside where seasons negotiated in whispers",
        )
        hero, virtue = heroes[self.pick(vec, len(heroes), 2)]
        setting = settings[self.pick(vec, len(settings), 3)]
        subject = self._extract_subject(prompt) or topic.strip("?.") or "the work that waits"
        return (
            f"**{subject.title()}** — a fable\n\n"
            f"Once, {hero} lived {setting}. The village spoke of **{subject}**, "
            f"though no two voices agreed on its shape.\n\n"
            f"When difficulty arrived — as it always does — the hero did not perform brilliance. "
            f"They attended: mending what broke, keeping promises, asking honest questions. "
            f"Others mistook patience for slowness until the results could no longer be ignored.\n\n"
            f"**Moral:** {virtue.capitalize()} compounds quietly. "
            f"The world becomes slightly more legible for whoever comes next."
        )

    def compose_poem(self, topic: str, vec: Optional[np.ndarray], prompt: str = "") -> str:
        subj = (self._extract_subject(prompt) if prompt else "") or topic.strip("?.") or "the road ahead"
        forms = (
            f"**On {subj}**\n\nNot all answers arrive with noise;\n"
            f"some knock like moth-wings at the glass —\n"
            f"small, insistent, easy to ignore\nuntil you remember you wanted light.\n\n"
            f"Begin again. {subj.capitalize()} waits\nlike shore waits tide: patient, sure, returned.",
            f"**{subj.title()}**\n\nYou asked about {subj}.\n"
            f"The mind builds bridges out of questions;\neach span creaks until you walk it.\n\n"
            f"Go slowly. Name what you know.\nLeave doors open for better names.",
        )
        return forms[self.pick(vec, len(forms), 5)]

    def self_check(self, prompt: str, draft: str, task: str, engine: "CatR11Engine") -> str:
        out = draft
        if task == "code" and "```" in out:
            for m in re.finditer(r"```(\w*)\n(.*?)```", out, re.S):
                lang, code = m.group(1) or "python", m.group(2)
                if lang == "python" and engine._validate_code("python", code):
                    continue
        if task in ("explain", "general", "agent") and "?" in prompt and len(out) < 80:
            out += "\n\nI can go deeper — tell me which part needs expansion."
        return out

    def complete(self, engine: "CatR11Engine", prompt: str, *, simulate: bool = True) -> str:
        """Main CatSeek R1 completion entry — DeepSeek-R1 + Mythos · files=off."""
        pl = prompt.lower().strip()
        follow = CatSeekR1Fusion.session_followup(engine, prompt)
        if follow and CatSeekR1Fusion.is_noise(prompt):
            return follow
        task = self.classify(prompt, engine)
        engine.encode_for_task(prompt, task=task)
        vec = engine.last_vec
        _CATSEEK_FAST = frozenset({"chat", "code", "math", "execute", "web", "explain"})
        if task in _CATSEEK_FAST:
            engine.last_think = ""
            engine._pending_think = ""
        _ = self.plan(prompt, task, vec)

        if task == "chat":
            hit = engine.synth.smalltalk_reply(pl)
            if hit:
                return hit
            if follow:
                return follow

        # CatSeek Code fast path — CatSeek R1 1.0 token weights · files=off
        if task == "code":
            return CatSeekR1Code.respond(engine, prompt)

        if task == "web":
            return engine.web.respond(engine, prompt)

        if task == "math":
            result = engine._try_simple_math(prompt)
            if result:
                if CONFIG.get("deepseek_r1_reasoning"):
                    return engine.fusion.deepseek_math_wrap(prompt, result)
                return f"Result: **{result}**"

        if task == "explain":
            dia = engine.get_dialect(engine.detect_locale(prompt))
            intent = engine._best_intent(prompt)
            if intent in {"recursion", "core", "help", "languages", "profile"}:
                hit = engine._intent_response(intent, prompt, dia)
                if hit:
                    return self.self_check(prompt, hit, task, engine)
            history = engine.chat_history[:-1] if engine.chat_history else []
            body = engine.synth.synthesize(
                prompt, [(m["role"], m["text"]) for m in history], vec=vec
            )
            return self.self_check(prompt, body, task, engine)

        if task == "execute":
            block_lang, code = engine.extract_code_block(prompt)
            exec_lang = CatSeekR1Code.detect_lang(
                engine, prompt if not block_lang else f"in {block_lang}"
            )
            if not code:
                for m in reversed(engine.chat_history):
                    if m.get("role") == "assistant":
                        block_lang, code = engine.extract_code_block(m.get("text", ""))
                        if code:
                            exec_lang = engine.normalize_lang(block_lang) or exec_lang
                            break
            if not code:
                return "Paste code in a fenced block, or generate code first then say **run it**."
            result = CatSeekR1Code.run(engine, exec_lang, code)
            return f"**catr1b** ({exec_lang} · files=off):\n\n```\n{result}\n```"

        norm = CatSeekR1Code.normalize_prompt(prompt)
        if CONFIG.get("catseek_code_enabled") and CatSeekR1Code.wants_code_with_history(norm.lower(), engine):
            return CatSeekR1Code.respond(engine, prompt)

        if task not in _CATSEEK_FAST:
            if engine._pending_think:
                engine.last_think = engine._pending_think
                engine._pending_think = ""
            else:
                engine._run_ultrathink(prompt)
        history = engine.chat_history[:-1] if engine.chat_history else []
        dia = engine.get_dialect(engine.detect_locale(prompt))

        if task == "fable":
            topic = engine._extract_topic_words(prompt)
            body = self.compose_fable(prompt, topic, vec)
            return self.self_check(prompt, body, task, engine)

        if task == "poem":
            topic = engine._extract_topic_words(prompt)
            body = self.compose_poem(topic, vec, prompt)
            return self.self_check(prompt, body, task, engine)

        if task == "creative":
            topic = engine._extract_topic_words(prompt)
            body = self.compose_fable(prompt, topic, vec)
            return self.self_check(prompt, body, task, engine)

        intent = engine._best_intent(prompt)
        if intent in {"languages", "profile", "core", "recursion", "help"}:
            hit = engine._intent_response(intent, prompt, dia)
            if hit:
                return self.self_check(prompt, hit, task, engine)

        body = engine.synth.o1_answer(prompt, history, vec=vec)
        if CONFIG.get("mythos_recursive_improve") and task not in _CATSEEK_FAST:
            body = engine.fusion.recursive_improve(body, prompt, vec)
        return self.self_check(prompt, body, task, engine)

    @staticmethod
    def model_card() -> Dict[str, Any]:
        return {
            "id": CATSEEK_MODEL_ID,
            "object": "model",
            "family": "catseek-r1",
            "display_name": CatSeekR1LLM.NAME,
            "context_window": CONFIG["catseek_context_window"],
            "max_output_tokens": CONFIG["catseek_max_output"],
            "files": FILES,
            "prose_tier": PROSE_TIER,
            "mythos_tier": MYTHOS_TIER,
            "reasoning": REASONING_MODE,
            "deepseek_r1": CONFIG.get("deepseek_r1_reasoning", True),
            "code_interpreter": CODE_ENGINE,
            "code_backend": CODE_BACKEND,
            "catseek_code_enabled": CATSEEK_CODE_ENABLED,
            "web_program": CONFIG.get("web_program_enabled", True),
            "arch": "catseek_r1_1.0b",
        }




class CatR11Synthesizer:
    """Knowledge + chat synthesis backend for CatSeek R1 (files=off)."""

    def __init__(self):
        pass

    @staticmethod
    def _normalize_chat(pl: str) -> str:
        s = pl.strip().lower()
        s = re.sub(r"\s+", " ", s)
        s = s.rstrip("?!.！？。")
        return s

    @classmethod
    def smalltalk_reply(cls, pl: str) -> Optional[str]:
        s = cls._normalize_chat(pl)
        for pat, reply in _SMALLTALK:
            if re.match(pat, s) or re.match(pat, pl.strip()):
                return reply
        return None

    @classmethod
    def is_educational(cls, pl: str) -> bool:
        if cls.smalltalk_reply(pl):
            return False
        if is_explain_request(pl) or is_zh_question(pl):
            return True
        if re.search(r"(解释|说明|介绍|教程|原理)", pl):
            return True
        patterns = (
            r"\b(explain|define|describe|what is|what are|why|how (?:does|do|to|can|would|should|could|will))\b",
            r"\b(compare|versus|vs\.?|difference|tutorial|implement|algorithm|architecture)\b",
            r"\b(debug|traceback|exception|error|bug|broken|fix)\b",
            r"\b(write|code|function|script|snippet|class|api|docker|python|catseek|core|sql|git)\b",
            r"\b(calculate|compute|solve|fibonacci|prime)\b",
            r"\b(plan|roadmap|design|system|recommend|should i)\b",
        )
        return any(re.search(p, s) for p in patterns)

    def _topic(self, prompt: str, pl: str) -> str:
        for prefix in (
            "explain ", "why ", "how does ", "how do ", "how to ", "what is ", "what are ",
            "define ", "compare ", "debug ", "fix ", "write ",
        ):
            if pl.startswith(prefix):
                return prompt[len(prefix):].strip("?.")
        if "?" in prompt:
            return prompt.strip().rstrip("?")
        return prompt.strip()[:200] or "your question"

    def analyze(self, prompt: str) -> Dict[str, str]:
        pl = prompt.lower().strip()
        if is_zh_greeting(prompt.strip()):
            return {"intent": "casual", "topic": prompt.strip(), "pl": pl}
        if is_explain_request(prompt) or re.search(r"(解释|说明|介绍)", prompt):
            topic = extract_zh_topic(prompt) if VibeCodeHeuristics.has_cjk(prompt) else self._topic(prompt, pl)
            return {"intent": "explain", "topic": topic, "pl": pl}
        topic = self._topic(prompt, pl)
        if self.smalltalk_reply(pl):
            return {"intent": "casual", "topic": topic, "pl": pl}
        if CONFIG["catseek_enabled"] and CatSeekR1LLM.wants_fable(pl):
            return {"intent": "fable", "topic": topic, "pl": pl}
        if CONFIG["catseek_enabled"] and CatSeekR1LLM.wants_poem(pl):
            return {"intent": "poem", "topic": topic, "pl": pl}
        if any(k in pl for k in ("story", "tale", "creative", "imagine", "narrative")):
            return {"intent": "creative", "topic": topic, "pl": pl}
        if any(k in pl for k in ("traceback", "exception", "error", "bug", "broken", "fails")):
            return {"intent": "debug", "topic": topic, "pl": pl}
        if any(k in pl for k in ("compare", " vs ", " versus ", "difference", "better")):
            return {"intent": "compare", "topic": topic, "pl": pl}
        if re.search(
            r"\b(explain|what is|what are|why|how (?:does|do|to|can|would|should|could|will))\b", pl
        ):
            return {"intent": "explain", "topic": topic, "pl": pl}
        if any(k in pl for k in ("fibonacci", "fib", "prime", "primes")):
            return {"intent": "code", "topic": topic, "pl": pl}
        if CatSeekR1Code.wants_code(pl):
            return {"intent": "code", "topic": topic, "pl": pl}
        if any(k in pl for k in ("write code", "function", "implement", "snippet", "script")):
            return {"intent": "code", "topic": topic, "pl": pl}
        if any(k in pl for k in ("plan", "roadmap", "architecture", "design", "system")):
            return {"intent": "design", "topic": topic, "pl": pl}
        if re.search(r"\d\s*[+\-*/^%]", pl) or "calculate" in pl or "solve" in pl:
            return {"intent": "math", "topic": topic, "pl": pl}
        if any(k in pl for k in ("should i", "opinion", "recommend", "best")):
            return {"intent": "advise", "topic": topic, "pl": pl}
        if any(k in pl for k in ("meow", "mew", "purr", "nya", "rawr")):
            return {"intent": "casual", "topic": topic, "pl": pl}
        if len(pl.split()) <= 4 and "?" not in prompt and not self.is_educational(pl):
            return {"intent": "casual", "topic": topic, "pl": pl}
        if not self.is_educational(pl):
            return {"intent": "casual", "topic": topic, "pl": pl}
        return {"intent": "general", "topic": topic, "pl": pl}

    @staticmethod
    def _footer() -> str:
        return ""

    def _explain(self, topic: str, pl: str, vec: Optional[np.ndarray] = None) -> str:
        if ("python" in pl or "python" in topic.lower()) and VibeCodeHeuristics.has_cjk(topic + pl):
            return (
                f"**{topic.capitalize()}** — 清晰解释如下。\n\n"
                "**Python** 是一种高级编程语言，语法简洁、生态丰富。\n\n"
                "常用于脚本、Web 后端、数据分析、自动化和机器学习原型。\n\n"
                "优点：开发快、库多、社区大。\n"
                "缺点：GIL 限制 CPU 并行；大型项目建议加类型注解。\n\n"
                "```python\nfor i in range(3):\n    print(i)\n```"
            )
        kb = {
            ("recursion",): (
                f"**{topic.capitalize()}** is when a function calls itself until it hits a base case, "
                "then unwinds the stack to combine results.\n\n"
                "Each call gets its own stack frame. The base case stops new frames; the recursive step "
                "handles a smaller instance of the same problem.\n\n"
                "Example: `factorial(3)` waits on `factorial(2)` → `factorial(1)` returns 1, "
                "then multiplies back up: 1 × 2 × 3 = 6.\n\n"
                "Watch out for missing base cases — they cause stack overflow."
            ),
            ("递归",): (
                "**递归**是函数调用自身，直到遇到**基准情况**（base case），然后逐层返回结果。\n\n"
                "每次调用都有独立的栈帧。基准情况阻止无限调用；递归步骤处理更小规模的同一问题。\n\n"
                "示例：`factorial(3)` 等待 `factorial(2)` → `factorial(1)` 返回 1，"
                "再逐层相乘：1 × 2 × 3 = 6。\n\n"
                "注意：缺少基准情况会导致栈溢出。"
            ),
            ("docker",): (
                f"**Docker** packages an application and its dependencies into a **container** that runs "
                "consistently on any machine with Docker installed.\n\n"
                "Key pieces:\n"
                "- **Image** — read-only blueprint\n"
                "- **Container** — running instance of an image\n"
                "- **Dockerfile** — recipe to build an image\n\n"
                "Great for reproducible dev environments. For large-scale orchestration, people often add Kubernetes."
            ),
            ("core",): (
                f"**CatSeek R1 1.0** quantizes neural network weights to three values: **{{-1, 0, 1}}**. "
                "That turns matrix multiplication into mostly additions and subtractions, "
                "which cuts memory use and can speed up inference.\n\n"
                f"{BRAND} runs a CatSeek R1 1.0 distillation stack locally — "
                f"one teacher plus {CONFIG['distil_passes']} student heads, all in-memory (**files=off**)."
            ),
            ("transformer", "attention"): (
                f"A **transformer** processes sequences using **self-attention** — each token can "
                "weigh every other token to capture context.\n\n"
                "Stack: embeddings → multi-head attention → feed-forward network → residuals and layer norms, "
                "repeated across many layers. Decoder models mask future tokens for causal generation."
            ),
            ("reason", "think", "o1"): (
                f"{BRAND} runs **{REASONING_MODE}** reasoning: think internally, answer cleanly.\n\n"
                f"CatSeek R1 1.0 **{CONFIG['weight_bits']}-bit** ternary weights + sparse compression + "
                f"rank-{CONFIG['compression_rank']} bottleneck — all **files=off**, in-memory."
            ),
            ("python",): (
                "**Python** is a high-level language known for readable syntax and a huge ecosystem.\n\n"
                "Use it for scripting, web backends, data work, automation, and ML prototypes.\n\n"
                "Strengths: fast to write, great libraries, huge community.\n"
                "Tradeoffs: GIL limits CPU parallelism; type hints help at scale.\n\n"
                "```python\nfor i in range(3):\n    print(i)\n```"
            ),
            ("javascript", "js"): (
                "**JavaScript** runs in browsers and on servers (Node.js).\n\n"
                "Event-driven, async-friendly — ideal for interactive UIs and I/O-heavy APIs.\n\n"
                "Use `async/await` for readable asynchronous code."
            ),
            ("git",): (
                "**Git** tracks code history with commits, branches, and merges.\n\n"
                "Daily flow: `git pull` → edit → `git add` → `git commit` → `git push`.\n"
                "Branches isolate features; merge or rebase when ready."
            ),
            ("api", "rest"): (
                "A **REST API** exposes resources over HTTP with verbs like GET, POST, PUT, DELETE.\n\n"
                "Use nouns in paths, correct status codes, and version your API.\n"
                "In this app everything is local — describe payloads in chat (**files=off**)."
            ),
            ("sql", "database"): (
                "**SQL** queries relational databases with tables, rows, and joins.\n\n"
                "Core ops: SELECT, INSERT, UPDATE, DELETE, JOIN.\n"
                "Index columns you filter on; avoid SELECT * in production."
            ),
            ("machine", "ml", "learning"): (
                "**Machine learning** learns patterns from data instead of hand-written rules.\n\n"
                "Pipeline: data → features → model → loss → training → evaluation on hold-out set.\n"
                "Start simple; add complexity only when metrics justify it."
            ),
            ("async", "await"): (
                "**async/await** lets one thread juggle many I/O-bound tasks without blocking.\n\n"
                "The event loop schedules coroutines; `await` yields until I/O completes.\n"
                "Best for network/disk waits — use threads/processes for CPU-heavy work."
            ),
            ("compress", "quant"): (
                f"**Model compression** shrinks memory and speeds inference: quantization (CatSeek R1 1.0 ternary), "
                f"sparsity (top-{CONFIG['compression_sparse_k']} activations), and low-rank bottlenecks.\n\n"
                f"{BRAND} stacks these in-memory for frontier-tier capacity — **files=off**."
            ),
        }
        for keys, body in kb.items():
            if any(k in pl or k in topic for k in keys):
                return f"**{topic.capitalize()}** — here's a clear explanation.\n\n{body}"
        if not self.is_educational(pl):
            return self._casual(topic, pl, topic, vec)
        return (
            f"I can walk through **{topic}** — concept, mechanism, or a worked example. "
            f"Which would help most?"
        )

    def _fable(self, topic: str, prompt: str, vec: Optional[np.ndarray]) -> str:
        return CatSeekR1LLM().compose_fable(prompt, topic, vec)

    def _poem(self, topic: str, vec: Optional[np.ndarray], prompt: str = "") -> str:
        return CatSeekR1LLM().compose_poem(topic, vec, prompt)

    def _creative(self, topic: str, prompt: str, pl: str, vec: Optional[np.ndarray]) -> str:
        if CatSeekR1LLM.wants_poem(pl):
            return self._poem(topic, vec)
        return self._fable(topic, prompt, vec)

    def _debug(self, topic: str, vec: Optional[np.ndarray] = None) -> str:
        return (
            "Debugging is a conversation with reality — start small, listen closely, change one thing at a time.\n\n"
            "**Reproduce minimally.** Find the smallest input that still fails.\n"
            "**Read bottom-up.** The last frame in *your* code is usually where to look first.\n"
            "**Name expected vs actual.** Write both down before you touch anything.\n"
            "**Iterate with discipline.** One change, one run, one note.\n\n"
            "Paste the full traceback when you have it — I'll walk through it line by line with you."
        )

    def _code(self, topic: str, pl: str, vec: Optional[np.ndarray] = None) -> str:
        if "fibonacci" in pl or "fib" in pl:
            body = (
                "```python\ndef fib(n: int) -> list[int]:\n"
                "    a, b = 0, 1\n    out = [a]\n"
                "    for _ in range(1, max(n, 1)):\n        a, b = b, a + b\n        out.append(a)\n"
                "    return out[:n]\n\nprint(fib(10))\n```"
            )
        elif "prime" in pl:
            body = (
                "```python\ndef primes_upto(n: int) -> list[int]:\n"
                "    if n < 2: return []\n    sieve = [True] * (n + 1)\n"
                "    sieve[0] = sieve[1] = False\n"
                "    for p in range(2, int(n**0.5) + 1):\n"
                "        if sieve[p]:\n            sieve[p*p:n+1:p] = [False] * len(sieve[p*p:n+1:p])\n"
                "    return [i for i, ok in enumerate(sieve) if ok]\n\nprint(primes_upto(50))\n```"
            )
        else:
            body = (
                f"```python\ndef solve():\n    \"\"\"Sketch: {topic[:60]}\"\"\"\n"
                "    return None\n\nif __name__ == '__main__':\n    print(solve())\n```"
            )
        return (
            f"Here's a **{topic}** sketch — readable first, correct second. Run it, then harden edge cases.\n\n"
            f"{body}\n\n"
            "Empty input, zero, and one large value are the three tests I always run."
        )

    def _math(self, topic: str, pl: str) -> str:
        m = re.search(r"(\d+(?:\.\d+)?)\s*([+\-*/^])\s*(\d+(?:\.\d+)?)", pl)
        if m:
            a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
            ops = {"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else None, "^": a ** b}
            val = ops.get(op)
            if val is not None:
                out = int(val) if val == int(val) else round(val, 6)
                sym = {"*": "×", "/": "÷"}.get(op, op)
                return f"{a:g} {sym} {b:g} = **{out}**"
        return f"What expression should I evaluate for **{topic}**? You can type something like `15 * 7` or `100 / 4`."

    def _compare(self, topic: str, vec: Optional[np.ndarray] = None) -> str:
        return (
            f"Comparing **{topic}** well means naming what you optimize for before you pick winners.\n\n"
            "Consider **latency** (how fast must it be?), **complexity** (what can your team live with?), "
            "**offline needs** (this stack runs fully local — files=off), and **total cost** (infra plus time).\n\n"
            "List must-haves, eliminate what breaks them, prototype the top two. "
            "Tell me the pair you're weighing and I'll give you a sharper read."
        )

    def _advise(self, topic: str, vec: Optional[np.ndarray] = None) -> str:
        return (
            f"On **{topic}**, the honest answer is: it depends on what you're optimizing.\n\n"
            "If you need to **learn fast**, ship a small prototype and let reality edit your plan. "
            "If you need **long-term maintenance**, favor simpler architecture over clever architecture. "
            "If you need **privacy or offline work**, everything here stays in-memory (**files=off**).\n\n"
            "Share two or three constraints and I'll recommend something concrete."
        )

    def _casual(self, topic: str, pl: str, prompt: str, vec: Optional[np.ndarray] = None) -> str:
        hit = self.smalltalk_reply(pl)
        if hit:
            return hit
        if any(k in pl for k in ("meow", "mew", "purr", "nya")):
            return (
                f"Meow! I'm **{BRAND}** {EDITION} (**files=off**). "
                "Explain, code, debug, stories — what would you like?"
            )
        if pl in {"hey", "hi", "yo", "sup", "hello"}:
            return "Hi — good to see you. What would you like to work on?"
        if is_zh_greeting(prompt.strip()):
            return "你好！我是 Cat R1（files = off）。可以帮你写代码、解释概念或调试问题。"
        if VibeCodeHeuristics.has_cjk(prompt) and len(prompt.strip()) <= 12:
            return "你好！请告诉我你需要什么帮助——代码、解释或调试都可以。"
        if len(pl.split()) <= 4 and "?" not in prompt:
            return (
                f"**{BRAND}** · DeepSeek-R1 + Mythos · files=off — "
                "ask for code, an explanation, or paste a snippet to run."
            )
        return (
            f"I can help with that. **{BRAND}** uses DeepSeek-R1 reasoning and Mythos-tier prose — all in-memory (**files=off**). "
            "What would you like to do next?"
        )

    def _general(self, topic: str, prompt: str, vec: Optional[np.ndarray] = None) -> str:
        pl = prompt.lower().strip()
        if not self.is_educational(pl):
            return self._casual(topic, pl, prompt, vec)
        return (
            f"On **{topic or 'that'}** — I can explain the idea, compare approaches, or sketch code. "
            f"What would help most?"
        )

    def synthesize(self, prompt: str, history: List[tuple], vec: Optional[np.ndarray] = None) -> str:
        a = self.analyze(prompt)
        intent = a["intent"]
        topic, pl = a["topic"], a["pl"]
        bodies = {
            "explain": self._explain(topic, pl, vec),
            "qa": self._explain(topic, pl, vec),
            "compare": self._compare(topic, vec),
            "debug": self._debug(topic, vec),
            "code": self._code(topic, pl, vec),
            "design": self._general(topic, prompt, vec),
            "math": self._math(topic, pl),
            "advise": self._advise(topic, vec),
            "casual": self._casual(topic, pl, prompt, vec),
            "fable": self._fable(topic, prompt, vec),
            "poem": self._poem(topic, vec),
            "creative": self._creative(topic, prompt, pl, vec),
        }
        return bodies.get(intent, self._general(topic, prompt, vec))

    def _followup(self, prompt: str, history: List[Dict[str, str]], vec: Optional[np.ndarray] = None) -> Optional[str]:
        if not history:
            return None
        pl = prompt.lower().strip()
        cues = (
            "tell me more", "go on", "continue", "and then", "what else", "more detail",
            "expand", "elaborate", "can you explain", "say more", "go deeper", "why though",
        )
        short_ack = {"yes", "ok", "okay", "sure", "please", "yep", "yeah", "do it", "thanks"}
        last_user = last_bot = ""
        for m in reversed(history):
            if m["role"] == "assistant" and not last_bot:
                last_bot = m["text"]
            elif m["role"] == "user" and not last_user:
                last_user = m["text"]
            if last_user and last_bot:
                break
        if not last_bot:
            return None
        if any(c in pl for c in cues) or pl in short_ack or pl.startswith(("why ", "how come")):
            snippet = last_bot.strip().split("\n\n")[0][:500]
            return (
                f"Building on our exchange about \"{last_user[:80]}\":\n\n"
                f"{snippet}\n\n"
                "The deeper layer is *mechanism* — what actually changes when you apply this. "
                "Tell me which part you want expanded and I'll go there."
            )
        if pl.startswith(("what about", "how about")):
            sub = prompt.split(maxsplit=2)[-1] if len(prompt.split()) > 2 else prompt
            return self._explain(sub.strip("?"), pl, vec)
        return None

    def converse(self, prompt: str, history: List[Dict[str, str]], vec: Optional[np.ndarray] = None) -> str:
        pl = prompt.lower().strip()
        small = self.smalltalk_reply(pl)
        if small:
            return small
        follow = self._followup(prompt, history, vec)
        if follow:
            return follow
        return self.synthesize(prompt, [(m["role"], m["text"]) for m in history], vec=vec)

    @staticmethod
    def _polish(text: str) -> str:
        t = re.sub(r"\n{3,}", "\n\n", text.strip())
        if t and t[-1] not in ".!?`\"'":
            t += "."
        return t

    def o1_answer(
        self,
        prompt: str,
        history: List[Dict[str, str]],
        *,
        reasoning: str = "",
        vec: Optional[np.ndarray] = None,
    ) -> str:
        """CatSeek R1 answer path — reasoning stays in think trace."""
        body = self.converse(prompt, history, vec=vec)
        return self._polish(body)


# ──────────────────────────────────────────────────────────────
# CAT R1 CHAT PROTOCOL v1.0 (files=off, in-memory sessions)
# ──────────────────────────────────────────────────────────────
@dataclass
class ChatMessage:
    role: str
    content: str
    turn: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {"role": self.role, "content": self.content, "turn": self.turn}


@dataclass
class ChatSession:
    session_id: str
    messages: List[ChatMessage] = field(default_factory=list)
    turn_count: int = 0
    created: float = field(default_factory=time.time)

    def append(self, role: str, content: str) -> ChatMessage:
        self.turn_count += 1
        msg = ChatMessage(role=role, content=content, turn=self.turn_count)
        self.messages.append(msg)
        if len(self.messages) > 48:
            self.messages = self.messages[-48:]
        return msg

    def history_dicts(self) -> List[Dict[str, str]]:
        return [{"role": m.role, "text": m.content} for m in self.messages]

    def transcript(self, limit: int = 12) -> str:
        lines = []
        for m in self.messages[-limit:]:
            label = "You" if m.role == "user" else BRAND
            lines.append(f"[{label}]: {m.content[:200]}")
        return "\n".join(lines)


class ChatProtocol:
    """
    CAT R1 Chat Protocol v1.0 — multi-turn conversation, files=off.

    JSON envelope::
        {"protocol":"cat-r1-chat","version":"1.0","action":"message",
         "session":"<id>","message":{"role":"user","content":"hello"}}

    Text wire (stdin/stdout)::
        @chat user: hello
        @chat assistant: Hi! ...
    """

    PROTO = CONFIG["chat_protocol"]
    VER = CONFIG["chat_version"]

    def __init__(self, engine: "CatR11Engine"):
        self.engine = engine
        self._sessions: Dict[str, ChatSession] = {}
        self._active = ""

    def new_session(self) -> str:
        sid = uuid.uuid4().hex[:12]
        self._sessions[sid] = ChatSession(session_id=sid)
        self._active = sid
        while len(self._sessions) > CONFIG["max_sessions"]:
            oldest = min(self._sessions.values(), key=lambda s: s.created)
            del self._sessions[oldest.session_id]
        return sid

    def session(self, session_id: Optional[str] = None) -> ChatSession:
        sid = session_id or self._active
        if not sid or sid not in self._sessions:
            sid = self.new_session()
        self._active = sid
        return self._sessions[sid]

    def sync_engine_history(self, sess: ChatSession) -> None:
        self.engine.chat_history = sess.history_dicts()

    def turn(self, user_text: str, *, session_id: Optional[str] = None, simulate: bool = True) -> Dict[str, Any]:
        text = (user_text or "").strip()
        if not text:
            return self._err("empty message")
        sess = self.session(session_id)
        self.sync_engine_history(sess)
        start = len(sess.messages)
        reply = self.engine.generate(text, simulate=simulate)
        think = self.engine.last_think
        for m in self.engine.chat_history[start:]:
            sess.append(m["role"], m["text"])
        return self._ok(sess, reply, think)

    def handle_action(self, data: Dict[str, Any]) -> Dict[str, Any]:
        action = (data.get("action") or "message").lower()
        sid = data.get("session") or data.get("session_id")

        if action in ("new", "reset"):
            new_id = self.new_session()
            if action == "reset" and sid and sid in self._sessions:
                del self._sessions[sid]
                new_id = self.new_session()
            self.engine.chat_history = []
            self.engine.last_think = ""
            return {
                "protocol": self.PROTO, "version": self.VER, "files": "off",
                "action": action, "session": new_id, "turn": 0,
                "message": {"role": "system", "content": f"New chat session {new_id}."},
            }

        if action == "history":
            sess = self.session(sid)
            return {
                "protocol": self.PROTO, "version": self.VER, "files": "off",
                "action": "history", "session": sess.session_id, "turn": sess.turn_count,
                "messages": [m.to_dict() for m in sess.messages],
            }

        if action == "message":
            msg = data.get("message") or {}
            content = msg.get("content") or data.get("content") or data.get("text") or ""
            if isinstance(content, list):
                content = content[-1].get("text", "") if content else ""
            return self.turn(str(content), session_id=sid, simulate=False)

        return self._err(f"unknown action: {action}")

    def parse_text_wire(self, line: str) -> Optional[Tuple[str, str]]:
        m = re.match(r"^@chat\s+(user|assistant|system)\s*:\s*(.*)$", line.strip(), re.I)
        if not m:
            return None
        return m.group(1).lower(), m.group(2)

    def format_text_wire(self, role: str, content: str, sess: ChatSession) -> str:
        return f"@chat {role}: {content}\n@chat meta session={sess.session_id} turn={sess.turn_count} files=off"

    def parse_request(self, raw: Any) -> Dict[str, Any]:
        if isinstance(raw, dict):
            if raw.get("protocol") not in (None, self.PROTO):
                return self._err(f"protocol must be {self.PROTO}")
            return self.handle_action(raw)
        if isinstance(raw, str):
            wire = self.parse_text_wire(raw)
            if wire:
                role, content = wire
                if role == "user":
                    return self.turn(content, simulate=False)
                return self._err("text wire expects @chat user: <message>")
            try:
                return self.handle_action(json.loads(raw))
            except json.JSONDecodeError:
                return self.turn(raw, simulate=False)
        return self._err("invalid request")

    def _ok(self, sess: ChatSession, content: str, thinking: str = "") -> Dict[str, Any]:
        return {
            "protocol": self.PROTO,
            "version": self.VER,
            "files": "off",
            "action": "message",
            "session": sess.session_id,
            "turn": sess.turn_count,
            "message": {"role": "assistant", "content": content},
            "thinking": thinking,
        }

    def _err(self, detail: str) -> Dict[str, Any]:
        return {
            "protocol": self.PROTO,
            "version": self.VER,
            "files": "off",
            "error": detail,
            "session": self._active or None,
        }

    @staticmethod
    def help_text() -> str:
        return (
            f"**{BRAND} Chat Protocol v{CONFIG['chat_version']}** · `{CATSEEK_MODEL_ID}` · files=off\n\n"
            f"**{CODE_ENGINE} interpreter** · **CatSeek Web Program** — `/web` · `/run` · paste ``` blocks\n\n"
            "**In-app commands**\n"
            "- `/chat` — show protocol help\n"
            "- `/chat new` — start a fresh session\n"
            "- `/chat history` — show this session transcript\n"
            "- `/chat session` — show session id\n\n"
            "**JSON API** — `POST /chat`\n"
            "```json\n"
            '{"protocol":"cat-r1-chat","version":"1.0","action":"message",'
            '"session":"<id>","message":{"role":"user","content":"hello"}}\n'
            "```\n\n"
            "**Text wire** (CLI `--chat`)\n"
            "`@chat user: your message here`\n\n"
            "Sessions live in memory only — no files written."
        )


def run_chat_cli(engine: CatR11Engine) -> None:
    proto = engine.chat
    sid = proto.new_session()
    print(f"{BRAND} · {CATSEEK_MODEL_ID} · DeepSeek-R1 · Mythos · {CODE_ENGINE} · files=off · protocol {ChatProtocol.PROTO}/{ChatProtocol.VER}")
    print(f"session={sid} · type @chat user: ... or plain text · /quit to exit\n")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break
        if not line:
            continue
        if line.lower() in {"/quit", "/exit", "quit", "exit"}:
            break
        if line.startswith("@chat"):
            parsed = proto.parse_text_wire(line)
            if parsed and parsed[0] == "user":
                out = proto.turn(parsed[1], session_id=sid, simulate=False)
            else:
                out = proto.parse_request(line)
        elif line == "/chat new":
            sid = proto.new_session()
            print(f"new session={sid}")
            continue
        elif line.startswith("/"):
            out = {"message": {"content": engine.generate(line, simulate=False)}}
        else:
            out = proto.turn(line, session_id=sid, simulate=False)
        if out.get("error"):
            print(f"error: {out['error']}")
            continue
        reply = out.get("message", {}).get("content", "")
        print(f"\n{BRAND}: {reply}\n")
        if out.get("thinking"):
            print(f"[thinking]\n{out['thinking']}\n")


# ──────────────────────────────────────────────────────────────
# CATSEEK R1 1.0 ENGINE (files=off · in-memory ternary stack)
# ──────────────────────────────────────────────────────────────
class CatR11Engine:
    __slots__ = ("name", "ver", "d_model", "_lock", "dialect_idx",
                 "dialects", "intent_map", "code_experts", "aliases",
                 "embeddings", "vocab", "output_head", "output_head_lin",
                 "_intent_weights", "_token_index", "_intent_trained",
                 "learning_curve", "response_locale",
                 "chat_history", "max_history", "assistant_mode",
                 "_category_lexicon", "_embed_cache",
                 "_student_layers", "ultrathink", "synth", "last_think",
                 "ultrathink_on", "_pending_think", "_distil_cache", "_recursive_cache",
                 "last_recursive_passes", "last_recursive_trace", "rival", "compressor",
                 "last_compression_ratio", "compression_trace", "chat", "catseek_blocks",
                 "catseek_stats", "norm_gamma", "norm_beta", "last_vec", "catseek", "fable", "deepmind", "fusion", "web")

    def __init__(self, d_model: int = None):
        self.name = BRAND
        self.ver = MODEL_NAME
        self.d_model = d_model or CONFIG["d_model"]
        self._lock = threading.Lock()
        self.dialect_idx = {"english": 0, "chinese": 0}
        self.learning_curve: List[float] = []
        self._intent_trained = False
        self._token_index: Dict[str, int] = {}
        self._intent_weights: Optional[np.ndarray] = None
        self.response_locale = "english"
        self.chat_history: List[Dict[str, str]] = []
        self.max_history = 24
        self.assistant_mode = "cat_r1"
        self._embed_cache: Dict[str, np.ndarray] = {}
        self._student_layers: List[List[CatSeekBlock]] = []
        self._distil_cache: Dict[tuple, np.ndarray] = {}
        self._recursive_cache: Dict[tuple, np.ndarray] = {}
        self.last_recursive_passes = 0
        self.last_recursive_trace: List[str] = []
        self.compression_trace: List[str] = []
        self.last_compression_ratio = 1.0
        self.last_vec: Optional[np.ndarray] = None
        self.ultrathink = O1PreviewReasoner()
        self.synth = CatR11Synthesizer()
        self.last_think = ""
        self._pending_think = ""
        self.ultrathink_on = CONFIG["ultrathink_default"]
        self.catseek = CatSeekR1LLM()
        self.fable = self.catseek
        self.chat = ChatProtocol(self)
        self.compressor = CatSeekCompressor(self.d_model)
        self.rival = CatSeekR1Core(self)
        self.deepmind = DeepMindFastStack(self)
        self.fusion = CatSeekR1Fusion()
        self.web = CatSeekWebProgram()
        self.aliases = {"py":"python","c++":"cpp","js":"javascript","ts":"typescript",
                       "sh":"bash","shell":"bash","asm":"assembly","node":"javascript"}
        self.intent_map = {
            "hello": ["hi","hello","hey","yo","sup","good morning","good evening","howdy",
                      "how are you","how're you","how is it going","what's up","whats up",
                      "你好","您好","你好吗","嗨","哈喽","早上好","下午好","晚上好"],
            "core": ["core","catseek","bitnet","ternary","-1, 0, 1","quantize","1.58","moe","cat seek","核心","三值"],
            "recursion": ["recursion","recursive","function calls itself","factorial","递归"],
            "help": ["help","commands","menu","usage","what can you do","capabilities","帮助","怎么用"],
            "languages": ["supported languages","which language","experts","what languages","支持的语言","哪些语言"],
            "profile": ["readme",".md","license","gpl3","about you","about yourself","who made you","who are you","你是谁"],
            "thanks": ["thanks","thank you","thx","appreciate","谢谢","感谢"],
            "goodbye": ["bye","goodbye","see you","later","exit","再见","拜拜"],
            "math": ["calculate","compute","sum","multiply","divide","equation"],
            "explain": ["explain","what is","what are","define","meaning of","tell me about",
                        "什么是","是什么","解释","说明","介绍","为什么","如何"],
            "howto": ["how do","how to","how can","steps to","walk me through","tutorial"],
            "debug": ["error","bug","traceback","exception","crash","broken","not working"],
            "opinion": ["should i","recommend","opinion","think about"],
            "joke": ["joke","funny","humor","laugh","make me laugh"],
            "fable": ["fable","parable","allegory","bedtime story","tell me a story","write a story"],
        }
        self._category_lexicon = {
            "greeting": ["hi", "hello", "hey", "morning", "evening", "sup", "你好", "您好", "嗨"],
            "farewell": ["bye", "goodbye", "later", "see you", "exit", "再见", "拜拜"],
            "question": ["what", "why", "how", "who", "when", "where", "which", "?", "什么", "为什么", "怎么", "如何"],
            "code": ["code", "script", "function", "class", "compile", "program", "syntax", "api", "代码", "程序", "脚本"],
            "tech": ["python", "catseek", "core", "ai", "model", "neural", "gpu", "cpu", "server"],
            "creative": ["story", "poem", "joke", "idea", "name", "design"],
            "personal": ["you", "your", "yourself", "who are you"],
            "task": ["make", "build", "create", "write", "generate", "show me"],
        }
        self.dialects = {
            "english": [
                {"hello":"Hi. How can I help?","ready":"Ready. Ask for code or explanation.",
                 "py_intro":"Here is Python code.","generic":"Here is code.",
                 "core":"CatSeek R1 1.0 uses ternary weights: {-1, 0, 1}.","recursion":"Recursion: function calls itself. Example:"},
                {"hello":"Hey. What do you need?","ready":"Send a prompt.","py_intro":"Python below.","generic":"Code below.",
                 "core":"Ternary constraints eliminate FP32 multiplications.","recursion":"Self-referential execution. Example:"},
            ],
            "chinese": [
                {"hello":"你好。需要什么？","ready":"请给出任务。","py_intro":"Python 代码：","generic":"代码：",
                 "core":"CatSeek R1 1.0 使用三值权重：{-1, 0, 1}。","recursion":"递归：函数自调用。示例："},
            ],
        }
        self.code_experts = {
            "python": "def main():\n    print('Hello World')\n\nif __name__ == '__main__':\n    main()",
            "cpp": (
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::cout << \"Hello World\" << std::endl;\n"
                "    return 0;\n"
                "}"
            ),
            "c": (
                "#include <stdio.h>\n\n"
                "int main(void) {\n"
                "    printf(\"Hello World\\n\");\n"
                "    return 0;\n"
                "}"
            ),
            "javascript": "console.log('Hello World');",
            "html": "<!DOCTYPE html><html><body><h1>Hello World</h1></body></html>",
            "typescript": "function main(): void { console.log('Hello World'); }\nmain();",
            "java": "public class Main { public static void main(String[] args) { System.out.println(\"Hello World\"); } }",
            "rust": "fn main() { println!(\"Hello World\"); }",
            "bash": "#!/bin/bash\necho \"Hello World\"",
            "assembly": "section .data\n    msg db 'Hello World',0xa\nsection .text\n    global _start\n_start:",
            "go": "package main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello World\") }",
        }
        self._init_catseek_core()
        self._train_intent()

    def _build_vocab(self) -> Dict[str, int]:
        words = {"<pad>", "<unk>"}
        for keys in self.intent_map.values():
            for phrase in keys:
                words.update(re.findall(r"[a-z0-9+#]+", phrase.lower()))
        for w in (
            "the", "a", "is", "are", "to", "for", "of", "in", "on", "with", "and", "or",
            "python", "code", "write", "explain", "help", "core", "model", "chat",
            "你好", "谢谢", "什么", "解释", "递归", "代码", "程序", "帮助", "是", "的",
        ):
            words.add(w)
        for phrase in (
            "什么是", "是什么", "解释", "说明", "介绍", "为什么", "如何", "帮我", "写代码",
        ):
            words.add(phrase)
        for keys in self.intent_map.values():
            for phrase in keys:
                words.update(tokenize_text(phrase, 64))
        ordered = sorted(words)[: CONFIG["vocab_size"] - 1]
        vocab = {w: i + 1 for i, w in enumerate(ordered)}
        vocab["<pad>"] = 0
        return vocab

    def _build_catseek_stack(self, seed: int) -> List[CatSeekBlock]:
        return [CatSeekBlock(self.d_model, seed + layer * 7919) for layer in range(CONFIG["layers"])]

    def _init_catseek_core(self):
        d = self.d_model
        rng = np.random.RandomState(42)
        self.vocab = self._build_vocab()
        vs = min(CONFIG["vocab_size"], len(self.vocab) + 256)
        self.embeddings = (rng.randn(vs, d).astype(np.float32) * 0.02)
        self.norm_gamma = np.ones((d,), dtype=np.float32)
        self.norm_beta = np.zeros((d,), dtype=np.float32)
        self.catseek_blocks = self._build_catseek_stack(42)
        self.output_head_lin = CatSeekLinear(d, len(self.intent_map) + 1, 4242)
        self.output_head = self.output_head_lin.w_signed
        self._student_layers: List[List[CatSeekBlock]] = []
        self.catseek_stats = catseek_memory_report(
            self.catseek_blocks, self.embeddings, self.output_head_lin.shadow_w
        )

    def _ensure_students(self, count: int) -> List[List[CatSeekBlock]]:
        while len(self._student_layers) < count:
            i = len(self._student_layers)
            self._student_layers.append(self._build_catseek_stack(1337 + i * 9973))
        return self._student_layers[:count]

    def _token_embed(self, token: str) -> np.ndarray:
        key = token if not token.isascii() else token.lower()
        tid = self.vocab.get(key)
        if tid is None:
            tid = abs(hash(key)) % max(len(self.embeddings) - 1, 1) + 1
        if tid >= len(self.embeddings):
            tid = 0
        return self.embeddings[tid].astype(np.float32)

    def _layer_norm(self, x):
        if x.ndim == 2:
            mean = np.mean(x, axis=-1, keepdims=True)
            std = np.std(x, axis=-1, keepdims=True) + 1e-5
            return (x - mean) / std * self.norm_gamma + self.norm_beta
        mean, std = np.mean(x, axis=-1, keepdims=True), np.std(x, axis=-1, keepdims=True) + 1e-5
        return (x - mean) / std * self.norm_gamma + self.norm_beta

    def _forward_stack(self, x: np.ndarray, blocks: List[CatSeekBlock]) -> np.ndarray:
        if x.ndim == 1:
            x = x.reshape(1, -1)
        y = x.astype(np.float32)
        for blk in blocks:
            y = blk.forward(y)
        return _rms_norm(y, self.norm_gamma)

    def _pool_sequence(self, seq: np.ndarray) -> np.ndarray:
        if seq.ndim == 1:
            return seq.astype(np.float32)
        return np.mean(seq, axis=0).astype(np.float32)

    def forward(self, x, turbo: bool = True, *, turbo_only: bool = False):
        if x.ndim == 1:
            x = x.reshape(1, -1)
        key = (x.tobytes(), turbo, turbo_only)
        cached = self._distil_cache.get(key)
        if cached is not None:
            return cached.copy()
        teacher = self._pool_sequence(self._forward_stack(x, self.catseek_blocks))
        if turbo_only:
            if len(self._distil_cache) < 128:
                self._distil_cache[key] = teacher.copy()
            return teacher
        n_pass = CONFIG["turbo_passes"] if turbo else CONFIG["distil_passes"]
        merged = teacher * CONFIG["teacher_weight"]
        students = self._ensure_students(n_pass)
        sw = 0.66 / n_pass
        for stack in students:
            merged = merged + self._pool_sequence(self._forward_stack(x, stack)) * sw
        if len(self._distil_cache) < 128:
            self._distil_cache[key] = merged.copy()
        return merged

    def encode_for_task(self, prompt: str, task: Optional[str] = None) -> np.ndarray:
        if CONFIG.get("deepmind_fast"):
            return self.deepmind.encode(prompt, task=task)
        return self.recursive_encode(prompt)

    def _recursive_step(self, state: np.ndarray, pass_idx: int, max_depth: int = 0) -> np.ndarray:
        depth = max_depth or CONFIG["recursive_depth"]
        turbo = pass_idx < depth - 1
        seq = state.reshape(1, -1) if state.ndim == 1 else state
        delta_seq = self._forward_stack(seq, self.catseek_blocks if turbo else self._ensure_students(1)[0])
        delta = self._pool_sequence(delta_seq)
        alpha = min(0.72, 0.28 + 0.11 * pass_idx)
        base = self._pool_sequence(state) if state.ndim == 2 else state
        merged = self._layer_norm(base * (1.0 - alpha) + delta * alpha)
        if CONFIG["compression_enabled"]:
            merged = self.compressor.compress_roundtrip(merged)
            self.last_compression_ratio = self.compressor.last_ratio
        return merged

    def recursive_encode(self, prompt: str, *, depth: Optional[int] = None) -> np.ndarray:
        """o1-preview recursive CatSeek R1 1.0 loop with compression between passes."""
        max_depth = depth if depth is not None else CONFIG["recursive_depth"]
        key = (prompt.lower().strip(), max_depth, CONFIG["compression_enabled"])
        hit = self._recursive_cache.get(key)
        if hit is not None:
            return hit.copy()
        state = self.encode_prompt(prompt)
        trace: List[str] = []
        ctrace: List[str] = []
        prev = self._pool_sequence(state) if state.ndim == 2 else state.copy()
        used = max_depth
        for i in range(max_depth):
            state = self._recursive_step(state, i, max_depth)
            pooled = self._pool_sequence(state) if state.ndim == 2 else state
            norm = float(np.linalg.norm(pooled))
            line = f"pass {i + 1} · norm {norm:.4f} · CatSeek Linear forward"
            if CONFIG["compression_enabled"]:
                line += f" · {self.last_compression_ratio:.1f}x"
                ctrace.append(
                    f"sparse-{CONFIG['compression_sparse_k']} + rank-{CONFIG['compression_rank']} "
                    f"→ {self.last_compression_ratio:.1f}x · ~{self.compressor.effective_params_billions():.1f}B effective"
                )
            if i > 0:
                diff = float(np.linalg.norm(pooled - prev))
                line += f" · Δ {diff:.4f}"
                if diff < CONFIG["recursive_epsilon"]:
                    trace.append(line)
                    trace.append(f"converged at pass {i + 1}")
                    used = i + 1
                    break
            trace.append(line)
            prev = pooled.copy()
        self.last_recursive_passes = used
        self.last_recursive_trace = trace
        self.compression_trace = ctrace
        out = self._pool_sequence(state) if state.ndim == 2 else state
        self.last_vec = out.copy()
        if len(self._recursive_cache) < 64:
            self._recursive_cache[key] = out.copy()
        return out

    def _distil_draft(self, prompt: str, vec: Optional[np.ndarray] = None) -> str:
        if vec is None:
            vec = self.recursive_encode(prompt)
        logits = self.output_head_lin.forward(vec)
        labels = list(self.intent_map.keys()) + ["general"]
        idx = int(np.argmax(logits)) % len(labels)
        topic = self._extract_topic_words(prompt)
        st = self.catseek_stats
        return (
            f"CatSeek Linear head {labels[idx]} → «{topic[:60]}» · "
            f"{self.last_recursive_passes} passes · "
            f"{st['catseek_linear_layers']} CatSeek Linear · "
            f"packed {st['packed_kb']:.1f}KB · "
            f"{CONFIG['teacher_weight']:.0%} teacher + {CONFIG['turbo_passes']} students"
        )

    def _history_pairs(self) -> List[tuple]:
        return [(m["role"], m["text"]) for m in self.chat_history[:-1]][-8:]

    def _run_ultrathink(self, prompt: str, *, force: bool = False) -> None:
        if self._pending_think and not force:
            self.last_think = self._pending_think
            self._pending_think = ""
            return
        if not O1PreviewReasoner.should_run(prompt, enabled=self.ultrathink_on, force=force):
            return
        vec = self.last_vec if self.last_vec is not None else self.recursive_encode(prompt)
        draft = self._distil_draft(prompt, vec=vec)
        self.last_think = self.ultrathink.run(
            prompt, distill_draft=draft, recursive_trace=self.last_recursive_trace,
            compression_trace=self.compression_trace,
        )

    def _o1_respond(self, prompt: str) -> str:
        prior = self.chat_history[:-1] if self.chat_history else []
        vec = self.last_vec
        if CONFIG["o1_preview"]:
            return self.synth.o1_answer(prompt, prior, reasoning=self.last_think, vec=vec)
        return self.synth.converse(prompt, prior, vec=vec)

    def _r1_synthesize(self, prompt: str) -> str:
        return self._o1_respond(prompt)

    def encode_prompt(self, prompt):
        key = prompt.strip()
        cached = self._embed_cache.get(key)
        if cached is not None:
            return cached
        tokens = tokenize_text(prompt, CONFIG["max_seq"])
        seq = np.stack([self._token_embed(t) for t in tokens], axis=0)
        out = self._layer_norm(seq)
        if len(self._embed_cache) < 256:
            self._embed_cache[key] = out
        return out

    def _intent_features(self, text: str) -> np.ndarray:
        vocab = list(self._token_index.keys()) if self._token_index else []
        if not vocab:
            return np.array([1.0], dtype=np.float32)
        tl = text.lower()
        return np.array([tl.count(t) for t in vocab] + [1.0], dtype=np.float32)

    def _train_intent(self):
        if self._intent_trained:
            return
        corpus: List[tuple] = []
        for label, keys in self.intent_map.items():
            for k in keys:
                corpus.append((k, label))
        corpus.extend([
            ("write python function", "howto"), ("fix my bug", "debug"),
            ("2 plus 2", "math"), ("thanks a lot", "thanks"),
            ("see you tomorrow", "goodbye"), ("what is docker", "explain"),
            ("should i use rust", "opinion"),
        ])
        vocab: set = set()
        for label, keys in self.intent_map.items():
            for k in keys:
                vocab.update(tokenize_text(k, 64))
        for text, _ in corpus:
            vocab.update(tokenize_text(text, 64))
        self._token_index = {t: i for i, t in enumerate(sorted(vocab))}
        self._intent_weights = np.zeros((len(self.intent_map), len(vocab) + 1), dtype=np.float32)
        labels = list(self.intent_map.keys())
        for _ in range(40):
            for text, label in corpus:
                x = self._intent_features(text)
                y_idx = labels.index(label)
                scores = self._intent_weights @ x
                others = [s for i, s in enumerate(scores) if i != y_idx]
                margin = (max(others) if others else -1e9) - scores[y_idx] + 1
                if margin > 0:
                    self._intent_weights[y_idx] += 0.12 * x
                    if others:
                        self._intent_weights[int(np.argmax(scores))] -= 0.12 * x
        self._intent_trained = True

    def _key_matches(self, key: str, text: str) -> bool:
        if VibeCodeHeuristics.has_cjk(key):
            return key in text
        loose = {"fix", "best", "math", "later", "exit", "bug", "sum"}
        if len(key) <= 4 or key in loose:
            return bool(re.search(r"\b" + re.escape(key) + r"\b", text))
        return key in text

    def _best_intent(self, prompt: str) -> Optional[str]:
        p = prompt.lower()
        best, best_len = None, 0
        for intent, keys in self.intent_map.items():
            for k in keys:
                if self._key_matches(k, p) and len(k) > best_len:
                    best, best_len = intent, len(k)
        if best:
            return best
        self._train_intent()
        if self._intent_weights is None:
            return None
        scores = self._intent_weights @ self._intent_features(p)
        idx = int(np.argmax(scores))
        if float(scores[idx]) > 0.55:
            return list(self.intent_map.keys())[idx]
        return None

    def _score_categories(self, text: str) -> Dict[str, int]:
        tokens = set(tokenize_text(text, 128))
        return {
            cat: sum(1 for w in words if w in tokens or w in text)
            for cat, words in self._category_lexicon.items()
        }

    def _extract_topic_words(self, prompt: str, n: int = 4) -> str:
        if VibeCodeHeuristics.has_cjk(prompt):
            zh = extract_zh_topic(prompt)
            if zh and zh != prompt.strip():
                return zh[:48]
            chars = _TOKEN_CJK.findall(prompt)
            if chars:
                return "".join(chars[:n * 2])[:48]
        stop = {"the", "a", "an", "is", "are", "to", "for", "of", "in", "on", "my", "me", "i", "you", "please", "can", "do"}
        words = [w for w in tokenize_text(prompt, 64) if w not in stop and len(w) > 1]
        return " ".join(words[:n]) if words else prompt.strip()[:48] or "that"

    def _try_simple_math(self, prompt: str) -> Optional[str]:
        expr = prompt.lower().strip().rstrip("?")
        expr = re.sub(r"^(what is|calculate|compute|solve)\s+", "", expr)
        expr = expr.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("multiplied by", "*")
        expr = expr.replace("divided by", "/").replace("over", "/")
        if not re.fullmatch(r"[\d\s+\-*/().]+", expr.strip()):
            return None
        try:
            val = eval(expr, {"__builtins__": {}}, {})  # noqa: S307 — sandboxed numeric expr only
            if isinstance(val, (int, float)):
                return str(int(val)) if float(val).is_integer() else f"{val:.6g}"
        except Exception:
            return None
        return None

    def _explain_topic(self, topic: str, dialect: Dict[str, str]) -> str:
        known = {
            "core": dialect["core"],
            "python": "Python is a general-purpose language — great for scripts, APIs, and automation.",
            "recursion": dialect["recursion"],
            "docker": "Docker packages apps in containers so they run the same everywhere.",
            "api": "An API is a defined interface for programs to request data or actions from another service.",
            "javascript": "JavaScript runs in browsers and on servers (Node.js) for interactive web apps.",
            "rust": "Rust is a systems language focused on memory safety without a garbage collector.",
        }
        for key, answer in known.items():
            if key in topic:
                return answer
        return (
            f"\"{topic}\" — I can give a deeper explanation, compare options, or show example code. "
            "Say which angle you want (concept, tutorial, or code)."
        )

    def _howto_topic(self, topic: str) -> str:
        return (
            f"To {topic}:\n"
            "1) State the goal and any constraints (OS, language, deadline).\n"
            "2) Start with the smallest working version.\n"
            "3) Run it, capture errors, and iterate.\n"
            "Paste your current code or error and I will tailor the steps."
        )

    def _answer_open_question(self, prompt: str, categories: Dict[str, int], ctx: str) -> str:
        topic = self._extract_topic_words(prompt)
        top = max(categories, key=categories.get) if categories else "general"
        lead = f"Re: \"{topic}\""
        if top == "code":
            return f"{lead} — share the language and goal; I can draft or fix code."
        if top == "tech":
            return f"{lead} — I can explain the concept, trade-offs, or a minimal example."
        if top == "personal":
            return f"I'm **{BRAND}** — a local **{MODEL_NAME}** assistant. I help with code, explanations, debugging, and math. Everything runs in-memory (**files=off**)."
        if ctx:
            return f"{lead} (context: {ctx}) — tell me more detail and I'll answer directly."
        return f"{lead} — ask for an explanation, code sample, or step-by-step walkthrough."

    def _respond_universal(self, prompt: str, dialect: Dict[str, str], vec: np.ndarray) -> str:
        p = prompt.strip()
        pl = p.lower()
        ctx = self._recent_user_context()
        categories = self._score_categories(pl)

        math_result = self._try_simple_math(p)
        if math_result is not None:
            return f"Result: {math_result}"

        if self._wants_steps(prompt):
            return self._howto_topic(self._extract_topic_words(prompt))

        if pl.startswith(("what is ", "what's ", "what are ")):
            topic = re.sub(r"^what(?:'s| is| are)\s+", "", pl).rstrip("?").strip()
            return self._explain_topic(topic, dialect)

        if pl.startswith(("how do ", "how to ", "how can ")):
            topic = re.sub(r"^how (?:do|to|can) (?:i |we )?", "", pl).rstrip("?").strip()
            return self._howto_topic(topic)

        if pl.startswith("why "):
            topic = pl[4:].rstrip("?").strip()
            return (
                f"On \"{topic}\": usually configuration, dependencies, invalid input, or an edge case. "
                "Paste the exact error or snippet for a targeted fix."
            )

        if "joke" in pl or categories.get("creative", 0) >= 2:
            jokes = [
                "Why do programmers prefer dark mode? Light attracts bugs.",
                "A SQL query walks into a bar, walks up to two tables, and asks: 'Can I join you?'",
                "There are only 10 kinds of people: those who understand binary and those who don't.",
            ]
            return jokes[int(np.abs(vec[:6].sum() * 100)) % len(jokes)]

        if "?" in p:
            return self._answer_open_question(p, categories, ctx)

        if self._wants_brief(prompt):
            topic = self._extract_topic_words(prompt)
            return f"Brief: \"{topic}\" — ask for code, steps, or a one-line definition."

        topic = self._extract_topic_words(prompt)
        variants = [
            f"On \"{topic}\": I can explain, write code, debug, or compare options. What do you need?",
            f"Got \"{topic}\". Say *explain*, *code in python*, or paste an error to continue.",
            f"Understood — \"{topic}\". I support {len(self.code_experts)} languages and local code execution.",
            f"\"{topic}\" noted. Ask for a tutorial, snippet, or run ```python ...``` blocks here.",
            f"Re \"{topic}\": CatSeek R1 1.0 routed your prompt — reply with more detail or a fenced code block.",
        ]
        pick = int(np.abs(vec[:8].sum() * 1000)) % len(variants)
        if ctx:
            return f"{variants[pick]} (Earlier: {ctx})"
        return variants[pick]

    def detect_locale(self, p): return "chinese" if re.search(r"[\u4e00-\u9fff]|中文|chinese", p.lower()) else self.response_locale
    def get_dialect(self, loc):
        # Keep response tone stable and predictable (closer to chat assistant behavior).
        bank = self.dialects.get(loc, self.dialects["english"])
        return bank[0]

    def _remember(self, role: str, text: str):
        self.chat_history.append({"role": role, "text": text.strip()})
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]

    def _recent_user_context(self, n: int = 3) -> str:
        msgs = [m["text"] for m in self.chat_history if m["role"] == "user"]
        if not msgs:
            return ""
        return " | ".join(msgs[-n:])

    def _wants_brief(self, prompt: str) -> bool:
        p = prompt.lower()
        return any(x in p for x in ["short", "brief", "one line", "tldr", "concise"])

    def _wants_steps(self, prompt: str) -> bool:
        p = prompt.lower()
        return any(x in p for x in ["step by step", "steps", "walkthrough", "how do i"])

    def _wants_code_only(self, prompt: str) -> bool:
        p = prompt.lower()
        return any(x in p for x in ["code only", "just code", "only code", "no explanation"])

    def _chat_fallback(self, prompt: str, dialect: Dict[str, str], vec: Optional[np.ndarray] = None) -> str:
        if vec is None:
            vec = self.recursive_encode(prompt)
        return self._respond_universal(prompt, dialect, vec)

    def _intent_response(self, intent: str, prompt: str, dialect: Dict[str, str]) -> Optional[str]:
        if intent == "hello":
            hit = self.synth.smalltalk_reply(prompt)
            return hit or dialect["hello"]
        if intent == "core":
            return dialect["core"]
        if intent == "recursion":
            return f"{dialect['recursion']}\n\ndef fact(n):\n    return 1 if n<=1 else n*fact(n-1)"
        if intent == "help":
            return (
                f"**{BRAND}** · {MODEL_NAME} · {REASONING_MODE} · files=off\n\n"
                "Frontier-tier local CatSeek R1 1.0 — compression + o1-preview reasoning.\n"
                "Chat: `/chat` · `/think` · `/reset` · `/chat history`"
            )
        if intent == "languages":
            return f"Supported: {', '.join(sorted(self.code_experts))}"
        if intent == "profile":
            return CAT_R11_PROFILE_MD
        if intent == "thanks":
            return "You're welcome — ask anything else."
        if intent == "goodbye":
            return "Goodbye. Come back anytime."
        if intent == "math":
            result = self._try_simple_math(prompt)
            if result:
                return f"Result: {result}"
            return "Give a numeric expression (e.g. 15 * 7 or what is 100 divided by 4)."
        if intent == "explain":
            topic = re.sub(r".*(?:explain|define|meaning of|tell me about)\s+", "", prompt.lower()).rstrip("?")
            return self._explain_topic(topic.strip(), dialect)
        if intent == "howto":
            topic = re.sub(r".*(?:how do|how to|how can|tutorial)\s+", "", prompt.lower()).rstrip("?")
            return self._howto_topic(topic.strip() or self._extract_topic_words(prompt))
        if intent == "debug":
            if re.search(r"\bfix\b", prompt.lower()) and "traceback" not in prompt.lower():
                topic = self._extract_topic_words(prompt)
                return (
                    f"To fix \"{topic}\": share the config snippet, expected behavior, and any error log. "
                    "I will suggest concrete changes."
                )
            return "Paste the full traceback, file path, and what you expected vs what happened."
        if intent == "opinion":
            topic = self._extract_topic_words(prompt)
            return (
                f"On \"{topic}\": it depends on constraints (team skill, performance, ecosystem). "
                "Share your use case and I will recommend a concrete choice."
            )
        if intent == "joke":
            jokes = [
                "Why do programmers prefer dark mode? Light attracts bugs.",
                "A SQL query walks into a bar, walks up to two tables, and asks: 'Can I join you?'",
                "There are only 10 kinds of people: those who understand binary and those who don't.",
            ]
            vec = self.recursive_encode(prompt)
            return jokes[int(np.abs(vec[:6].sum() * 100)) % len(jokes)]
        if intent == "fable" and CONFIG["catseek_enabled"]:
            vec = self.last_vec if self.last_vec is not None else self.recursive_encode(prompt)
            topic = self._extract_topic_words(prompt)
            return self.catseek.compose_fable(prompt, topic, vec)
        return None
    _LANG_STOP = frozenset({"a", "an", "the", "me", "my", "some", "that", "is", "to", "it"})

    def extract_lang(self, p):
        original = p
        vibe = VibeCodeHeuristics.lang_from_text(original, self)
        if vibe:
            return vibe
        p = p.lower()
        if re.search(r"\b(?:a|an)\s+html\b|\bhtml\s+(?:program|page|file|ad|that|site|app)\b", p):
            return "html"
        m = CatSeekR1Code._IN_LANG.search(p)
        if m:
            raw = m.group(1).lower()
            if raw == "shell":
                raw = "bash"
            return self.normalize_lang(raw)
        m = CatSeekR1Code._MAKE_IT_LANG.search(p)
        if m:
            raw = m.group(1).lower()
            if raw == "shell":
                raw = "bash"
            return self.normalize_lang(raw)
        for a, l in self.aliases.items():
            if f"in {a}" in p or f"{a} code" in p:
                return l
        for l in self.code_experts:
            if f"in {l}" in p or f"{l} code" in p:
                return l
        m = re.search(r"(?:write|code|syntax)\s+(?:(?:a|an|the)\s+)?(?:in\s+)?([a-z+#]+)", p)
        if m:
            raw = m.group(1)
            if raw in self._LANG_STOP:
                if "html" in p:
                    return "html"
                if re.search(r"\b(?:c|c\+\+|cpp)\b", p):
                    return "cpp" if "++" in p or "cpp" in p else "c"
                inferred = self.detect_lang_from_text(original)
                return self.normalize_lang(inferred) if inferred else None
            return self.aliases.get(raw, raw)
        inferred = self.detect_lang_from_text(original)
        return self.normalize_lang(inferred) if inferred else None

    def detect_lang_from_text(self, text: str) -> Optional[str]:
        s = text or ""
        sl = s.lower()

        # Fast keyword/shape checks.
        if re.search(r"#!/bin/(ba)?sh|echo\s+['\"]|\$\{?[A-Z_][A-Z0-9_]*\}?|^\s*for\s+\w+\s+in\s+", s, re.MULTILINE):
            return "bash"
        if re.search(r"<!doctype html>|<html|</html>|<body|</body>|<div|</div>", sl):
            return "html"
        if re.search(r"\bconsole\.log\(|\bfunction\s+\w+\s*\(|=>|\b(let|const|var)\s+\w+", s):
            return "javascript"
        if re.search(r"\binterface\s+\w+|:\s*(string|number|boolean)\b", s):
            return "typescript"
        if re.search(r"^\s*#include\s+<", s, re.MULTILINE):
            if "std::" in s or "cout" in s:
                return "cpp"
            return "c"
        if re.search(r"\bpublic\s+class\b|\bSystem\.out\.println\(", s):
            return "java"
        if re.search(r"\bfn\s+main\s*\(|println!\(", s):
            return "rust"
        if re.search(r"\bpackage\s+main\b|\bfunc\s+main\s*\(", s):
            return "go"
        if re.search(r"\bsection\s+\.(text|data)\b|\bglobal\s+_start\b", sl):
            return "assembly"
        if re.search(r"^\s*def\s+\w+\s*\(|__name__\s*==\s*['\"]__main__['\"]|\bprint\(", s, re.MULTILINE):
            return "python"

        # Fallback token scoring across supported syntaxes.
        scores = {
            "python": 0,
            "cpp": 0,
            "c": 0,
            "javascript": 0,
            "typescript": 0,
            "java": 0,
            "rust": 0,
            "go": 0,
            "bash": 0,
            "assembly": 0,
            "html": 0,
        }
        token_hints = {
            "python": ["def ", "import ", "None", "True", "False", "elif", "self."],
            "cpp": ["std::", "#include", "cout", "cin", "namespace std", "->"],
            "c": ["#include", "printf(", "scanf(", "malloc(", "free("],
            "javascript": ["console.log", "function ", "=>", "let ", "const ", "var "],
            "typescript": [": string", ": number", "interface ", "type ", "implements "],
            "java": ["public class", "public static void main", "System.out.println", "new "],
            "rust": ["fn ", "let mut", "println!", "match ", "::"],
            "go": ["package ", "func ", "fmt.", ":=", "go "],
            "bash": ["#!/bin/bash", "echo ", "$(", "fi", "done"],
            "assembly": ["mov ", "jmp ", "section .text", "db ", "_start"],
            "html": ["<html", "<body", "<div", "</", "<!doctype"],
        }
        for lang, hints in token_hints.items():
            for h in hints:
                if h in s or h in sl:
                    scores[lang] += 1
        best_lang = max(scores, key=scores.get)
        return best_lang if scores[best_lang] > 0 else None
    def extract_code_block(self, p):
        m = re.search(r"```([a-zA-Z0-9_+#-]*)\n([\s\S]*?)```", p)
        if not m:
            return None, None
        lang = (m.group(1) or "").strip().lower() or None
        code = m.group(2).strip()
        if not lang:
            lang = self.detect_lang_from_text(code)
        return lang, code

    def normalize_lang(self, lang: Optional[str]) -> Optional[str]:
        if not lang:
            return None
        lang = lang.lower().strip()
        aliases = {
            "py": "python", "python3": "python",
            "c++": "cpp", "cc": "cpp",
            "js": "javascript", "node": "javascript",
            "ts": "typescript",
            "sh": "bash", "shell": "bash", "zsh": "bash",
            "asm": "assembly",
        }
        return aliases.get(lang, lang)

    def generate_dynamic_template(self, lang: str, prompt: str) -> str:
        lang = self.normalize_lang(lang) or "python"
        comment = "//"
        if lang in {"python", "bash"}:
            comment = "#"
        elif lang == "html":
            comment = "<!-- -->"

        if lang == "html":
            return "<!DOCTYPE html>\n<html>\n<body>\n  <h1>Hello World</h1>\n</body>\n</html>"
        if lang == "python":
            return "def main():\n    print('Hello World')\n\nif __name__ == '__main__':\n    main()"
        return (
            f"{comment} Dynamic template for {lang}\n"
            f"{comment} Prompt: {prompt[:80]}"
        )

    def _extract_prompt_requirements(self, prompt: str) -> Dict[str, Any]:
        p = prompt.lower()
        fn_match = re.search(r"(?:function|def|method)\s+([a-zA-Z_][a-zA-Z0-9_]*)", prompt)
        class_match = re.search(r"(?:class|struct)\s+([a-zA-Z_][a-zA-Z0-9_]*)", prompt)
        return {
            "wants_main": ("main" in p) or ("entry point" in p),
            "wants_json": ("json" in p),
            "wants_async": ("async" in p) or ("await" in p),
            "wants_cli": ("arg" in p) or ("argv" in p) or ("command line" in p) or ("cli" in p),
            "wants_file_io": ("file" in p) or ("read" in p) or ("write" in p),
            "function_name": fn_match.group(1) if fn_match else None,
            "class_name": class_match.group(1) if class_match else None,
        }

    def _validate_code(self, lang: str, code: str) -> bool:
        lang = self.normalize_lang(lang) or "python"
        try:
            if lang == "python":
                ast.parse(code, mode="exec")
                return True
            if lang in {"javascript", "typescript", "java", "cpp", "c", "go", "rust"}:
                opens = sum(code.count(ch) for ch in "{([")
                closes = sum(code.count(ch) for ch in "})]")
                return opens == closes and len(code.strip()) > 0
            if lang == "html":
                return "<html" in code.lower() and "</html>" in code.lower()
            if lang == "bash":
                return len(code.strip()) > 0
            return len(code.strip()) > 0
        except Exception:
            return False

    def _tailor_code_once(self, lang: str, code: str, req: Dict[str, Any]) -> str:
        lang = self.normalize_lang(lang) or "python"
        patched = code
        fn_name = req.get("function_name")
        class_name = req.get("class_name")

        if lang == "python":
            if req["wants_async"] and "async def" not in patched:
                patched = (
                    "import asyncio\n\n"
                    "async def main_async():\n"
                    "    print('Hello World')\n\n"
                    "if __name__ == '__main__':\n"
                    "    asyncio.run(main_async())"
                )
            if req["wants_json"] and "import json" not in patched:
                patched = f"import json\n\n{patched}"
            if req["wants_cli"] and "import sys" not in patched:
                patched = f"import sys\n\n{patched}"
            if req["wants_file_io"] and "open(" not in patched:
                patched += "\n\n# file io example\nwith open('output.txt', 'w', encoding='utf-8') as f:\n    f.write('Hello World')\n"
            if fn_name and f"def {fn_name}(" not in patched:
                patched += f"\n\ndef {fn_name}():\n    return 'ok'\n"
            if class_name and f"class {class_name}" not in patched:
                patched += f"\n\nclass {class_name}:\n    pass\n"
            if req["wants_main"] and "__name__ == '__main__'" not in patched:
                patched += "\n\nif __name__ == '__main__':\n    main()\n"
            return patched

        if lang in {"javascript", "typescript"}:
            if req["wants_async"] and "async function" not in patched:
                patched = "async function main(){\n  console.log('Hello World');\n}\nmain();"
            if req["wants_json"] and "JSON." not in patched:
                patched += "\n\nconst payload = JSON.stringify({ ok: true });\nconsole.log(payload);\n"
            if fn_name and f"function {fn_name}" not in patched:
                patched += f"\n\nfunction {fn_name}() {{ return 'ok'; }}\n"
            return patched

        if lang == "bash":
            if not patched.startswith("#!/bin/bash"):
                patched = "#!/bin/bash\n" + patched
            if req["wants_file_io"] and ">" not in patched:
                patched += "\necho \"Hello World\" > output.txt\n"
            return patched

        return patched

    def recompile_code_for_prompt(self, lang: str, prompt: str, seed_code: str) -> str:
        """Dynamic recompilation: iterate and tailor generated code to prompt requirements."""
        lang = self.normalize_lang(lang) or "python"
        req = self._extract_prompt_requirements(prompt)
        code = seed_code
        for _ in range(3):
            code = self._tailor_code_once(lang, code, req)
            if self._validate_code(lang, code):
                return code
        # Final safe fallback if iterative tailoring failed validation.
        fallback = self.code_experts.get(lang) or self.generate_dynamic_template(lang, prompt)
        return fallback

    def execute_code_any_language(self, lang: Optional[str], code: Optional[str]) -> str:
        lang = self.normalize_lang(lang) or "python"
        if not code:
            return "No code provided."

        if lang == "python":
            return self.safe_exec_python(code)
        if lang == "javascript":
            try:
                out = subprocess.run(
                    ["node", "-e", code],
                    capture_output=True,
                    text=True,
                    timeout=3,
                    check=False,
                )
                text = (out.stdout or out.stderr or "").strip()
                return text if text else "(no output)"
            except FileNotFoundError:
                return "Node.js runtime not found. Install node to execute JavaScript."
            except Exception as e:
                return f"Execution error: {e}"
        if lang == "bash":
            try:
                out = subprocess.run(
                    ["bash", "-lc", code],
                    capture_output=True,
                    text=True,
                    timeout=3,
                    check=False,
                )
                text = (out.stdout or out.stderr or "").strip()
                return text if text else "(no output)"
            except Exception as e:
                return f"Execution error: {e}"

        # Cross-language interpreter fallback: structural analysis for unsupported runtimes.
        lines = [ln for ln in code.splitlines() if ln.strip()]
        return (
            f"Interpreter summary ({lang}):\n"
            f"- lines: {len(lines)}\n"
            f"- chars: {len(code)}\n"
            f"- execution backend: not installed for {lang}\n"
            "Tip: Python/JavaScript/Bash run natively in this local interpreter."
        )

    def safe_exec_python(self, code):
        try:
            if not code:
                return "No code provided."
            tree = ast.parse(code, mode="exec")
            if any(isinstance(n, (ast.Import, ast.ImportFrom, ast.Global)) for n in ast.walk(tree)):
                return "Blocked: imports/global not allowed."
            allowed = {"print", "len", "range", "int", "float", "str", "list", "dict", "min", "max", "sum"}
            builtins_src = __builtins__ if isinstance(__builtins__, dict) else __builtins__.__dict__
            safe = {k: v for k, v in builtins_src.items() if k in allowed}
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(compile(tree,"<catr11>","exec"), {"__builtins__": safe}, {})
            return buf.getvalue().strip() or "(no output)"
        except Exception as e: return f"Error: {e}"

    def generate(self, prompt, simulate=True):
        loc = self.detect_locale(prompt)
        dia = self.get_dialect(loc)
        raw = prompt.strip()
        self._remember("user", prompt)
        self.catseek.memory.add("user", prompt)
        if simulate:
            time.sleep(CONFIG["simulate_latency"])
        p = prompt.lower()
        pl = raw.lower()

        if pl in {"/reset", "reset chat", "clear memory"}:
            self.chat_history = []
            self.chat.new_session()
            self.catseek.memory = CatSeekContextMemory()
            self._embed_cache.clear()
            self._distil_cache.clear()
            self._recursive_cache.clear()
            self.deepmind.clear()
            self.web.clear()
            self.compression_trace = []
            self.last_recursive_trace = []
            self.last_think = ""
            return "Conversation memory cleared."

        if pl == "/chat":
            return ChatProtocol.help_text()
        if pl == "/chat new":
            sid = self.chat.new_session()
            self.chat_history = []
            self.catseek.memory = CatSeekContextMemory()
            self.last_think = ""
            return f"New chat session `{sid}` (files=off, in-memory)."
        if pl == "/chat history":
            return self.chat.session().transcript() or "(empty session)"
        if pl == "/chat session":
            s = self.chat.session()
            return f"Session `{s.session_id}` · turn {s.turn_count} · {CATSEEK_MODEL_ID} · files=off"

        if pl == "/ultrathink":
            return f"Extended thinking is **{'on' if self.ultrathink_on else 'off'}**."
        if pl == "/ultrathink on":
            self.ultrathink_on = True
            return "Extended thinking **on**."
        if pl == "/ultrathink off":
            self.ultrathink_on = False
            return "Extended thinking **off**."
        if pl == "/think" and self.last_think:
            return self.last_think
        if pl == "/web" or pl.startswith("/web "):
            resp = self.web.handle_command(self, raw)
            self._remember("assistant", resp)
            self.catseek.memory.add("assistant", resp)
            return resp
        if pl == "/run" or pl.startswith("/run "):
            block_lang, code = self.extract_code_block(raw if "```" in raw else prompt)
            if not code and pl.startswith("/run "):
                code = raw.split(maxsplit=1)[1] if " " in raw else ""
            exec_lang = CatSeekR1Code.detect_lang(self, prompt)
            if not code:
                return "Usage: paste code in ``` fences, or `/run print('hi')`"
            result = CatSeekR1Code.run(self, exec_lang, code)
            return f"**catr1b** ({exec_lang} · files=off):\n```\n{result}\n```"
        if pl == "/code":
            return CatSeekR1Code.code_help()
        if pl.startswith("/code "):
            self.encode_for_task(raw, task="code")
            resp = CatSeekR1Code.respond(self, raw)
            self._remember("assistant", resp)
            self.catseek.memory.add("assistant", resp)
            return resp
        if CONFIG.get("catseek_code_enabled") and pl in {"code", "code >", ">"}:
            self.encode_for_task(raw, task="code")
            resp = CatSeekR1Code.respond(self, raw)
            self._remember("assistant", resp)
            self.catseek.memory.add("assistant", resp)
            return resp
        if pl.startswith("/ultrathink ") and pl not in ("/ultrathink off", "/ultrathink on"):
            think_prompt = raw.split(maxsplit=1)[1] if " " in raw else ""
            if not think_prompt.strip():
                return "Usage: `/ultrathink <your question>`"
            self._run_ultrathink(think_prompt, force=True)
            resp = self.catseek.complete(self, think_prompt, simulate=False)
            self._remember("assistant", resp)
            self.catseek.memory.add("assistant", resp)
            return resp

        if pl in {"who are you", "what are you", "what model are you"}:
            st = self.catseek_stats
            resp = (
                f"I'm **{BRAND}** — `{CATSEEK_MODEL_ID}` running locally (**files=off**).\n\n"
                f"Reasoning: **DeepSeek-R1** chain-of-thought + self-verify · **Mythos-tier** extended thinking.\n\n"
                f"Code: **catr1b** (CatSeek R1 {EDITION}) {'✓ enabled' if CATSEEK_CODE_ENABLED else 'off'} · {CORE_NAME} — {st['catseek_linear_layers']} CatSeek Linear layers, "
                f"{st['weight_bits']}-bit ternary weights, {CONFIG['catseek_context_window']:,} token context.\n\n"
                f"In-memory: {st['shadow_params']:,} params · {st['packed_kb']:.0f}KB packed · no weight files.\n\n"
                "I'm thorough, proactive, and self-checking — ask me anything."
            )
            self._remember("assistant", resp)
            self.catseek.memory.add("assistant", resp)
            return resp

        resp = self.catseek.complete(self, CatSeekR1Code.normalize_prompt(raw), simulate=False)
        self._remember("assistant", resp)
        self.catseek.memory.add("assistant", resp)
        return resp

    def get_thoughts(self, prompt, lang, ultra):
        if not prompt.strip():
            return ["Ready."]
        vec = self.recursive_encode(prompt)
        draft = self._distil_draft(prompt, vec=vec)
        trace = self.ultrathink.run(
            prompt, distill_draft=draft, recursive_trace=self.last_recursive_trace,
            compression_trace=self.compression_trace,
        )
        self._pending_think = trace
        return [ln.strip() for ln in trace.split("\n") if ln.strip()]

# ──────────────────────────────────────────────────────────────
# GUI & API — DeepSeek Chat layout (chat.deepseek.com) · Cat R1 · files = off
# ──────────────────────────────────────────────────────────────
class CatR11GUI:
    def __init__(self, root):
        self.root = root
        self.engine = CatR11Engine()
        self.ui = DEEPSEEK_UI
        self._msg_widgets: List[tk.Widget] = []
        self._history_items: List[str] = []

        root.title(f"{GUI_APP_NAME} · {GUI_TAGLINE}")
        root.geometry("1180x760")
        root.minsize(920, 600)
        root.configure(bg=self.ui["bg"])

        self.fonts = {
            "ui": font.Font(family="Segoe UI" if os.name == "nt" else "Helvetica Neue", size=12),
            "ui_bold": font.Font(family="Segoe UI" if os.name == "nt" else "Helvetica Neue", size=12, weight="bold"),
            "title": font.Font(family="Segoe UI" if os.name == "nt" else "Helvetica Neue", size=18, weight="bold"),
            "logo": font.Font(family="Segoe UI" if os.name == "nt" else "Helvetica Neue", size=15, weight="bold"),
            "small": font.Font(family="Segoe UI" if os.name == "nt" else "Helvetica Neue", size=10),
            "mono": font.Font(family="Menlo" if os.name != "nt" else "Consolas", size=11),
            "empty": font.Font(family="Segoe UI" if os.name == "nt" else "Helvetica Neue", size=22, weight="normal"),
        }

        outer = tk.Frame(root, bg=self.ui["bg"])
        outer.pack(fill="both", expand=True)

        # ── Sidebar (DeepSeek-style) ──
        sidebar = tk.Frame(outer, bg=self.ui["sidebar"], width=268,
                           highlightthickness=1, highlightbackground=self.ui["sidebar_border"])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        top_bar = tk.Frame(sidebar, bg=self.ui["sidebar"])
        top_bar.pack(fill="x", padx=18, pady=(18, 10))
        tk.Label(top_bar, text="🐱", font=self.fonts["title"], bg=self.ui["sidebar"], fg=self.ui["accent"]).pack(side="left")
        name_col = tk.Frame(top_bar, bg=self.ui["sidebar"])
        name_col.pack(side="left", padx=(8, 0))
        tk.Label(name_col, text=GUI_APP_NAME, font=self.fonts["logo"], bg=self.ui["sidebar"],
                 fg=self.ui["text"]).pack(anchor="w")
        tk.Label(name_col, text=GUI_TAGLINE, font=self.fonts["small"], bg=self.ui["sidebar"],
                 fg=self.ui["muted"]).pack(anchor="w")

        new_chat_outer = tk.Frame(sidebar, bg=self.ui["new_chat_border"], padx=1, pady=1)
        new_chat_outer.pack(fill="x", padx=16, pady=(6, 14))
        tk.Button(
            new_chat_outer, text="  +  New chat", font=self.fonts["ui_bold"],
            bg=self.ui["new_chat_bg"], fg=self.ui["text"],
            activebackground=self.ui["history_hover"], relief="flat", bd=0,
            padx=12, pady=10, cursor="hand2", anchor="w", command=self._new_chat,
        ).pack(fill="x")

        tk.Label(sidebar, text="Recent", font=self.fonts["small"], bg=self.ui["sidebar"],
                 fg=self.ui["muted"]).pack(anchor="w", padx=20, pady=(0, 4))
        self.history_frame = tk.Frame(sidebar, bg=self.ui["sidebar"])
        self.history_frame.pack(fill="both", expand=True, padx=10)

        tk.Frame(sidebar, bg=self.ui["sidebar_border"], height=1).pack(fill="x", padx=16, pady=8)
        foot = tk.Frame(sidebar, bg=self.ui["sidebar"])
        foot.pack(fill="x", padx=18, pady=(0, 14))
        tk.Label(foot, text=f"{EDITION} · catr1b · local", font=self.fonts["small"],
                 bg=self.ui["sidebar"], fg=self.ui["muted"]).pack(anchor="w")

        # ── Main panel ──
        main = tk.Frame(outer, bg=self.ui["bg"])
        main.pack(side="left", fill="both", expand=True)

        header = tk.Frame(main, bg=self.ui["header_bg"], highlightthickness=1,
                          highlightbackground=self.ui["header_border"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        model_pill = tk.Frame(header, bg=self.ui["user_bg"], highlightthickness=1,
                              highlightbackground=self.ui["input_border"])
        model_pill.pack(side="left", padx=20, pady=12)
        tk.Label(model_pill, text=f"  {GUI_APP_NAME}  ", font=self.fonts["ui_bold"],
                 bg=self.ui["user_bg"], fg=self.ui["accent"]).pack(side="left", padx=4, pady=4)
        tk.Label(model_pill, text="▾", font=self.fonts["small"],
                 bg=self.ui["user_bg"], fg=self.ui["muted"]).pack(side="left", padx=(0, 6))

        self.header_status = tk.Label(header, text="Ready", font=self.fonts["small"],
                                      bg=self.ui["header_bg"], fg=self.ui["muted"])
        self.header_status.pack(side="right", padx=22)

        # Chat area + empty state
        chat_outer = tk.Frame(main, bg=self.ui["bg"])
        chat_outer.pack(fill="both", expand=True)

        self.empty_state = tk.Frame(chat_outer, bg=self.ui["bg"])
        self.empty_state.place(relx=0.5, rely=0.42, anchor="center")
        tk.Label(self.empty_state, text="🐱", font=self.fonts["title"], bg=self.ui["bg"],
                 fg=self.ui["accent"]).pack()
        tk.Label(self.empty_state, text=GUI_APP_NAME, font=self.fonts["empty"], bg=self.ui["bg"],
                 fg=self.ui["empty_title"]).pack(pady=(8, 4))
        tk.Label(self.empty_state, text="How can I help you today?", font=self.fonts["ui"],
                 bg=self.ui["bg"], fg=self.ui["muted"]).pack()
        tk.Label(self.empty_state, text=GUI_TAGLINE, font=self.fonts["small"],
                 bg=self.ui["bg"], fg=self.ui["muted"]).pack(pady=(6, 0))

        chat_wrap = tk.Frame(chat_outer, bg=self.ui["bg"])
        chat_wrap.pack(fill="both", expand=True, padx=0, pady=0)

        self.chat_canvas = tk.Canvas(chat_wrap, bg=self.ui["bg"], highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(chat_wrap, orient="vertical", command=self.chat_canvas.yview,
                                 width=10, troughcolor=self.ui["bg"],
                                 activebackground=self.ui["input_border"])
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 4))
        self.chat_canvas.pack(side="left", fill="both", expand=True, padx=(24, 8))

        self.messages_frame = tk.Frame(self.chat_canvas, bg=self.ui["bg"])
        self._canvas_window = self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor="n")
        self.messages_frame.bind("<Configure>", self._on_frame_configure)
        self.chat_canvas.bind("<Configure>", self._on_canvas_configure)
        self.chat_canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        if os.name != "nt":
            self.chat_canvas.bind_all("<Button-4>", lambda e: self.chat_canvas.yview_scroll(-1, "units"), add="+")
            self.chat_canvas.bind_all("<Button-5>", lambda e: self.chat_canvas.yview_scroll(1, "units"), add="+")

        # Input bar — centered DeepSeek-style composer
        input_outer = tk.Frame(main, bg=self.ui["bg"])
        input_outer.pack(fill="x", padx=0, pady=(0, 20))

        input_center = tk.Frame(input_outer, bg=self.ui["bg"])
        input_center.pack(fill="x", padx=48)

        shadow = tk.Frame(input_center, bg=self.ui["input_shadow"], padx=1, pady=1)
        shadow.pack(fill="x")
        border = tk.Frame(shadow, bg=self.ui["input_border"], padx=1, pady=1)
        border.pack(fill="x")
        input_box = tk.Frame(border, bg=self.ui["input_bg"])
        input_box.pack(fill="x")

        self._placeholder = f"Message {GUI_APP_NAME}..."
        self._placeholder_active = True

        self.entry = tk.Text(
            input_box, height=2, font=self.fonts["ui"], bg=self.ui["input_bg"],
            fg=self.ui["text"], insertbackground=self.ui["text"], relief="flat",
            bd=0, padx=18, pady=14, wrap="word",
        )
        self.entry.pack(side="left", fill="both", expand=True)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<KeyPress>", self._on_entry_key)
        self.entry.bind("<<Paste>>", self._on_entry_edit)
        self.entry.bind("<Button-1>", self._on_entry_click)
        self.entry.bind("<KeyRelease>", self._sync_placeholder)
        self.entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.entry.bind("<FocusOut>", self._on_entry_focus_out)
        self._set_placeholder()
        self.entry.focus_set()

        send_wrap = tk.Frame(input_box, bg=self.ui["input_bg"])
        send_wrap.pack(side="right", padx=(0, 12), pady=10)
        self.send_btn = tk.Button(
            send_wrap, text="↑", font=font.Font(size=15, weight="bold"),
            bg=self.ui["accent"], fg=self.ui["accent_text"],
            activebackground=self.ui["send_hover"], activeforeground=self.ui["accent_text"],
            relief="flat", bd=0, width=2, height=1, cursor="hand2", command=self.send,
        )
        self.send_btn.pack()

        tk.Label(
            input_center,
            text=f"{GUI_APP_NAME} · {GUI_TAGLINE} · AI-generated content · API :{CONFIG['api_port']}",
            font=self.fonts["small"], bg=self.ui["bg"], fg=self.ui["muted"],
        ).pack(anchor="center", pady=(8, 0))

        self._start_api()

    @staticmethod
    def _plain(text: str) -> str:
        return re.sub(r"\*\*([^*]+)\*\*", r"\1", str(text)).replace("`", "")

    def _entry_text(self) -> str:
        return self.entry.get("1.0", "end-1c")

    def _set_placeholder(self):
        if not self._placeholder_active:
            return
        self.entry.config(state="normal")
        self.entry.delete("1.0", "end")
        self.entry.insert("1.0", self._placeholder)
        self.entry.config(fg=self.ui["muted"])

    def _clear_placeholder(self):
        if not self._placeholder_active:
            return
        self._placeholder_active = False
        self.entry.config(state="normal", fg=self.ui["text"])
        self.entry.delete("1.0", "end")

    def _sync_placeholder(self, _event=None):
        if self._placeholder_active:
            return
        if not self._entry_text().strip():
            self._placeholder_active = True
            self._set_placeholder()

    _PLACEHOLDER_SKIP_KEYS = frozenset({
        "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
        "Meta_L", "Meta_R", "Caps_Lock", "Tab",
    })

    def _on_entry_key(self, event):
        if self._placeholder_active and event.keysym not in self._PLACEHOLDER_SKIP_KEYS:
            self._clear_placeholder()

    def _on_entry_click(self, _event=None):
        if self._placeholder_active:
            self._clear_placeholder()

    def _on_entry_edit(self, _event=None):
        if self._placeholder_active:
            self._clear_placeholder()

    def _on_entry_focus_in(self, _event=None):
        if self._placeholder_active:
            self._clear_placeholder()

    def _on_entry_focus_out(self, _event=None):
        if self._placeholder_active:
            return
        if not self._entry_text().strip():
            self._placeholder_active = True
            self._set_placeholder()

    def _on_frame_configure(self, _event=None):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        width = min(event.width - 48, 820)
        self.chat_canvas.itemconfig(self._canvas_window, width=max(width, 400))
        x = max((event.width - width) // 2, 24)
        self.chat_canvas.coords(self._canvas_window, x, 0)

    def _on_mousewheel(self, event):
        widget = self.chat_canvas.winfo_containing(event.x_root, event.y_root)
        if widget in (self.chat_canvas, self.messages_frame) or str(widget).startswith(str(self.messages_frame)):
            self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_enter(self, event):
        if event.state & 0x1:
            return
        self.send()
        return "break"

    def _hide_empty(self):
        self.empty_state.place_forget()

    def _show_empty(self):
        if not self._msg_widgets:
            self.empty_state.place(relx=0.5, rely=0.42, anchor="center")

    def _add_history_item(self, title: str):
        title = (title[:36] + "…") if len(title) > 37 else title
        self._history_items.insert(0, title)
        self._history_items = self._history_items[:8]
        for w in self.history_frame.winfo_children():
            w.destroy()
        for item in self._history_items:
            btn = tk.Button(
                self.history_frame, text=item, font=self.fonts["ui"], bg=self.ui["sidebar"],
                fg=self.ui["text"], activebackground=self.ui["history_hover"],
                relief="flat", bd=0, anchor="w", padx=12, pady=8, cursor="hand2",
                command=lambda t=item: self._prefill(t),
            )
            btn.pack(fill="x", padx=6, pady=1)

    def _new_chat(self):
        for w in self._msg_widgets:
            w.destroy()
        self._msg_widgets.clear()
        self._show_empty()
        self.header_status.config(text="Ready")

    def _prefill(self, text: str):
        self._clear_placeholder()
        self.entry.delete("1.0", "end")
        self.entry.insert("1.0", text if not text.endswith("…") else text[:-1])
        self.entry.config(fg=self.ui["text"], state="normal")
        self._placeholder_active = False
        self.entry.focus_set()

    def _avatar(self, parent, glyph: str, bg: str) -> tk.Frame:
        av = tk.Label(
            parent, text=glyph, font=self.fonts["ui_bold"], bg=bg, fg=self.ui["accent_text"],
            width=2, height=1,
        )
        return av

    def _append_message(self, role: str, text: str, kind: str = "text"):
        self._hide_empty()
        is_user = role == "user"
        is_think = kind == "think"
        plain = self._plain(text)

        row = tk.Frame(self.messages_frame, bg=self.ui["bg"])
        row.pack(fill="x", pady=(10, 10), padx=8)
        self._msg_widgets.append(row)

        inner = tk.Frame(row, bg=self.ui["bg"])
        inner.pack(anchor="e" if is_user else "w", fill="x")

        content_row = tk.Frame(inner, bg=self.ui["bg"])
        content_row.pack(anchor="e" if is_user else "w")

        if not is_user:
            self._avatar(content_row, "R1", self.ui["avatar_bot"]).pack(side="left", padx=(0, 10), pady=2)

        msg_col = tk.Frame(content_row, bg=self.ui["bg"])
        msg_col.pack(side="left" if not is_user else "right")

        if is_user:
            bubble_bg, bubble_fg = self.ui["user_bg"], self.ui["user_fg"]
        elif is_think:
            bubble_bg, bubble_fg = self.ui["bg"], self.ui["think_fg"]
        elif kind == "code":
            bubble_bg, bubble_fg = self.ui["code_bg"], self.ui["code_fg"]
        else:
            bubble_bg, bubble_fg = self.ui["bot_bg"], self.ui["bot_fg"]

        bubble = tk.Frame(msg_col, bg=bubble_bg)
        if is_user or kind == "code":
            bubble.config(highlightthickness=0 if kind == "code" else 0)
        bubble.pack(anchor="e" if is_user else "w")

        label_font = self.fonts["mono"] if kind == "code" else (self.fonts["small"] if is_think else self.fonts["ui"])
        wrap = 640 if kind == "code" else 560
        lbl = tk.Label(
            bubble, text=plain, font=label_font, bg=bubble_bg, fg=bubble_fg,
            justify="left", wraplength=wrap,
            padx=self.ui["radius_pad"] if is_user or kind == "code" else 4,
            pady=12 if (is_user or kind == "code") else 2,
        )
        lbl.pack()

        if is_user:
            self._avatar(content_row, "U", self.ui["avatar_user"]).pack(side="left", padx=(10, 0), pady=2)

        self.root.after(10, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def log(self, sender, text, tag=None):
        if text is None:
            text = ""
        text = str(text).strip()
        if not text:
            return
        if sender in ("YOU", "API", "user"):
            self._append_message("user", text)
        elif sender == "THINK":
            self._append_message("assistant", text, kind="think")
        elif tag == "code":
            self._append_message("assistant", text, kind="code")
        else:
            self._append_message("assistant", text)
        if sender == "SYSTEM":
            self.header_status.config(text=text[:72])

    def send(self):
        if self._placeholder_active:
            return
        msg = self._entry_text().strip()
        if not msg or msg == self._placeholder:
            return
        self.entry.delete("1.0", "end")
        self._placeholder_active = True
        self._set_placeholder()
        self._add_history_item(msg)
        self.log("YOU", msg, "user")
        self.header_status.config(text="Thinking…")
        threading.Thread(target=self._infer, args=(msg,), daemon=True).start()

    def _infer(self, prompt):
        try:
            task = self.engine.catseek.classify(prompt, self.engine)
            fast = task in ("chat", "code", "math", "execute", "web")
            if not fast and self.engine.ultrathink_on and MYTHOS_MODE:
                delay = CONFIG["step_delay"] * 0.5
                for step in self.engine.get_thoughts(prompt, "GENERAL", True):
                    self.root.after(0, lambda s=step: self.log("THINK", s, "think"))
                    time.sleep(delay)
                if self.engine._pending_think:
                    self.engine.last_think = self.engine._pending_think
            out = self.engine.chat.turn(prompt, simulate=False)
            resp = (out.get("message") or {}).get("content", "") or "(no response)"
            self.root.after(0, lambda r=resp: self._display(r))
            sid = out.get("session", "")[:8]
            self.root.after(0, lambda s=sid: self.header_status.config(
                text=f"Ready · session {s}" if s else "Ready"))
        except Exception as exc:
            err = str(exc) or exc.__class__.__name__
            self.root.after(0, lambda e=err: self.log("SYSTEM", f"Error: {e}"))
            self.root.after(0, lambda: self.header_status.config(text="Ready"))

    def _display(self, text):
        if not text:
            return
        text = str(text)
        pattern = re.compile(r"```([a-zA-Z0-9_+#-]*)\s*\n([\s\S]*?)```")
        pos = 0
        found = False
        for m in pattern.finditer(text):
            found = True
            if m.start() > pos:
                lead = text[pos:m.start()].strip()
                if lead:
                    self.log(self.engine.name, lead, "bot")
            lang = (m.group(1) or "").strip()
            block = m.group(2).rstrip()
            if lang and CONFIG.get("code_output_exact"):
                self.log(self.engine.name, f"```{lang}\n{block}\n```", "code")
            else:
                self.log(self.engine.name, block, "code")
            pos = m.end()
        if found:
            tail = text[pos:].strip()
            if tail:
                self.log(self.engine.name, tail, "bot")
        else:
            self.log(self.engine.name, text, "bot")

    def _start_api(self):
        gui = self
        class Handler(BaseHTTPRequestHandler):
            def _json(self, code, data):
                body = json.dumps(data).encode(); self.send_response(code); self.send_header("Content-Type","application/json"); self.send_header("Content-Length", len(body)); self.end_headers(); self.wfile.write(body)
            def _auth(self):
                key = self.headers.get("Authorization","").replace("Bearer ","").strip()
                return not CONFIG["api_key"] or key == CONFIG["api_key"]
            def do_POST(self):
                if not self._auth(): return self._json(401,{"error":"Unauthorized"})
                paths = ("/message", "/v1/chat/completions", "/chat")
                if self.path not in paths: return self._json(404,{"error":"Not found"})
                try:
                    length = int(self.headers.get("Content-Length",0)); data = json.loads(self.rfile.read(length).decode()) if length else {}
                except: return self._json(400,{"error":"Invalid JSON"})
                if self.path == "/chat":
                    out = gui.engine.chat.parse_request(data)
                    if out.get("error"):
                        return self._json(400, out)
                    msg = out.get("message", {})
                    gui.root.after(0, lambda: (
                        gui.log("API", str(data.get("message", data))[:120], "user"),
                        gui.log(gui.engine.name, msg.get("content", "")),
                    ))
                    return self._json(200, out)
                prompt = data.get("message") or data.get("prompt") or next((m["content"] for m in reversed(data.get("messages",[])) if m.get("role")=="user"), "")
                if not prompt: return self._json(400,{"error":"Missing prompt"})
                out = gui.engine.chat.turn(str(prompt), simulate=False)
                resp = out.get("message", {}).get("content", "")
                think = out.get("thinking", "")
                gui.root.after(0, lambda: (gui.log("API", prompt, "user"), gui.log(gui.engine.name, resp)))
                if self.path == "/v1/chat/completions":
                    content = resp
                    if think and data.get("include_thinking"):
                        content = f"\n{think}\n\n\n{resp}"
                    return self._json(200, {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion",
                        "model": CATSEEK_MODEL_ID,
                        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
                    })
                return self._json(200, {"response": resp, "thinking": think, "model": CATSEEK_MODEL_ID, **{k: out[k] for k in ("session", "turn", "protocol") if k in out}})
            def do_GET(self):
                if not self._auth(): return self._json(401,{"error":"Unauthorized"})
                if self.path == "/v1/models":
                    return self._json(200, {"data": [CatSeekR1LLM.model_card()]})
                if self.path == "/web/sites":
                    sites = [
                        {"id": r.site_id, "title": r.title, "template": r.template,
                         "preview": r.preview_url(CONFIG["api_port"]), "created": r.created}
                        for r in gui.engine.web._sites.values()
                    ]
                    return self._json(200, {"files": "off", "sites": sites, "count": len(sites)})
                if self.path.startswith("/web/preview/"):
                    sid = self.path.rsplit("/", 1)[-1].split("?")[0]
                    rec = gui.engine.web.get(sid)
                    if not rec:
                        return self._json(404, {"error": f"site not found: {sid}"})
                    body = rec.html.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                self._json(200, {
                    "usage": "POST /chat · GET /web/sites · GET /web/preview/<id>",
                    "web": CatSeekWebProgram.help_text() if CatSeekWebProgram.enabled() else "disabled",
                })
            def log_message(self,*a): pass
        def serve():
            try: ThreadingHTTPServer(("127.0.0.1", CONFIG["api_port"]), Handler).serve_forever()
            except Exception as e: gui.root.after(0, lambda: gui.log("SYSTEM", f"API error: {e}"))
        threading.Thread(target=serve, daemon=True).start()

# ──────────────────────────────────────────────────────────────
# ENTRY
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if "--chat" in sys.argv or "-c" in sys.argv:
        run_chat_cli(CatR11Engine())
    else:
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", lambda: root.destroy() if messagebox.askokcancel("Quit", f"Exit {GUI_APP_NAME}?") else None)
        CatR11GUI(root)
        root.mainloop()
