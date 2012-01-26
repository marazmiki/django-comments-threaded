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
         * Add new comments via AJAX
         */
        $(form).submit(function(){
            $.post(
                $(this).attr('action'),
                $(this).serialize(),
                function(json){
                    var newThread = function(){
                        return $('<ul />')
                            .addClass('thread')
                            .data('id', json.tree_id)
                            .attr('data-id', json.tree_id)
                        ;
                    };
                    var newReply = function(){
                        return $('<li />')
                            .addClass('tree-' + json.tree_id)
                            .append(json.comment)
                        ;
                    };
                    if (json.success) {
                        /* The replying */
                        if (json.parent_id) {

                            /* Find the parent node */
                            var parentNode = $('#comment-' + json.parent_id).closest('LI');

                            if ($('ul.thread', parentNode).size() == 0 ) {
                                parentNode.append( newThread() );
                            };

                            $('ul.thread:first', parentNode).append( newReply() );

                        /* The new thread */
                        } else {
                            $('#comments').append(newThread().append( newReply()));

                        };
                            json.parent_id;
                            json.comment;
                            json.tree_id;
                            json.id;
                    };
                    console.log( json );
                }, 'json');
            return false;
        })

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
         * Cancel the replying: restore original form action,
         * move the form back and hide the 'cancel' button
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