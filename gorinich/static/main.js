/**
 * Created by kulapard on 23/05/15.
 */
function getEditor() {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.setHighlightActiveLine(true);
    editor.setShowPrintMargin(true);
    editor.setFontSize(12);
    editor.getSession().setUseSoftTabs(true);
    editor.getSession().setUseWrapMode(true);

    return editor;
}

$(function () {
    var editor = getEditor();

    editor.getSession().on('change', function (e) {
        //console.log(e);
        var action = {};
        action.uid = UID;
        action.action = 'updateText';
        action.text = editor.getValue();
        conn.send(JSON.stringify(action));
    });

    //editor.getSession().selection.on('changeSelection', function (e) {
    //    console.log(e);
    //});

    //editor.getSession().selection.on('changeCursor', function (e) {
    //    console.log(e);
    //    var cursor = editor.selection.getCursor();
    //    var action = {};
    //    action.action = 'changeCursor';
    //    action.row = cursor.row;
    //    action.column = cursor.column;
    //    console.log(action);
    //
    //    conn.send(JSON.stringify(action));
    //});

    var conn = null;

    function changeCursor(newPosition) {
        var cursor = editor.selection.getCursor();
        var new_row = newPosition.row;
        var new_column = newPosition.column;
        if (new_row != cursor.row || new_column != cursor.column) {
            console.log('Row:' + cursor.row + '->' + new_row);
            console.log('Column:' + cursor.column + '->' + new_column);
            editor.moveCursorTo(new_row, new_column);
        }
    }

    function processAction(action) {
        console.log('processAction:', action);
        if (action.action == 'removeText') {
            //editor.removeSelectionMarker(action.range);
        }
        else if (action.action == 'changeCursor') {
            //var newPosition = {};
            //newPosition.row = action.row;
            //newPosition.column = action.column;
            //changeCursor(newPosition);
        }
        else if (action.action == 'updateText') {
            var old_text = editor.getValue();
            console.log('old_text:', old_text);
            console.log('new_text:', action.text);
            //if (old_text != action.text) {
            //    editor.setValue(action.text);
            //}
        }
    }

    function connect() {
        disconnect();

        conn = new SockJS('http://' + window.location.host + '/sync?pad_id=' + PAD_ID);

        conn.onopen = function () {
            console.log('Connected.');
        };

        conn.onmessage = function (e) {
            console.log('Received: ', e.data);
            //if (e.data.includes(":")) processMsg(e.data);
            try {
                var action = $.parseJSON(e.data);
            } catch (err) {
                console.log('Not a JSON message received:', e.data);
                return;
            }
            if (action.uid != UID) {
                processAction(action);
            }
        };

        conn.onclose = function () {
            console.log('Disconnected');
            conn = null;
        };
    }

    function disconnect() {
        if (conn != null) {
            console.log('Disconnecting...');

            conn.close();
            conn = null;
        }
    }

    connect();

});