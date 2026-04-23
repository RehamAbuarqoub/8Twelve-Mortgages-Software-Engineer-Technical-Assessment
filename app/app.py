from flask import Flask, jsonify, render_template_string
from app.routes.leads import leads_bp

app = Flask(__name__)
app.register_blueprint(leads_bp)


@app.route("/", methods=["GET"])
def home():
    # Very simple test page so you can enter the lead data and get the response
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lead Assessment</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                line-height: 1.6;
                background: #f8f9fa;
            }

            h1 {
                color: #222;
            }

            .card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 20px;
            }

            label {
                display: block;
                margin-top: 12px;
                font-weight: bold;
            }

            input, select {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 6px;
                box-sizing: border-box;
            }

            button {
                margin-top: 18px;
                padding: 10px 16px;
                border: none;
                border-radius: 6px;
                background: #007bff;
                color: white;
                cursor: pointer;
                font-size: 15px;
            }

            button:hover {
                background: #0056b3;
            }

            pre {
                background: #f4f4f4;
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
            }

            .note {
                color: #555;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <h1>Lead Assessment</h1>
        <p class="note">
           I'vwe created this page to let you test the REST API and see the AI summary on the screen.
        </p>

        <div class="card">
            <h2>Enter Lead Data</h2>

            <label for="name">Name</label>
            <input id="name" type="text" placeholder="Shrey Raval">

            <label for="email">Email</label>
            <input id="email" type="email" placeholder="shrey@email.com">

            <label for="phone">Phone</label>
            <input id="phone" type="text" placeholder="1234567890">

            <label for="source">Source</label>
            <input id="source" type="text" placeholder="website">

        <label for="status">Status</label>
<select id="status">
    <option value="new">New</option>
    <option value="in_progress">In Progress</option>
    <option value="ready">Ready</option>
</select>

            <button onclick="submitLead()">Submit Lead</button>
        </div>

        <div class="card">
            <h2>Response</h2>
            <pre id="result">No result yet.</pre>
        </div>

        <script>
            async function submitLead() {
                const payload = {
                    name: document.getElementById("name").value,
                    email: document.getElementById("email").value || null,
                    phone: document.getElementById("phone").value || null,
                    source: document.getElementById("source").value,
                    status: document.getElementById("status").value
                };

                const resultBox = document.getElementById("result");
                resultBox.textContent = "Loading...";

                try {
                    const response = await fetch("/leads", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(payload)
                    });

                    const data = await response.json();

                    resultBox.textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    resultBox.textContent = "Error: " + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)