/**
 * Created by victorzhao on 10/18/15.
 */

function populateList(event) {
    var comment_area = document.createElement("LI");
    var input = document.createElement("textarea");
    var button = document.createElement("button");
    button.click(addComment);

    comment_area.appendChild(input);
    comment_area.appendChild(button);


    var post = $(event.target).parent();
    var post_id = post.attr('id').split("_")[1];
    $.get("/grumblr/get-comments/" + post_id).done(function (data) {
        var list = $(event.target);
        list.append(comment_area);
        list.data('max-entry', data['max-entry']);
        list.html('');
        for (var i = 0; i < data.comments.length; i++) {
            comment = data.comments[i];
            var new_comment = $(comment.html);
            new_comment.data("comment_id", comment.id);
            list.append(new_comment);
        }
    });

    window.setInterval(getUpdates, 5000);
}


}


function addComment(target) {
    var contentField = $(event.target).siblings("textarea");
    var post = $(event.target).parent(".post_item");
    var post_id = post.attr('id').split("_")[1];
    $.post("/grumblr/add-comment/" + post_id, {content: contentField.val()})
        .done(function(data) {
            getUpdates();
            contentField.val("").focus();
        });
}

function getUpdates() {
    var list = $(event.target).parent(".dropdown-menu");
    var max_entry = list.data("max-entry");

    var post = $(event.target).parent(".post_item");
    var post_id = post.attr('id').split("_")[1];

    $.get("/grumblr/get-comment-changes/"+ post_id + "/" + max_entry).done(function(data) {
        list.data('max-entry', data['max-entry']);
        for (var i = 0; i < data.comments.length; i++) {
            var comment = data.comments[i];
            if (comment.deleted) {
                $("#comment_" + comment.id).remove();
            } else {
                var new_comment = $(comment.html);
                new_comment.data("comment-id", comment.id);
                list.append(new_comment);
            }
        }
    });
}

$(document).ready(function () {
    // TODO: add handler for the post button
    $("#comment-btn").click(populateList);

    //
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

