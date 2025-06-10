# 🔐 API Project for Book Review Application in Django

1. **Technologies Used**
    - Django
    - Django REST Framework
    - djangorestframework-simplejwt
    - Custom User Model
    - Email Backend (SMTP)
    - CORS Headers

2. **Project Structure**

    ├── account/        # user creation and management  
    ├── book_review/    # Main project directory
    ├── book/           # book and review creation api 
    ├── manage.py

3. **API Endpoints**

    | Method  | Endpoint                                            | Description                        |
    | ------- | ----------------------------------------------------| ---------------------------------  |
    | POST    | `/account/register/`                                | Register a new user                |
    | GET     | `/account/activate/<uidb64>/<token>/`               | Activate account via email         |
    | POST    | `/account/password-reset/`                          | Request password reset email       |
    | POST    | `/account/password-reset-confirm/<uidb64>/<token>/` | Reset password                     |
    | POST    | `/account/resend-activation`                        | To resend activation URL           |
    | POST    | `/account/change-password/`                         | Change password (logged-in users)  |
    | GET/PUT | `/account/user-update/`                             | got or update user information     |

    | POST    | `/api/token/`                                       | Login and get JWT token            |
    | POST    | `/api/token/refresh/`                               | Refresh JWT token                  |

    | GET     | `/books/`                                           | To get all of books                |
    | POST    | `/books/create/`                                    | To create a new book               |
    | GET     | `/books/<pk>/`                                      | To get detail of a book with review|
    | GET     | `/books/user/<pk>/`                                 | To get all books of a user         |
    | DELETE  | `/books/book-delete/<pk>/`                          | To delete one specific book        |
    | POST    | `/books/review-create/<book-id>`                    | To create a new review             |
    | DELETE  | `/books/review/<pk>/`                               | To delete one specific review      |

    For development purposes
    |         | `api/schema/`                                       | To download schema file for APIs   |
    |         | `api/schema/swagger-ui/`                            | To see different APIs              |

    |         | `silk/`                                             | To analyse the queries to database |

This project is a work in progress, and I'm continuously learning and improving. Contributions and feedback are welcome!