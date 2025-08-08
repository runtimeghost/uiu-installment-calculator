var socketio;

function calculate(link) {
    document.getElementById("result").innerText = "Please wait";
    const scholarship = document.getElementById("scholarship").value;
    const totalCredits = document.getElementById("credit").value;
    const transport = document.getElementById("transport").checked;
    const oldBatch = document.getElementById("oldBatch").value;

    fetch(link, {
        "method": "post",
        "body": JSON.stringify(
            {
                "socket_id": socketio.id,
                "oldBatch": oldBatch == "yes",
                "scholarship": scholarship,
                "credit": totalCredits,
                "transport": transport
            }
        ),
        "headers": {
            "content-type": "application/json; charset=UTF-8}"
        }
    });
}

window.onload = function () {
    socketio = io();
    // socketio.connect("http://127.0.0.1:8080");

    // socketio.on("connect", function () {
    //     console.log("Connected");
    // });

    socketio.on("result", function (data) {
        const result = document.getElementById("result");
        result.innerText = `Total trimester Fee: ${data["total"]} Tk
            1st installment: ${data["first"]} Tk
            2nd installment: ${data["second"]} Tk
            3rd installment: ${data["third"]} Tk`;
    });

    socketio.on("error", function (data) {
        document.getElementById("result").innerText = data["msg"];
    });

};