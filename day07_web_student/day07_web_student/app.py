import pandas as pd
from functools import wraps
from pathlib import Path
from urllib.parse import quote 

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from services.data_service import load_dashboard_data
from services.qa_service import answer_question


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["SECRET_KEY"] = "day07-classroom-demo-key"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("请先登录后再访问数据看板。", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    return redirect(url_for("dashboard") if "username" in session else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == "student" and password == "day07":
            session["username"] = username
            flash("登录成功，欢迎进入电商用户分析系统。", "success")
            return redirect(url_for("dashboard"))
        flash("账号或密码错误。演示账号：student / day07", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("你已安全退出。", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    category = request.args.get("category", "全部")
    dashboard_data = load_dashboard_data(BASE_DIR, category)
    return render_template(
        "dashboard.html",
        username=session["username"],
        selected_category=category,
        **dashboard_data,
    )


@app.route("/assistant")
@login_required
def assistant():
    return render_template("assistant.html", username=session["username"])


@app.route("/api/ask", methods=["POST"])
@login_required
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"ok": False, "answer": "请输入一个与项目数据有关的问题。"}), 400
    return jsonify({"ok": True, "answer": answer_question(BASE_DIR, question)})


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404

@app.route("/download")
@login_required
def download_csv():
    import pandas as pd
    category = request.args.get("category", "全部")
    
    data_dir = BASE_DIR / "data"
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    
    if category != "全部":
        category_df = category_df[category_df["PreferedOrderCat"] == category]
    
    export_df = category_df.rename(columns={
        "PreferedOrderCat": "偏好品类",
        "用户数": "用户数",
        "流失率": "流失率",
        "平均订单数": "平均订单数"
    })[["偏好品类", "用户数", "流失率", "平均订单数"]]
    
    # 生成文件名（英文，避免中文编码问题）
    if category == "全部":
        filename = "all_categories.csv"
    else:
        # 移除特殊字符，保证文件名安全
        safe_category = category.replace(" & ", "_").replace(" ", "_")
        filename = f"{safe_category}_category.csv"
    
    # 对文件名进行 URL 编码
    encoded_filename = quote(filename)
    
    return export_df.to_csv(index=False, encoding="utf-8-sig"), 200, {
        "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
        "Content-Type": "text/csv; charset=utf-8-sig"
    }
if __name__ == "__main__":
    app.run(debug=False, port=5000)

