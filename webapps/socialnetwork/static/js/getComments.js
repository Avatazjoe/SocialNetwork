var state = 0;
var req;
var postID;
function sendCommentRequest(th){
	if(window.XMLHttpRequest){
		req = new XMLHttpRequest();
	} else {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	var idString = th.id;
	var index = idString.indexOf("getcomment") + 10;
	postID = parseInt(idString.substring(index));
	req.onreadystatechange = handleCommentResponse;
	req.open("GET", "/socialnetwork/comment_list/" + postID, true);
	req.send();
}

function handleCommentResponse(){
	if(req.readyState != 4 || req.status != 200){
		return;
	}
	var list = document.getElementById("commentgroup" + postID);
	var nodes = list.childNodes;
	var nodesNumber = nodes.length;
	for(var i = 0; i != nodesNumber; i++){
		list.removeChild(list.firstChild);
	}
	var response = req.responseXML;
	var receiveComments = response.getElementsByTagName("comments")[0].getElementsByTagName("comment");
	var size = receiveComments.length;
	for(var i = 0; i != size; i++){
		var imgUrl = receiveComments[i].getElementsByTagName("imgurl")[0].childNodes[0].nodeValue;
		var profileUrl = receiveComments[i].getElementsByTagName("profileurl")[0].childNodes[0].nodeValue;
		var commenterName = receiveComments[i].getElementsByTagName("commentername")[0].childNodes[0].nodeValue;
		var commentTime = receiveComments[i].getElementsByTagName("commenttime")[0].childNodes[0].nodeValue;
		var commentText = receiveComments[i].getElementsByTagName("commenttext")[0].childNodes[0].nodeValue;
		var newComment = document.createElement("div");
		newComment.className = "container-fluid";
		var newTable = document.createElement("table");
		newTable.className = "table";
		var newCommentName = document.createElement("th");
		newCommentName.innerHTML = "<a href = '" + profileUrl + "'>" + commenterName + "</a>";
		var newCommentTime = document.createElement("th");
		newCommentTime.className = "pull-right";
		newCommentTime.innerHTML = commentTime;
		newTable.appendChild(newCommentName);
		newTable.appendChild(newCommentTime);
		var newCommentBody = document.createElement("div");
		newCommentBody.className = "row";
		var newCommentImg = document.createElement("div");
		newCommentImg.className = "col-md-1";
		newCommentImg.innerHTML = "<img class = 'img-thumbnail thumbnailsize' src = '" + 
									imgUrl + "'>";
		var newCommentText = document.createElement("div");
		newCommentText.className = "col-md-11";
		var textWell = document.createElement("div");
		textWell.className = "well breaklines";
		textWell.innerHTML = commentText;
		newCommentText.appendChild(textWell);
		newCommentBody.appendChild(newCommentImg);
		newCommentBody.appendChild(newCommentText);
		list.insertBefore(newCommentBody, list.childNodes[0]);
		list.insertBefore(newTable, list.childNodes[0]);
	}
	
}