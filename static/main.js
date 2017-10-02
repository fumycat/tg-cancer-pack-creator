function base64ToBlob(base64, mime) 
{
    mime = mime || '';
    var sliceSize = 1024;
    var byteChars = window.atob(base64);
    var byteArrays = [];

    for (var offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
        var slice = byteChars.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, {type: mime});
}

$(function() {
  $('.image-editor').cropit({
    exportZoom: 1.25,
    imageBackground: true,
    imageBackgroundBorderWidth: 20,
  });
  $('.export').click(function() {
    $(this).prop("disabled", true);
    var imageData = $('.image-editor').cropit('export');
    var base64ImageContent = imageData.replace(/^data:image\/(png|jpg);base64,/, "");
    var blob = base64ToBlob(base64ImageContent, 'image/png');                
    var formData = new FormData();
    formData.append('picture', blob);

    $.ajax({
      type: "POST",
      url: "/upload",
      cache: false,
      contentType: false,
      processData: false,
      data: formData,
      success: function(responce){
        window.location.href = '/j/' + responce + '/0';
      }
    });
  });
});
