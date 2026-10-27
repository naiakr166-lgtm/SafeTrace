
from flask import Flask, render_template, request, redirect, url_for, flash
import blockchain_core as bc

app = Flask(__name__)
app.secret_key = "safetrace-local-demo"

@app.route("/")
def home():
    return render_template("index.html", devices=bc.devices)

@app.route("/register", methods=["POST"])
def register():
    device_id = request.form.get("device_id", "").strip()
    device_type = request.form.get("device_type", "").strip()

    if not bc.verify_blockchain():
        flash("تحذير: سجل البلوك تشين غير سليم.")
    elif not device_id or not device_type:
        flash("يرجى تعبئة جميع الحقول.")
    elif device_id in bc.devices:
        flash("هذا الجهاز مسجل مسبقًا.")
    else:
        bc.register_device(device_id, device_type)
        flash("تم تسجيل الجهاز بنجاح!")

    return redirect(url_for("home"))

@app.route("/damage", methods=["POST"])
def damage():
    device_id = request.form.get("device_id", "").strip()
    issue = request.form.get("issue", "").strip()

    if not bc.verify_blockchain():
        flash("تحذير: سجل البلوك تشين غير سليم.")
    elif not device_id or not issue:
        flash("يرجى تعبئة جميع الحقول.")
    elif device_id not in bc.devices:
        flash("الجهاز غير موجود.")
    elif bc.devices[device_id]["status"] == "Unsafe":
        flash("الجهاز مصنف بالفعل بأنه غير آمن.")
    else:
        bc.report_damage(device_id, issue)
        flash("تم تسجيل العطل وتصنيف الجهاز بأنه غير آمن!")

    return redirect(url_for("home"))

@app.route("/lend", methods=["POST"])
def lend():
    device_id = request.form.get("device_id", "").strip()
    center = request.form.get("center", "").strip()

    if not bc.verify_blockchain():
        flash("تحذير: سجل البلوك تشين غير سليم.")
    elif not device_id or not center:
        flash("يرجى تعبئة جميع الحقول.")
    elif device_id not in bc.devices:
        flash("الجهاز غير موجود.")
    elif bc.devices[device_id]["status"] == "Unsafe":
        flash("تم رفض الإعارة! الجهاز غير آمن ويحتاج إلى صيانة.")
    else:
        bc.lend_device(device_id, center)
        flash("تمت إعارة الجهاز بنجاح!")

    return redirect(url_for("home"))

@app.route("/repair", methods=["POST"])
def repair():
    device_id = request.form.get("device_id", "").strip()
    technician_id = request.form.get("technician_id", "").strip()

    if not bc.verify_blockchain():
        flash("تحذير: سجل البلوك تشين غير سليم.")
    elif not device_id or not technician_id:
        flash("يرجى تعبئة جميع الحقول.")
    elif device_id not in bc.devices:
        flash("الجهاز غير موجود.")
    elif technician_id not in bc.authorized_technicians:
        flash("تم رفض الإصلاح! الفني غير مصرح له.")
    elif bc.devices[device_id]["status"] != "Unsafe":
        flash("الجهاز غير مصنف بأنه يحتاج إلى إصلاح.")
    else:
        bc.repair_device(device_id, technician_id)
        flash("تم اعتماد الإصلاح من فني مصرح له!")

    return redirect(url_for("home"))

@app.route("/history", methods=["POST"])
def history():
    device_id = request.form.get("device_id", "").strip()

    if not bc.verify_blockchain():
        flash("تحذير: سجل البلوك تشين غير سليم.")
        return redirect(url_for("home"))

    if device_id not in bc.devices:
        flash("الجهاز غير موجود.")
        return redirect(url_for("home"))

    device_history = bc.get_device_history(device_id)

    return render_template(
        "index.html",
        devices=bc.devices,
        selected_device=device_id,
        device_history=device_history
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)