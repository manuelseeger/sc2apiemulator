$.fn.serializeObject = function () {
  return this.serializeArray().reduce((obj, item) => {
    obj[item.name] = item.value;
    return obj;
  }, {});
};

function push() {
  let rawData = $('#configForm').serializeObject();

  // Convert radio values for booleans
  if ("replay" in rawData) rawData.replay = rawData.replay === "true";
  if ("autotime" in rawData) rawData.autotime = rawData.autotime === "true";

  // Convert checkboxes properly
  $('input[type="checkbox"]').each(function () {
    rawData[$(this).attr("name")] = $(this).prop("checked");
  });

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
      // Remove individual player fields
      ["name", "race", "result", "enabled"].forEach(key => delete rawData[key + i]);
    }
  }

  // Post the payload
  $.post({
    url: "/set",
    data: JSON.stringify(rawData),
    contentType: "application/json",
    processData: false,
    success: response => console.log("Data saved:", response)
  });
}

$(function () {
  $('#configForm').change(() => {
    push();
    $.get("/ui", response => $("#ui-response").text(JSON.stringify(response)));
    $.get("/game", response => $("#game-response").text(JSON.stringify(response)));
  }).trigger("change");
});
