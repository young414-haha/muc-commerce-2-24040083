from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    # TODO 4-1：补充“流失率”“偏好品类”“生命周期风险”和“订单”四类问答。
    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
    # 1. 流失情况
    if any(word in normalized for word in ["流失率", "流失人数", "流失情况"]):
        churn_rate = metrics['流失率']
        churn_count = int(metrics['流失人数'])
        total_users = int(metrics['用户数'])
        return (
            f"总体流失率为{churn_rate:.1%}，"
            f"流失人数为{churn_count:,}人，"
            f"总用户数为{total_users:,}人。"
        )
    # 2. 偏好品类（用户最多的品类）
    if any(word in normalized for word in ["哪个品类", "最多用户", "偏好品类", "最受欢迎"]):
        # 找到用户数最多的品类
        max_row = category_df.loc[category_df["用户数"].idxmax()]
        category = max_row["PreferedOrderCat"]
        user_count = int(max_row["用户数"])
        return f"用户最多的品类是「{category}」，共有{user_count:,}名用户。"
    # 3. 生命周期风险
    if any(word in normalized for word in ["哪个阶段", "风险最高", "生命周期", "流失最高"]):
        # 找到流失率最高的阶段
        max_row = segment_df.loc[segment_df["流失率"].idxmax()]
        segment = max_row["TenureGroup"]
        churn_rate = max_row["流失率"]
        user_count = int(max_row["用户数"])
        return (
            f"流失风险最高的生命周期阶段是「{segment}」，"
            f"流失率为{churn_rate:.1%}，该阶段共有{user_count:,}名用户。"
        )
    # 4. 订单情况
    if any(word in normalized for word in ["平均订单", "订单数", "人均订单"]):
        avg_orders = metrics['平均订单数']
        median_orders = metrics['订单数中位数']
        return f"平均订单数为{avg_orders:.2f}单，订单数中位数为{median_orders:.1f}单。"
    # 不支持的问题
    return (
        "抱歉，我目前只能回答以下几类问题：\n"
        "1. 总用户数（如：系统中有多少用户？）\n"
        "2. 流失情况（如：总体流失率是多少？）\n"
        "3. 偏好品类（如：哪个品类用户最多？）\n"
        "4. 生命周期风险（如：哪个阶段风险最高？）\n"
        "5. 订单情况（如：平均订单数是多少？）\n"
        "请换个问法再试一次。"
    )
    return (
        "基础问答尚未完成。目前只能回答总用户数；请继续完成TODO 4-1。"
        "请换一种更具体的问法。"
    )
