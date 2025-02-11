document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("configForm");

  function serializeForm(form) {
    const formData = {};
    Array.from(form.elements).forEach(el => {
      if (!el.name) return;
      if (el.type === "checkbox") {
        formData[el.name] = el.checked;
      } else if (el.type === "radio") {
        if (el.checked) formData[el.name] = el.value;
      } else {
        formData[el.name] = el.value;
      }
    });
    return formData;
  }

  function push() {
    let rawData = serializeForm(form);

    // Convert radio values for booleans
    if ("replay" in rawData) rawData.replay = rawData.replay === "true";
    if ("autotime" in rawData) rawData.autotime = rawData.autotime === "true";

    if (rawData.additional_menu_state === "") {
      delete rawData.additional_menu_state;
    }

    // Build players array (players 1 to 8)
    rawData.players = [];
    for (let i = 1; i <= 8; i++) {
      if (rawData["name" + i] !== undefined && rawData["enabled" + i] === true) {
        rawData.players.push({
          id: i,
          name: rawData["name" + i],
          race: rawData["race" + i],
          result: rawData["result" + i]
        });
      }
    }

    // Remove individual player fields
    for (let i = 1; i <= 8; i++) {
      ["name", "race", "result", "enabled"].forEach(key => delete rawData[key + i]);
    }

    // Post the payload
    fetch("/set", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(rawData)
    })
      .then(response => response.json())
      .then(data => {
        console.log("Data saved:", data);
        // Update responses after successful POST
        updateResponse("ui-response", "/ui");
        updateResponse("game-response", "/game");
      })
      .catch(error => console.error("Error:", error));
  }

  function updateResponse(elementId, url) {
    fetch(url)
      .then(response => response.json())
      .then(data => {
        const el = document.getElementById(elementId);
        if (el) {
          el.textContent = JSON.stringify(data);
        }
      })
      .catch(error => console.error("Fetch error:", error));
  }

  form.addEventListener("change", () => {
    push();
  });

  // Trigger an initial change event
  form.dispatchEvent(new Event("change"));
});
