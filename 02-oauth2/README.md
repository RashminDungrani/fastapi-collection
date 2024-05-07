# Security - OAuth2

* Official Documentation [link](https://fastapi.tiangolo.com/tutorial/security/)

## QA

1. What is OAuth2 ?
    - OAuth2 is a specification that defines several ways to handle authentication and authorization.

    - It covers various complex use cases, including authentication via a "third party" service like Facebook, Google, Twitter, or GitHub.

1. Why use python-jose ?
    - Python-jose is a library that provides support for JSON Web Tokens (JWT), which are commonly used in OAuth2 for token-based authentication and authorization.

    - It simplifies the process of generating, decoding, and verifying JWT tokens, making it easier to implement secure authentication mechanisms in your application.

    - It offers functionalities such as token encryption, token signing, and token verification, essential for secure communication between clients and servers in OAuth2 workflows.

1. Why python-multipart ?
    - OAuth2 often uses "form data" for sending the username and password during authentication. Python-multipart helps handle such form data requests efficiently.

1. Why passlib ?
    - PassLib is a Python package designed to manage password hashes securely.

    - It supports multiple secure hashing algorithms and provides utilities for working with them.

    - The recommended algorithm for password hashing is "Bcrypt," which is supported by PassLib.

    - To install PassLib with Bcrypt, use the following command:
        ```shell
        poetry add passlib[bcrypt]
        ```
