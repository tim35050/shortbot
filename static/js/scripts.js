var eliza = new ElizaBot();
var elizaLines = new Array();

var displayCols = 60;
var displayRows = 20;

function elizaReset() {
	eliza.reset();
	elizaLines.length = 0;
	elizaStep();
}

function elizaStep(shortenMessage) {
	var f = document.forms.e_form;
	var userinput = f.text_input.value;
	var botName = 'SHORTBOT'
	var userName = 'YOU'
	if (shortenMessage != "") {
		var usr = userName + ':   ' + userinput;
		var rpl = botName + ': ' + shortenMessage;
		elizaLines.push(usr);
		elizaLines.push(rpl);
		$(".response").html(elizaLines.join('<br />'));
	} else {
		if (eliza.quit) {
			$(".response").html('');
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
			$(".response").html(elizaLines.join('<br />'));
		}
		else if (elizaLines.length == 0) {
			// no input and no saved lines -> output initial
			var initial = botName + ': ' + eliza.getInitial();
			elizaLines.push(initial);
			$(".response").html(initial + '<br />');
		}
	}
	f.text_input.value = '';
	f.text_input.focus();
}

function processInput() {
	var result = '';
	input = $('input[name="text_input"]').val()
	if (input.substring(0,7) == "http://") {
		$.getJSON('/_process_url', {
	    	url: input
	  	}, function(data) {
			elizaStep(data.result);
	  	});
	} else {
		elizaStep('');
	}
}

function validateURL(value) {

}

$("#text_input").keyup(function(event){
    if(event.keyCode == 13){
		processInput();		
    }
});
