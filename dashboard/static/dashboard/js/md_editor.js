(function(window, document, undefined) {

    window.onload = init;
  
    function init(){
        let mdTextarea = document.getElementsByClassName("md-editor__textarea")[0];

        document.getElementById("bold-button").addEventListener("click", function() {
            styleText(mdTextarea, "*", "*")
        })

        document.getElementById("italic-button").addEventListener("click", function() {
            styleText(mdTextarea, "_", "_")
        })

        document.getElementById("underline-button").addEventListener("click", function() {
            styleText(mdTextarea, "__", "__")
        })

        document.getElementById("spoiler-button").addEventListener("click", function() {
            styleText(mdTextarea, "~", "~")
        })

        document.getElementById("link-button").addEventListener("click", function() {
            styleText(mdTextarea, "[](", ")")
        })

        document.getElementById("code-button").addEventListener("click", function() {
            styleText(mdTextarea, "```", "```")
        })
    }

  })(window, document, undefined);


function styleText(textatrea, commandStart, commandEnd) {
    if (textatrea.selectionStart == textatrea.selectionEnd) {
        textatrea.setRangeText(`${commandStart}${commandEnd}`, textatrea.selectionStart, textatrea.selectionEnd, "end");
        textatrea.focus();
        return;
    }
    
    let selected = textatrea.value.slice(textatrea.selectionStart, textatrea.selectionEnd);
    textatrea.setRangeText(`${commandStart}${selected}${commandEnd}`);
}