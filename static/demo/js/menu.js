//user actions
$(function() {
	$('div.menuItem').bind('mouseenter',function(){

		this.className = "menuItem hovered";
		updateToggleableColors(this.innerHTML);

	}).bind('mouseleave',function(){

		this.className = "menuItem";
		updateToggleableColors(pageVariables.name);

	}).bind('click',function(){

		updatePageContent(this.innerHTML);
		updateToggleableColors(pageVariables.name);

	});
});

//page load functions
$(document).ready(function(){
	var page = getPageParameter("page");
	updatePageContent(page);
});



//sets an elements color by setting the appropriate class name to it
function updateElementColor(element, className) {
	element.className = "toggleColor "+className;
}

// sets ALL classes with the name "toggleColor" to have the new color class applied
function updateToggleableColors(newClassName) {
	$.each($('.toggleColor'), function(i, element) {
		updateElementColor(element, newClassName);
	});
}

// gets a parameter URL (blah.com?name=THIS_IS_THE_RESULT)
function getPageParameter(name) {
	return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

// updates the page content with the appropriate styles, as well as fetched data
function updatePageContent(pageName) {
	if (pageName) pageVariables.name = pageName;
	updateToggleableColors(pageVariables.name);
	loadPageContent(pageVariables.name);
	//loadPageContent("file:///D:/webapp/pages/"+pageVariables.name+".html");
}

// loads the page content, to be put into the div with id "page"
function loadPageContent(pageName) {
	$("#loadingbar").show();
	$('#page').html("");

	if (!pageVariables.content[pageName]) {
		var url = "pages/"+pageName+".html"
		if (pageName === "archives") {
			url = "http://users.wpi.edu/~tjmeyer/files/";
		}
		$("#page").load(url, function() {
			$("#loadingbar").hide();
		});
		pageVariables.content[pageName] = $("#page").html();
	} else {
		$("#page").html(pageVariables.content[pageName]);
	}
}










pageVariables = {
	name:"home",
	content: {
		home:"",
		projects:"",
		education:"",
		work:"",
		blog:"",
		archives:""
	}
};
