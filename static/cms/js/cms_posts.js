





$(function () {
   $(".delete-post-btn").click(function () {
       var self = $(this);
       var post_id  = self.parent().parent().attr('data-id');
       zlalert.alertConfirm({
            "msg": "您确定要删除这篇帖子吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dpost/',
                    'data':{
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
});