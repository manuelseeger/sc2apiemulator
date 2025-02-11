$.fn.serializeObject = function () {
  var o = {};
  var a = this.serializeArray();
  $.each(a, function () {
    o[this.name] = this.value;
  });
  return o;
};

function push() {
  var rawData = $('#configForm').serializeObject();

  // Convert radio values for booleans
  if ("replay" in rawData) {
    rawData.replay = rawData.replay === "true";
  }
  if ("autotime" in rawData) {
    rawData.autotime = rawData.autotime === "true";
  }
  // Convert checkboxes properly
  $('input[type="checkbox"]').each(function () {
    rawData[$(this).attr("name")] = $(this).prop("checked");
  });

  // Build players array (assuming players 1 to 8)
  var players = [];
  for (var i = 1; i <= 8; i++) {
    // Only add a player if the name field is present
    if (rawData["name" + i] !== undefined) {
      players.push({
        id: i,
        name: rawData["name" + i],
        race: rawData["race" + i],
        result: rawData["result" + i],
        enabled: rawData["enabled" + i] === true
      });
      // Remove individual fields from rawData
      delete rawData["name" + i];
      delete rawData["race" + i];
      delete rawData["result" + i];
      delete rawData["enabled" + i];
    }
  }
  rawData.players = players;

  // Post the payload
  $.post({
    url: "/set",
    data: JSON.stringify(rawData),
    contentType: "application/json",
    processData: false,
    success: function (response) {
      console.log("Data saved:", response);
    }
  });
}

$(function () {
  $('#configForm').change(function () {
    push();
    $.get("/ui", function (response) {
      $("#ui-response").text(JSON.stringify(response));
    });
    $.get("/game", function (response) {
      $("#game-response").text(JSON.stringify(response));
    });
  });
  $('#configForm').trigger("change");
});
