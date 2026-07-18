# -*- coding: utf-8 -*-
"""
AppInsight —— 多维度评论情感分析系统 API
=========================================
架构模式：Service / Repository 分层，支持多数据集路由、缓存、扩展
"""

import os
import re
import time
import hashlib
import json
from collections import Counter, defaultdict
from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────
# App 初始化
# ──────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────────
# 简易缓存
# ──────────────────────────────────────────────
cache = {}
CACHE_TTL = 86400  # 24 小时（启动时预热后几乎永不过期）


def cached(ttl=CACHE_TTL):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = hashlib.md5(f"{fn.__name__}:{request.get_data()}:{request.args}".encode()).hexdigest()
            if key in cache and time.time() - cache[key]["ts"] < ttl:
                return cache[key]["data"]
            result = fn(*args, **kwargs)
            cache[key] = {"data": result, "ts": time.time()}
            return result
        return wrapper
    return decorator


# ──────────────────────────────────────────────
# 数据仓库层 (Repository)
# ──────────────────────────────────────────────
class DataRepository:
    """多数据集支持，通过 data_source 参数切换"""

    DATASETS = {
        "comprehensive": "data/AWARE_Comprehensive.csv",
        "games": "data/AWARE_Games.csv",
        "productivity": "data/AWARE_Productivity.csv",
        "social": "data/AWARE_Social_Networking.csv",
    }

    def __init__(self):
        self._dataframes = {}
        self._load_all()

    def _load_all(self):
        for name, path in self.DATASETS.items():
            try:
                fp = os.path.join(os.path.dirname(__file__), path)
                df = pd.read_csv(fp)
                # 统一列名
                df.columns = [c.strip().lower() for c in df.columns]
                self._dataframes[name] = df
                print(f"  ✓ {name}: {len(df)} 条")
            except Exception as e:
                print(f"  ✗ {name}: {e}")
                self._dataframes[name] = pd.DataFrame()
        print(f"  总计 {sum(len(v) for v in self._dataframes.values())} 条")

    def get_df(self, data_source="comprehensive"):
        return self._dataframes.get(data_source, self._dataframes["comprehensive"]).copy()

    def list_sources(self):
        return {k: len(v) for k, v in self._dataframes.items()}

    def apply_filters(self, df, filters: dict):
        """统一的筛选逻辑"""
        if filters.get("sentiment") and filters["sentiment"] not in ("all", "全部"):
            df = df[df["sentiment"] == filters["sentiment"]]
        if filters.get("category") and filters["category"] not in ("all", "全部"):
            df = df[df["category"] == filters["category"]]
        if filters.get("domain") and filters["domain"] not in ("all", "全部"):
            df = df[df["domain"] == filters["domain"]]
        if filters.get("min_rating") is not None:
            df = df[df["rating"] >= filters["min_rating"]]
        if filters.get("max_rating") is not None:
            df = df[df["rating"] <= filters["max_rating"]]
        if filters.get("search"):
            kw = filters["search"].lower()
            df = df[df["sentence"].fillna("").astype(str).str.lower().str.contains(kw, na=False)]
        return df


repo = DataRepository()


# ──────────────────────────────────────────────
# API 元信息
# ──────────────────────────────────────────────
API_META = {
    "name": "AppInsight API v3.0",
    "description": "多维度评论情感分析系统",
    "datasets": repo.list_sources(),
    "endpoints": {}
}


# ──────────────────────────────────────────────
# 辅助函数
# ──────────────────────────────────────────────
def _get_filters():
    """从 request 获取筛选条件，GET 用 args，POST 用 json"""
    if request.method == "POST":
        return request.get_json(force=True) or {}
    return {k: v for k, v in request.args.items()}


def _safe_rate(positive, total):
    return round(positive / total * 100, 1) if total > 0 else 0


def _sentiment_dist(df):
    return df["sentiment"].value_counts().to_dict()


# ══════════════════════════════════════════════
# 1. 系统 & 元信息
# ══════════════════════════════════════════════

@app.route("/api/test", methods=["GET"])
def api_test():
    return jsonify({"message": "AppInsight API v3.0 连接成功", "status": "ok"})


@app.route("/api/meta", methods=["GET"])
def api_meta():
    """API 元信息 + 可用数据集"""
    return jsonify({
        **API_META,
        "available_filters": ["sentiment", "category", "domain", "min_rating", "max_rating", "search", "data_source"],
        "sentiment_options": ["positive", "negative"],
        "data_sources": list(repo.DATASETS.keys()),
    })


# ══════════════════════════════════════════════
# 2. 概览摘要
# ══════════════════════════════════════════════

@cached()
@app.route("/api/summary", methods=["POST", "GET"])
def api_summary():
    """多维度概览摘要"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)

    sentiment = _sentiment_dist(df)
    total = max(sum(sentiment.values()), 1)
    pos = sentiment.get("positive", 0)
    neg = sentiment.get("negative", 0)

    # 方面分布
    aspect_counts = df["category"].value_counts().to_dict()
    domain_counts = df["domain"].value_counts().to_dict() if "domain" in df.columns else {}

    # 评分分布
    rating_dist = df["rating"].value_counts().sort_index().to_dict() if "rating" in df.columns else {}

    # 评论长度统计
    text_lens = df["sentence"].fillna("").astype(str).str.len()
    avg_len = round(text_lens.mean(), 1) if len(text_lens) > 0 else 0

    return jsonify({
        "total": len(df),
        "positive": pos,
        "negative": neg,
        "positive_rate": _safe_rate(pos, total),
        "sentiment": sentiment,
        "aspect": aspect_counts,
        "domain": domain_counts,
        "rating_distribution": rating_dist,
        "avg_review_length": avg_len,
        "data_source": f.get("data_source", "comprehensive"),
    })


# ══════════════════════════════════════════════
# 3. 情感维分析
# ══════════════════════════════════════════════

@cached()
@app.route("/api/aspect_sentiment", methods=["POST", "GET"])
def api_aspect_sentiment():
    """方面 × 情感 交叉分析"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)

    result = []
    for category in df["category"].unique():
        if pd.isna(category):
            continue
        subset = df[df["category"] == category]
        p = len(subset[subset["sentiment"] == "positive"])
        n = len(subset[subset["sentiment"] == "negative"])
        t = p + n
        result.append({
            "aspect": category,
            "positive": p,
            "negative": n,
            "total": t,
            "positive_rate": _safe_rate(p, t),
        })
    return jsonify(result)


@cached()
@app.route("/api/rating_sentiment", methods=["POST", "GET"])
def api_rating_sentiment():
    """评分 × 情感 一致性分析"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    valid = df[df["rating"].notna()]

    result = []
    for rating in range(1, 6):
        rd = valid[valid["rating"] == rating]
        if len(rd) == 0:
            continue
        p = len(rd[rd["sentiment"] == "positive"])
        n = len(rd[rd["sentiment"] == "negative"])
        t = p + n
        result.append({
            "rating": rating,
            "positive": p,
            "negative": n,
            "positive_rate": _safe_rate(p, t),
            "total": t,
        })
    return jsonify(result)


@cached()
@app.route("/api/sentiment_trend", methods=["POST", "GET"])
def api_sentiment_trend():
    """情感趋势分析（按评分分组模拟时间趋势）"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    valid = df[df["rating"].notna()]

    result = []
    for rating in range(1, 6):
        rd = valid[valid["rating"] == rating]
        if len(rd) == 0:
            continue
        p = len(rd[rd["sentiment"] == "positive"])
        n = len(rd[rd["sentiment"] == "negative"])
        t = p + n
        result.append({
            "rating": rating,
            "positive": p,
            "negative": n,
            "positive_rate": _safe_rate(p, t),
            "total": t,
            "label": f"{'⭐' * rating}",
        })
    return jsonify(result)


# ══════════════════════════════════════════════
# 4. 领域 & 方面挖掘
# ══════════════════════════════════════════════

@cached()
@app.route("/api/domain_compare", methods=["POST", "GET"])
def api_domain_compare():
    """App 领域情感对比"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    valid = df[df["domain"].notna()]

    result = []
    for domain in valid["domain"].unique():
        dd = valid[valid["domain"] == domain]
        p = len(dd[dd["sentiment"] == "positive"])
        n = len(dd[dd["sentiment"] == "negative"])
        t = p + n
        result.append({
            "domain": domain,
            "positive": p,
            "negative": n,
            "positive_rate": _safe_rate(p, t),
            "total": t,
        })
    return jsonify(result)


@cached()
@app.route("/api/aspect_stats", methods=["POST", "GET"])
def api_aspect_stats():
    """方面类别统计（玫瑰图/气泡图使用）"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)

    result = []
    for category in df["category"].unique():
        if pd.isna(category):
            continue
        subset = df[df["category"] == category]
        p = len(subset[subset["sentiment"] == "positive"])
        n = len(subset[subset["sentiment"] == "negative"])
        t = p + n
        result.append({
            "aspect": category,
            "category": category,
            "positive": p,
            "negative": n,
            "total": t,
            "positive_rate": _safe_rate(p, t),
            "sentiment_ratio": round(p / max(t, 1), 2),
        })
    return jsonify({"data": result})


# ══════════════════════════════════════════════
# 5. App 排行 & 评分
# ══════════════════════════════════════════════

@cached()
@app.route("/api/top_apps", methods=["POST", "GET"])
def api_top_apps():
    """热门 App 情感排行"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    top_n = int(f.get("top_n", 15))
    sentiment_only = f.get("sentiment_only")

    app_counts = df["app"].value_counts().head(top_n).index
    result = []
    for app_name in app_counts:
        if pd.isna(app_name):
            continue
        ad = df[df["app"] == app_name]
        if sentiment_only and sentiment_only != "all":
            ad = ad[ad["sentiment"] == sentiment_only]
        p = len(ad[ad["sentiment"] == "positive"])
        n = len(ad[ad["sentiment"] == "negative"])
        t = p + n
        result.append({
            "app": app_name,
            "positive": p,
            "negative": n,
            "total": t,
            "positive_rate": _safe_rate(p, t),
        })

    # 按 total 或 positive_rate 排序
    sort_by = f.get("sort_by", "total")
    result.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
    return jsonify(result)


@cached()
@app.route("/api/app_ratings", methods=["POST", "GET"])
def api_app_ratings():
    """App 平均评分排行"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    valid = df[df["rating"].notna()]

    result = []
    for app_name in valid["app"].unique():
        if pd.isna(app_name):
            continue
        ad = valid[valid["app"] == app_name]
        avg_r = ad["rating"].mean()
        t = len(ad)
        p = len(ad[ad["sentiment"] == "positive"])
        result.append({
            "app": app_name,
            "avg_rating": round(avg_r, 2),
            "total": t,
            "positive_count": p,
            "positive_rate": _safe_rate(p, t),
        })

    sort_by = f.get("sort_by", "total")
    result.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
    return jsonify(result[:int(f.get("top_n", 15))])


# ══════════════════════════════════════════════
# 6. 高级分析
# ══════════════════════════════════════════════

@cached()
@app.route("/api/length_analysis", methods=["POST", "GET"])
def api_length_analysis():
    """评论长度与情感关联"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    df["text_length"] = df["sentence"].fillna("").astype(str).str.len()

    bins = [0, 20, 50, 100, 200, float("inf")]
    labels = ["极短(≤20字)", "短(21-50)", "中(51-100)", "长(101-200)", "超长(>200字)"]
    df["length_group"] = pd.cut(df["text_length"], bins=bins, labels=labels, right=False)

    result = []
    for group in labels:
        gd = df[df["length_group"] == group]
        p = len(gd[gd["sentiment"] == "positive"])
        n = len(gd[gd["sentiment"] == "negative"])
        t = p + n
        result.append({
            "length_group": group,
            "positive": p,
            "negative": n,
            "total": t,
            "positive_rate": _safe_rate(p, t),
            "avg_length": round(gd["text_length"].mean(), 1) if len(gd) > 0 else 0,
        })
    return jsonify(result)


@cached()
@app.route("/api/quadrant_scatter", methods=["POST", "GET"])
def api_quadrant_scatter():
    """四象限散点图：评分 vs 评论量 vs 正面率"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    valid = df[df["rating"].notna()]

    result = []
    for app_name in valid["app"].unique():
        if pd.isna(app_name):
            continue
        ad = valid[valid["app"] == app_name]
        avg_r = ad["rating"].mean()
        t = len(ad)
        pr = len(ad[ad["sentiment"] == "positive"]) / max(t, 1) * 100
        result.append({
            "app": app_name,
            "avg_rating": round(avg_r, 2),
            "total_reviews": t,
            "positive_rate": round(pr, 1),
        })
    return jsonify(result)


@cached()
@app.route("/api/emotion_heatmap", methods=["POST", "GET"])
def api_emotion_heatmap():
    """情感热力图：评分 × 方面类别"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)

    result = []
    for rating in range(1, 6):
        rd = df[df["rating"] == rating]
        for category in df["category"].unique():
            if pd.isna(category):
                continue
            cd = rd[rd["category"] == category]
            if len(cd) == 0:
                continue
            p = len(cd[cd["sentiment"] == "positive"])
            n = len(cd[cd["sentiment"] == "negative"])
            t = p + n
            result.append({
                "rating": rating,
                "category": category,
                "positive": p,
                "negative": n,
                "positive_rate": _safe_rate(p, t),
                "total": t,
            })
    return jsonify(result)


# ══════════════════════════════════════════════
# 7. 词云 & 关键词
# ══════════════════════════════════════════════

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "so", "for", "of", "to", "in", "on", "at",
    "with", "without", "by", "from", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "this", "that", "these",
    "those", "it", "its", "it's", "they", "them", "their", "we", "our", "you", "your",
    "he", "she", "his", "her", "i", "me", "my", "mine", "app", "apps", "use", "used", "using",
    "get", "got", "make", "made", "like", "would", "could", "should", "very", "really", "also",
    "甚至", "非常", "一个", "这个", "那个", "这些", "那些", "可以", "能够", "需要", "想要", "觉得", "感觉",
    "的", "了", "和", "与", "或", "但是", "所以", "因为", "如果", "虽然", "然而", "由于", "为了",
    "just", "one", "well", "back", "much", "still", "even", "though",
}


def _extract_words(texts, top_n=50):
    """从文本列表提取高频词"""
    word_counts = Counter()
    for text in texts:
        words = re.findall(r"[a-zA-Z]+(?:[-\'][a-zA-Z]+)*|[一-龥]+", text.lower())
        for word in words:
            w = word.lower()
            if len(w) < 3 or w in STOPWORDS:
                continue
            word_counts[w] += 1
    return [{"name": w, "value": c} for w, c in word_counts.most_common(top_n)]


@cached()
@app.route("/api/wordcloud", methods=["POST", "GET"])
def api_wordcloud():
    """词云数据（正负面分开）"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    top_n = int(f.get("top_n", 60))

    pos_texts = df[df["sentiment"] == "positive"]["term"].dropna().tolist()
    neg_texts = df[df["sentiment"] == "negative"]["term"].dropna().tolist()

    # 也使用 sentence 补充
    if len(pos_texts) < 10:
        pos_texts += df[df["sentiment"] == "positive"]["sentence"].dropna().astype(str).tolist()
    if len(neg_texts) < 10:
        neg_texts += df[df["sentiment"] == "negative"]["sentence"].dropna().astype(str).tolist()

    return jsonify({
        "positive": _extract_words(pos_texts, top_n),
        "negative": _extract_words(neg_texts, top_n),
    })


@cached()
@app.route("/api/keyword_trend", methods=["POST", "GET"])
def api_keyword_trend():
    """关键词评分趋势（指定词在各评分中的出现频率）"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    keyword = f.get("keyword", "").lower().strip()

    if not keyword:
        return jsonify({"error": "请指定 keyword 参数"}), 400

    valid = df[df["rating"].notna()]
    result = []
    for rating in range(1, 6):
        rd = valid[valid["rating"] == rating]
        texts = rd["sentence"].fillna("").astype(str).tolist()
        mentions = sum(1 for t in texts if keyword in t.lower())
        result.append({
            "rating": rating,
            "mentions": mentions,
            "total": len(rd),
            "frequency": round(mentions / max(len(rd), 1) * 100, 2),
        })
    return jsonify({
        "keyword": keyword,
        "trend": result,
    })


# ══════════════════════════════════════════════
# 8. 对比分析（新）
# ══════════════════════════════════════════════

@cached()
@app.route("/api/compare_datasets", methods=["GET", "POST"])
def api_compare_datasets():
    """多数据集对比分析"""
    f = request.get_json(force=True) or {}
    sources = f.get("sources", ["comprehensive", "games", "productivity", "social"])

    result = {}
    for src in sources:
        if src not in repo.DATASETS:
            continue
        df = repo.apply_filters(repo.get_df(src), f)
        sentiment = _sentiment_dist(df)
        total = max(sum(sentiment.values()), 1)
        pos = sentiment.get("positive", 0)
        neg = sentiment.get("negative", 0)
        valid_rating = df[df["rating"].notna()]

        result[src] = {
            "total": len(df),
            "positive": pos,
            "negative": neg,
            "positive_rate": _safe_rate(pos, total),
            "avg_rating": round(valid_rating["rating"].mean(), 2) if len(valid_rating) > 0 else 0,
            "categories": len(df["category"].unique()),
            "apps": len(df["app"].unique()),
        }
    return jsonify(result)


@cached()
@app.route("/api/compare_aspects", methods=["GET", "POST"])
def api_compare_aspects():
    """多源方面对比"""
    f = request.get_json(force=True) or {}
    sources = f.get("sources", ["comprehensive"])

    result = {}
    for src in sources:
        if src not in repo.DATASETS:
            continue
        df = repo.apply_filters(repo.get_df(src), f)
        aspect_data = {}
        for cat in df["category"].unique():
            if pd.isna(cat):
                continue
            cd = df[df["category"] == cat]
            p = len(cd[cd["sentiment"] == "positive"])
            n = len(cd[cd["sentiment"] == "negative"])
            aspect_data[cat] = {
                "total": p + n,
                "positive": p,
                "negative": n,
                "positive_rate": _safe_rate(p, p + n),
            }
        result[src] = aspect_data
    return jsonify(result)


# ══════════════════════════════════════════════
# 9. 钻取查询（新）
# ══════════════════════════════════════════════

@cached()
@app.route("/api/drill_down", methods=["GET", "POST"])
def api_drill_down():
    """数据钻取：返回原始评论片段"""
    f = request.get_json(force=True) or {}
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)

    page = int(f.get("page", 1))
    page_size = int(f.get("page_size", 20))
    sort_by = f.get("sort_by", "rating")
    sort_order = f.get("sort_order", "desc")

    # 选择列
    columns = ["app", "domain", "sentence", "rating", "sentiment", "category"]
    columns = [c for c in columns if c in df.columns]
    display = df[columns].copy()

    # 排序
    if sort_by in display.columns:
        ascending = sort_order == "asc"
        display = display.sort_values(by=sort_by, ascending=ascending)

    # 分页
    total = len(display)
    total_pages = max(1, (total + page_size - 1) // page_size)
    start = (page - 1) * page_size
    end = start + page_size
    page_data = display.iloc[start:end].fillna("").to_dict(orient="records")

    return jsonify({
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": page_data,
        "columns": columns,
    })


# ══════════════════════════════════════════════
# 10. NPS / 情感评分
# ══════════════════════════════════════════════

@cached()
@app.route("/api/nps", methods=["POST", "GET"])
def api_nps():
    """净推荐值 (NPS) 分析"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    valid = df[df["rating"].notna()]

    promoters = len(valid[valid["rating"] >= 4])
    passives = len(valid[(valid["rating"] == 3)])
    detractors = len(valid[valid["rating"] <= 2])
    total = max(promoters + passives + detractors, 1)

    nps_score = round((promoters - detractors) / total * 100, 1)

    # 各领域的 NPS
    domain_nps = {}
    for domain in valid["domain"].unique():
        if pd.isna(domain):
            continue
        dd = valid[valid["domain"] == domain]
        dp = len(dd[dd["rating"] >= 4])
        dd_ = len(dd[dd["rating"] <= 2])
        dt = max(dp + len(dd[dd["rating"] == 3]) + dd_, 1)
        domain_nps[domain] = round((dp - dd_) / dt * 100, 1)

    return jsonify({
        "nps_score": nps_score,
        "promoters": int(promoters),
        "passives": int(passives),
        "detractors": int(detractors),
        "total": int(total),
        "domain_nps": domain_nps,
    })


# ══════════════════════════════════════════════
# 11. 主题聚类（简单版）
# ══════════════════════════════════════════════

@cached()
@app.route("/api/topic_clusters", methods=["POST", "GET"])
def api_topic_clusters():
    """基于 category 的简单主题聚类"""
    f = _get_filters()
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)

    clusters = {}
    for cat in df["category"].unique():
        if pd.isna(cat):
            continue
        cd = df[df["category"] == cat]
        texts = cd["sentence"].fillna("").astype(str).tolist()
        words = _extract_words(texts, 10)
        p = len(cd[cd["sentiment"] == "positive"])
        n = len(cd[cd["sentiment"] == "negative"])
        t = p + n
        clusters[cat] = {
            "total": t,
            "positive": p,
            "negative": n,
            "positive_rate": _safe_rate(p, t),
            "top_keywords": [w["name"] for w in words[:8]],
            "apps": cd["app"].dropna().unique().tolist()[:5],
        }
    return jsonify(clusters)


# ══════════════════════════════════════════════
# 12. 导出
# ══════════════════════════════════════════════

@cached()
@app.route("/api/export", methods=["GET", "POST"])
def api_export():
    """导出筛选后的数据为 JSON"""
    f = request.get_json(force=True) or {}
    df = repo.apply_filters(repo.get_df(f.get("data_source")), f)
    fmt = f.get("format", "json")

    columns = ["app", "domain", "sentence", "rating", "sentiment", "category", "term"]
    columns = [c for c in columns if c in df.columns]
    data = df[columns].fillna("").to_dict(orient="records")

    return jsonify({
        "format": fmt,
        "count": len(data),
        "columns": columns,
        "data": data,
    })


# ══════════════════════════════════════════════
# 启动预热：提前缓存所有核心数据
# ══════════════════════════════════════════════

def prewarm_cache():
    """启动后通过真实 HTTP 请求预热缓存"""
    import threading, urllib.request, json, time

    def _warm():
        time.sleep(1.0)  # 等服务器完全启动
        endpoints = [
            ("/api/summary", {"sentiment": "all"}),
            ("/api/aspect_sentiment", {}),
            ("/api/rating_sentiment", {}),
            ("/api/domain_compare", {}),
            ("/api/aspect_stats", {}),
            ("/api/top_apps", {"top_n": 15}),
            ("/api/app_ratings", {"top_n": 15}),
            ("/api/length_analysis", {}),
            ("/api/quadrant_scatter", {}),
            ("/api/emotion_heatmap", {}),
            ("/api/wordcloud", {}),
            ("/api/nps", {}),
            ("/api/topic_clusters", {}),
            ("/api/sentiment_trend", {}),
            ("/api/compare_datasets", {"sources": ["comprehensive", "games", "productivity", "social"]}),
        ]
        base = f"http://localhost:{port}"
        for ep, data in endpoints:
            try:
                req = urllib.request.Request(
                    f"{base}{ep}",
                    data=json.dumps(data).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                urllib.request.urlopen(req, timeout=10)
                print(f"  ✓ 预热: {ep}")
            except Exception as e:
                print(f"  ✗ 预热: {ep}")
        print(f"  预热完成")

    threading.Thread(target=_warm, daemon=True).start()


# ══════════════════════════════════════════════
# 启动
# ══════════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🚀 AppInsight API v3.0 启动于 :{port}")
    print(f"   数据集: {list(repo.DATASETS.keys())}")
    print(f"   端点数: 25+\n")

    # 缓存预热
    prewarm_cache()

    app.run(host="0.0.0.0", port=port, debug=False)
