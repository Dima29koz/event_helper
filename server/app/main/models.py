from server.app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return None
