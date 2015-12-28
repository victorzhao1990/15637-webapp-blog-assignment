/**
 * Created by victorzhao on 10/18/15.
 */

function getUpdatesComm(post) {
    console.log("XXXX");
    console.log(post.id);
    var list = $("#" + "post_" + post.id).find(".dropdown-menu");
    var max_entry = list.data("max-entry");
    $.get("/grumblr/get-comment-changes/"+ post.id + "/" + max_entry).done(function(data) {
        list.data('max-entry', data['max-entry']);
        for (var i = 0; i < data.comments.length; i++) {
            var comment = data.comments[i];
            if (comment.deleted) {
                $("#comment_" + comment.id).remove();
            } else {
                var new_comment = $(comment.html);
                new_comment.data("comment-id", comment.id);
                list.prepend(new_comment);
            }
        }
    });
}

function addComment(e) {
    var contentField = $("#" + "post_" + e.data.id).find("textarea");
    $.post("/grumblr/add-comment/" + e.data.id, {content: contentField.val()})
        .done(function(data){
        getUpdatesComm(e.data);
        contentField.val("").focus();
    });
}

function addContent2Btn(post) {
    var postDiv = $("#" + "post_" + post.id);
    var list = postDiv.find(".dropdown-menu");
    $.get("/grumblr/get-comments/" + post.id).done(function(data) {
        list.html('');
            list.data('max-entry', data['max-entry']);
            list.append(
                $('<li/>', {'id': "comment-area"}).append(
                    $('<textarea/>', {'id': "inputbox"})
                ).append(
                    $('<button/>', {'id': "sub-comm", 'text': "Submit"})
                )
            );
            list.on('click', function(e) {
                e.stopPropagation();
            });
            postDiv.find("#sub-comm").click(post, addComment);
            for (var i = 0; i < data.comments.length; i++) {
                comment = data.comments[i];
                var new_comment = $(comment.html);
                new_comment.data("comment-id", comment.id);
                list.prepend(new_comment);
            }
    });
}


function populateList() {
    var userid = $(".blog-title").find("img").attr("alt");
    console.log(userid);
    $.get("/grumblr/get-posts/" + userid).done(function(data){
       var list = $("#post-list");
        list.html('');
        list.data('max-entry', data['max-entry']);
        for (var i = 0; i < data.posts.length; i++) {
            post = data.posts[i];
            var new_post = $(post.html);
            new_post.data("post-id", post.id);
            list.prepend(new_post);
            addContent2Btn(post);
        }
    });
}


function addPost() {
    var contentField = $("#new_post");
    $.post("/grumblr/add-post", {content: contentField.val()}).done(function(data) {
            getUpdates();
            contentField.val("").focus();
    });
}

function getUpdates() {
    var list = $("#post-list")
    var max_entry = list.data("max-entry")
    $.get("/grumblr/get-changes/"+ max_entry).done(function(data){
        list.data('max-entry', data['max-entry']);
        for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            if (post.deleted) {
                $("#post_" + post.id).remove();
            } else {
                var new_post = $(post.html);
                new_post.data("post-id", post.id);
                list.prepend(new_post);
            }
        }
    });
}

$(document).ready(function () {
    // TODO: add handler for the post button
    $("#post-btn").click(addPost);
    populateList();

    //window.setInterval(getUpdates, 5000);

    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});
