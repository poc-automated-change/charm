## Activate Virtual Env 
source .venv/bin/activate

/mnt/c/git_projects/charm/backend/.venv/bin/python3.14 /mnt/c/git_projects/charm/backend/manage.py runserver

POST   /api/chat/message/                    # Send chat message
GET    /api/chat/conversations/              # List conversations
GET    /api/chat/conversations/{id}/         # Get conversation details
DELETE /api/chat/conversations/{id}/delete/  # Delete conversation
GET    /api/change-requests/                 # List change requests
GET    /api/change-requests/{id}/            # Get change request
GET    /admin/                                # Django admin interface