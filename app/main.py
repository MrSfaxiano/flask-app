from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Write Jenkinsfile", "done": True},
]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@app.route("/tasks/done", methods=["GET"])
def get_done_tasks():
    done = [t for t in tasks if t["done"]]
    return jsonify(done), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
