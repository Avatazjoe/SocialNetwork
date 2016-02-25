var req;

function sendRequest(){
	if(window.XMLHttpRequest){
		req = new XMLHttpRequest();
	} else {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	req.onreadystatechange = handleResponse;
	req.open("GET", "/socialnetwork/post_list", true);
	req.send();
}

function handleResponse(){
	if(req.readyState != 4 || req.status != 200){
		return;
	}
	
	var serverSet = new Set();
	var localSet = new Set();
	var list = document.getElementById("postInfo");
    var localChildNodes = list.childNodes;
	for(var i = 0; i != localChildNodes.length; i++){
		if(localChildNodes[i].id){
			localSet.add(localChildNodes[i].id);
		} else {
			list.removeChild(list.childNodes[i]);
			i--;
		}
	}
	var response = req.responseXML;
	var receivePosts = response.getElementsByTagName("posts")[0].getElementsByTagName("post");
	var serverSize = receivePosts.length;
	for(var i = 0; i != serverSize; i++){
		serverSet.add(receivePosts[i].getElementsByTagName("postid")[0].childNodes[0].nodeValue);
	}
	var localSetArray = Array.from(localSet);
	var localSize = localSetArray.length;
	var serverSetArray = Array.from(serverSet);
	var removeList = [];
	/*since everytime we remove a node from the list, the list size will reduce by one
	  therefore,  we have to add an align parameter
	 */
	var align = 0;
	for(var i = 0; i != localSize; i++){
		if(!serverSet.has(localSetArray[i])){
			list.removeChild(list.childNodes[i - align++]);
		}
	}
	
	for(var i = 0; i != serverSize; i++){
		if(!localSet.has(serverSetArray[i])){
		var newPost = document.createElement("div");
		var showPosts;
		var postID = receivePosts[i].getElementsByTagName("postidnumber")[0].childNodes[0].nodeValue;
		newPost.id = ("postgroup" + postID);
		showPosts += "<table class = 'table'><tbody><tr>";
		showPosts += "<th><a herf = '" + receivePosts[i].getElementsByTagName("profileurl")[0].childNodes[0].nodeValue + "'>"
					+ receivePosts[i].getElementsByTagName("username")[0].childNodes[0].nodeValue + "</a></th>";
		showPosts += "<th>" + receivePosts[i].getElementsByTagName("posttime")[0].childNodes[0].nodeValue + "</th>";
		showPosts += "<th><a herf = '" + receivePosts[i].getElementsByTagName("followurl")[0].childNodes[0].nodeValue + "'>"
					+ receivePosts[i].getElementsByTagName("follow")[0].childNodes[0].nodeValue + "</th>";
		showPosts += "</tr></tbody></table>";
		showPosts += "<div class = 'row'>";
		showPosts += "<div class = 'col-md-1'><img class = 'img-thumbnail thumbnailsize' src = '"
					+ receivePosts[i].getElementsByTagName("imgurl")[0].childNodes[0].nodeValue + "'>" + "</div>";
		showPosts += "<div class = 'col-md-11'><div class = 'well breaklines'>" 
					+ receivePosts[i].getElementsByTagName("posttext")[0].childNodes[0].nodeValue + "</div>";
		
		showPosts += "<div class = 'collapse' id = 'comments" + postID + "'>";
		showPosts += "<label for = 'comment'>Make a comment</label>	";
		showPosts += "<input class = 'form-control' type = 'text' name = 'comment'></input>";
		showPosts += "<div class = 'form-group'>";
		showPosts += "<input type = 'hidden' name = 'post' value = '" + postID + "'></input></div>";
		showPosts += "<input class= 'btn btn-sm btn-primary' type = 'submit' id = 'docomment"
																		+ postID + "'>";
		showPosts += "</div>";
		showPosts += "<button type='button' class='btn btn-default pull-right' data-toggle = 'collapse' data-target = '#comments"
						+ postID + "' aria-expanded = 'false' aria-controls = 'comments" + postID + "' id = '" + postID 
						+ "' onclick = 'sendCommentRequest(th)' >";
		showPosts += " <span class = 'glyphicon glyphicon-menu-hamburger' aria-hidden='true'></span></button>";
		showPosts += "</div></div>"
		newPost.innerHTML = showPosts;
		list.insertBefore(newPost, list.childNodes[0]);
		}
	}
}


window.setInterval(sendRequest, 5000);