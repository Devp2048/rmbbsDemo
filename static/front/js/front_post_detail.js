$(function () {
    var ue = UE.getEditor("editor", {
       'serverUrl':  '/ueditor/upload/',
        toolbars: [
            [
                'undo',
                'redo',
                'bold',
                'italic',
                'source',
                'blockquote',
                'selectall',
                'insertcode',
                'fontfamily',
                'fontsize',
                'simpleupload',
                'emotion'
            ]
        ]
    });
    window.ue = ue;
});

$(function () {
    $("#submit-comment").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            window.location = '/signin/';
        }else{
            var content = window.ue.getContent();
            var post_id = $("#post-content").attr("data-id");
            zlajax.post({
                'url': '/acomment/',
                'data': {
                   'content': content,
                   'post_id': post_id
                },
                'success': function (data) {
                    if(data['code'] === 200){
                        window.location.reload();
                    }else{
                        zlalert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});