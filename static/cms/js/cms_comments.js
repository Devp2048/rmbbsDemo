


$(function () {
   $(".delete-comment-btn").click(function () {
       var self = $(this);
       var comment_id  = self.parent().parent().attr('data-id');
       zlalert.alertConfirm({
            "msg": "您确定要删除这条评论吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dcomment/',
                    'data':{
                        'comment_id': comment_id
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
});