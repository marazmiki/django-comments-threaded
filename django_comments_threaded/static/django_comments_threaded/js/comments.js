(function($){
    $(function(){
        var panel = $('#comments-panel');
        var form  = $('#comments-widget').find('form');
        var formPlaceholder = $('#form-placeholder');
        var cancelReplyButton = form.find('input[name="_cancel"]');
        var defaultFormAction = form.attr('action');
        var messageInput = form.find('textarea');

        var newCommentButton = panel.find('a.count');
        var refreshCommentButton = panel.find('.btn-refresh');
        var activeComment = null;
        var lastTimeUpdate = null;

        /**
         * Counts new comments and write its number into button
         */
        var countNewComments = function() {
            var 
                size = $('div.comment.new').size(),
                ncb = newCommentButton
            ;
            ncb.html(size);

            if (size > 0) {
                ncb.show();
            } else {
                ncb.hide();
            };
        };

        /**
         * Replying
         */
        $('div.comment a.reply-link').live('click', function(e){
            var link = $(this); 

            form.attr('action', link.attr('href'));
            link.closest('div.comment').after(form);
            cancelReplyButton.show();
            messageInput.focus();

            return false;
        });

        /**
         *
         */
        cancelReplyButton.click(function(e){
            form.attr('action', defaultFormAction);
            cancelReplyButton.hide();
            formPlaceholder.append(form);

            return false;
        });

        /**
         * Refresh comments button
         */
        panel.find('.btn-refresh').click(function(){
            panel.addClass('in-progress');
            $.get($(this).attr('href'), {},
                function(json){
                    lastTimeUpdate = json.last_readed,
                    newCommentButton.text(json.new_comments.length);
                    panel.removeClass('in-progress');
                }, 'json'
            );
            return false;
        });

        /**
         * Navigate to next new comment and marks it as readed
         */
        newCommentButton.click(function(){
            var current = $('div.comment.new:first'); 
            var currId  = current.attr('id');

            if (activeComment) {
                activeComment.removeClass('new');
                activeComment.removeClass('active');
            };

            if (currId) {
                current.addClass('active');
                activeComment = current;
                location.hash = currId;
            };
            countNewComments();
            return false;
        });

        /**
         * Initialize new comments count
         */
        countNewComments();
    });
})(jQuery);