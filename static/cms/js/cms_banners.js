// 清除由编辑时产生的默认信息
$(function () {
   $("#add-banner").click(function () {
       var banner = $("#banner-Modal");
       banner.find("input[name='name']").val("");
       banner.find("input[name='image_url']").val("");
       banner.find("input[name='link_url']").val("");
       banner.find("input[name='priority']").val("");

       var save_banner_btn = banner.find("#save-banner-btn");
       save_banner_btn.attr('data-type', 'add');
       save_banner_btn.removeAttr('data-id');
   });
});

$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var banner = $("#banner-Modal");
        var nameE = banner.find("input[name=name]");
        var image_urlE = banner.find("input[name=image_url]");
        var link_urlE = banner.find("input[name=link_url]");
        var priorityE = banner.find("input[name=priority]");

        var name = nameE.val();
        var image_url = image_urlE.val();
        var link_url = link_urlE.val();
        var priority = priorityE.val();

        if(!name || !image_url || !link_url || !priority){
            var index = !name?0:(!image_url?1:(!link_url?2:3));
            var msg = ["图片名称","图片地址","跳转链接","权重"];
            zlalert.alertInfoToast("请输入"+msg[index]);
            return;
        }

        var url = '';
        var submitType = self.attr('data-type');
        var bannerId = self.attr('data-id');
        if(submitType === 'update'){
            url = "/cms/ubanner/";
        }else{
            url = "/cms/abanner/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    banner.modal('hide');
                    window.location.reload();
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        });
    });
});

$(function () {
   $(".edit-banner-btn").click(function () {
       var banner = $("#banner-Modal");
       banner.modal('show');
       var this_parent = $(this).parent().parent();
       banner.find("input[name='name']").val(this_parent.attr('data-name'));
       banner.find("input[name='image_url']").val(this_parent.attr('data-image'));
       banner.find("input[name='link_url']").val(this_parent.attr('data-link'));
       banner.find("input[name='priority']").val(this_parent.attr('data-priority'));

       var save_banner_btn = banner.find("#save-banner-btn");
       save_banner_btn.attr('data-type', 'update');
       save_banner_btn.attr('data-id', this_parent.attr('data-id'));
   });
});

$(function () {
   $(".delete-banner-btn").click(function () {
       var self = $(this);
       var banner_id  = self.parent().parent().attr('data-id');
       zlalert.alertConfirm({
            "msg": "您确定要删除这个轮播图吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dbanner/',
                    'data':{
                        'banner_id': banner_id
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

$(function () {
    rmqiniu.setUp({
        'domain': 'http://poyp9yrz8.bkt.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/c/uptoken/',
        'success': function (up, file, info) {
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);
        }
    });
});