$(function () {
   $("#add-board").click(function () {
       var board = $("#board-Modal");
       board.find("input[name='name']").val("");

       var save_board_btn = board.find("#save-board-btn");
       save_board_btn.attr('data-type', 'add');
       save_board_btn.removeAttr('data-id');
   });
});

$(function () {
    $("#save-board-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var board = $("#board-Modal");
        var nameE = board.find("input[name=name]");
        var name = nameE.val();
        if (!name) {
            zlalert.alertInfoToast("请输入版块名称");
            return;
        }

        var url = '';
        var submitType = self.attr('data-type');
        var boardId = self.attr('data-id');
        if (submitType === 'update') {
            url = "/cms/uboard/";
        } else {
            url = "/cms/aboard/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'name': name,
                'board_id': boardId
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    board.modal('hide');
                    window.location.reload();
                } else {
                    zlalert.alertInfo((data['message']));
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        });
    });
});

$(function () {
   $(".edit-board-btn").click(function () {
       var board = $("#board-Modal");
       board.modal('show');
       var this_parent = $(this).parent().parent();
       board.find("input[name='name']").val(this_parent.attr('data-name'));

       var save_board_btn = board.find("#save-board-btn");
       save_board_btn.attr('data-type', 'update');
       save_board_btn.attr('data-id', this_parent.attr('data-id'));
   });
});

$(function () {
   $(".delete-board-btn").click(function () {
       var self = $(this);
       var board_id  = self.parent().parent().attr('data-id');
       zlalert.alertConfirm({
            "msg": "您确定要删除这个板块吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dboard/',
                    'data':{
                        'board_id': board_id
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