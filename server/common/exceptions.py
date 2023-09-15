class MemberWithGivenUserIDExists(Exception):
    def __init__(self):
        super().__init__('Member with given user_id is already exists')
