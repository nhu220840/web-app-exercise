from flask import Flask, jsonify

app = Flask(__name__)

# Mock Data for API Testing
# In a real application, this data would come from a database

# Users data structure - represents user profiles
users_data = [
    {
        "id": 1,
        "firstName": "John",
        "lastName": "Wick", 
        "email": "john.wick@gmail.com",
        "phone": "+84 983 658 012",
        "dateOfBirth": "1990-05-15",
        "gender": "male"
    },
    {
        "id": 2,
        "firstName": "Black",
        "lastName": "Widow",
        "email": "black.widow@gmail.com", 
        "phone": "+84 913 738 835",
        "dateOfBirth": "1985-08-22",
        "gender": "female"
    },
    {
        "id": 3,
        "firstName": "Steve",
        "lastName": "Rogers",
        "email": "steve.rogesr@gmail.com",
        "phone": "+84 243 938 129", 
        "dateOfBirth": "1992-03-10",
        "gender": "male"
    }
]

# Representations of social media posts
posts_data = [
    {
        "id": 1,
        "text": "This is my first post on this platform!",
        "image": "https://(self-defined :D )",  # Random placeholder image
        "likes": 45,
        "tags": ["introduction", "first-post"],
        "publishDate": "2024-01-15 10:30:00",  
        "owner": {  # Embedded user information
            "id": 1,
            "firstName": "John",
            "lastName": "Wick"
        }
    },
    {
        "id": 2,
        "text": "Beautiful sunset today! Nature is amazing.",
        "image": "https://(self-defined AGAIN XD)",
        "likes": 78,
        "tags": ["nature", "sunset", "photography"],
        "publishDate": "2024-01-16 18:45:00",
        "owner": {
            "id": 2,
            "firstName": "Black",
            "lastName": "Widow"
        }
    },
    {
        "id": 3,
        "text": "Just finished reading an amazing book! Highly recommend.",
        "image": "https://google.com/imghp", 
        "likes": 23,
        "tags": ["books", "reading", "recommendation"],
        "publishDate": "2024-01-17 14:20:00",
        "owner": {
            "id": 3,
            "firstName": "Steve",
            "lastName": "Rogers"
        }
    }
]

# Comments data structure - represents comments on posts
comments_data = [
    {
        "id": 1,
        "message": "Great post! Thanks for sharing.",
        "owner": {
            "id": 2,
            "firstName": "John",
            "lastName": "Wick"
        },
        "post": 1,  # References post ID
        "publishDate": "2024-01-15 11:00:00"
    },
    {
        "id": 2,
        "message": "I totally agree with this!",
        "owner": {
            "id": 3,
            "firstName": "Black",
            "lastName": "Widow"
        },
        "post": 1,
        "publishDate": "2024-01-15 11:30:00"
    },
    {
        "id": 3,
        "message": "Absolutely stunning! Where was this taken?",
        "owner": {
            "id": 1,
            "firstName": "Steve",
            "lastName": "Rogers"
        },
        "post": 2,
        "publishDate": "2024-01-16 19:00:00"
    },
    {
        "id": 4,
        "message": "What book was it? I'm looking for new reads.",
        "owner": {
            "id": 2,
            "firstName": "John",
            "lastName": "Wick"
        },
        "post": 3,
        "publishDate": "2024-01-17 15:00:00"
    }
]

# API Endpoints - Users Section

@app.route('/users')
def get_users():
    """
    Get all users in the system
    
    Returns:
        JSON: List of all users with pagination metadata
        
    API Response Format:
    {
        "data": [...],     # Array of user objects
        "total": 3,        # Total number of users
        "page": 1,         # Current page number
        "limit": 20        # Items per page
    }
    
    Example URL: GET /users
    """
    # jsonify() converts Python dictionaries/lists to JSON format
    # Also sets proper Content-Type header (application/json)
    return jsonify({
        "data": users_data,
        "total": len(users_data),
        "page": 1,
        "limit": 20
    })

@app.route('/user/<int:user_id>')
def get_user(user_id):
    # Get detailed information about a specific user
    # 
    # Args:
    #     user_id (int): The ID of the user to retrieve
    #     
    # Returns:
    #     JSON: User object or error message
    #     
    # Example URLs:
    #     GET /user/1 -> Returns John Wick's details
    #     GET /user/999 -> Returns 404 error
    # Use next() with generator expression to find user
    # next() returns first match or None if no match found
    user = next((user for user in users_data if user["id"] == user_id), None)
    
    if user:
        return jsonify(user)  # Return user data as JSON
    else:
        # Return error with 404 status code (Not Found)
        return jsonify({"error": "User not found"}), 404

@app.route('/user/<int:user_id>/posts')
def get_user_posts(user_id):
    # Get all posts created by a specific user
    # 
    # Args:
    #     user_id (int): The ID of the user whose posts to retrieve
    #     
    # Returns:
    #     JSON: List of posts by the user or error message
    #     
    # Example URL: GET /user/1/posts
    # First, verify that the user exists
    user = next((user for user in users_data if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Filter posts by user ID using list comprehension
    # Check if post owner's ID matches the requested user ID
    user_posts = [post for post in posts_data if post["owner"]["id"] == user_id]
    
    return jsonify({
        "data": user_posts,
        "total": len(user_posts),
        "page": 1,
        "limit": 20
    })

# API Endpoints - Posts Section

@app.route('/posts')
def get_posts():
    """
    Get all posts in the system
    
    Returns:
        JSON: List of all posts with pagination metadata
        
    Example URL: GET /posts
    """
    return jsonify({
        "data": posts_data,
        "total": len(posts_data),
        "page": 1,
        "limit": 20
    })

@app.route('/post/<int:post_id>/comments')
def get_post_comments(post_id):
    """
    Get all comments for a specific post
    
    Args:
        post_id (int): The ID of the post whose comments to retrieve
        
    Returns:
        JSON: List of comments for the post or error message
        
    Example URL: GET /post/1/comments
    """
    # Verify that the post exists
    post = next((post for post in posts_data if post["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    # Filter comments by post ID
    post_comments = [comment for comment in comments_data if comment["post"] == post_id]
    
    return jsonify({
        "data": post_comments,
        "total": len(post_comments),
        "page": 1,
        "limit": 20
    })

@app.route('/post/<int:post_id>')
def get_post(post_id):
    """
    Get detailed information about a specific post
    
    Args:
        post_id (int): The ID of the post to retrieve
        
    Returns:
        JSON: Post object or error message
        
    Example URL: GET /post/1
    """
    post = next((post for post in posts_data if post["id"] == post_id), None)
    if post:
        return jsonify(post)
    else:
        return jsonify({"error": "Post not found"}), 404

# Home/Documentation Route

@app.route('/')
def home():
    """
    API documentation and endpoint listing
    
    Returns:
        JSON: API documentation with available endpoints
        
    This serves as a simple API documentation page
    """
    return jsonify({
        "message": "Flask API Backend - Similar to DummyAPI",
        "endpoints": {
            "users": {
                "/users": "List all users",
                "/user/{user_id}": "Get user details", 
                "/user/{user_id}/posts": "Get user's posts"
            },
            "posts": {
                "/posts": "List all posts",
                "/post/{post_id}": "Get post details",
                "/post/{post_id}/comments": "Get post comments"
            }
        },
        "example_urls": [
            "/users",
            "/user/1", 
            "/user/1/posts",
            "/posts",
            "/post/1",
            "/post/1/comments"
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)