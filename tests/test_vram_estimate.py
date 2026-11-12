import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import vram_estimate as V  # noqa: E402


def test_kv_cache_matches_model_shape():
    # 2 (K, V) x 36 layers x 8 heads x 128 dims x 2 bytes = 144 KiB per token at f16
    assert V.kv_cache_bytes(1) == 147_456
    assert abs(V.kv_cache_bytes(8192) / V.GIB - 1.125) < 1e-9


def test_q8_cache_is_about_half():
    assert 0.5 < V.kv_cache_bytes(8192, "q8_0") / V.kv_cache_bytes(8192) < 0.55


def test_more_context_and_bigger_quant_need_more():
    assert V.estimate("Q4_K_M", 4096) < V.estimate("Q4_K_M", 8192) < V.estimate("Q6_K", 8192) < V.estimate("Q8_0", 8192)


def test_partial_offload_scales_down():
    assert V.estimate("Q4_K_M", 4096, "q8_0", 18) < V.estimate("Q4_K_M", 4096, "q8_0", 36)


def test_best_fit_picks_quality_when_room():
    assert V.best_fit(24)["quant"] == "Q8_0"
    small = V.best_fit(6)
    assert small["quant"] == "Q4_K_M" and small["gpu_layers"] == V.LAYERS
    tiny = V.best_fit(4)
    assert tiny is not None and tiny["gpu_layers"] < V.LAYERS
