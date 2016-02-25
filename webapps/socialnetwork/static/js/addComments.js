var req;
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addComment(th){
	if(window.XMLHttpRequest){
		req = new XMLHttpRequest();
	} else {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	var idString = th.id;
	var index = idString.indexOf("docomment") + 9;
	var postID = parseInt(idString.substring(index));
	req.onreadystatechange = function(){
		if(req.readyState != 4 || req.status != 200){
			return;
		}
		else
			sendCommentRequest(th);
	};
	var commentText = document.getElementById("commenttext" + postID);
	req.open("POST", "/socialnetwork/do_comment", true);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	req.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
	var sendInfo = "post=" + postID + "&" + "comment=" + commentText.value;
	req.send(sendInfo);
	commentText.value = "";
	
}