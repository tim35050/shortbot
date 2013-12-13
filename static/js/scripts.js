var eliza = new ElizaBot();
var elizaLines = new Array();

var displayCols = 60;
var displayRows = 20;

function elizaReset() {
	eliza.reset();
	elizaLines.length = 0;
	$(".response").html('');
	elizaStep();
}

function elizaStep(json) {
	var f = document.forms.e_form;
	var userinput = f.text_input.value;
	var botName = '> SHORTBOT'
	var userName = '> YOU'
	if (json != "") {
		var usr = userName + ':   ' + json.you;
		var rpl = botName + ': ' + json.shortbot;
		elizaLines.push(usr);
		elizaLines.push(rpl);
		writeResponse(usr + '<br />' + rpl);
	} else {
		if (eliza.quit) {
			writeResponse('');
			if (confirm("This session is over.\nStart over?")) elizaReset();
			f.text_input.focus();
			return;
		}
		else if (userinput != '') {
			var usr = userName + ':   ' + userinput;
			var rpl = botName + ': ' + eliza.transform(userinput);
			elizaLines.push(usr);
			elizaLines.push(rpl);
			// display nicely
			// (fit to textarea with last line free - reserved for extra line caused by word wrap)
			var temp  = new Array();
			var l = 0;
			for (var i=elizaLines.length-1; i>=0; i--) {
				l += 1 + Math.floor(elizaLines[i].length/displayCols);
				if (l >= displayRows) break
				else temp.push(elizaLines[i]);
			}
			elizaLines = temp.reverse();
			writeResponse(usr + '<br />' + rpl);
		}
		else if (elizaLines.length == 0) {
			// no input and no saved lines -> output initial
			var initial = botName + ': ' + eliza.getInitial();
			elizaLines.push(initial);
			writeResponse(initial + '<br />')
		}
	}
	f.text_input.value = '';
	f.text_input.focus();
}

function writeResponse(msg) {
	$(".response").html($(".response").html() + '<div class="pair">' + msg + '</div>')
}

function processInput() {
	var result = '';
	input = $('input[name="text_input"]').val()
	if (is_valid_url(input)) {
		startLoading()
		$.getJSON('/_process_url', {
	    	url: input
	  	}, function(data) {
	  		stopLoading()
			elizaStep(data.result);
	  	});
	} else {
		elizaStep('');
	}
}

var loadingStatus = false;

var myInterval = 0;

// STARTS and Resets the loop if any
function startLoading() {
	document.forms.e_form.text_input.value += " *** Loading";
    myInterval = setInterval( "addDot()", 500 );  // run
}
function stopLoading() {
	clearInterval(myInterval);
}
function addDot() {
	document.forms.e_form.text_input.value += ".";
}
function is_valid_url(url) {
	return url.match(/^(ht|f)tps?:\/\/[a-z0-9-\.]+\.[a-z]{2,4}\/?([^\s<>\#%"\,\{\}\\|\\\^\[\]`]+)?$/);
}

$("#text_input").keyup(function(event){
    if(event.keyCode == 13){
		processInput();		
    }
});
