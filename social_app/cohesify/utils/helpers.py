def clear_media_in_undo(deleted_posts_stack):
    posts = deleted_posts_stack.arr
    for post in posts:
        if post.media:
            post.media.delete(save=False)
    deleted_posts_stack.clear_stack()