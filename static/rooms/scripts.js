// globals
var barcode = '';
var key_mode = 'checkout'; // checkout == normal process; return == only return.
var refreshed = true;

// clock function to show current military time
function updateClock() {
	var today = new Date();
	var h = today.getHours();
	var m = today.getMinutes();
	
	// if clock just changed to an interval of 30, refresh the whole page
	if ((m == 30 || m == 0) && !refreshed) {
		safeRefresh();
	} else if (m != 30 && m !== 0 && refreshed) {
		refreshed = false;
	}
	
	if (h < 10) {
		h = '0' + h;
  	}
  	if (m < 10) {
  		m = '0' + m;
	}
	$('#clock').html(h + '' + m);
}

// safely refreshes the current window if and only if no dialogs are open so it
// won't interrupt any reservations in progress.
function safeRefresh() {
	if ($('#safe').html() == 'true') {
		window.location.reload();
	}
}

function errorDialogClose(dialog) {
	$(dialog).dialog({title: 'An Error Occured',}); // override back to default
	$(dialog).dialog('close');
	$('#id_keybarcode').focus();
}

function loginDialogOk(dialog) {
	$(dialog).dialog('close');
	$.getJSON('/ajax_login/?barcode=' + $('#id_barcode').attr('value'),
		function(data) {
			$('#id_barcode').attr('value',''); // reset barcode input box
			if (data['auth']) {
				email = data['message'];
				$('#scan_key_form').dialog('open');
				$('#id_keybarcode').focus();
			} else {
				$(dialog).html(data['error']);
				$(dialog).dialog('open');
			}
		}
	);
}

function scanKeyDialogOk(dialog) {
	$(dialog).dialog('close');
	if (key_mode == 'checkout') {
		$.getJSON('/ajax_roomkey/?barcode=' + $('#id_keybarcode').attr('value'),
			function(data) {
				barcode = $('#id_keybarcode').attr('value');
				$('#id_keybarcode').attr('value','');
				if (data['error'].length > 0) {
					$('#error_dialog').html(data['error']);
					$('#error_dialog').dialog('open');
				} else {
					$('#select_time_form').dialog('open');
				}
			}
		);
	} else if (key_mode == 'return') {
		$.getJSON('/ajax_roomkey_checkin/?barcode=' + $('#id_keybarcode').attr('value'),
			function(data) {
				$('#id_keybarcode').attr('value','');
				if (data['success']) {
					$('#error_dialog').dialog({title: 'Thank You',
						buttons: {
							'OK': function() {	
								$(dialog).dialog('close');
								window.location.reload();
							}
						},
					});
					$('#error_dialog').html('Your key has been returned. Thank you.');
					$('#error_dialog').dialog('open');
				} else {
					$('#error_dialog').html(data['error']);
					$('#error_dialog').dialog('open');
				}
			}
		);
	}
}

function selectTimeDialogOk(dialog) {
	// push the requested minutes, email address, and room to the server
	$.getJSON('/ajax_reserve/?email=' + email + '&barcode=' + barcode
		+ '&minutes=' + $('#time_slider').slider('value'),
		function(data) {
			if (data['success']) {
				$(dialog).dialog('close');
				$('#error_dialog').dialog({
					title: 'Reservation Complete',
					buttons: {
						'OK': function() {
							$(dialog).dialog('close');
							window.location.reload();
						}
					}
				});
				$('#error_dialog').html('Your reservation was successful. You may now proceed to your room.');
				$('#error_dialog').dialog('open');
			} else {
				$('#error_dialog').html(data['error']);
				$('#error_dialog').dialog('open');
			}
		}
	);
}

$(document).ready(function() {

$('#error_dialog').dialog({
	autoOpen: false,
	closeOnEscape: true,
	draggable: false,
	modal: true,
	resizable: false,
	title: 'An Error Occured',
	buttons: {
		'Close': function() { errorDialogClose(this); },
	},
})
.keyup(function(e) {
	// handler for when ENTER/RETURN is pressed in this dialog
    if (e.keyCode == 13) {
        errorDialogClose(this);
    }
})
;

$('#time_slider').slider({
	// all values in minutes
	value: 30,
	min: 30,
	max: (30 * 2 * 4), // 4 hours
	step: 30, // 30 minute increments
	slide: function(event,ui) {
		var minutes = ui.value % 60; // get left over minutes
		var hours = Math.round( (ui.value - minutes) / 60); // get hours
		var report = '';
		
		mins = '';
		hrs = '';
		if (minutes > 0) {
			mins = minutes + ' minutes';
		}
		if (hours > 0) {
			hrs = hours + ' hour';
			if (hours > 1) { hrs += 's'; }
			report = hrs;
		}
		if (mins.length > 0) {
			if (report.length > 0) { report += ' and '; }
			report += mins;
		}
		
		$('#time').html(report);
	},
}); // value can be obtained by $('#time_slider').slider('value')

$('#login_form').dialog({
	autoOpen: false,
	closeOnEscape: true,
	draggable: false,
	modal: true,
	resizable: false,
	title: 'Scan Library Card Now...',
	buttons: {
		'Next': function() { loginDialogOk(this); },
		'Cancel': function() {
			$(this).dialog('close');
			$('#id_barcode').attr('value','');
			$('#safe').html('true');
		}
	},
})
.keyup(function(e) {
	// handler for when ENTER/RETURN is pressed in this dialog
    if (e.keyCode == 13) {
        loginDialogOk(this);
    }
});

$('#scan_key_form').dialog({
	autoOpen: false,
	closeOnEscape: true,
	draggable: false,
	modal: true,
	resizable: false,
	title: 'Scan Key Now...',
	buttons: {
		'Next': function() { scanKeyDialogOk(this); },
		'Cancel': function() {
			$(this).dialog('close');
			$('#id_keybarcode').attr('value','');
			$('#safe').html('true');
		}
	},
})
.keyup(function(e) {
	// handler for when ENTER/RETURN is pressed in this dialog
    if (e.keyCode == 13) {
        scanKeyDialogOk(this);
    }
});

$('#select_time_form').dialog({
	autoOpen: false,
	closeOnEscape: true,
	draggable: false,
	modal: true,
	resizable: false,
	title: 'Select Length of Time',
	buttons: {
		'Submit': function() { selectTimeDialogOk(this); },
		'Cancel': function() {
			$(this).dialog('close');
			$('#safe').html('true');
		}
	},
})
.keyup(function(e) {
	// handler for when ENTER/RETURN is pressed in this dialog
    if (e.keyCode == 13) {
        selectTimeDialogOk(this);
    }
});

$('#bookroom').button()
	.click(function() {
		$('#safe').html('false');
		key_mode = 'checkout';
		$('#login_form').dialog('open');
		$('#id_barcode').focus();
	})
;

$('#checkin').button()
	.click(function() {
		$('#safe').html('false');
		key_mode = 'return';
		$('#scan_key_form').dialog('open');
		$('#id_keybarcode').focus();
	})
;

// refresh the onscreen clock every half a second
window.setInterval('updateClock()',500);
});
